'''
KPI processing and analytics toolkit for opentestbed
Author: Mina Rady <mina1.rady@orange.com>, July 2020
'''
import os
import json
import datetime
import pdb
import json
import numpy as np

SLOTDURATION = .01
BATTERY_WH=8.2
def init_stat_info():
    return {
        "mean":[],
        "median":[],
        "std":[],
        "min_v":[],
        "max_v":[],
        "first_q":[],
        "third_q":[],
        "raw":[]
    }

global_stats={
"pdr":init_stat_info(),
"latency":init_stat_info(),
"dagRank":init_stat_info(),
"maxBufferSize":init_stat_info(),
"minBufferSize":init_stat_info(),
"numCellsUsage":init_stat_info(),
"numNeighbors":init_stat_info(),
"dutyCycle":init_stat_info(),
"dutyCycleTx":init_stat_info(),
"dutyCycle_0":init_stat_info(),
"dutyCycleTx_0":init_stat_info(),
"dutyCycle_1":init_stat_info(),
"dutyCycleTx_1":init_stat_info(),
"dutyCycle_2":init_stat_info(),
"dutyCycleTx_2":init_stat_info(),
"lifetime":init_stat_info()
}

def init_mote_info():
    return {
        "pdr":init_stat_info(),
        "latency":init_stat_info(),
        "dagRank":init_stat_info(),
        "maxBufferSize":init_stat_info(),
        "minBufferSize":init_stat_info(),
        "numCellsUsage":init_stat_info(),
        "numNeighbors":init_stat_info(),
        "dutyCycle":init_stat_info(),
        "dutyCycleTx":init_stat_info(),
        "dutyCycle_0":init_stat_info(),
        "dutyCycleTx_0":init_stat_info(),
        "dutyCycle_1":init_stat_info(),
        "dutyCycleTx_1":init_stat_info(),
        "dutyCycle_2":init_stat_info(),
        "dutyCycleTx_2":init_stat_info(),
        "lifetime":init_stat_info()
        }

#  contains the stats per mote, mote_id> {kpi> info}
mote_stats= {}

#  contains the stats by mote per kpi, kpi> mote1, mote2 ...
kpi_stats_by_mote= {
"pdr":init_stat_info(),
"latency":init_stat_info(),
"dagRank":init_stat_info(),
"maxBufferSize":init_stat_info(),
"minBufferSize":init_stat_info(),
"numCellsUsage":init_stat_info(),
"numNeighbors":init_stat_info(),
"dutyCycle":init_stat_info(),
"dutyCycleTx":init_stat_info(),
"dutyCycle_0":init_stat_info(),
"dutyCycleTx_0":init_stat_info(),
"dutyCycle_1":init_stat_info(),
"dutyCycleTx_1":init_stat_info(),
"dutyCycle_2":init_stat_info(),
"dutyCycleTx_2":init_stat_info(),
"lifetime":init_stat_info()
}


pdr_table={
    "motes":[],
    "pkt_count":[],
    "min_counter":[],
    "max_counter":[],
    "pdr":[],
    "first_pkt":[]
}

def data_describe (data):
    mean= np.mean(data)
    median = np.median(data)
    std = np.std(data)
    first_q = np.quantile(data, 0.25)
    third_q = np.quantile(data, 0.75)
    # pdb.set_trace()
    return mean,median,std, np.min(np.array(data)), np.max(np.array(data)),first_q,third_q;

def update_globalstats (kpi,raw):
    mean,median,std,min_v,max_v,first_q,third_q = data_describe(raw)
    global_stats [kpi]['mean'].append(mean)
    global_stats [kpi]['median'].append(median)
    global_stats [kpi]['std'].append(std)
    global_stats [kpi]['min_v'].append(min_v)
    global_stats [kpi]['max_v'].append(max_v)
    global_stats [kpi]['first_q'].append(first_q)
    global_stats [kpi]['third_q'].append(third_q)
    global_stats [kpi]['raw'].append(raw)

