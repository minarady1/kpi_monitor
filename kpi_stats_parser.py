import glob
import os
import json
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  
import getKPI



LOG_DIR_NAME = 'logs'
#network_settings = ['24GHZ_62MOTES','OFDMSUBGHZ_62MOTES','FSKSUBGHZ_62MOTES']
#network_settings = ['OFDMSUBGHZ_62MOTES_STATLOGS','FSKSUBGHZ_62MOTES_STATLOGS']
#network_settings = ['FSK1_Subghz_run_1','OFDM1_MCS3_Subghz_run_1','OQPSK_24GHz_run_1']
#network_settings = ['FSK1_Subghz_4PPS_run_1','OFDM1_MCS3_Subghz_4PPS_run_1','OQPSK_24GHz_4PPS_run_1']
#network_settings = ['OQPSK_24GHz_4PPS_run_1','OQPSK_24GHz_run_1']
#network_settings = ['OFDM1_MCS3_Subghz_4PPS_run_1','OFDM1_MCS3_Subghz_run_1']
#network_settings = ['OFDM1_MCS3_Subghz_50percent_density_run_1','OFDM1_MCS3_Subghz_4PPS_run_1','OFDM1_MCS3_Subghz_run_1']
#network_settings = ['OFDM1_MCS3_Subghz_50percent_density_run_1','OQPSK_24GHz_50percent_density_run_1','FSK1_Subghz_50percent_density_run_1']
#network_settings = ['FSK1_Subghz_10percent_disturbance','OQPSK_24GHz_10percent_disturbance_run_1']
#network_settings = ['FSK_SUBGHZ_41SF','OFDM_SUBGHZ_41SF','OQPSK_24GHz_41SF']
#run_id = "run_3"
#network_settings = ['fsk_41sf_45nbrs','ofdm_41sf_45nbrs','oqpsk_41sf_45nbrs']
#labels = ['FSK1_868MHz','OFDM_868MHz','OQPSK_2.4GHz']
#network_settings = ['fsk_41sf_45nbrs','fsk_30ppm_101sf_2min626_3500desync']
#labels = ['FSK1_868MHz_41SF','FSK1_868MHz_101SF']

network_settings = ['openqueuestats']
labels = ['openqueuestats']
run_id = "temp"

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


#for i in range(len(x_axis)):
#	print '{},{}'.format(x_axis[i],avg_dutyCycle[i],avg_latency[i],avg_pdr[i],avg_cellsUsage[i])


