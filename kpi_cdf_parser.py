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
PLOT_DIR_NAME = 'cdf_plots_full'

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

# network_settings = ['fsk_2','ofdm_1','oqpsk_2']
# labels = ['FSK_868MHz','OFDM_868MHz','OQPSK_2.4GHz']
network_settings = ['fsk_2']
labels = ['FSK_868MHz']

run_id = "run_5"

log_dir_path = os.path.join(os.getcwd(), LOG_DIR_NAME,run_id)

class CDF:
    def __init__ (self, kpi, enforce_lim, xlim, ylim):
        self.xlimit = xlim
        self.kpi = kpi
        self.ylimit = ylim
        self.enforce_lim = enforce_lim,

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
        xlimit = self.xlimit
        ylimit = self.ylimit
        print kpi_name
        XLABEL = 'Time (mins)'
        iterate=-1
        for network_setting in network_settings: 
            iterate+=1
            figure_index=-1
            global_stats, rpl_node_count,rpl_churn,timestamp,rpl_timestamp,time_to_firstpacket = getKPI.get_kpis(network_setting,0,90,3,log_dir_path)
            x_ax = timestamp
            sorted_data = []
            num_bins = 100
            i = 3
            while i < 90-3:
                r =  global_stats [kpi_name]['raw'][i*60]
                sorted_data=np.sort(r)
                counts, bin_edges = np.histogram (sorted_data, bins=num_bins, normed=True)
                cdf = np.cumsum (counts)
                figure_index+=1
                plt.figure(figure_index)
                plt.plot ( bin_edges[1:], cdf/cdf[-1],label= "{} @ min {}".format(labels [iterate],i))
                plt.xlabel(kpi_name)
                if (self.enforce_lim==1):
                    print "enforcing lim"
                    plt.xlim(xlimit)
                    plt.ylim(ylimit)
                plt.ylabel('Portion of motes')
                plt.title('{} CDF cross-section @ min {}'.format(kpi_name,i))
                plt.grid(True)
                plt.legend()
                plot_dir_path = os.path.join(os.getcwd(), PLOT_DIR_NAME, run_id,kpi_name)
                if not os.path.exists(plot_dir_path):
                    os.makedirs(plot_dir_path)    
                plt.savefig( os.path.join(os.getcwd(), plot_dir_path, '{}_cdf_plot_min{}.png'.format(kpi_name,i)) , bbox_inches='tight', dpi=300)                
                i+=10
                # i+=90
     

name = sys.argv[1]
xl = float(sys.argv[2])
xh=  float(sys.argv[3])
yl = float(sys.argv[4])
yh=  float(sys.argv[5])
enforce_lim = int(sys.argv[6])
x = [xl,xh]
y = [yl,yh]
print enforce_lim
x0 = CDF(name,enforce_lim,x,y)
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

