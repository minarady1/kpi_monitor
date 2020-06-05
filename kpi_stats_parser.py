import glob
import os
import json
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  

LOG_DIR_NAME = 'logs'
#network_settings = ['24GHZ_62MOTES','OFDMSUBGHZ_62MOTES','FSKSUBGHZ_62MOTES']
#network_settings = ['OFDMSUBGHZ_62MOTES_STATLOGS','FSKSUBGHZ_62MOTES_STATLOGS']
network_settings = ['OFDMSUBGHZ_65MOTES','FSKSUBGHZ_65MOTES','OQPSK24GHZ_65MOTES']
run_id = "STATLOGS_5"

log_dir_path = os.path.join(os.getcwd(), LOG_DIR_NAME,run_id)
plot_dir_path = os.path.join(os.getcwd(), 'plots', run_id)
if not os.path.exists(plot_dir_path):
    os.makedirs(plot_dir_path)
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

# returns normalized datetime array in mins
def datetime_arr_normalize (arr):
    delta_arr = []
    if (len (arr)>1):
        ref = datetime.datetime.strptime(arr [0], '%Y-%m-%d %H:%M:%S.%f')
        for dts in arr:
            dt = datetime.datetime.strptime(dts, '%Y-%m-%d %H:%M:%S.%f')
            delta = dt-ref
            delta_arr.append(float(delta.seconds)/60)

    return delta_arr


