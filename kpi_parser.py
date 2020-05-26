import glob
import os
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  

LOG_DIR_NAME = 'logs'
network_settings = ['24GHZ_62MOTES','OFDMSUBGHZ_62MOTES','FSKSUBGHZ_62MOTES']

log_dir_path = os.path.join(os.getcwd(), LOG_DIR_NAME)
#print log_dir_path

#============================ data describer ==================================
def data_describe (data):
	mean= np.mean(data)
	median = np.median(data)
	std = np.std(data)
	first_q = np.quantile(data, 0.25)
	third_q = np.quantile(data, 0.75)	
	return mean,median,std,min(data),max(data),first_q,third_q


def get_kpis(network_setting):
    x_axis         = []
    avg_dutyCycle  = []
    avg_latency    = []
    avg_pdr 	   = []
    avg_cellsUsage = []

    for filename in os.listdir(log_dir_path):
        if ("log-kpis-"+network_setting in filename):
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
    return avg_latency,avg_pdr,avg_cellsUsage,avg_dutyCycle

#for i in range(len(x_axis)):
#	print '{},{}'.format(x_axis[i],avg_dutyCycle[i],avg_latency[i],avg_pdr[i],avg_cellsUsage[i])
avg_dutyCycle_plot = plt.figure(1)
avg_latency_plot = plt.figure(2)
avg_pdr_plot = plt.figure(3)
avg_cellsUsage_plot = plt.figure(4)
for network_setting in network_settings:
    avg_latency,avg_pdr,avg_cellsUsage,avg_dutyCycle = get_kpis(network_setting)
    #avg_dutyCycle_plot = plt.figure(1)
    plt.figure(1)
    plt.plot(avg_dutyCycle, label= network_setting)
    plt.xlabel('Sample index')
    plt.ylabel('Average Duty Cycle, {}'.format(network_setting))
    
    plt.figure(2)
    #avg_latency_plot = plt.figure(2)
    plt.plot(avg_latency, label= network_setting)
    plt.xlabel('Sample index')
    plt.ylabel('Average Latency, {}'.format(network_setting))
    
    #avg_latency_mean,avg_latency_median,avg_latency_std,avg_latency_min,avg_latency_max,avg_latency_1q,avg_latency_3q = data_describe(avg_latency)
    plt.figure(3)
    #avg_pdr_plot = plt.figure(3)
    plt.plot(avg_pdr, label= network_setting)
    plt.xlabel('Sample index')
    plt.ylabel('Average PDR, {}'.format(network_setting))
    
    plt.figure(4)
    #avg_cellsUsage_plot = plt.figure(4)
    plt.plot(avg_cellsUsage, label= network_setting)
    plt.xlabel('Sample index')
    plt.ylabel('Average Cell Usage, {}'.format(network_setting))

plt.figure(1)
plt.legend()    
plt.savefig("avg_avg_dutyCycle_plot.png", bbox_inches='tight')

plt.figure(2)
plt.legend()    
plt.savefig("avg_latency_plot.png", bbox_inches='tight')

plt.figure(3)
plt.legend()    
plt.savefig("avg_pdr_plot.png", bbox_inches='tight')

plt.figure(4)
plt.legend()    
plt.savefig("avg_cellsUsage_plot.png", bbox_inches='tight')
#plt.show()

