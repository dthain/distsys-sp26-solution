#!/usr/bin/env python3

"""
A1 - Measurement Basics
Sebastian Gutierrez

Test 2: touch file in $HOME

"""

import time, os

ITERS = 1500

def main():

    path = os.path.join(os.path.expanduser('~'), 'testfile.txt')


    start_time = time.perf_counter()
    for _ in range(ITERS):
        with open(path, 'w') as f:
            pass
        os.remove(path)

    elapsed_time = time.perf_counter() - start_time

    print(f"elapsed time: {elapsed_time}; no. iterations: {ITERS}; avg. time per opn: {elapsed_time/ITERS}")

if __name__ == "__main__":
    main()
