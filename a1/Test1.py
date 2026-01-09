#!/usr/bin/env python3

"""
A1 - Measurement Basics
Sebastian Gutierrez

Test 1: trivial function call

"""

import time 

ITERS = 85000000

def trivial_function():
    pass

def main():

    start_time = time.perf_counter()
    for _ in range(ITERS):
        trivial_function()

    elapsed_time = time.perf_counter() - start_time

    print(f"elapsed time: {elapsed_time}; no. iterations: {ITERS}; avg. time per opn: {elapsed_time/ITERS}")
    
if __name__ == "__main__":
    main()
