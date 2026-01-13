#!/usr/bin/env python3

# make a connection to a server
# send TCP packets of incremental size

import socket
import time


bufsizes = [32, 64, 128, 256, 512, 1024, 2048, 4096]
#bufsizes = [1024, 2048, 4096]


IP = socket.gethostname()

TCP_PORT = 5006

for bufsize in bufsizes:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, TCP_PORT))

    tcp_start = time.perf_counter()
    for i in range(4096):
        data = bytes(255 for _ in range(i*2))
        msglen = len(data)
        sent = 0
        while sent < msglen:
            sent += sock.send(data[sent:sent+min(bufsize, msglen - sent)])

    tcp_elapsed = time.perf_counter() - tcp_start
    print(f"TCP bufsize: {bufsize}; elapsed time: {tcp_elapsed}")
    sock.close()