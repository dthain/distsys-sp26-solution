#!/usr/bin/env python3

# make a connection to a server
# send UDP packets of incremental size

import socket
import time
import sys


bufsizes = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
#bufsizes = [1024, 2048, 4096]

if len(sys.argv) != 3:
    print("Usage: udpclient.py <SERVER_IP> <UDP_PORT>")
    sys.exit(1)

IP = sys.argv[1]
UDP_PORT = int(sys.argv[2])

for bufsize in bufsizes: 
    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP

    udp_start = time.perf_counter()
    
    for i in range(2048):
        data = bytes(255 for _ in range(1024))
        msglen = len(data)
        sent = 0
        while sent < msglen:
            sent += sock.sendto(data[sent:sent+min(bufsize, msglen - sent)], (IP, UDP_PORT))
    ack, addr = sock.recvfrom(3)  # receive acknowledgment
    if ack != b'ack':
        print("No ack from server")

    udp_elapsed = time.perf_counter() - udp_start
    print(f"UDP bufsize: {bufsize}; elapsed time: {udp_elapsed}")

    sock.close()