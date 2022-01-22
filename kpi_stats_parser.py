'''
KPI processing and analytics toolkit for opentestbed
Author: Mina Rady <mina1.rady@orange.com>, July 2020
'''
import sys
import glob
import os
import json
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  
import getKPI
import math
import pdb

LOG_DIR_NAME = 'logs'
PLOT_DIR_NAME = 'plots'

#  make sure that g6tisch logs have the keyword "hybrid" in them
network_settings = [
'g6_fsk',
'g6_ofdm',
'g6_oqpsk',
'g6_hybrid_basicdio_251'

]

labels = [
'FSK_868MHz',
'OFDM_868MHz',
'OQPSK_2.4GHz',
'g6TiSCH' #g6_hybrid_basicdio_251

]


run_id = "run_16"

log_dir_path = os.path.join(os.getcwd(), LOG_DIR_NAME,run_id)
plot_dir_path = os.path.join(os.getcwd(), PLOT_DIR_NAME, run_id)
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


XLIMIT = [3,90] # default [3,90]
XLABEL = 'time (mins)'
TYPE = 'mean' # mean
iterate=-1
churn_a = []
for network_setting in network_settings: 
    iterate+=1
    figure_index=-1
    
    global_stats, kpi_stats_by_mote, rpl_node_count,rpl_churn, rpl_phys,timestamp,rpl_timestamp,time_to_firstpacket,pdr_table = \
    getKPI.get_kpis(network_setting,0,90,3,log_dir_path) #default 0,90,3

    x_ax = timestamp

    figure_index+=1
    plt.figure(figure_index)
    plt.plot(x_ax, global_stats ['dutyCycle'][TYPE], label= labels [iterate])
    plt.fill_between( x_ax,global_stats ['dutyCycle']['first_q'],global_stats ['dutyCycle']['third_q'], alpha=0.2)
    plt.xlim(XLIMIT) 
    plt.ylabel('overall radio duty cycle (%)')
    plt.xlabel(XLABEL)
  
    figure_index+=1
    plt.figure(figure_index)
    plt.plot(x_ax, global_stats ['dutyCycle_1'][TYPE], label= '{}-FSK'.format(labels [iterate]))
    plt.fill_between( x_ax,global_stats ['dutyCycle_1']['first_q'],global_stats ['dutyCycle_1']['third_q'], alpha=0.2)

    plt.plot(x_ax, global_stats ['dutyCycle_2'][TYPE], label= '{}-OFDM'.format(labels [iterate]))
    plt.fill_between( x_ax,global_stats ['dutyCycle_2']['first_q'],global_stats ['dutyCycle_2']['third_q'], alpha=0.2)
      
    plt.plot(x_ax, global_stats ['dutyCycle_0'][TYPE], label= '{}-OQPSK'.format(labels [iterate]))
    plt.fill_between( x_ax,global_stats ['dutyCycle_0']['first_q'],global_stats ['dutyCycle_0']['third_q'], alpha=0.2)
    plt.xlim(XLIMIT) 
    plt.ylabel('duty cycle of the different radios (%)')
    plt.xlabel(XLABEL)
    
    
    figure_index+=1
    plt.figure(figure_index)
    plt.plot(x_ax, global_stats ['dutyCycleTx'][TYPE], label= labels [iterate])
    plt.fill_between( x_ax,global_stats ['dutyCycleTx']['first_q'],global_stats ['dutyCycleTx']['third_q'], alpha=0.2)
    plt.xlim(XLIMIT) 
    plt.ylabel('radio transmission duty cycle (%)')
    plt.xlabel(XLABEL)

    figure_index+=1
    plt.figure(figure_index)
    if ("hybrid" in network_setting):
        plt.plot(x_ax, global_stats ['dutyCycleTx_1'][TYPE], label= '{}-FSK'.format(labels [iterate]))
        plt.fill_between( x_ax,global_stats ['dutyCycleTx_1']['first_q'],global_stats ['dutyCycleTx_1']['third_q'], alpha=0.2)
        
        plt.plot(x_ax, global_stats ['dutyCycleTx_2'][TYPE], label= '{}-OFDM'.format(labels [iterate]))
        plt.fill_between( x_ax,global_stats ['dutyCycleTx_2']['first_q'],global_stats ['dutyCycleTx_2']['third_q'], alpha=0.2)

        plt.plot(x_ax, global_stats ['dutyCycleTx_0'][TYPE], label= '{}-OQPSK'.format(labels [iterate]))
        plt.fill_between( x_ax,global_stats ['dutyCycleTx_0']['first_q'],global_stats ['dutyCycleTx_0']['third_q'], alpha=0.2)
        
        plt.xlim(XLIMIT) 
        plt.ylabel('duty cycle of the different radios (%)')
        plt.xlabel(XLABEL)

    figure_index+=1
    plt.figure(figure_index)
    avg_latency_secs = global_stats ['latency'][TYPE]
    # avg_latency_median_secs = global_stats ['latency']['median']
    avg_latency_first_q_secs = global_stats ['latency']['first_q']
    avg_latency_third_q_secs =  global_stats ['latency']['third_q']
    plt.plot(x_ax,avg_latency_secs, label= labels [iterate])
    plt.fill_between( x_ax,avg_latency_first_q_secs,avg_latency_third_q_secs, alpha=0.2)
    plt.xlim(XLIMIT) 
    plt.ylabel('end-to-end latency (s)')
    plt.xlabel(XLABEL)

    figure_index+=1
    plt.figure(figure_index)
    plt.plot(x_ax,global_stats ['pdr'][TYPE], label= labels [iterate])
    plt.xlim(XLIMIT) 
    plt.ylabel('average end-to-end PDR')
    plt.xlabel(XLABEL)
    print ('PDR -----------')
    # print global_stats ['pdr']

    figure_index+=1
    plt.figure(figure_index)
    plt.plot(x_ax,global_stats ['numCellsUsage'][TYPE], label= labels [iterate])
    plt.fill_between( x_ax,global_stats ['numCellsUsage']['first_q'],global_stats ['numCellsUsage']['third_q'], alpha=0.2)
    plt.xlim(XLIMIT) 
    plt.ylabel('average cells usage')
    plt.xlabel(XLABEL)

    figure_index+=1
    plt.figure(figure_index)
    plt.plot(x_ax,global_stats ['numNeighbors'][TYPE], label= labels [iterate])
    plt.fill_between( x_ax,global_stats ['numNeighbors']['first_q'],global_stats ['numNeighbors']['third_q'], alpha=0.2)
    plt.xlim(XLIMIT) 
    plt.ylabel('number of neighbors')
    plt.xlabel(XLABEL)

    figure_index+=1
    plt.figure(figure_index)
    # avg_bufferSize_percent = [(i/20)*100 for i in global_stats ['maxBufferSize']['max_v']]
    # avg_bufferSize_first_q_percent = [(i/20)*100 for i in global_stats ['maxBufferSize']['first_q']]
    # avg_bufferSize_third_q_percent = [(i/20)*100 for i in global_stats ['maxBufferSize']['third_q']]
    plt.plot(x_ax,global_stats ['maxBufferSize'][TYPE], label= labels [iterate])
    # plt.fill_between( x_ax,global_stats ['maxBufferSize']['first_q'],global_stats ['maxBufferSize']['third_q'], alpha=0.2)
    # plt.ylim(bottom=0, top=5) 
    plt.xlim(XLIMIT) 
    plt.ylabel('average packet buffer occupancy (packets)')
    plt.xlabel(XLABEL)

    figure_index+=1
    plt.figure(figure_index)
    # avg_bufferSize_percent = [(i/20)*100 for i in global_stats ['maxBufferSize']['max_v']]
    # avg_bufferSize_first_q_percent = [(i/20)*100 for i in global_stats ['maxBufferSize']['first_q']]
    # avg_bufferSize_third_q_percent = [(i/20)*100 for i in global_stats ['maxBufferSize']['third_q']]
    plt.plot(x_ax,global_stats ['maxBufferSize']['max_v'], label= labels [iterate])
    # plt.fill_between( x_ax,global_stats ['maxBufferSize']['first_q'],global_stats ['maxBufferSize']['third_q'], alpha=0.2)
    # plt.ylim(bottom=0) 
    plt.xlim([30,90]) 
    plt.yticks(range(0,21,2))
    plt.ylabel('maximum packet buffer occupancy in the network (packets)')
    plt.xlabel(XLABEL)

    figure_index+=1
    plt.figure(figure_index)
    plt.plot(x_ax,global_stats ['dagRank'][TYPE], label= labels [iterate])
    plt.fill_between( x_ax,global_stats ['dagRank']['first_q'],global_stats ['dagRank']['third_q'], alpha=0.2)
    plt.ylabel('DAG rank')
    plt.yscale('log')
    plt.xlim(XLIMIT) 
    plt.xlabel(XLABEL)

    figure_index+=1
    plt.figure(figure_index)
    plt.plot(rpl_timestamp,rpl_node_count, label= labels [iterate])
    plt.ylabel('number of nodes reporting DAOs')
    plt.xlabel(XLABEL)
    plt.xlim(XLIMIT) 

    figure_index+=1
    churn_a.append(rpl_churn)
    plt.figure(figure_index)
    plt.plot(rpl_timestamp,rpl_churn, label= labels [iterate],)
    plt.xlabel(XLABEL)
    plt.ylabel('network churn (RPL DAG Churn)')
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
    plt.ylabel('portion of motes reporting data')

    # hybrid radio distribution
    figure_index+=1
    plt.figure(figure_index)
    if ("hybrid" in network_setting):
        plt.plot(rpl_timestamp,rpl_phys [1], label= labels [iterate]+" FSK_868MHz")
        plt.plot(rpl_timestamp,rpl_phys [2], label= labels [iterate]+" OFDM_868MHz")
        plt.plot(rpl_timestamp,rpl_phys [0], label= labels [iterate]+" O-QPSK_2.4GHz")
        plt.xlim([0,30])
        max_tick = max(max(rpl_phys [1]),max(rpl_phys [2]),max(rpl_phys [0]))
        # pdb.set_trace()
        yint = range(0, 20, 2) # forcing int y axis
        plt.xlabel(XLABEL)
        plt.yticks(yint) 

        plt.ylabel('number of data up-links')