def update_mote_kpi (src_id,kpi,raw):

    mean,median,std,min_v,max_v,first_q,third_q = data_describe(raw)
    if (src_id not in mote_stats):
        mote_stats [src_id] = init_mote_info();
    mote_stats [src_id][kpi] ['mean'].append(mean)
    mote_stats [src_id][kpi] ['median'].append(median)
    mote_stats [src_id][kpi] ['std'].append(std)
    mote_stats [src_id][kpi] ['min_v'].append(min_v)
    mote_stats [src_id][kpi] ['max_v'].append(max_v)
    mote_stats [src_id][kpi] ['first_q'].append(first_q)
    mote_stats [src_id][kpi] ['third_q'].append(third_q)
    mote_stats [src_id][kpi] ['raw'].append(raw)

    kpi_stats_by_mote [kpi] ['mean'].append(mean)
    kpi_stats_by_mote [kpi] ['median'].append(median)
    kpi_stats_by_mote [kpi] ['std'].append(std)
    kpi_stats_by_mote [kpi] ['min_v'].append(min_v)
    kpi_stats_by_mote [kpi] ['max_v'].append(max_v)
    kpi_stats_by_mote [kpi] ['first_q'].append(first_q)
    kpi_stats_by_mote [kpi] ['third_q'].append(third_q)
    kpi_stats_by_mote [kpi] ['raw'].append(raw)
    # print (json.dumps(kpi_stats_by_mote))
    # pdb.set_trace()



def clear_globalstats():
    global global_stats
    global mote_stats
    global kpi_stats_by_mote
    
    global_stats={
    "pdr":init_stat_info(),
    "latency":init_stat_info(),
    "dagRank":init_stat_info(),
    "maxBufferSize":init_stat_info(),
    "minBufferSize":init_stat_info(),
    "numCellsUsage":init_stat_info(),
    "numNeighbors":init_stat_info(),
    "dutyCycle":init_stat_info(),
    "dutyCycleTx":init_stat_info(),
    "dutyCycle_0":init_stat_info(),
    "dutyCycleTx_0":init_stat_info(),
    "dutyCycle_1":init_stat_info(),
    "dutyCycleTx_1":init_stat_info(),
    "dutyCycle_2":init_stat_info(),
    "dutyCycleTx_2":init_stat_info(),
    "lifetime":init_stat_info()
    }

    #  contains the stats per mote, mote_id> {kpi> info}
    mote_stats= {}

    #  contains the stats by mote per kpi, kpi> mote1, mote2 ...
    kpi_stats_by_mote= {
    "pdr":init_stat_info(),
    "latency":init_stat_info(),
    "dagRank":init_stat_info(),
    "maxBufferSize":init_stat_info(),
    "minBufferSize":init_stat_info(),
    "numCellsUsage":init_stat_info(),
    "numNeighbors":init_stat_info(),
    "dutyCycle":init_stat_info(),
    "dutyCycleTx":init_stat_info(),
    "dutyCycle_0":init_stat_info(),
    "dutyCycleTx_0":init_stat_info(),
    "dutyCycle_1":init_stat_info(),
    "dutyCycleTx_1":init_stat_info(),
    "dutyCycle_2":init_stat_info(),
    "dutyCycleTx_2":init_stat_info(),
    "lifetime":init_stat_info()
    }

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

def datetime_delta (ts1, ts2):
    delta_arr = []
    # pdb.set_trace()
    ref = datetime.datetime.strptime(ts1, '%Y-%m-%d %H:%M:%S.%f')
    dt = datetime.datetime.strptime(ts2, '%Y-%m-%d %H:%M:%S.%f')
    delta = (dt-ref).total_seconds()

    return delta
# clculate expeted battery lifetime
def compute_battery_lifetime_single (
    dutyCycle    , dutyCycleTx, phy):
    

    Itx  = 0
    Irx  = 0
    vs = 0
    dutyCycleRx = dutyCycle-dutyCycleTx
    if (phy =="ofdm" or phy =="fsk" ):
        Itx  = 62
        Irx  = 28
        vs   = 2.5
    elif (phy=="oqpsk"):
        Itx  = 24
        Irx  = 20
        vs   = 3
    else:
        print ("unknown phy detected in logs")
    ptx = Itx*vs*0.001
    prx = Irx*vs*0.001
    E_day_wh = dutyCycleTx*24*ptx + dutyCycleRx*24*prx
    days = BATTERY_WH/ (E_day_wh)
    # print "--dc ",phy
    # print dutyCycle
    # print dutyCycleTx
    # print days
    # print (E_day_wh, days)
    return days

        
