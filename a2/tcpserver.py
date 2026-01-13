#!/usr/bin/env python3

# receive TCP packets

import socket
import time

bufsizes = [32, 64, 128, 256, 512, 1024, 2048, 4096]
#bufsizes = [1024, 2048, 4096]


data_lengths = []
for i in range(4096):
    data = bytes(255 for _ in range(i*2))
    data_lengths.append(len(data))

#tcp socket
TCP_PORT = 5006

tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.bind((socket.gethostname(), TCP_PORT))

for bufsize in bufsizes:
    # tcp receive loop
    msg_count = 0

    print("listening")
    tcp_sock.listen()
    conn, addr = tcp_sock.accept()
    while msg_count < 4096:
        bytes_recv = 0
        while bytes_recv < data_lengths[msg_count]:
            data = conn.recv(min(bufsize, data_lengths[msg_count] - bytes_recv))
            bytes_recv += len(data)
        msg_count += 1

    print(f"TCP msg {msg_count} received")

tcp_sock.close()