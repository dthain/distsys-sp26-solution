#!/usr/bin/env python3

# receive UDP packets

import socket
import time

bufsizes = [32, 64, 128, 256, 512, 1024, 2048, 4096]
#bufsizes = [1024, 2048, 4096]


data_lengths = []
for i in range(4096):
    data = bytes(255 for _ in range(i*2))
    data_lengths.append(len(data))

UDP_PORT = 5005

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
udp_sock.bind((socket.gethostname(), UDP_PORT))

for bufsize in bufsizes:
    msg_count = 0
    while msg_count < 4096:
        bytes_recv = 0
        while bytes_recv < data_lengths[msg_count]:
            data = udp_sock.recv(min(bufsize, data_lengths[msg_count] - bytes_recv))
            bytes_recv += len(data)
        msg_count += 1

    print("UDP reception complete")

udp_sock.close()