#saving the plots

    # print "----  PDR TABLE -----"
    # print (pdr_table)
    # print "----  End PDR TABLE -----"
# sys.exit()

figure_index=-1

figure_index+=1
plt.figure(figure_index)
plt.grid(True)
plt.legend()    
plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'dutyCycle_plot_{}.png'.format(TYPE)) , bbox_inches='tight', dpi=300)

figure_index+=1
plt.figure(figure_index)
plt.grid(True)
plt.legend()    
plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'dutyCycle_hybrid_plot_{}.png'.format(TYPE)) , bbox_inches='tight', dpi=300)

figure_index+=1
plt.figure(figure_index)
plt.grid(True)
plt.legend()    
plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'dutyCycleTx_plot_{}.png'.format(TYPE)) , bbox_inches='tight', dpi=300)

figure_index+=1
plt.figure(figure_index)
plt.grid(True)
plt.legend()    
plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'dutyCycleTx_hybrid_plot_{}.png'.format(TYPE)) , bbox_inches='tight', dpi=300)

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
plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'latency_plot_{}.png'.format(TYPE)) , bbox_inches='tight', dpi=300)

figure_index+=1
plt.figure(figure_index)
plt.grid(True)
plt.legend()    
plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'pdr_plot_{}.png'.format(TYPE)) , bbox_inches='tight', dpi=300)

