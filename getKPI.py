import os
import json
import datetime
import numpy as np

def init_stat_info():
    return {
        "mean":[],
        "median":[],
        "std":[],
        "min_v":[],
        "max_v":[],
        "first_q":[],
        "third_q":[]
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
"dutyCycleTx":init_stat_info()
}

def data_describe (data):
    mean= np.mean(data)
    median = np.median(data)
    std = np.std(data)
    first_q = np.quantile(data, 0.25)
    third_q = np.quantile(data, 0.75)   
    return mean,median,std,min(data),max(data),first_q,third_q;

def update_globalstats (kpi,mean,median,std,min_v,max_v,first_q,third_q):
    global_stats [kpi]['mean'].append(mean)
    global_stats [kpi]['median'].append(median)
    global_stats [kpi]['std'].append(std)
    global_stats [kpi]['min_v'].append(min_v)
    global_stats [kpi]['max_v'].append(max_v)
    global_stats [kpi]['first_q'].append(first_q)
    global_stats [kpi]['third_q'].append(third_q)



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

def get_kpis(network_setting,log_dir_path):
    raw_data = {}

    # the main timestamp, used through windows
    timestamp    = []
    
    # used for rpl
    rpl_timestamp_s    = []
    rpl_node_count = []
    rpl_churn = []

    # used cdf
    time_to_firstpacket = []
    first_arrivals = []

    for filename in os.listdir(log_dir_path):
        if ("log-kpis-"+network_setting in filename):
            print filename
            file_dir=os.path.join(log_dir_path,filename)
            with open (file_dir) as f:
                for line in f:
                    data=json.loads(line)
                    pkt_info=data['data']['pkt_info']
                    src_id = data['data']['pkt_info']['src_id']
                    rpl_timestamp_s.append(data['timestamp'])
                    rpl_node_count.append(data['data']['rpl_node_count'])
                    rpl_churn.append(data['data']['rpl_churn'])

                    #populate dictionary of avg _kpi for each mote 
                    if src_id in raw_data:
                        raw_data[src_id]['counter'].append(pkt_info['counter'])
                        raw_data[src_id]['latency'].append(pkt_info['latency'])
                        raw_data[src_id]['dagRank'].append(pkt_info['dagRank'])
                        raw_data[src_id]['maxBufferSize'].append(pkt_info['maxBufferSize'])
                        raw_data[src_id]['minBufferSize'].append(pkt_info['minBufferSize'])
                        raw_data[src_id]['numCellsUsedTx'].append(pkt_info['numCellsUsedTx'])
                        raw_data[src_id]['numCellsUsedRx'].append(pkt_info['numCellsUsedRx'])
                        raw_data[src_id]['numNeighbors'].append(pkt_info['numNeighbors'])
                        raw_data[src_id]['dutyCycle'].append(float(pkt_info['numTicksOn'])/float(pkt_info['numTicksInTotal']))
                        raw_data[src_id]['dutyCycleTx'].append(float(pkt_info['numTicksTx'])/float(pkt_info['numTicksInTotal']))
                        raw_data[src_id]['timedelta'].append(data["data"]['time_elapsed']["seconds"])
                    else:
                        raw_data[src_id] = {
                            'counter'        : [pkt_info['counter']],
                            'latency'        : [pkt_info['latency']],
                            'dagRank'        : [pkt_info['dagRank']],
                            'maxBufferSize'  : [pkt_info['maxBufferSize']],
                            'minBufferSize'  : [pkt_info['minBufferSize']],
                            'numCellsUsedTx' : [pkt_info['numCellsUsedTx']],
                            'numCellsUsedRx' : [pkt_info['numCellsUsedRx']],
                            'numNeighbors'   : [pkt_info['numNeighbors']],
                            'dutyCycle'      : [pkt_info['dutyCycle'] ],
                            'dutyCycleTx'    : [pkt_info['dutyCycleTx'] ],
                            'timedelta'      : [data["data"]['time_elapsed']["seconds"]]
                        }
                    
                    #processing time to first packet
                    if src_id not in first_arrivals:
                        first_arrivals.append(src_id)
                        secs  = float(data['data']['time_elapsed']['seconds'])
                        usecs = float(data['data']['time_elapsed']['microseconds'])
                        time_elapsed_secs = secs + (usecs/1e6)
                        time_to_firstpacket.append(float(time_elapsed_secs))

            continue
        else:
            continue
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
                        raw_data[src_id]['dutyCycleTx'])
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
    windowsize= 180 #secs, should be around 15 samples for 15 minutes
    max_duration = 60*30 #90 minutes
    
    t1 = 0
    t2 = t1+windowsize


    
    while t2<max_duration:
        # clear network-level arrays
        arr_avg_pdr_all           = []
        arr_avg_latency_all       = []
        arr_avg_dagRank_all       = []
        arr_avg_maxBufferSize_all = []
        arr_avg_minBufferSize_all = []
        arr_avg_numCellsUsage_all = []
        arr_avg_numNeighbors_all  = []
        arr_avg_dutyCycle_all     = []
        arr_avg_dutyCycleTx_all   = []

        #for the data of each mote
        for src_id in raw_data_table:
            #filter the data of the current window
            window_data = filter(lambda x: (x[0]>=t1 and x[0]<t2), raw_data_table [src_id])
            
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
                dutyCycleTx = [ list(tuple) for tuple in  tuples]

                #now getting all the local averages for this mote/window combination

                timedelta
                counter.sort()
                avg_pdr                 = float(len(set(counter)))/float(1+counter[-1]-counter[0])
                avg_latency             = sum(latency)/len(latency)
                avg_dagRank             = sum(dagRank)/len(dagRank)
                avg_maxBufferSize       = sum(maxBufferSize)/len(maxBufferSize)
                avg_minBufferSize       = sum(minBufferSize)/len(minBufferSize)
                avg_numCellsUsedTx      = sum(numCellsUsedTx)/len(numCellsUsedTx)
                avg_numCellsUsedRx      = sum(numCellsUsedRx)/len(numCellsUsedRx)
                avg_numNeighbors        = sum(numNeighbors)/len(numNeighbors)
                avg_dutyCycle           = sum(dutyCycle)/len(dutyCycle)
                avg_dutyCycleTx         = sum(dutyCycleTx)/len(dutyCycleTx)

                #now putting all these averages in network-level array
                arr_avg_pdr_all.append(avg_pdr)
                arr_avg_latency_all.append(avg_latency)
                arr_avg_dagRank_all.append(avg_dagRank)
                arr_avg_maxBufferSize_all.append(avg_maxBufferSize) 
                arr_avg_minBufferSize_all.append(avg_minBufferSize)
                arr_avg_numCellsUsage_all.append(avg_numCellsUsedTx+avg_numCellsUsedRx) 
                arr_avg_numNeighbors_all.append(avg_numNeighbors)  
                arr_avg_dutyCycle_all.append(avg_dutyCycle)
                arr_avg_dutyCycleTx_all.append(avg_dutyCycleTx)

        # at this point, you have all the data for this window.
        mean,median,std,min_v,max_v,first_q,third_q = data_describe(arr_avg_pdr_all)
        update_globalstats('pdr',mean,median,std,min_v,max_v,first_q,third_q)

        mean,median,std,min_v,max_v,first_q,third_q = data_describe(arr_avg_latency_all)
        update_globalstats('latency',mean,median,std,min_v,max_v,first_q,third_q)
        mean,median,std,min_v,max_v,first_q,third_q = data_describe(arr_avg_dagRank_all)
        update_globalstats('dagRank',mean,median,std,min_v,max_v,first_q,third_q)

        mean,median,std,min_v,max_v,first_q,third_q = data_describe(arr_avg_maxBufferSize_all)
        update_globalstats('maxBufferSize',mean,median,std,min_v,max_v,first_q,third_q)

        mean,median,std,min_v,max_v,first_q,third_q = data_describe(arr_avg_minBufferSize_all)
        update_globalstats('minBufferSize',mean,median,std,min_v,max_v,first_q,third_q)

        mean,median,std,min_v,max_v,first_q,third_q = data_describe(arr_avg_numCellsUsage_all)
        update_globalstats('numCellsUsage',mean,median,std,min_v,max_v,first_q,third_q)

        mean,median,std,min_v,max_v,first_q,third_q = data_describe(arr_avg_numNeighbors_all)
        update_globalstats('numNeighbors',mean,median,std,min_v,max_v,first_q,third_q)

        mean,median,std,min_v,max_v,first_q,third_q = data_describe(arr_avg_dutyCycle_all)
        update_globalstats('dutyCycle',mean,median,std,min_v,max_v,first_q,third_q)

        mean,median,std,min_v,max_v,first_q,third_q = data_describe(arr_avg_dutyCycleTx_all)
        update_globalstats('dutyCycleTx',mean,median,std,min_v,max_v,first_q,third_q)

        # print "{}->{}".format(t1,t2)
        
        # used for global stats 
        timestamp.append(float(t2)/float(60))
        t1+=1
        t2+=1

    #used for rpl
    rpl_timestamp = datetime_arr_normalize(rpl_timestamp_s)
    return  global_stats, rpl_node_count,rpl_churn,timestamp,rpl_timestamp,time_to_firstpacket;

#get_kpis ("openqueuestats",os.path.join(os.getcwd(), "logs","temp"))