#!/usr/bin/env python3

# receive TCP packets

import socket
import sys

bufsizes = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]

data_len = 2048*len(bytes(255 for _ in range(1024)))

#tcp socket
if len(sys.argv) != 2:
    print("Usage: tcpserver.py <TCP_PORT>")
    sys.exit(1)

TCP_PORT = int(sys.argv[1])

tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.bind((socket.gethostname(), TCP_PORT))

print("listening")
tcp_sock.listen()
conn, addr = tcp_sock.accept()

for bufsize in bufsizes:
    bytes_recv = 0
    while bytes_recv < data_len:
        data = conn.recv(min(bufsize, data_len - bytes_recv))
        bytes_recv += len(data)

    conn.send(b'ack')  # send acknowledgment each 2048*1024 bytes
    print(f"Bufsize {bufsize} complete")

conn.recv(0) # to ensure client has received ack before closing
tcp_sock.close()