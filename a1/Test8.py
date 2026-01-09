#!/usr/bin/env python3

"""
A1 - Measurement Basics
Sebastian Gutierrez

Test 8: JSON parsing

"""

import time, json

ITERS = 4025

def main():

    start_time = time.perf_counter()
    for _ in range(ITERS):
        fp = open("big.json")

        obj = json.load(fp) # parsing into memory
        
        fp.close()

    elapsed_time = time.perf_counter() - start_time

    print(f"elapsed time: {elapsed_time}; no. iterations: {ITERS}; avg. time per opn: {elapsed_time/ITERS}")

if __name__ == "__main__":
    main()
