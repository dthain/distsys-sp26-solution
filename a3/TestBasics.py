import HashTableClient
import sys
import subprocess

if len(sys.argv)!=3:
	print("usage: python TestBasics.py <host> <port>");
	sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])

client = HashTableClient.HashTableClient(host,port)

subprocess.run(["./create_data", "clean"])
subprocess.run(["./create_data", "make", "1", "128"])

value = "test_data_1"

print(f"insert({value})")
client.insert(value)

print(f"lookup({value})")
result = client.lookup(value)

if result!=value:
    raise Exception("error in returned value: {}, Expected: {}".format(result, value))
else:
    print("returns {}".format(result))

print(f"remove({value})")
client.remove(value)

try:
    print(f"lookup({value})")
    result = client.lookup(value)
except KeyError:
    print("lookup correctly returned KeyError")
else:
    raise Exception("lookup did not return KeyError!")

subprocess.run(["./create_data", "clean"])
subprocess.run(["./create_data", "make", "3", "128"])

client.insert("test_data_1")
client.insert("test_data_2")
client.insert("test_data_3")

print(f"query('test_data_1')")
print(f"query('test_data_2')")
print(f"query('test_data_3')")
result = client.query("test_data_3")
print("result: {}".format(result))

subprocess.run(["./create_data", "clean"])