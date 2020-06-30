import os
import json
import datetime

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
    timestamp_s    = []
    rpl_node_count = []
    rpl_churn = []
    time_to_firstpacket = []

    avg_dutyCycle  = []
    avg_dutyCycle_first_q = []
    avg_dutyCycle_third_q= []
    avg_dutyCycle_std= []
    avg_dutyCycle_median= []
    
    avg_dutyCycleTx  = []
    avg_dutyCycleTx_first_q = []
    avg_dutyCycleTx_third_q= []
    avg_dutyCycleTx_std= []
    avg_dutyCycleTx_median= []
    
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
    avg_latency_median= []
    
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
    avg_pdr_min= []
    avg_pdr_max= []
    avg_pdr_median= []
    
    avg_cellsUsage_first_q= []
    avg_cellsUsage = []
    avg_cellsUsage_third_q= []
    avg_cellsUsage_std= []
    
    avg_numNeighbors = []
    avg_numNeighbors_first_q= []
    avg_numNeighbors_third_q= []
    avg_numNeighbors_std= []
    avg_numNeighbors_max= []

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
                    avg_dutyCycle_median.append(data['data']['stats']['avg_dutyCycle']['median'])

                    avg_dutyCycleTx.append(data['data']['avg_dutyCycleTx'])
                    avg_dutyCycleTx_first_q.append(data['data']['stats']['avg_dutyCycleTx']['first_q'])
                    avg_dutyCycleTx_third_q.append(data['data']['stats']['avg_dutyCycleTx']['third_q'])
                    avg_dutyCycleTx_std.append(data['data']['stats']['avg_dutyCycleTx']['std'])
                    avg_dutyCycleTx_median.append(data['data']['stats']['avg_dutyCycleTx']['median'])

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
                    avg_latency_median.append(data['data']['stats']['avg_latency']['median'])

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
                    avg_pdr_min.append(data['data']['stats']['avg_pdr']['min_v'])
                    avg_pdr_max.append(data['data']['stats']['avg_pdr']['max_v'])
                    avg_pdr_median.append(data['data']['stats']['avg_pdr']['median'])

                    
                    avg_cellsUsage.append(data['data']['avg_cellsUsage'])
                    avg_cellsUsage_first_q.append(data['data']['stats']['avg_cellsUsage']['first_q'])
                    avg_cellsUsage_third_q.append(data['data']['stats']['avg_cellsUsage']['third_q'])                   
                    avg_cellsUsage_std.append(data['data']['stats']['avg_cellsUsage']['std'])

                    avg_numNeighbors.append(data['data']['stats']['avg_numNeighbors']['mean'])
                    avg_numNeighbors_first_q.append(data['data']['stats']['avg_numNeighbors']['first_q'])
                    avg_numNeighbors_third_q.append(data['data']['stats']['avg_numNeighbors']['third_q'])                   
                    avg_numNeighbors_std.append(data['data']['stats']['avg_numNeighbors']['std'])
                    avg_numNeighbors_max.append(data['data']['stats']['avg_numNeighbors']['max_v'])


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
    return avg_latency,avg_latency_first_q,avg_latency_third_q,avg_latency_std,avg_latency_median,\
    avg_pdr,avg_pdr_first_q,avg_pdr_third_q,avg_pdr_std,avg_pdr_min,avg_pdr_max,avg_pdr_median,\
    avg_cellsUsage,avg_cellsUsage_first_q,avg_cellsUsage_third_q,avg_cellsUsage_std,\
    avg_dutyCycle,avg_dutyCycle_first_q,avg_dutyCycle_third_q,avg_dutyCycle_std,avg_dutyCycle_median,\
    avg_dutyCycleTx,avg_dutyCycleTx_first_q,avg_dutyCycleTx_third_q,avg_dutyCycleTx_std,avg_dutyCycleTx_median,\
    avg_dutyCycleRx,avg_dutyCycleRx_first_q,avg_dutyCycleRx_third_q,avg_dutyCycleRx_std,\
    avg_dutyCycleTxRx,avg_dutyCycleTxRx_first_q,avg_dutyCycleTxRx_third_q,avg_dutyCycleTxRx_std,\
    avg_numNeighbors,avg_numNeighbors_first_q,avg_numNeighbors_third_q,avg_numNeighbors_std,avg_numNeighbors_max,\
    avg_dagRank,avg_dagRank_first_q,avg_dagRank_third_q,avg_dagRank_std,\
    avg_bufferSize,avg_bufferSize_first_q,avg_bufferSize_third_q,avg_bufferSize_std,\
    rpl_node_count,rpl_churn,timestamp,time_to_firstpacket;