#!/usr/bin/env python3

"""
A1 - Measurement Basics
Sebastian Gutierrez

Test 4: current wall clock time

"""

import time

ITERS = 32500000

def main():

    start_time = time.perf_counter()
    for _ in range(ITERS):
        time.clock_gettime(time.CLOCK_REALTIME) # time.ctime() for readable

    elapsed_time = time.perf_counter() - start_time

    print(f"elapsed time: {elapsed_time}; no. iterations: {ITERS}; avg. time per opn: {elapsed_time/ITERS}")

if __name__ == "__main__":
    main()
