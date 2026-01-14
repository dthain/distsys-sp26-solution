#!/usr/bin/env python3

# receive UDP packets

import socket
import sys

bufsizes = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
#bufsizes = [1024, 2048, 4096]

if len(sys.argv) != 2:
    print("Usage: udpserver.py <UDP_PORT>")
    sys.exit(1)

UDP_PORT = int(sys.argv[1])

data_len = 2048*len(bytes(255 for _ in range(1024)))

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) 
udp_sock.bind((socket.gethostname(), UDP_PORT))

for bufsize in bufsizes:
    bytes_recv = 0
    while bytes_recv < data_len:
        data, addr = udp_sock.recvfrom(min(bufsize, data_len - bytes_recv))
        bytes_recv += len(data)
    udp_sock.sendto(b'ack', addr)  # send acknowledgment

    print("Bufsize {} complete".format(bufsize))

udp_sock.close()