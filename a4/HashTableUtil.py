import pickle
import socket

from dataclasses import dataclass

class HashTableFile:
    def __init__(self, filename: str, data: bytes = None, size: int = None):
        self.filename = filename
        self.data = data
        self.size = size

    def from_disk(self, path: str = None):
        if path:
            with open(path, 'rb') as file:
                self.data = file.read()
                self.size = len(self.data)
        else:
            with open(self.filename, 'rb') as file:
                self.data = file.read()
                self.size = len(self.data)
        return self

    def to_disk(self, path: str):
        with open(path, 'wb') as file:
            file.write(self.data)
        return self
    
    def free_data(self):
        self.data = None
    
@dataclass 
class HTFileMetadata:
    filename: str = ""
    size: int = 0
    file: HashTableFile = None
    path_on_disk: str = ""

@dataclass
class HTMessageBody:
    status: str = ""
    size: int = 0
    filename: str = ""
    file: HashTableFile = None
    query: bool = False

class HTMessage:
    @staticmethod
    def serialize(self) -> bytes:
        return pickle.dumps(self)

    def __init__(self, intent: str, body: HTMessageBody):
        self.intent = intent
        self.body = body
        self.serialized = self.serialize(self)
        self.size = len(self.serialized)

    def send_varlen(self, sock: socket.socket):
        # Send a fixed-size header containing the size of the message
        size_bytes = self.size.to_bytes(8, byteorder='big', signed=False)
        sock.sendall(size_bytes)
        #print("sent size:", self.size)

        # wait for ack
        ack = sock.recv(len(b'ACK'))
        if ack != b'ACK':
            raise Exception("Did not receive ack on size header")
        
        #print("received ack for size header")

        # send the actual serialized message
        sock.sendall(self.serialized)

        # wait for ack
        ack = sock.recv(len(b'ACK'))
        if ack != b'ACK':
            raise Exception("Did not receive ack on full message")
        
        #print("received ack for full message, total bytes sent:", self.size)

        print(f"TX {self.size} bytes, {self.intent} {self.body.filename}")

        return self.size
    
    def recv_varlen(sock: socket.socket):
        # need to handle client disconnection
        # receive the fixed-size header
        size_bytes = sock.recv(8)
        size = int.from_bytes(size_bytes, byteorder='big', signed=False)
        #print("received size bytes:", size)
        sock.sendall(b'ACK')

        # receive the actual serialized message
        data = sock.recv(size)
        sock.sendall(b'ACK')

        # deserialize the message
        message = pickle.loads(data)

        print(f"RX {size} bytes, {message.intent} {message.body.status} {message.body.filename}")

        return message
