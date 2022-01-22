'''
KPI processing and analytics toolkit for opentestbed
Author: Mina Rady <mina1.rady@orange.com>, July 2020
'''

import glob
import os
import json
import pdb
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
YLABEL=''
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

# network_settings = [ 'g6_fsk_3','g6_oqpsk','g6_hybrid', 'g6_hybrid_qfm_251_2']
# labels = ['FSK_868MHz','OQPSK_2.4GHz','Hybrid 6TiSCH','Hybrid 6TiSCH OFDM base']

# network_settings = ['g6_fsk_4','g6_ofdm','g6_oqpsk','g6_hybrid_qfm_152', 'g6_hybrid_qfm_251','g6_hybrid_qfm_271']
# labels = ['FSK_868MHz','OFDM_868MHz','OQPSK_2.4GHz','g6TiSCH-OQPSK base','g6TiSCH-OFDM base','g6TiSCH-OFDM base-high FSK']

network_settings = [
'g6_fsk',
'g6_ofdm',
'g6_oqpsk',
'g6_hybrid_qfm_251',
# 'g6_hybrid_qfm_152',
# 'g6_hybrid_162qfm_1dio_5retries_1defcost'
]
labels = [
'FSK_868MHz',
'OFDM_868MHz',
'OQPSK_2.4GHz',
'g6TiSCH',
# 'g6_hybrid_qfm_152', 
# 'g6_hybrid_162qfm_1dio_5retries_1defcost'
]

run_id = "run_8"
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
        data_list = []
        for network_setting in network_settings: 
            iterate+=1
            global_stats, kpi_stats_by_mote, rpl_node_count,rpl_churn, rpl_phys,timestamp,rpl_timestamp,time_to_firstpacket,pdr_table =\
                getKPI.get_kpis(network_setting,self.t1,self.t2,self.t2-self.t1,log_dir_path)
            x_ax = timestamp
            sorted_data = []
            num_bins = 200
            i = 3
            while i < 90-3:
                r = []
                r =  global_stats [kpi_name]['raw'][0]
                # r =  kpi_stats_by_mote ['lifetime']['mean']
                # pdb.set_trace()
                data_list.append(np.array(r))
                i+=90
        if (kpi_name=='maxBufferSize'):
            plt.axvline(x=15,linewidth=2, color='r', alpha=0.7, label="High priority limit")
        plt.hist(data_list, density=True, bins=NUMBINS, label=labels)
        plt.figure(0)
        plt.xlabel(XLABEL)
        # plt.ylabel('Number of data samples')
        plt.ylabel(YLABEL)
        plt.grid(True)
        plt.legend()
        plot_dir_path = os.path.join(os.getcwd(), PLOT_DIR_NAME, run_id, DIR_TAG+TAG)
        if not os.path.exists(plot_dir_path):
            os.makedirs(plot_dir_path)    
        plt.savefig( os.path.join(os.getcwd(), plot_dir_path, '{}_pdf_plot_{}_{}_mins.png'.format(kpi_name,TAG,str(self.t2-self.t1))) , bbox_inches='tight', dpi=300)
        print "finished ", kpi_name
     

name = sys.argv[1]
t1 = int(sys.argv[2])
t2 = int(sys.argv[3])
TAG = sys.argv[4]
XLABEL = sys.argv[5]
YLABEL = sys.argv[6]
NUMBINS =int(sys.argv[7])

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