figure_index+=1
plt.figure(figure_index)
plt.grid(True)
plt.legend()    
plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'cellsUsage_plot_{}.png'.format(TYPE)) , bbox_inches='tight', dpi=300)

figure_index+=1
plt.figure(figure_index)
plt.grid(True)
plt.legend()    
plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'neighbors_time.png'.format(TYPE)) , bbox_inches='tight', dpi=300)

figure_index+=1
plt.figure(figure_index)
plt.grid(True)
plt.legend()    
plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'bufferSize_plot_{}.png'.format(TYPE)) , bbox_inches='tight', dpi=300)

figure_index+=1
plt.figure(figure_index)
plt.grid(True)
plt.legend()    
plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'max_bufferSize_plot.png') , bbox_inches='tight', dpi=300)


figure_index+=1
plt.figure(figure_index)
plt.grid(True)
plt.legend()        
plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'dagrank_time.png') , bbox_inches='tight', dpi=300)

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

figure_index+=1
plt.figure(figure_index)
plt.grid(True)
plt.legend()    
plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'rpl_phys.png') , bbox_inches='tight', dpi=300)

figure_index+=1
plt.figure(figure_index)
plt.grid(True)
plt.yscale('log')
plt.hist(churn_a, density=False, bins=10, label=labels)
# for a in churn_a:
    # print sum(a)
plt.legend()    
plt.savefig( os.path.join(os.getcwd(), plot_dir_path, 'churn_pdf.png') , bbox_inches='tight', dpi=300)



#plt.show()

