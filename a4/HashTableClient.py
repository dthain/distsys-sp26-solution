# This is the client RPC interface to the HashTable server.
# It's job is to send JSON requests, read back responses,
# and translate them into the expected function call format.

import socket
import json
import http.client
from HashTableUtil import HashTableFile, HTMessage, HTMessageBody

class HashTableClient:
    def __init__(self,host,port):

        self.host = host
        self.port = port

        print("connecting to {}:{}".format(self.host,self.port))

        self.sock = socket.socket()

        # Note: connect() expects a (host,port) tuple here, and so
        # there must be two sets of parentheses in connect( (host,port) )
        self.sock.connect((self.host,self.port))

        # # Note: The socket is much easier to use if we wrap a "file"
        # # object (more properly called a stream).  Note that the object
        # # must be created in a read-write mode, otherwise you can't write to it.
        # self.stream = self.sock.makefile(mode="rw")

    
    # This is a common method for performing a single RPC.
    # Convert the request object into a JSON string, and send it.
    # Wait for a response to come back, and then either return the
    # "result" field, if it exists, or throw an exception.

    def dorpc( self, message: HTMessage ):
        # send the message
        message.send_varlen(self.sock)

        # receive status response
        response = HTMessage.recv_varlen(self.sock)

        if response.intent == "STATUS":
            body = response.body
            if body.status == "OK":
                return response
            elif body.status == "KEYERROR":
                raise KeyError
            else:
                raise Exception(body.status)
        else:
            raise Exception("Invalid message from server!")
        
        return None
        


    # For each of the request types, create a request object,
    # and then invoke the common dorpc method.

    def insert( self, key ):
        ht_file = HashTableFile(key).from_disk()
        ht_message = HTMessage("INSERT", HTMessageBody(filename=key, file=ht_file))
        return self.dorpc(ht_message)

    def lookup( self, key ):
        ht_message = HTMessage("LOOKUP", HTMessageBody(filename=key))
        result = self.dorpc(ht_message)

        if result:
            ht_file = result.body.file
            ht_file.to_disk(key)
            return key

    def remove( self, key ):
        ht_message = HTMessage("REMOVE", HTMessageBody(filename=key))
        return self.dorpc(ht_message)

    def size( self ):
        ht_message = HTMessage("SIZE", HTMessageBody())
        return self.dorpc(ht_message)
        
    def query( self, key ):
        ht_message = HTMessage("QUERY", HTMessageBody(filename=key))
        return self.dorpc(ht_message)

