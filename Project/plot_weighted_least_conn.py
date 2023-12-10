import matplotlib.pyplot as plt 
import numpy as np  

file_name1 = './weighted_least_connection/response_times_3.txt'
file_name2 = './weighted_least_connection/response_times_5.txt'
file_name3 = './weighted_least_connection/response_times_7.txt'

values1 = []
with open(file_name1) as f:
	for line in f.readlines():
		values1.append(float(line.strip()))

values2 = []
with open(file_name2) as f:
	for line in f.readlines():
		values2.append(float(line.strip()))

values3 = []
with open(file_name3) as f:
	for line in f.readlines():
		values3.append(float(line.strip()))

plt.plot(np.linspace(1,1+len(values1)),values1,label='Number of servers = 3')
plt.plot(np.linspace(1,1+len(values1)),values2,label='Number of servers = 5')
plt.plot(np.linspace(1,1+len(values1)),values3,label='Number of servers = 7')
plt.title("Avg Response time vs Number of clients for Weighted Least Connections algorithm")

plt.legend()

plt.show()