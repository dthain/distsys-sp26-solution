#!/usr/bin/env python3

"""
A1 - Measurement Basics
Sebastian Gutierrez

Test 9: scandir of home directory

"""

import time, os

ITERS = 9250

def main():
    start_time = time.perf_counter()

    for _ in range(ITERS):
        for dirent in os.scandir("/escnfs/home/sgutier5/"):
            os.stat(dirent)

    elapsed_time = time.perf_counter() - start_time

    print(f"elapsed time: {elapsed_time}; no. iterations: {ITERS}; avg. time per opn: {elapsed_time/ITERS}") 

if __name__ == "__main__":
    main()