def get_kpis(network_setting):
    timestamp_s    = []
    rpl_node_count = []
    rpl_churn = []
    time_to_firstpacket = []

    avg_dutyCycle  = []
    avg_dutyCycle_first_q = []
    avg_dutyCycle_third_q= []
    avg_dutyCycle_std= []
    
    avg_dutyCycleTx  = []
    avg_dutyCycleTx_first_q = []
    avg_dutyCycleTx_third_q= []
    avg_dutyCycleTx_std= []
    
    avg_dutyCycleRx  = []
    avg_dutyCycleRx_first_q = []
    avg_dutyCycleRx_third_q= []
    avg_dutyCycleRx_std= []
    
    avg_dutyCycleTxRx  = []
    avg_dutyCycleTxRx_first_q = []
    avg_dutyCycleTxRx_third_q= []
    avg_dutyCycleTxRx_std= []
    
    avg_latency    = []
    avg_latency_first_q= []
    avg_latency_third_q= []
    avg_latency_std= []
    
    avg_dagRank    = []
    avg_dagRank_first_q= []
    avg_dagRank_third_q= []
    avg_dagRank_std= []
        
    avg_bufferSize    = []
    avg_bufferSize_first_q= []
    avg_bufferSize_third_q= []
    avg_bufferSize_std= []
    
    avg_pdr 	   = []
    avg_pdr_first_q= []
    avg_pdr_third_q= []
    avg_pdr_std= []
    
    avg_cellsUsage_first_q= []
    avg_cellsUsage = []
    avg_cellsUsage_third_q= []
    avg_cellsUsage_std= []
    
    avg_numNeighbors = []
    avg_numNeighbors_first_q= []
    avg_numNeighbors_third_q= []
    avg_numNeighbors_std= []

    first_arrivals = []
    for filename in os.listdir(log_dir_path):
        if ("log-kpis-"+network_setting in filename):
            print filename
            file_dir=os.path.join(log_dir_path,filename)
            with open (file_dir) as f:
                for line in f:
                    data=json.loads(line)
                    timestamp_s.append(data['timestamp'])

                    avg_dutyCycle.append(data['data']['avg_dutyCycle'])
                    avg_dutyCycle_first_q.append(data['data']['stats']['avg_dutyCycle']['first_q'])
                    avg_dutyCycle_third_q.append(data['data']['stats']['avg_dutyCycle']['third_q'])
                    avg_dutyCycle_std.append(data['data']['stats']['avg_dutyCycle']['std'])

                    avg_dutyCycleTx.append(data['data']['avg_dutyCycleTx'])
                    avg_dutyCycleTx_first_q.append(data['data']['stats']['avg_dutyCycleTx']['first_q'])
                    avg_dutyCycleTx_third_q.append(data['data']['stats']['avg_dutyCycleTx']['third_q'])
                    avg_dutyCycleTx_std.append(data['data']['stats']['avg_dutyCycleTx']['std'])

                    avg_dutyCycleRx.append(data['data']['avg_dutyCycleRx'])
                    avg_dutyCycleRx_first_q.append(data['data']['stats']['avg_dutyCycleRx']['first_q'])
                    avg_dutyCycleRx_third_q.append(data['data']['stats']['avg_dutyCycleRx']['third_q'])
                    avg_dutyCycleRx_std.append(data['data']['stats']['avg_dutyCycleRx']['std'])

                    avg_dutyCycleTxRx.append(data['data']['avg_dutyCycleTxRx'])
                    avg_dutyCycleTxRx_first_q.append(data['data']['stats']['avg_dutyCycleTxRx']['first_q'])
                    avg_dutyCycleTxRx_third_q.append(data['data']['stats']['avg_dutyCycleTxRx']['third_q'])
                    avg_dutyCycleTxRx_std.append(data['data']['stats']['avg_dutyCycleTxRx']['std'])

                    avg_latency.append(data['data']['avg_latency'])
                    avg_latency_first_q.append(data['data']['stats']['avg_latency']['first_q'])
                    avg_latency_third_q.append(data['data']['stats']['avg_latency']['third_q'])
                    avg_latency_std.append(data['data']['stats']['avg_latency']['std'])

                    avg_dagRank.append(data['data']['avg_dagRank'])
                    avg_dagRank_first_q.append(data['data']['stats']['avg_dagRank']['first_q'])
                    avg_dagRank_third_q.append(data['data']['stats']['avg_dagRank']['third_q'])
                    avg_dagRank_std.append(data['data']['stats']['avg_dagRank']['std'])

                    avg_bufferSize.append(data['data']['avg_bufferSize'])
                    avg_bufferSize_first_q.append(data['data']['stats']['avg_bufferSize']['first_q'])
                    avg_bufferSize_third_q.append(data['data']['stats']['avg_bufferSize']['third_q'])
                    avg_bufferSize_std.append(data['data']['stats']['avg_bufferSize']['std'])

                    avg_pdr.append(data['data']['avg_pdr'])
                    avg_pdr_first_q.append(data['data']['stats']['avg_pdr']['first_q'])
                    avg_pdr_third_q.append(data['data']['stats']['avg_pdr']['third_q'])
                    avg_pdr_std.append(data['data']['stats']['avg_pdr']['std'])

                    avg_cellsUsage.append(data['data']['avg_cellsUsage'])
                    avg_cellsUsage_first_q.append(data['data']['stats']['avg_cellsUsage']['first_q'])
                    avg_cellsUsage_third_q.append(data['data']['stats']['avg_cellsUsage']['third_q'])                   
                    avg_cellsUsage_std.append(data['data']['stats']['avg_cellsUsage']['std'])

                    avg_numNeighbors.append(data['data']['stats']['avg_numNeighbors']['mean'])
                    avg_numNeighbors_first_q.append(data['data']['stats']['avg_numNeighbors']['first_q'])
                    avg_numNeighbors_third_q.append(data['data']['stats']['avg_numNeighbors']['third_q'])                   
                    avg_numNeighbors_std.append(data['data']['stats']['avg_numNeighbors']['std'])

                    rpl_node_count.append(data['data']['rpl_node_count'])
                    rpl_churn.append(data['data']['rpl_churn'])

                    #processing time to first packet
                    src_id = data['data']['src_id']
                    if src_id not in first_arrivals:
                        first_arrivals.append(src_id)
                        secs  = float(data['data']['time_elapsed']['seconds'])
                        usecs = float(data['data']['time_elapsed']['microseconds'])
                        time_elapsed_secs = secs + (usecs/1e6)
                        time_to_firstpacket.append(float(time_elapsed_secs))
            continue
        else:
            continue
    timestamp = datetime_arr_normalize(timestamp_s)
    print len(time_to_firstpacket)
    print len(timestamp)
    print len(avg_dutyCycle)
    print len(avg_dutyCycleTx)
    print len(avg_dutyCycleRx)
    print len(avg_dutyCycleTxRx)
    print len(avg_latency)
    print len(avg_bufferSize)
    print len(avg_dagRank)
    print len(avg_pdr)
    print len(avg_cellsUsage)
    print len(avg_numNeighbors)
    return avg_latency,avg_latency_first_q,avg_latency_third_q,avg_latency_std,\
    avg_pdr,avg_pdr_first_q,avg_pdr_third_q,avg_pdr_std,\
    avg_cellsUsage,avg_cellsUsage_first_q,avg_cellsUsage_third_q,avg_cellsUsage_std,\
    avg_dutyCycle,avg_dutyCycle_first_q,avg_dutyCycle_third_q,avg_dutyCycle_std,\
    avg_dutyCycleTx,avg_dutyCycleTx_first_q,avg_dutyCycleTx_third_q,avg_dutyCycleTx_std,\
    avg_dutyCycleRx,avg_dutyCycleRx_first_q,avg_dutyCycleRx_third_q,avg_dutyCycleRx_std,\
    avg_dutyCycleTxRx,avg_dutyCycleTxRx_first_q,avg_dutyCycleTxRx_third_q,avg_dutyCycleTxRx_std,\
    avg_numNeighbors,avg_numNeighbors_first_q,avg_numNeighbors_third_q,avg_numNeighbors_std,\
    avg_dagRank,avg_dagRank_first_q,avg_dagRank_third_q,avg_dagRank_std,\
    avg_bufferSize,avg_bufferSize_first_q,avg_bufferSize_third_q,avg_bufferSize_std,\
    rpl_node_count,rpl_churn,timestamp,time_to_firstpacket;

