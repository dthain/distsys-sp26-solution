#!/usr/bin/env python3

# make a connection to a server
# send UDP packets of incremental size

import socket
import time


bufsizes = [32, 64, 128, 256, 512, 1024, 2048, 4096]
#bufsizes = [1024, 2048, 4096]


IP = socket.gethostname()

UDP_PORT = 5005

for bufsize in bufsizes: 
    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP

    udp_start = time.perf_counter()
    for i in range(4096):
        data = bytes(255 for _ in range(i*2))
        msglen = len(data)
        sent = 0
        while sent < msglen:
            sent += sock.sendto(data[sent:sent+min(bufsize, msglen - sent)], (IP, UDP_PORT))

    udp_elapsed = time.perf_counter() - udp_start
    print(f"UDP bufsize: {bufsize}; elapsed time: {udp_elapsed}")

    sock.close()