def compute_battery_lifetime_hybrid (
    dutyCycle_0, dutyCycleTx_0, 
    dutyCycle_1, dutyCycleTx_1, 
    dutyCycle_2, dutyCycleTx_2
    ):
    dutyCycleRx_0 = dutyCycle_0 - dutyCycleTx_0
    dutyCycleRx_1 = dutyCycle_1 - dutyCycleTx_1
    dutyCycleRx_2 = dutyCycle_2 - dutyCycleTx_2
    
    ptx_atmel = 62*2.5*0.001
    prx_atmel = 28*2.5*0.001

    ptx_ti = 24*3*0.001
    prx_ti = 20*3*0.001

    E_day_wh = dutyCycleTx_0*24*ptx_ti + dutyCycleRx_0*24*prx_ti +\
               dutyCycleTx_1*24*ptx_atmel + dutyCycleRx_1*24*prx_atmel +\
               dutyCycleTx_2*24*ptx_atmel + dutyCycleRx_2*24*prx_atmel
    days = BATTERY_WH/ E_day_wh
    # print "--dc hybrid---"
    # print dutyCycle_0
    # print dutyCycleTx_0
    # print dutyCycle_1
    # print dutyCycleTx_1
    # print dutyCycle_2
    # print dutyCycleTx_2
    # print days

    return days


