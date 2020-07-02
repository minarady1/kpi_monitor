import glob
import os
import json
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import getKPI
import sys

LOG_DIR_NAME = 'logs'

#network_settings = ['oqpsk_41sf_45nbrs','FSK_SUBGHZ_41SF']
#network_settings = ['fsk_41sf_45nbrs','ofdm_41sf_45nbrs','oqpsk_41sf_45nbrs']
#labels = ['FSK1_868MHz','OFDM_868MHz','OQPSK_2.4GHz']
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
TRANSP= 0.04
fig, axs = plt.subplots(8, sharex=True,figsize=[7.5,13])
iterate=-1
for network_setting in network_settings: 
    iterate+=1
    #avg_latency,avg_latency_first_q,avg_latency_third_q,avg_latency_std,avg_latency_median,\
    #avg_pdr,avg_pdr_first_q,avg_pdr_third_q,avg_pdr_std,avg_pdr_min,avg_pdr_max,avg_pdr_median,\
    #avg_cellsUsage,avg_cellsUsage_first_q,avg_cellsUsage_third_q,avg_cellsUsage_std,\
    #avg_dutyCycle,avg_dutyCycle_first_q,avg_dutyCycle_third_q,avg_dutyCycle_std,avg_dutyCycle_median,\
    #avg_dutyCycleTx,avg_dutyCycleTx_first_q,avg_dutyCycleTx_third_q,avg_dutyCycleTx_std,avg_dutyCycleTx_median,\
    #avg_dutyCycleRx,avg_dutyCycleRx_first_q,avg_dutyCycleRx_third_q,avg_dutyCycleRx_std,\
    #avg_dutyCycleTxRx,avg_dutyCycleTxRx_first_q,avg_dutyCycleTxRx_third_q,avg_dutyCycleTxRx_std,\
    #avg_numNeighbors,avg_numNeighbors_first_q,avg_numNeighbors_third_q,avg_numNeighbors_std,avg_numNeighbors_max,\
    #avg_dagRank,avg_dagRank_first_q,avg_dagRank_third_q,avg_dagRank_std,\
    #avg_bufferSize,avg_bufferSize_first_q,avg_bufferSize_third_q,avg_bufferSize_std,\
    #rpl_node_count,rpl_churn,timestamp,time_to_firstpacket = 
    global_stats, rpl_node_count,rpl_churn,timestamp,rpl_timestamp,time_to_firstpacket = getKPI.get_kpis(network_setting,log_dir_path)
    
    
    x_ax = timestamp
    figure_index=-1
    

    figure_index+=1
    axs[figure_index].plot(x_ax,global_stats ['numNeighbors']['mean'], label= labels [iterate])
    l,h = std_add_subtract (global_stats ['numNeighbors']['mean'],global_stats ['numNeighbors']['std'])
    axs[figure_index].fill_between( x_ax,l,h, alpha=0.2)
    axs[figure_index].set_title('Average Number of Neighbors', fontsize=10)
    axs[figure_index].grid(True)
    axs[figure_index].set_ylim([0,40])
    axs[figure_index].axvspan(0, 20, color='red', alpha=TRANSP)
    axs[figure_index].axvspan(60, 90, color='blue', alpha=TRANSP)
    #disturbance event
    #axs[figure_index].axvspan(31, 32, color='red', alpha=0.5) 
    axs[figure_index].set_xlim(XLIMIT)
    
    #figure_index+=1
    #axs[figure_index].plot(x_ax,avg_numNeighbors_max, label= labels [iterate])
    #axs[figure_index].set_title('Max Number of Neighbors', fontsize=10)
    #axs[figure_index].grid(True)
    #axs[figure_index].set_ylim([0,40])
    ##axs[figure_index].axhspan(30, 30, color='red', alpha=0.5)
    #axs[figure_index].axvspan(0, 5, color='blue', alpha=TRANSP)
    #axs[figure_index].axvspan(5.5, 12.5, color='red', alpha=TRANSP)
    #axs[figure_index].axvspan(20, 27.5, color='grey', alpha=TRANSP)
    ##disturbance event
    ##axs[figure_index].axvspan(31, 32, color='red', alpha=0.5)    

    figure_index+=1
    axs[figure_index].plot(x_ax,global_stats ['maxBufferSize']['max_v'], label= labels [iterate])
    axs[figure_index].fill_between( x_ax,global_stats ['maxBufferSize']['first_q'],global_stats ['maxBufferSize']['third_q'], alpha=0.2)
    axs[figure_index].set_title('Max Packet Buffer Occupancy (Packets)', fontsize=10)
    #axs[figure_index].set_ylim(bottom=0,top=3)
    axs[figure_index].axhspan(15, 15, color='red', alpha=0.5)
    axs[figure_index].axvspan(0, 20, color='red', alpha=TRANSP)
    axs[figure_index].axvspan(60, 90, color='blue', alpha=TRANSP)
    axs[figure_index].grid(True)
    #disturbance event
    #axs[figure_index].axvspan(31, 32, color='red', alpha=0.5)

    figure_index+=1
    axs[figure_index].plot(x_ax,global_stats ['dagRank']['mean'], label= labels [iterate])
    l,h = std_add_subtract (global_stats ['dagRank']['mean'],global_stats ['dagRank']['std'])
    axs[figure_index].fill_between( x_ax,global_stats ['dagRank']['first_q'],global_stats ['dagRank']['third_q'], alpha=0.2)
    axs[figure_index].axvspan(0, 20, color='red', alpha=TRANSP)
    axs[figure_index].axvspan(60, 90, color='blue', alpha=TRANSP)
    axs[figure_index].set_title('Average DAG Rank', fontsize=10)
    axs[figure_index].grid(True)
    #disturbance event
    #axs[figure_index].axvspan(31, 32, color='red', alpha=0.5)

    #figure_index+=1
    #axs[figure_index].plot(x_ax,rpl_churn, label= labels [iterate])
    #axs[figure_index].set_title ('Network Churn', fontsize=10)
    #axs[figure_index].grid(True)
    #axs[figure_index].axvspan(0, 5, color='blue', alpha=TRANSP)
    #axs[figure_index].axvspan(5.5, 15, color='red', alpha=TRANSP)
    #axs[figure_index].axvspan(20, 27.5, color='grey', alpha=TRANSP)
    ##disturbance event
    ##axs[figure_index].axvspan(31, 32, color='red', alpha=0.5)   


    figure_index+=1
    axs[figure_index].plot(rpl_timestamp,rpl_node_count, label= labels [iterate])
    axs[figure_index].set_title('Network Size (RPL DAG Nodes)', fontsize=10)
    axs[figure_index].grid(True)
    axs[figure_index].axvspan(0, 20, color='red', alpha=TRANSP)
    axs[figure_index].axvspan(60, 90, color='blue', alpha=TRANSP)
    #disturbance event
    #axs[figure_index].axvspan(31, 32, color='red', alpha=0.5)    

    #figure_index+=1
    #axs[figure_index].plot(x_ax,avg_pdr_min, label= labels [iterate])
    #axs[figure_index].set_title('Minimum PDR Ratio', fontsize=10)
    #axs[figure_index].grid(True)
    #axs[figure_index].axvspan(5.5,15, color='red', alpha=TRANSP)
    #axs[figure_index].axvspan(0, 5, color='blue', alpha=TRANSP)
    #axs[figure_index].axvspan(20, 27.5, color='grey', alpha=TRANSP)
    ##disturbance event
    ##axs[figure_index].axvspan(31, 32, color='red', alpha=0.5)

    figure_index+=1
    axs[figure_index].plot(x_ax,global_stats ['pdr']['mean'], label= labels [iterate])
    axs[figure_index].fill_between( x_ax,global_stats ['pdr']['first_q'],global_stats ['pdr']['third_q'], alpha=0.2)
    axs[figure_index].set_title('Average PDR Ratio', fontsize=10)
    axs[figure_index].grid(True)
    axs[figure_index].axvspan(0, 20, color='red', alpha=TRANSP)
    axs[figure_index].axvspan(60, 90, color='blue', alpha=TRANSP)
    ##disturbance event
    ##axs[figure_index].axvspan(31, 32, color='red', alpha=0.5)

    figure_index+=1
    axs[figure_index].axvspan(0, 20, color='red', alpha=TRANSP)
    axs[figure_index].axvspan(60, 90, color='blue', alpha=TRANSP)
    avg_latency_secs = [i*.04 for i in global_stats ['latency']['mean']]
    avg_latency_first_q_secs = [i*.04 for i in global_stats ['latency']['first_q']]
    avg_latency_third_q_secs = [i*.04 for i in global_stats ['latency']['third_q']]
    axs[figure_index].plot(x_ax,avg_latency_secs, label= labels [iterate])
    axs[figure_index].fill_between( x_ax,avg_latency_first_q_secs,avg_latency_third_q_secs, alpha=0.2)
    axs[figure_index].set_title('Average Latency (secs)', fontsize=10)
    axs[figure_index].grid(True)
    #disturbance event
    #axs[figure_index].axvspan(31, 32, color='red', alpha=0.5)


    #figure_index+=1
    #axs[figure_index].plot(x_ax,avg_cellsUsage, label= labels [iterate])
    #l,h = std_add_subtract (avg_cellsUsage,avg_cellsUsage_std)
    #axs[figure_index].fill_between( x_ax,avg_cellsUsage_first_q,avg_cellsUsage_third_q, alpha=0.2)
    #axs[figure_index].set_title('Average Cells Usage')



    #figure_index+=1
    #axs[figure_index].plot(x_ax,avg_dutyCycleTx, label= labels [iterate])
    #l,h = std_add_subtract (avg_dutyCycleTx,avg_dutyCycleTx_std)
    #axs[figure_index].fill_between( x_ax,avg_dutyCycleTx_first_q,avg_dutyCycleTx_third_q, alpha=0.2)
    #axs[figure_index].set_title('Average Tx Duty Cycle (%)', fontsize=10)
    #axs[figure_index].grid(True)
    
    figure_index+=1
    axs[figure_index].plot(x_ax, global_stats ['dutyCycleTx']['mean'], label= labels [iterate])
    axs[figure_index].fill_between( x_ax,global_stats ['dutyCycleTx']['first_q'],global_stats ['dutyCycleTx']['third_q'], alpha=0.2)
    axs[figure_index].set_title('Average Radio Transmission Duty Cycle (%)', fontsize=10)
    axs[figure_index].grid(True)
    axs[figure_index].axvspan(0, 20, color='red', alpha=TRANSP)
    axs[figure_index].axvspan(60, 90, color='blue', alpha=TRANSP)   
    
    # print figure_index
    figure_index+=1
    axs[figure_index].plot(x_ax, global_stats ['dutyCycle']['mean'], label= labels [iterate])
    axs[figure_index].fill_between( x_ax,global_stats ['dutyCycle']['first_q'],global_stats ['dutyCycle']['third_q'], alpha=0.2)
    axs[figure_index].set_title('Average Radio Power Duty Cycle (%)', fontsize=10)
    axs[figure_index].grid(True)
    axs[figure_index].axvspan(0, 20, color='red', alpha=TRANSP)
    axs[figure_index].axvspan(60, 90, color='blue', alpha=TRANSP)    

    axs[figure_index].set_xlabel('Time (mins)')
    fig.legend(l,     # The line objects
               labels=labels,   # The labels for each line
               loc="lower center",   # Position of legend
               borderaxespad=0.1   # Small spacing around legend box
               )

plt.subplots_adjust(left=0.09, bottom=0.10, right = 0.96, top = 0.98,hspace=0.28)
plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'aggregate_plot_reliability.png') ,  dpi=300)
plt.show()