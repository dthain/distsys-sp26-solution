#!/usr/bin/env python3

"""
A1 - Measurement Basics
Sebastian Gutierrez

Test 5: dictionary insertion

"""

import time

ITERS = 51250000

def main():
    
    dictionary = {}

    start_time = time.perf_counter()
    for count in range(ITERS):
        dictionary[count] = 1

    elapsed_time = time.perf_counter() - start_time

    print(f"elapsed time: {elapsed_time}; no. iterations: {ITERS}; avg. time per opn: {elapsed_time/ITERS}")

if __name__ == "__main__":
    main()
