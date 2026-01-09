#!/usr/bin/env python3

"""
A1 - Measurement Basics
Sebastian Gutierrez

Test 7: making an HTTP connection

"""

import time, http.client as hc

ITERS = 50

def main():
    
    start_time = time.perf_counter()

    for _ in range(ITERS):
        conn = hc.HTTPConnection('www.google.com')
        conn.request("GET","/")

        response = conn.getresponse() # reading HTML
        response.read()
        conn.close()

    elapsed_time = time.perf_counter() - start_time

    print(f"elapsed time: {elapsed_time}; no. iterations: {ITERS}; avg. time per opn: {elapsed_time/ITERS}")

if __name__ == "__main__":
    main()
