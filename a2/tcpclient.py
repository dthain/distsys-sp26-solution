#!/usr/bin/env python3

# make a connection to a server
# send TCP packets of incremental size

import socket
import time
import sys


bufsizes = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]

if len(sys.argv) != 3:
    print("Usage: tcpclient.py <hostname> <port>")
    sys.exit(1)

IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, TCP_PORT))

for bufsize in bufsizes:
    tcp_start = time.perf_counter()
    
    for i in range(2048):
        data = bytes(255 for _ in range(1024))
        msglen = len(data)
        sent = 0
        while sent < msglen:
            sent += sock.send(data[sent:sent+min(bufsize, msglen - sent)])
    
    data = sock.recv(3)  # receive acknowledgment
    print(data)

    tcp_elapsed = time.perf_counter() - tcp_start
    print(f"TCP bufsize: {bufsize}; elapsed time: {tcp_elapsed}")

sock.close()