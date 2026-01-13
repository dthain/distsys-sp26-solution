import time
import math
import os
import sys
import SpreadSheetClient

if len(sys.argv)!=3:
	print("usage: python TestPerf.py <host> <port>");
	sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])

client = SpreadSheetClient.SpreadSheetClient(host,port)

count = 1000

start = time.time()
for i in range(count):
    client.insert(i,i,i)
stop = time.time()
elapsed = stop - start

print("insert: xput {} ops/s, latency {}s".format(count/elapsed,elapsed/count))

start = time.time()
for i in range(count):
    client.lookup(i,i)
stop = time.time()
elapsed = stop - start

print("lookup: xput {} ops/s, latency {}s".format(count/elapsed,elapsed/count))

start = time.time()
for i in range(count):
    client.size()
stop = time.time()
elapsed = stop - start

print("size: xput {} ops/s, latency {}s".format(count/elapsed,elapsed/count))

start = time.time()
for i in range(count):
    client.query(0,0,100,100)
stop = time.time()
elapsed = stop - start

print("query:   xput {} ops/s, latency {}s".format(count/elapsed,elapsed/count))

count = 1000

start = time.time()
for i in range(count):
    client.remove(i,i)
stop = time.time()
elapsed = stop - start

print("remove:   xput {} ops/s, latency {}s".format(count/elapsed,elapsed/count))




