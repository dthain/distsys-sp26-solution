import HashTableClient
from HashTableUtil import HashTableFile
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

key = "test_data_1"

file = HashTableFile(key).from_disk()

#print(f"insert({key})")
client.insert(key, file)

subprocess.run(["mv", key, f"{key}_copy"])

#print(f"lookup({key})")
result = client.lookup(key)
result.to_disk(f"{key}")

p = subprocess.run(["cmp", key, f"{key}_copy"])

if p.returncode !=0:
    raise Exception("error in file contents for key: {}".format(key))
else:
    print("file contents match for key: {}".format(key))


#print(f"remove({key})")
client.remove(key)

try:
 #   print(f"lookup({key})")
    result = client.lookup(key)
except KeyError:
    pass
    #print("lookup correctly returned KeyError")
else:
    raise Exception("lookup did not return KeyError!")

subprocess.run(["./create_data", "clean"])
subprocess.run(["./create_data", "make", "3", "128"])

td1 = HashTableFile("test_data_1").from_disk()
td2 = HashTableFile("test_data_2").from_disk()
td3 = HashTableFile("test_data_3").from_disk()


client.insert("test_data_1", td1)
client.insert("test_data_2", td2)
client.insert("test_data_3", td3)

# print(f"query('test_data_1')")
# print(f"query('test_data_2')")
# print(f"query('test_data_3')")
result = client.query("test_data_3")
#print("result: {}".format(result.body.query))

subprocess.run(["./create_data", "clean"])