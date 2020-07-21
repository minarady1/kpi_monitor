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
import sys



LOG_DIR_NAME = 'logs'
PLOT_DIR_NAME = 'pdf_plots_full'
DIR_TAG='full_'
XLABEL=''
NUMBINS=100

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

network_settings = ['fsk_2','ofdm_1','oqpsk_2']
labels = ['FSK_868MHz','OFDM_868MHz','OQPSK_2.4GHz']
# network_settings = ['fsk_2']
# labels = ['FSK_868MHz']

run_id = "run_5"

log_dir_path = os.path.join(os.getcwd(), LOG_DIR_NAME,run_id)

class FullCDF:
    def __init__ (self, kpi,t1,t2):
        self.kpi = kpi
        self.t1 = t1
        self.t2 = t2

    #============================ data describer ==================================
    def data_describe (self,data):
    	mean= np.mean(data)
    	median = np.median(data)
    	std = np.std(data)
    	first_q = np.quantile(data, 0.25)
    	third_q = np.quantile(data, 0.75)	
    	return mean,median,std,min(data),max(data),first_q,third_q

    def std_add_subtract (self,data_list,std_list):
        zip_object = zip(data_list,std_list)
        std_sub = []
        std_add = []
        for d_i, s_i in zip_object:
            std_sub.append(d_i-s_i)
            std_add.append(d_i+s_i)

        return std_sub,std_add;


    #for i in range(len(x_axis)):
    #	print '{},{}'.format(x_axis[i],avg_dutyCycle[i],avg_latency[i],avg_pdr[i],avg_cellsUsage[i])

    def create_cdf(self):
        kpi_name = self.kpi
        print kpi_name
        iterate=-1
        plt.figure(0)
        for network_setting in network_settings: 
            data_list = []
            iterate+=1
            global_stats, rpl_node_count,rpl_churn,timestamp,rpl_timestamp,time_to_firstpacket =\
                getKPI.get_kpis(network_setting,self.t1,self.t2,self.t2-self.t1-1,log_dir_path)
            x_ax = timestamp
            sorted_data = []
            num_bins = 200
            i = 3
            while i < 90-3:
                r =  global_stats [kpi_name]['raw'][0]
                data_list.append(np.array(r))
                i+=90
            plt.hist(data_list, bins = 'auto', normed=True, label=labels)
            print "finished ",network_setting," in ",kpi_name
            plt.figure(0)
            plt.xlabel(XLABEL)
            plt.ylabel('Number of data samples')
            plt.grid(True)
            plt.legend()
            plot_dir_path = os.path.join(os.getcwd(), PLOT_DIR_NAME, run_id, DIR_TAG+TAG)
            if not os.path.exists(plot_dir_path):
                os.makedirs(plot_dir_path)    
            plt.savefig( os.path.join(os.getcwd(), plot_dir_path, '{}_cdf_plot_full_{}.png'.format(kpi_name,TAG)) , bbox_inches='tight', dpi=300)
            print "finished ", kpi_name
     

name = sys.argv[1]
t1 = int(sys.argv[2])
t2 = int(sys.argv[3])
TAG = sys.argv[4]
XLABEL = sys.argv[5]
NUMBINS =int(sys.argv[6])

x0 = FullCDF(name,t1,t2)
x0.create_cdf() 

# for i in k:
# cdf = CDF(i)
# cdf.create_cdf()
# create_cdf ('maxBufferSize')
# create_cdf ('latency')
#create_cdf ('dutyCycle')
#create_cdf ('numNeighbors')
# create_cdf ('dagRank')
# create_cdf ('pdr')
#plt.show()

