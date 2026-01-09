#!/usr/bin/env python3

"""
A1 - Measurement Basics
Sebastian Gutierrez

Test 6: opening TCP conection

"""

import time, socket

ITERS = 95
address = ('localhost', 25) # connecting to SMTP

def main():

    start_time = time.perf_counter() 
    for _ in range(ITERS):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        sock.close()

    elapsed_time = time.perf_counter() - start_time
    
    print(f"elapsed time: {elapsed_time}; no. iterations: {ITERS}; avg. time per opn: {elapsed_time/ITERS}")

if __name__ == "__main__":
    main()
