#!/usr/bin/env python3

"""
A1 - Measurement Basics
Sebastian Gutierrez

Test 3: touch file in /tmp

"""

import time, os

ITERS = 275000
path = r'/tmp/testfile.txt'

def main():

    start_time = time.perf_counter()
    for _ in range(ITERS):
        with open(path, 'w') as f:
            pass
        os.remove(path)

    elapsed_time = time.perf_counter() - start_time

    print(f"elapsed time: {elapsed_time}; no. iterations: {ITERS}; avg. time per opn: {elapsed_time/ITERS}")

if __name__ == "__main__":
    main()