XLIMIT = [3,90]
XLABEL = 'Time (mins)'
iterate=-1
for network_setting in network_settings: 
    iterate+=1
    figure_index=-1
    
    global_stats, rpl_node_count,rpl_churn,timestamp,rpl_timestamp,time_to_firstpacket = getKPI.get_kpis(network_setting,log_dir_path)
    
    x_ax = timestamp

    figure_index+=1
    plt.figure(figure_index)
    plt.plot(x_ax, global_stats ['dutyCycle']['mean'], label= labels [iterate])
    plt.fill_between( x_ax,global_stats ['dutyCycle']['first_q'],global_stats ['dutyCycle']['third_q'], alpha=0.2)
    plt.xlim(XLIMIT) 
    plt.ylabel('Average Duty Cycle')
    plt.xlabel(XLABEL)

    
    figure_index+=1
    plt.figure(figure_index)
    plt.plot(x_ax, global_stats ['dutyCycleTx']['mean'], label= labels [iterate])
    plt.fill_between( x_ax,global_stats ['dutyCycleTx']['first_q'],global_stats ['dutyCycleTx']['third_q'], alpha=0.2)
    plt.xlim(XLIMIT) 
    plt.ylabel('Average Tx Duty Cycle (%)')
    plt.xlabel(XLABEL)

    #figure_index+=1
    #plt.figure(figure_index)
    #plt.plot(x_ax,avg_dutyCycleRx, label= labels [iterate])
    #l,h = std_add_subtract (avg_dutyCycleRx,avg_dutyCycleRx_std)
    #plt.fill_between( x_ax,l,h, alpha=0.2)
    #plt.xlabel('Timespan (mins)')
    #plt.ylabel('Average Rx Duty Cycle')
    
    #figure_index+=1
    #plt.figure(figure_index)
    #plt.plot(x_ax,avg_dutyCycleTxRx, label= labels [iterate])
    #l,h = std_add_subtract (avg_dutyCycleTxRx,avg_dutyCycleTxRx_std)
    #plt.fill_between( x_ax,l,h, alpha=0.2)
    #plt.xlabel('Timespan (mins)')
    #plt.ylabel('Average TxRx Duty Cycle')

    figure_index+=1
    plt.figure(figure_index)
    avg_latency_ms = [i*.04 for i in global_stats ['latency']['mean']]
    avg_latency_median_ms = [i*.04 for i in global_stats ['latency']['median']]
    avg_latency_std_ms = [i*.04 for i in global_stats ['latency']['std']]
    avg_latency_first_q_ms = [i*.04 for i in global_stats ['latency']['first_q']]
    avg_latency_third_q_ms = [i*.04 for i in global_stats ['latency']['third_q']]
    plt.plot(x_ax,avg_latency_ms, label= labels [iterate])
    plt.fill_between( x_ax,avg_latency_first_q_ms,avg_latency_third_q_ms, alpha=0.2)
    plt.xlim(XLIMIT) 
    plt.ylabel('Average Latency (secs)')
    plt.xlabel(XLABEL)

    figure_index+=1
    plt.figure(figure_index)
    plt.plot(x_ax,global_stats ['pdr']['mean'], label= labels [iterate])
    plt.fill_between( x_ax,global_stats ['pdr']['first_q'],global_stats ['pdr']['third_q'], alpha=0.2)
    plt.xlim(XLIMIT) 
    plt.ylabel('Average End-to-End PDR')
    plt.xlabel(XLABEL)

    figure_index+=1
    plt.figure(figure_index)
    plt.plot(x_ax,global_stats ['numCellsUsage']['mean'], label= labels [iterate])
    plt.fill_between( x_ax,global_stats ['numCellsUsage']['first_q'],global_stats ['numCellsUsage']['third_q'], alpha=0.2)
    plt.xlim(XLIMIT) 
    plt.ylabel('Average Cells Usage')
    plt.xlabel(XLABEL)

    figure_index+=1
    plt.figure(figure_index)
    plt.plot(x_ax,global_stats ['numCellsUsage']['mean'], label= labels [iterate])
    plt.fill_between( x_ax,global_stats ['numCellsUsage']['first_q'],global_stats ['numCellsUsage']['third_q'], alpha=0.2)
    plt.xlim(XLIMIT) 
    plt.ylabel('Average Number of Neighbors')
    plt.xlabel(XLABEL)

    figure_index+=1
    plt.figure(figure_index)
    # avg_bufferSize_percent = [(i/20)*100 for i in global_stats ['maxBufferSize']['max_v']]
    # avg_bufferSize_first_q_percent = [(i/20)*100 for i in global_stats ['maxBufferSize']['first_q']]
    # avg_bufferSize_third_q_percent = [(i/20)*100 for i in global_stats ['maxBufferSize']['third_q']]
    plt.plot(x_ax,global_stats ['maxBufferSize']['max_v'], label= labels [iterate])
    plt.fill_between( x_ax,global_stats ['maxBufferSize']['first_q'],global_stats ['maxBufferSize']['third_q'], alpha=0.2)
    plt.ylim(bottom=0) 
    plt.xlim(XLIMIT) 
    plt.ylabel('Max Packet Buffer Occupancy (Packets)')
    plt.xlabel(XLABEL)

    figure_index+=1
    plt.figure(figure_index)
    plt.plot(x_ax,global_stats ['dagRank']['mean'], label= labels [iterate])
    plt.fill_between( x_ax,global_stats ['dagRank']['first_q'],global_stats ['dagRank']['third_q'], alpha=0.2)
    plt.ylabel('Average DAG Rank')
    plt.xlim(XLIMIT) 
    plt.xlabel(XLABEL)

    figure_index+=1
    plt.figure(figure_index)
    plt.plot(rpl_timestamp,rpl_node_count, label= labels [iterate])
    plt.ylabel('Network Size (RPL DAG Nodes)')
    plt.xlabel(XLABEL)
    plt.xlim(XLIMIT) 

    figure_index+=1
    plt.figure(figure_index)
    plt.plot(rpl_timestamp,rpl_churn, label= labels [iterate])
    plt.xlabel(XLABEL)
    plt.ylabel('Network Churn (RPL  DAG Churn)')
    plt.xlim(XLIMIT) 

    #cdf plot for time to first packet
    figure_index+=1
    time_to_firstpacket_mins= [float(i/60) for i in time_to_firstpacket]
    sortedtime = np.sort(time_to_firstpacket_mins)
    num_bins = 100
    counts, bin_edges = np.histogram (sortedtime, bins=num_bins, normed=True)
    cdf = np.cumsum (counts)
    plt.figure(figure_index)
    plt.plot ( bin_edges[1:], cdf/cdf[-1],label= labels [iterate])
    plt.xlabel(XLABEL)
    plt.ylabel('Portion of motes reporting data')


#saving the plots
figure_index=-1

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