#for i in range(len(x_axis)):
#	print '{},{}'.format(x_axis[i],avg_dutyCycle[i],avg_latency[i],avg_pdr[i],avg_cellsUsage[i])

for network_setting in network_settings: 
    avg_latency,avg_latency_first_q,avg_latency_third_q,avg_latency_std,\
    avg_pdr,avg_pdr_first_q,avg_pdr_third_q,avg_pdr_std,\
    avg_cellsUsage,avg_cellsUsage_first_q,avg_cellsUsage_third_q,avg_cellsUsage_std,\
    avg_dutyCycle,avg_dutyCycle_first_q,avg_dutyCycle_third_q,avg_dutyCycle_std,\
    avg_dutyCycleTx,avg_dutyCycleTx_first_q,avg_dutyCycleTx_third_q,avg_dutyCycleTx_std,\
    avg_dutyCycleRx,avg_dutyCycleRx_first_q,avg_dutyCycleRx_third_q,avg_dutyCycleRx_std,\
    avg_dutyCycleTxRx,avg_dutyCycleTxRx_first_q,avg_dutyCycleTxRx_third_q,avg_dutyCycleTxRx_std,\
    avg_numNeighbors,avg_numNeighbors_first_q,avg_numNeighbors_third_q,avg_numNeighbors_std,\
    avg_dagRank,avg_dagRank_first_q,avg_dagRank_third_q,avg_dagRank_std,\
    avg_bufferSize,avg_bufferSize_first_q,avg_bufferSize_third_q,avg_bufferSize_std,\
    rpl_node_count,rpl_churn,timestamp, time_to_firstpacket = get_kpis(network_setting)
    
    x_ax = timestamp
    figure_index=0
    
    figure_index+=1
    plt.figure(figure_index)
    plt.plot(x_ax, avg_dutyCycle, label= network_setting)
    l,h = std_add_subtract (avg_dutyCycle,avg_dutyCycle_std)
    plt.fill_between( x_ax,l,h, alpha=0.2)
    plt.xlabel('Timespan (mins)')
    plt.ylabel('Average Duty Cycle')
    
    figure_index+=1
    plt.figure(figure_index)
    plt.plot(x_ax,avg_dutyCycleTx, label= network_setting)
    l,h = std_add_subtract (avg_dutyCycleTx,avg_dutyCycleTx_std)
    plt.fill_between( x_ax,l,h, alpha=0.2)
    plt.xlabel('Timespan (mins)')
    plt.ylabel('Average Tx Duty Cycle')
    
    #figure_index+=1
    #plt.figure(figure_index)
    #plt.plot(x_ax,avg_dutyCycleRx, label= network_setting)
    #l,h = std_add_subtract (avg_dutyCycleRx,avg_dutyCycleRx_std)
    #plt.fill_between( x_ax,l,h, alpha=0.2)
    #plt.xlabel('Timespan (mins)')
    #plt.ylabel('Average Rx Duty Cycle')
    
    #figure_index+=1
    #plt.figure(figure_index)
    #plt.plot(x_ax,avg_dutyCycleTxRx, label= network_setting)
    #l,h = std_add_subtract (avg_dutyCycleTxRx,avg_dutyCycleTxRx_std)
    #plt.fill_between( x_ax,l,h, alpha=0.2)
    #plt.xlabel('Timespan (mins)')
    #plt.ylabel('Average TxRx Duty Cycle')

    figure_index+=1
    plt.figure(figure_index)
    avg_latency_ms = [i*40 for i in avg_latency]
    avg_latency_std_ms = [i*40 for i in avg_latency_std]
    avg_latency_first_q_ms = [i*40 for i in avg_latency_first_q]
    avg_latency_third_q_ms = [i*40 for i in avg_latency_third_q]
    plt.plot(x_ax,avg_latency_ms, label= network_setting)
    l,h = std_add_subtract (avg_latency_ms,avg_latency_std_ms)
    plt.fill_between( x_ax,avg_latency_first_q_ms,avg_latency_third_q_ms, alpha=0.2)
    plt.xlabel('Timespan (mins)')
    plt.ylabel('Average Latency (ms)')
    
    figure_index+=1
    plt.figure(figure_index)
    plt.plot(x_ax,avg_pdr, label= network_setting)
    l,h = std_add_subtract (avg_pdr,avg_pdr_std)
    plt.fill_between( x_ax,l,h, alpha=0.2)
    plt.xlabel('Timespan (mins)')
    plt.ylabel('Average PDR')
    
    figure_index+=1
    plt.figure(figure_index)
    plt.plot(x_ax,avg_cellsUsage, label= network_setting)
    l,h = std_add_subtract (avg_cellsUsage,avg_cellsUsage_std)
    plt.fill_between( x_ax,l,h, alpha=0.2)
    plt.xlabel('Timespan (mins)')
    plt.ylabel('Average Cells Usage')
    
    figure_index+=1
    plt.figure(figure_index)
    plt.plot(x_ax,avg_numNeighbors, label= network_setting)
    l,h = std_add_subtract (avg_numNeighbors,avg_numNeighbors_std)
    plt.fill_between( x_ax,l,h, alpha=0.2)
    plt.xlabel('Timespan (mins)')
    plt.ylabel('Average Number of Neighbors')
 
    figure_index+=1
    plt.figure(figure_index)
    avg_bufferSize_percent = [(i/20)*100 for i in avg_bufferSize]
    avg_bufferSize_std_percent = [(i/20)*100 for i in avg_bufferSize_std]
    avg_bufferSize_first_q_percent = [(i/20)*100 for i in avg_bufferSize_first_q]
    avg_bufferSize_third_q_percent = [(i/20)*100 for i in avg_bufferSize_third_q]
    plt.plot(x_ax,avg_bufferSize_percent, label= network_setting)
    l,h = std_add_subtract (avg_bufferSize_percent,avg_bufferSize_std_percent)
    plt.fill_between( x_ax,avg_bufferSize_first_q_percent,avg_bufferSize_third_q_percent, alpha=0.2)
    plt.xlabel('Timespan (mins)')
    plt.ylabel('Average Packet Buffer Occupancy (%)')
    
    figure_index+=1
    plt.figure(figure_index)
    plt.plot(x_ax,avg_dagRank, label= network_setting)
    l,h = std_add_subtract (avg_dagRank,avg_dagRank_std)
    plt.fill_between( x_ax,avg_dagRank_first_q,avg_dagRank_third_q, alpha=0.2)
    plt.xlabel('Timespan (mins)')
    plt.ylabel('Average DAG Rank')

    figure_index+=1
    plt.figure(figure_index)
    plt.plot(x_ax,rpl_node_count, label= network_setting)
    plt.xlabel('Timespan (mins)')
    plt.ylabel('Network Size (RPL DAG Nodes)')

    figure_index+=1
    plt.figure(figure_index)
    plt.plot(x_ax,rpl_churn, label= network_setting)
    plt.xlabel('Timespan (mins)')
    plt.ylabel('Network Churn (RPL  DAG Churn)')

    #cdf plot for time to first packet
    figure_index+=1
    sortedtime = np.sort(time_to_firstpacket)
    num_bins = 100
    counts, bin_edges = np.histogram (sortedtime, bins=num_bins, normed=True)
    cdf = np.cumsum (counts)
    plt.figure(figure_index)
    plt.plot (bin_edges[1:], cdf/cdf[-1],label= network_setting)
    plt.xlabel('Time to First Packet (seconds)')
    plt.ylabel('F(x)')

