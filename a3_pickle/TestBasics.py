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

#print(f"insert({value})")
client.insert(value)

subprocess.run(["mv", value, f"{value}_copy"])

#print(f"lookup({value})")
result = client.lookup(value)

p = subprocess.run(["cmp", value, f"{value}_copy"])

if p.returncode !=0:
    raise Exception("error in file contents for key: {}".format(value))
else:
    print("file contents match for key: {}".format(value))

if result!=value:
    raise Exception("error in returned value: {}, Expected: {}".format(result, value))
else:
    print("returns {}".format(result))

#print(f"remove({value})")
client.remove(value)

try:
 #   print(f"lookup({value})")
    result = client.lookup(value)
except KeyError:
    pass
    #print("lookup correctly returned KeyError")
else:
    raise Exception("lookup did not return KeyError!")

subprocess.run(["./create_data", "clean"])
subprocess.run(["./create_data", "make", "3", "128"])

client.insert("test_data_1")
client.insert("test_data_2")
client.insert("test_data_3")

# print(f"query('test_data_1')")
# print(f"query('test_data_2')")
# print(f"query('test_data_3')")
result = client.query("test_data_3")
#print("result: {}".format(result.body.query))

subprocess.run(["./create_data", "clean"])