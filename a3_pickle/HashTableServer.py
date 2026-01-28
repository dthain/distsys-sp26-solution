import socket
import time
import json
import sys
import select
import HashTable

from HashTableUtil import HashTableFile, HTMessage, HTMessageBody

class HashTableServer:
    def __init__(self,port):

        self.port = port

        # Turn this to true to enable more messages.
        self.debug = False

        # Set up the listening TCP connection as "master"
        self.master = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)

        # Note: Turn on SO_REUSEADDR option in order to keep running
        # server on the same port every time.
        self.master.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

        # Note: See the double parens?  bind() accepts a tuple of (host,port)
        # and so we write bind( (host,port) ) and not bind(host,port)
        self.master.bind((socket.gethostname(),port))

        # This number doesn't matter much, it's the maximum number of queued connection.
        self.master.listen(5)
        self.table = HashTable.HashTable()

    def run(self):

        # Ask the socket what the local host and port are:
        (host,port) = self.master.getsockname()
        print("server: listening on port {}".format(port))

        # The server should run forever, no matter how many clients connect.
        while True:

            (conn,addr) = self.master.accept()
            print("server: connection from {}:{}".format(addr[0],addr[1]))

            while self.handle_request(conn):
                # connection is good, keep going
                pass

            print("server: disconnected from {}:{}".format(addr[0],addr[1]))

    # This function has been re-written to handle a single request from a client.
    # Just process one request, send one response, and then return.

    def handle_request(self,conn):

            # Note 1: The socket object by itself is difficult to use,
            # so we wrap it up in a "file" object (more accurately, a stream)

            # Note 2: makefile() by default returns a read-only stream,
            # so we must describe it as a read-write stream to write to it.

            #stream = conn.makefile(mode="rw")

            # Our interaction with a single client could throw any number
            # of exceptions.  This try blocks wraps up all of them, and
            # if an unhandled exception is thrown, the connection is dropped
            # and we go back to accepting connections.

            try:
                    # Assume a message is on a single line, and parse
                    # it into a native Python object.

                    message = HTMessage.recv_varlen(conn)

                    if not message:
                        # The client must have disconnected, so return False
                        return False

                    if self.debug:
                        print("message: {} ".format(message.intent))

                    # For each method type, attempt to perform the operation.
                    # If a key error occurs along the way, then return a
                    # special JSON object indicating an exception.

                    if message.intent=="INSERT":
                        try:
                            self.table.insert(message.body.filename,message.body.file)
                            response = HTMessage("STATUS", HTMessageBody(status="OK"))
                        except KeyError:
                            response = HTMessage("STATUS", HTMessageBody(status="KEYERROR"))
                    elif message.intent=="REMOVE":
                        try:
                            self.table.remove(message.body.filename)
                            response = HTMessage("STATUS", HTMessageBody(status="OK"))
                        except KeyError:
                            response = HTMessage("STATUS", HTMessageBody(status="KEYERROR"))
                    elif message.intent=="LOOKUP":
                        try:
                            result = self.table.lookup(message.body.filename)
                            response = HTMessage("STATUS", HTMessageBody(status="OK", file=result))
                        except KeyError:
                            response = HTMessage("STATUS", HTMessageBody(status="KEYERROR"))
                    elif message.intent=="SIZE":
                        try:
                            result = self.table.size()
                            response = HTMessage("STATUS", HTMessageBody(status="OK", size=result))
                        except KeyError:
                            response = HTMessage("STATUS", HTMessageBody(status="KEYERROR"))
                    elif message.intent=="QUERY":
                        result = self.table.query(message.body.filename)
                        response = HTMessage("STATUS", HTMessageBody(status="OK", query=result))
                    else:
                        response = HTMessage("STATUS", HTMessageBody(status="INVALIDMETHOD"))

                    if self.debug:
                        print("response: {} {} ".format(response.intent, response.body.status))

                    # Turn the response object back into a JSON string,
                    # and send it along.  Note that the string gets a newline,
                    # and we must use flush in order to force it to be sent.

                    response.send_varlen(conn)

            except Exception as e:
                # The server failed to process the request, so return False
                print("exception: {}".format(e))
                return False

            # The request was processed successfully, so return True
            return True

if len(sys.argv)!=2:
	print("usage: python HashTableServer.py <port>")
	sys.exit(1)

port = sys.argv[1]

server = HashTableServer(int(port))
server.run()