def get_kpis(network_setting, start_time_mins, max_duration_mins,window_size_mins, log_dir_path, mote_id=all):
    print ("****")
    print (network_setting)
    print (start_time_mins)
    print (max_duration_mins)
    print (window_size_mins)
    print ("----")
    
    
    # clearing the variables
    clear_globalstats()
    
    raw_data = {}

    # the main timestamp, used through windows
    timestamp    = []
    
    # used for rpl
    rpl_timestamp_s    = []
    rpl_node_count = []
    rpl_churn = []
    rpl_phys = {
    0:[],
    1:[],
    2:[],
    }

    # used cdf
    time_to_firstpacket = []
    time_to_firstpacket_dict = {}
    first_arrivals = []
    first_ts = 0
    check= 0
    # process the entire file into a data structure
    for filename in os.listdir(log_dir_path):
        if ("log-kpis-"+network_setting in filename):
            print (filename)
            file_dir=os.path.join(log_dir_path,filename)
            with open (file_dir) as f:
                for line in f:
                    data=json.loads(line)
                    pkt_info=data['data']['pkt_info']
                    src_id = data['data']['pkt_info']['src_id']
                    if (check==0):
                        first_ts = data['timestamp']
                        check =1
                    # pdb.set_trace()
                    if (mote_id!= all and str(mote_id)!=str(src_id)):
                        continue
                    rpl_timestamp_s.append(data['timestamp'])
                    rpl_node_count.append(data['data']['rpl_node_count'])
                    rpl_churn.append(data['data']['rpl_churn'])
                    
                    if "0" in data['data']["rpl_phy_stats"]:
                        rpl_phys[0].append(data['data']["rpl_phy_stats"]["0"])
                    else:
                        rpl_phys[0].append(0)

                    if "1" in data['data']["rpl_phy_stats"]:
                        rpl_phys[1].append(data['data']["rpl_phy_stats"]["1"])
                    else:
                        rpl_phys[1].append(0)

                    if "2" in data['data']["rpl_phy_stats"]:
                        rpl_phys[2].append(data['data']["rpl_phy_stats"]["2"])
                    else:
                        rpl_phys[2].append(0)


                    phy = ""
                    if ("hybrid" in network_setting):
                        phy = "hybrid"
                    elif  ("oqpsk" in network_setting):
                        phy = "oqpsk"
                    elif  ("fsk" in network_setting):
                        phy = "fsk"
                    elif  ("ofdm" in network_setting):
                        phy="ofdm"
                    else:
                        print ("unknown phy in log file name")

                    dutyCycle      = float(pkt_info['numTicksOn'])/float(pkt_info['numTicksInTotal']) 
                    dutyCycleTx    = float(pkt_info['numTicksTx'])/float(pkt_info['numTicksInTotal']) 
                    dutyCycle_0    = float(pkt_info['numTicksOn_0'])/float(pkt_info['numTicksInTotal']) 
                    dutyCycleTx_0  = float(pkt_info['numTicksTx_0'])/float(pkt_info['numTicksInTotal']) 
                    dutyCycle_1    = float(pkt_info['numTicksOn_1'])/float(pkt_info['numTicksInTotal']) 
                    dutyCycleTx_1  = float(pkt_info['numTicksTx_1'])/float(pkt_info['numTicksInTotal']) 
                    dutyCycle_2    = float(pkt_info['numTicksOn_2'])/float(pkt_info['numTicksInTotal']) 
                    dutyCycleTx_2  = float(pkt_info['numTicksTx_2'])/float(pkt_info['numTicksInTotal'])
                    singledc       = (float(pkt_info['numTicksOn_0'])+ float(pkt_info['numTicksOn_1'])+float(pkt_info['numTicksOn_2']))/float(pkt_info['numTicksInTotal'])
                    singledc_tx    = (float(pkt_info['numTicksTx_0'])+ float(pkt_info['numTicksTx_1'])+float(pkt_info['numTicksTx_2']))/float(pkt_info['numTicksInTotal'])
                    lifetime = 0
                    if (phy =="hybrid"):
                        lifetime = compute_battery_lifetime_hybrid(
                            dutyCycle_0, dutyCycleTx_0,
                            dutyCycle_1, dutyCycleTx_1,
                            dutyCycle_2, dutyCycleTx_2)
                    else: # since only one variable is assigned and the others are 0
                        lifetime = compute_battery_lifetime_single (singledc,singledc_tx,phy)

                    #populate dictionary of avg _kpi for each mote 
                    if src_id in raw_data:
                        # ignore duplicate data. 
                        if (pkt_info['counter'] not in raw_data[src_id]['counter']):
                            raw_data[src_id]['counter'].append(pkt_info['counter'])
                            raw_data[src_id]['latency'].append(float(pkt_info['latency'])*float(SLOTDURATION))
                            raw_data[src_id]['dagRank'].append(pkt_info['dagRank'])
                            raw_data[src_id]['maxBufferSize'].append(int(pkt_info['maxBufferSize']))
                            raw_data[src_id]['minBufferSize'].append(pkt_info['minBufferSize'])
                            raw_data[src_id]['numCellsUsedTx'].append(pkt_info['numCellsUsedTx'])
                            raw_data[src_id]['numCellsUsedRx'].append(pkt_info['numCellsUsedRx'])
                            raw_data[src_id]['numNeighbors'].append(int(pkt_info['numNeighbors']))
                            raw_data[src_id]['dutyCycle'].append(dutyCycle*100)
                            raw_data[src_id]['dutyCycleTx'].append(dutyCycleTx*100)
                            raw_data[src_id]['dutyCycle_0'].append(dutyCycle_0*100)
                            raw_data[src_id]['dutyCycleTx_0'].append(dutyCycleTx_0*100)
                            raw_data[src_id]['dutyCycle_1'].append(dutyCycle_1*100)
                            raw_data[src_id]['dutyCycleTx_1'].append(dutyCycleTx_1*100)
                            raw_data[src_id]['dutyCycle_2'].append(dutyCycle_2*100)
                            raw_data[src_id]['dutyCycleTx_2'].append(dutyCycleTx_2*100)
                            raw_data[src_id]['lifetime'].append(lifetime)
                            # raw_data[src_id]['timedelta'].append(data["data"]['time_elapsed']["seconds"])
                            raw_data[src_id]['timedelta'].append(datetime_delta(first_ts,data['timestamp']))
                    else:

                        # pdb.set_trace()
                        raw_data[src_id] = {
                            'counter'        : [pkt_info['counter']],
                            'latency'        : [float(pkt_info['latency'])*float(SLOTDURATION)],
                            'dagRank'        : [pkt_info['dagRank']],
                            'maxBufferSize'  : [int(pkt_info['maxBufferSize'])],
                            'minBufferSize'  : [pkt_info['minBufferSize']],
                            'numCellsUsedTx' : [pkt_info['numCellsUsedTx']],
                            'numCellsUsedRx' : [pkt_info['numCellsUsedRx']],
                            'numNeighbors'   : [pkt_info['numNeighbors']],
                            'dutyCycle'      : [dutyCycle     *100],
                            'dutyCycleTx'    : [dutyCycleTx   *100],
                            'dutyCycle_0'    : [dutyCycle_0   *100],
                            'dutyCycleTx_0'  : [dutyCycleTx_0 *100],
                            'dutyCycle_1'    : [dutyCycle_1   *100],
                            'dutyCycleTx_1'  : [dutyCycleTx_1 *100],
                            'dutyCycle_2'    : [dutyCycle_2   *100],
                            'dutyCycleTx_2'  : [dutyCycleTx_2 *100],
                            'lifetime'       : [lifetime ],
                            # 'timedelta'      : [data["data"]['time_elapsed']["seconds"]],
                            'timedelta'      : [datetime_delta(first_ts,data['timestamp'])]

                        }

                    #processing time to first packet
                    if src_id not in first_arrivals:
                        first_arrivals.append(src_id)
                        # secs  = float(data['data']['time_elapsed']['seconds'])
                        # usecs = float(data['data']['time_elapsed']['microseconds'])
                        time_elapsed_secs =datetime_delta(first_ts,data['timestamp'])# secs + (usecs/1e6)
                        # print time_elapsed_secs
                        time_to_firstpacket.append(float(time_elapsed_secs))
                        time_to_firstpacket_dict [src_id] = float(time_elapsed_secs);

            continue
        else:
            continue

    pdb.set_trace()
    raw_data_table = {}
    for src_id in raw_data:
        table = zip(    raw_data[src_id]['timedelta'],
                        raw_data[src_id]['counter'],
                        raw_data[src_id]['latency'],
                        raw_data[src_id]['dagRank'],
                        raw_data[src_id]['maxBufferSize'],
                        raw_data[src_id]['minBufferSize'],
                        raw_data[src_id]['numCellsUsedTx'],
                        raw_data[src_id]['numCellsUsedRx'],
                        raw_data[src_id]['numNeighbors'],
                        raw_data[src_id]['dutyCycle'],
                        raw_data[src_id]['dutyCycleTx'],
                        raw_data[src_id]['dutyCycle_0'],
                        raw_data[src_id]['dutyCycleTx_0'],
                        raw_data[src_id]['dutyCycle_1'],
                        raw_data[src_id]['dutyCycleTx_1'],
                        raw_data[src_id]['dutyCycle_2'],
                        raw_data[src_id]['dutyCycleTx_2'],
                        raw_data[src_id]['lifetime'])
        raw_data_table [src_id]= table 


    #calculate the averages
    '''
    So at this point you have a dictionary of tables for each mote, they can be sorted and filtered
    - define window size
    - empty avg array
    loop conditions: 0 until time_delta - windowsize
        for each mote data
            filter dictionary by t + window_size
            compute all the averages as usual
            add them to the averages aray
    '''
    window_size= window_size_mins*60 #secs, should be around 15 samples for 15 minutes
    # windowsize= 60*89 #secs, should be around 15 samples for 15 minutes
    max_duration = max_duration_mins*60 #90 minutes
    
    t1 = start_time_mins*60
    t2 = t1+window_size


    
    while t2<=max_duration:
        # print "iterating..."
        # clear network-level arrays
        arr_pdr_all           = []
        arr_latency_all       = []
        arr_dagRank_all       = []
        
        arr_maxBufferSize_all = []
        
        arr_minBufferSize_all = []
        arr_numCellsUsage_all = []
        arr_numNeighbors_all  = []
        arr_dutyCycle_all     = []
        arr_dutyCycleTx_all   = []
        arr_dutyCycle_0_all     = []
        arr_dutyCycleTx_0_all   = []
        arr_dutyCycle_1_all     = []
        arr_dutyCycleTx_1_all   = []
        arr_dutyCycle_2_all     = []
        arr_dutyCycleTx_2_all   = []
        arr_lifetime_all   = []

        #for the data of each mote
        for src_id in raw_data_table:
            #filter the data of the current window
            window_data = filter(lambda x: (x[0]>=t1 and x[0]<t2), raw_data_table [src_id])
            # pdb.set_trace()
            #if there is any data for this mote within this window, calculate the stats
            if window_data:

                #decoupling the columns
                tuples = zip(*window_data)
                # initializing the arrays
                timedelta=[]
                counter=[]
                latency=[]
                dagRank=[]
                maxBufferSize=[]
                minBufferSize=[]
                numCellsUsedTx=[]
                numCellsUsedRx=[]
                numNeighbors=[]
                dutyCycle=[]
                dutyCycleTx=[]
                dutyCycle_0=[]
                dutyCycleTx_0=[]
                dutyCycle_1=[]
                dutyCycleTx_1=[]
                dutyCycle_2=[]
                dutyCycleTx_2=[]
                lifetime=[]

                # unzipping
                timedelta,\
                counter,\
                latency,\
                dagRank,\
                maxBufferSize,\
                minBufferSize,\
                numCellsUsedTx,\
                numCellsUsedRx,\
                numNeighbors,\
                dutyCycle,\
                dutyCycleTx,\
                dutyCycle_0,\
                dutyCycleTx_0,\
                dutyCycle_1,\
                dutyCycleTx_1,\
                dutyCycle_2,\
                dutyCycleTx_2,\
                lifetime = list (tuples)# [ list(tuple) for tuple in  tuples]

                #now getting all the local averages for this mote/window combination

                timedelta
                counter.sort()
                pdr                 = float(len(set(counter)))/float(1+counter[-1]-counter[0])
                
                pdr_table["motes"].append(src_id)
                pdr_table["pkt_count"].append(float(len(set(counter))))
                pdr_table["min_counter"].append(counter[0])
                pdr_table["max_counter"].append(counter[-1])
                pdr_table["pdr"].append(pdr)
                pdr_table["first_pkt"].append(time_to_firstpacket_dict[src_id])

                # avg_latency             = sum(latency)/len(latency)
                # avg_dagRank             = sum(dagRank)/len(dagRank)
                # avg_maxBufferSize       = sum(maxBufferSize)/len(maxBufferSize)
                # avg_minBufferSize       = sum(minBufferSize)/len(minBufferSize)
                # avg_numCellsUsedTx      = sum(numCellsUsedTx)/len(numCellsUsedTx)
                # avg_numCellsUsedRx      = sum(numCellsUsedRx)/len(numCellsUsedRx)
                # avg_numNeighbors        = sum(numNeighbors)/len(numNeighbors)
                # avg_dutyCycle           = sum(dutyCycle)/len(dutyCycle)
                # avg_dutyCycleTx         = sum(dutyCycleTx)/len(dutyCycleTx)

                #now putting all these averages in network-level array
                arr_pdr_all.append(pdr)
                arr_latency_all.extend(latency)
                arr_dagRank_all.extend(dagRank)
                # print (arr_maxBufferSize_all)
                arr_maxBufferSize_all.extend(maxBufferSize)
                # print (arr_maxBufferSize_all)

                arr_minBufferSize_all.extend(minBufferSize)
                arr_numCellsUsage_all.extend(numCellsUsedTx+numCellsUsedRx) 
                arr_numNeighbors_all.extend(numNeighbors)  
                arr_dutyCycle_all.extend(dutyCycle)
                arr_dutyCycleTx_all.extend(dutyCycleTx)
                arr_dutyCycle_0_all.extend(dutyCycle_0)
                arr_dutyCycleTx_0_all.extend(dutyCycleTx_0)
                arr_dutyCycle_1_all.extend(dutyCycle_1)
                arr_dutyCycleTx_1_all.extend(dutyCycleTx_1)
                arr_dutyCycle_2_all.extend(dutyCycle_2)
                arr_dutyCycleTx_2_all.extend(dutyCycleTx_2)
                arr_lifetime_all.extend(lifetime)
            # process stats per mote
            update_mote_kpi(str(src_id), 'lifetime',lifetime)
        # pdb.set_trace()
        # at this point, you have all the data for this window.
        # print (t1)
        # print (t2)
        update_globalstats('pdr',arr_pdr_all)

        update_globalstats('latency',arr_latency_all)
        
        update_globalstats('dagRank',arr_dagRank_all)

        update_globalstats('maxBufferSize',arr_maxBufferSize_all)

        update_globalstats('minBufferSize',arr_minBufferSize_all)

        update_globalstats('numCellsUsage',arr_numCellsUsage_all)

        update_globalstats('numNeighbors',arr_numNeighbors_all)

        update_globalstats('dutyCycle',arr_dutyCycle_all)

        update_globalstats('dutyCycleTx',arr_dutyCycleTx_all)

        update_globalstats('dutyCycle_0',arr_dutyCycle_0_all)

        update_globalstats('dutyCycleTx_0',arr_dutyCycleTx_0_all)

        update_globalstats('dutyCycle_1',arr_dutyCycle_1_all)

        update_globalstats('dutyCycleTx_1',arr_dutyCycleTx_1_all)

        update_globalstats('dutyCycle_2',arr_dutyCycle_2_all)

        update_globalstats('dutyCycleTx_2',arr_dutyCycleTx_2_all)

        update_globalstats('lifetime',arr_lifetime_all)

        # print "{}->{}".format(t1,t2)
        
        # used for global stats 
        timestamp.append(float(t2)/float(60))
        t1+=1
        t2+=1

    #used for rpl
    rpl_timestamp = datetime_arr_normalize(rpl_timestamp_s)
    return  global_stats, kpi_stats_by_mote, rpl_node_count,rpl_churn, rpl_phys,timestamp,rpl_timestamp,time_to_firstpacket,pdr_table;

# get_kpis ("fsk_2",os.path.join(os.getcwd(), "logs","run_5"))