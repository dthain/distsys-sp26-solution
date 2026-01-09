#!/usr/bin/env python3

"""
A1 - Measurement Basics
Sebastian Gutierrez

Test 10: ls -l home directory scan

"""

import time, subprocess

ITERS = 1550

def main():

    start_time = time.perf_counter()
    for _ in range(ITERS):
        subprocess.run(["ls -l  ~"], shell=True, stdout=subprocess.DEVNULL)

    elapsed_time = time.perf_counter() - start_time

    print(f"elapsed time: {elapsed_time}; no. iterations: {ITERS}; avg. time per opn: {elapsed_time/ITERS}")

  

if __name__ == "__main__":
    main()
