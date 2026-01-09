# This is the client RPC interface to the HashTable server.
# It's job is to send JSON requests, read back responses,
# and translate them into the expected function call format.

import socket
import json
import http.client
from HashTableFile import HashTableFile

class HashTableClient:
    def __init__(self,host,port):

        self.host = host
        self.port = port

        print("connecting to {}:{}".format(self.host,self.port))

        # Now make the connection to the indicated host,port
        self.sock = socket.socket()

        # Note: connect() expects a (host,port) tuple here, and so
        # there must be two sets of parentheses in connect( (host,port) )
        self.sock.connect((self.host,self.port))

        # Note: The socket is much easier to use if we wrap a "file"
        # object (more properly called a stream).  Note that the object
        # must be created in a read-write mode, otherwise you can't write to it.
        self.stream = self.sock.makefile(mode="rw")

    
    # This is a common method for performing a single RPC.
    # Convert the request object into a JSON string, and send it.
    # Wait for a response to come back, and then either return the
    # "result" field, if it exists, or throw an exception.

    def dorpc( self, request ):
        line = json.dumps(request)
        self.stream.write(line+"\n")
        self.stream.flush()
        line = self.stream.readline()
        response = json.loads(line)
        if "status" in response:
            if response["status"] == "OK":
                return response["result"]
            elif response["type"] == "KeyError":
                raise KeyError
            else:
                raise Exception(response["type"])
        else:
            raise Exception("Invalid message from server!")

    # For each of the request types, create a request object,
    # and then invoke the common dorpc method.

    def insert( self, key ):
        ht_file = HashTableFile(key, None)
        value = json.dumps( ht_file.__dict__ )
        request = { "method" : "insert", "key" : key,  "value" : value }
        return self.dorpc(request)

    def lookup( self, key ):
        request = { "method" : "lookup", "key" : key }
        result = self.dorpc(request)
        if result:
            class_dict = json.loads(result)
            ht_file = HashTableFile(None, class_dict)
            ht_file.unpack()
            return key

    def remove( self, key ):
        request = { "method" : "remove", "key" : key }
        return self.dorpc(request)

    def size( self ):
        request = { "method" : "size" }
        return self.dorpc(request)
        
    def query( self, key ):
        request = { "method" : "query", "key" : key }
        return self.dorpc(request)

