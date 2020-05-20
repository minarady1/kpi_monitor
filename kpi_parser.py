import glob
import os
import json
import matplotlib.pyplot as plt

LOG_DIR_NAME = 'logs'
network_setting = '24GHZ_OQPSK'

log_dir_path = os.path.join(os.getcwd(), LOG_DIR_NAME)
#print log_dir_path

x_axis         = []
avg_dutyCycle  = []
avg_latency    = []
avg_pdr 	   = []
avg_cellsUsage = []

for filename in os.listdir(log_dir_path):
    if ("log-kpis-24GHZ_OQPSK" in filename):
    	print filename
    	file_dir=os.path.join(log_dir_path,filename)
    	with open (file_dir) as f:
    		for line in f:
    			data=json.loads(line)
    			x_axis.append(data['timestamp'])
    			avg_dutyCycle.append(data['data']['avg_dutyCycle'])
    			avg_latency.append(data['data']['avg_latency'])
    			avg_pdr.append(data['data']['avg_pdr'])
    			avg_cellsUsage.append(data['data']['avg_cellsUsage'])
    			#print '{},{}'.format(data['timestamp'],data['data']['avg_dutyCycle'])
    		#print data
        continue
    else:
        continue
print len(x_axis)
print len(avg_dutyCycle)
print len(avg_latency)
print len(avg_pdr)
print len(avg_cellsUsage)

for i in range(len(x_axis)):
	print '{},{}'.format(x_axis[i],avg_dutyCycle[i],avg_latency[i],avg_pdr[i],avg_cellsUsage[i])

avg_dutyCycle_plot = plt.figure(1)
plt.plot(avg_dutyCycle)
plt.xlabel('Sample index')
plt.ylabel('Average Duty Cycle, {}'.format(network_setting))

avg_latency_plot = plt.figure(2)
plt.plot(avg_latency)
plt.xlabel('Sample index')
plt.ylabel('Average Latency, {}'.format(network_setting))

avg_pdr_plot = plt.figure(3)
plt.plot(avg_pdr)
plt.xlabel('Sample index')
plt.ylabel('Average PDR, {}'.format(network_setting))

avg_cellsUsage_plot = plt.figure(4)
plt.plot(avg_cellsUsage)
plt.xlabel('Sample index')
plt.ylabel('Average Cell Usage, {}'.format(network_setting))



plt.show()
