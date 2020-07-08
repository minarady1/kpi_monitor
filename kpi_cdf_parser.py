'''
KPI processing and analytics toolkit for opentestbed
Author: Mina Rady <mina1.rady@orange.com>, July 2020
'''

import glob
import os
import json
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  
import getKPI



LOG_DIR_NAME = 'logs'
PLOT_DIR_NAME = 'cdf_plots'

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

network_settings = ['fsk_2','ofdm','oqpsk_2']
labels = ['FSK_868MHz','OFDM_868MHz','OQPSK_2.4GHz']

run_id = "run_5"

log_dir_path = os.path.join(os.getcwd(), LOG_DIR_NAME,run_id)


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



def create_cdf(kpi_name):
    XLIMIT = [3,90]
    XLABEL = 'Time (mins)'
    iterate=-1
    for network_setting in network_settings: 
        iterate+=1
        figure_index=-1
        global_stats, rpl_node_count,rpl_churn,timestamp,rpl_timestamp,time_to_firstpacket = getKPI.get_kpis(network_setting,log_dir_path)
        x_ax = timestamp
        sorted_data = []
        num_bins = 40
        i = 3
        while i < 90-3:
            r =  global_stats [kpi_name]['raw'][i*60]
            sorted_data=np.sort(r)
            counts, bin_edges = np.histogram (sorted_data, bins=num_bins, normed=True)
            cdf = np.cumsum (counts)
            figure_index+=1
            plt.figure(figure_index)
            plt.plot ( bin_edges[1:], cdf/cdf[-1],label= "{} @ min {}".format(labels [iterate],i))
            plt.xlabel('Duty Cycle')
            plt.ylabel('Portion of motes')
            plt.title('Duty cycle cdf cross section at minute {}'.format(i))
            plt.grid(True)
            plt.legend()
            plot_dir_path = os.path.join(os.getcwd(), PLOT_DIR_NAME, run_id, kpi_name)
            if not os.path.exists(plot_dir_path):
                plot_dir_path = os.path.join(os.getcwd(), PLOT_DIR_NAME, run_id, kpi_name)
                os.makedirs(plot_dir_path)    
            plt.savefig( os.path.join(os.getcwd(), plot_dir_path, '{}_plot_w_5_bins_40_min{}.png'.format(kpi_name,i)) , bbox_inches='tight', dpi=300)
            i+=5
#create_cdf ('latency')
create_cdf ('dutyCycle')
#plt.show()