#saving the plots
figure_index=0

figure_index+=1
plt.figure(figure_index)
plt.grid(True)
plt.legend()    
plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'avg_avg_dutyCycle_plot.png') , bbox_inches='tight', dpi=300)

figure_index+=1
plt.figure(figure_index)
plt.grid(True)
plt.legend()    
plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'avg_avg_dutyCycleTx_plot.png') , bbox_inches='tight', dpi=300)

#figure_index+=1
#plt.figure(figure_index)
#plt.grid(True)
#plt.legend()    
#plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'avg_avg_dutyCycleRx_plot.png') , bbox_inches='tight', dpi=300)

#figure_index+=1
#plt.figure(figure_index)
#plt.grid(True)
#plt.legend()    
#plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'avg_avg_dutyCycleTxRx_plot.png') , bbox_inches='tight', dpi=300)

figure_index+=1
plt.figure(figure_index)
plt.grid(True)
plt.legend()    
plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'avg_latency_plot.png') , bbox_inches='tight', dpi=300)

figure_index+=1
plt.figure(figure_index)
plt.grid(True)
plt.legend()    
plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'avg_pdr_plot.png') , bbox_inches='tight', dpi=300)

figure_index+=1
plt.figure(figure_index)
plt.grid(True)
plt.legend()    
plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'avg_cellsUsage_plot.png') , bbox_inches='tight', dpi=300)

figure_index+=1
plt.figure(figure_index)
plt.grid(True)
plt.legend()    
plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'avg_numNeighbors_plot.png') , bbox_inches='tight', dpi=300)

figure_index+=1
plt.figure(figure_index)
plt.grid(True)
plt.legend()    
plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'avg_bufferSize_plot.png') , bbox_inches='tight', dpi=300)

figure_index+=1
plt.figure(figure_index)
plt.grid(True)
plt.legend()    
plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'avg_dagRank_plot.png') , bbox_inches='tight', dpi=300)

figure_index+=1
plt.figure(figure_index)
plt.grid(True)
plt.legend()    
plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'rpl_node_count_plot.png') , bbox_inches='tight', dpi=300)

figure_index+=1
plt.figure(figure_index)
plt.grid(True)
plt.legend()    
plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'rpl_churn_plot.png') , bbox_inches='tight', dpi=300)

figure_index+=1
plt.figure(figure_index)
plt.grid(True)
plt.legend()    
plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'time_firstpacket_cdf.png') , bbox_inches='tight', dpi=300)

#plt.show()

