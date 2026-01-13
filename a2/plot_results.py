import matplotlib.pyplot as plt

f = open("results.log", "r")

tcp_results = {}
udp_results = {}

for line in f.readlines():
    items = line.split(' ')
    if items[0] == "TCP":
        bufsize = int(items[2].strip(';'))
        tcp_time = float(items[5].strip())
        tcp_results[bufsize] = tcp_time
    elif items[0] == "UDP":
        bufsize = int(items[2].strip(';'))
        udp_time = float(items[5].strip())
        udp_results[bufsize] = udp_time

print(tcp_results)
print(udp_results)

plt.xlabel('Buffer Size (bytes)')
plt.ylabel('Elapsed Time (seconds)')
plt.title('TCP vs UDP Transmission Times')


plt.plot(tcp_results.keys(), tcp_results.values(), color='blue')

plt.plot(udp_results.keys(), udp_results.values(), color='red')

plt.show()