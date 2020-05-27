import glob
import os
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  

LOG_DIR_NAME = 'logs'
#network_settings = ['24GHZ_62MOTES','OFDMSUBGHZ_62MOTES','FSKSUBGHZ_62MOTES']
network_settings = ['OFDMSUBGHZ_62MOTES_STATLOGS']

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

def std_add_subtract (data_list,std_list):
    zip_object = zip(data_list,std_list)
    std_sub = []
    std_add = []
    for d_i, s_i in zip_object:
        std_sub.append(d_i-s_i)
        std_add.append(d_i+s_i)

    return std_sub,std_add;

def get_kpis(network_setting):
    x_axis         = []
    avg_dutyCycle  = []
    avg_latency    = []
    avg_pdr 	   = []
    avg_cellsUsage = []
    avg_dutyCycle_first_q = []
    avg_dutyCycle_third_q= []
    avg_dutyCycle_std= []
    avg_latency_first_q= []
    avg_latency_third_q= []
    avg_latency_std= []
    avg_pdr_first_q= []
    avg_pdr_third_q= []
    avg_pdr_std= []
    avg_cellsUsage_first_q= []
    avg_cellsUsage_third_q= []
    avg_cellsUsage_std= []

    for filename in os.listdir(log_dir_path):
        if ("log-kpis-"+network_setting in filename):
            print filename
            file_dir=os.path.join(log_dir_path,filename)
            with open (file_dir) as f:
                for line in f:
                    data=json.loads(line)
                    x_axis.append(data['timestamp'])
                    avg_dutyCycle.append(data['data']['avg_dutyCycle'])
                    avg_dutyCycle_first_q.append(data['data']['stats']['avg_dutyCycle']['first_q'])
                    avg_dutyCycle_third_q.append(data['data']['stats']['avg_dutyCycle']['third_q'])
                    avg_dutyCycle_std.append(data['data']['stats']['avg_dutyCycle']['std'])

                    avg_latency.append(data['data']['avg_latency'])
                    avg_latency_first_q.append(data['data']['stats']['avg_latency']['first_q'])
                    avg_latency_third_q.append(data['data']['stats']['avg_latency']['third_q'])
                    avg_latency_std.append(data['data']['stats']['avg_latency']['std'])

                    avg_pdr.append(data['data']['avg_pdr'])
                    avg_pdr_first_q.append(data['data']['stats']['avg_pdr']['first_q'])
                    avg_pdr_third_q.append(data['data']['stats']['avg_pdr']['third_q'])
                    avg_pdr_std.append(data['data']['stats']['avg_pdr']['std'])

                    avg_cellsUsage.append(data['data']['avg_cellsUsage'])
                    avg_cellsUsage_first_q.append(data['data']['stats']['avg_cellsUsage']['first_q'])
                    avg_cellsUsage_third_q.append(data['data']['stats']['avg_cellsUsage']['third_q'])                   
                    avg_cellsUsage_std.append(data['data']['stats']['avg_cellsUsage']['std'])                   
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
    return avg_latency,avg_latency_first_q,avg_latency_third_q,avg_latency_std,\
    avg_pdr,avg_pdr_first_q,avg_pdr_third_q,avg_pdr_std,\
    avg_cellsUsage,avg_cellsUsage_first_q,avg_cellsUsage_third_q,avg_cellsUsage_std,\
    avg_dutyCycle,avg_dutyCycle_first_q,avg_dutyCycle_third_q,avg_dutyCycle_std;

#for i in range(len(x_axis)):
#	print '{},{}'.format(x_axis[i],avg_dutyCycle[i],avg_latency[i],avg_pdr[i],avg_cellsUsage[i])
avg_dutyCycle_plot = plt.figure(1)
avg_latency_plot = plt.figure(2)
avg_pdr_plot = plt.figure(3)
avg_cellsUsage_plot = plt.figure(4)
for network_setting in network_settings: 
    avg_latency,avg_latency_first_q,avg_latency_third_q,avg_latency_std,\
    avg_pdr,avg_pdr_first_q,avg_pdr_third_q,avg_pdr_std,\
    avg_cellsUsage,avg_cellsUsage_first_q,avg_cellsUsage_third_q,avg_cellsUsage_std,\
    avg_dutyCycle,avg_dutyCycle_first_q,avg_dutyCycle_third_q,avg_dutyCycle_std = get_kpis(network_setting)
    
    x_ax = np.linspace(0, len(avg_cellsUsage), len(avg_cellsUsage))
    
    plt.figure(1)
    plt.plot(avg_dutyCycle, label= network_setting)
    plt.xlabel('Sample index')
    plt.ylabel('Average Duty Cycle, {}'.format(network_setting))
    
    plt.figure(2)
    plt.plot(avg_latency, label= network_setting)
    plt.xlabel('Sample index')
    plt.ylabel('Average Latency, {}'.format(network_setting))
    
    plt.figure(3)
    plt.plot(avg_pdr, label= network_setting)
    plt.xlabel('Sample index')
    plt.ylabel('Average PDR, {}'.format(network_setting))
    
    plt.figure(4)
    l,h = std_add_subtract (avg_cellsUsage,avg_cellsUsage_std)
    plt.plot(avg_cellsUsage, label= network_setting)
    plt.fill_between( x_ax,l,h, alpha=0.2)
    plt.xlabel('Sample index')
    plt.ylabel('Average Cell Usage, {}'.format(network_setting))

plt.figure(1)
plt.grid(True)
plt.legend()    
plt.savefig("avg_avg_dutyCycle_plot.png", bbox_inches='tight')

plt.figure(2)
plt.grid(True)
plt.legend()    
plt.savefig("avg_latency_plot.png", bbox_inches='tight')

plt.figure(3)
plt.grid(True)
plt.legend()    
plt.savefig("avg_pdr_plot.png", bbox_inches='tight')

plt.figure(4)
plt.grid(True)
plt.legend()    
plt.savefig("avg_cellsUsage_plot.png", bbox_inches='tight')
#plt.show()

