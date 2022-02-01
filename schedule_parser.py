import collections
import scheduleData
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  


oqpskData= scheduleData.oqpskData
ofdmData = scheduleData.ofdmData
fskData = scheduleData.fskData

slot_usage_count_theoretical =[]
slot_usage_count =[]
res_anycast_usage_map ={}
res_anycast_usage_map_nbrs ={}
res_p2p_usage_map ={}

#resource allocated on one end for a neighbor but not allocated on the other end!!
res_p2p_awkward_usage_map ={}

ch_usage_count =[]
SLOTFRAME_LENGTH= 40
CHANNELS= 16
RESOURCE_BLOCKS = 16*40
ACTIVE_MIN_CELLS = 3

def are_adjacent(i,j):
    m = data.get (i)
    #print ("inside are_adjacent for {} and {}".format(i,j))
    if m:
        neighbors = m.get('Neighbors')
        if neighbors:
            for n in neighbors:
                addr = n['addr']
                if addr == j:
                    return True

def slot_hash (i):
    i_addr = int(i,16)
    i_slot_hash = ACTIVE_MIN_CELLS+(i_addr%(SLOTFRAME_LENGTH-ACTIVE_MIN_CELLS))
    i_ch_hash = (i_addr%(CHANNELS))
    return i_slot_hash,i_ch_hash

def same_hash (i,j):
    sli,chi = slot_hash (i)
    slj,chj = slot_hash (j)
    #print ("{} , {} : {},{} -  {},{}".format(i,j,sli,chi,slj,chj))
    # if (sli==slj and chi==chj):
    if (sli==slj):
        print ("cell hash conflict {},{} : {},{}".format(i,j,sli,slj))
        return True
    else:
        return False

def get_conflicts(slot_list):
    counter=collections.Counter(slot_list)
    values = counter.values()
    conflicts = [i for i in values if i >= 2]
    return conflicts

def estimate_conflict (mote_list):
    #print slot_usage_count
    for m in mote_list:
        for n in mote_list:
            if (m!=n):
               same_hash (m,n)
               


    #slot_usage_count = get_conflicts (slot_usage_count_theoretical)
    #counter=collections.Counter(slot_usage_count)
    #print "Slot usage histogram:"
    #print(counter)
    ## Counter({1: 4, 2: 4, 3: 2, 5: 2, 4: 1})
    #print "Total number of slot conflicts in the network:"
    #print (sum(counter.values()))
    #print "Total number of nodes affected with slot conflicts:"
    ## [4, 4, 2, 1, 2]
    #print(counter.keys())
    #print(len(counter.keys()))



def plot(data,label,figureIndex):
    dedicated_etx = []
    shared_rx = []
    shared_etx=[]


    for m in data:
        s = data[m].get("Schedule")
        if s:                              
            for slot in s:
                if ( slot ['numTx']>0):
                    etx = round(float(slot ['numTx']+1)/float(slot ['numTxACK']+1),2)
                    if (slot['neighbor']!=  ' (None)' and slot ['shared']==0):
                        dedicated_etx.append(etx)
                        # print "dedicated eTx {} / {} = {}".format(slot ['numTx'], slot ['numTxACK'], etx)
                    if (slot ['shared']==1):
                        shared_etx.append(etx)
                        # print "shared    eTx {} / {} = {}".format(slot ['numTx'], slot ['numTxACK'], etx)
 
                if (slot ['shared']==1 and slot ['numRx']>0):
                    shared_rx.append(slot ['numRx'])
                    # print "shared    rx  {}".format(slot ['numRx'])

    plt.figure(figureIndex)
    data_list=[]
    data_list.append(np.array(dedicated_etx))
    plt.hist(data_list, bins = 15, label=label+" dedicated links")
    print (len(data_list))
    data_list=[]
    print (len(data_list))
    data_list.append(np.array(shared_etx))
    plt.hist(data_list, bins = 15,label= label+" shared links")
    plt.xlabel("ETX")
    # plt.ylabel('Number of data samples')
    plt.ylabel("Mote Count")
    plt.yscale('log')
    plt.grid(True)
    plt.legend()  
    plt.savefig(os.path.join(os.getcwd(),label+"_pdf_etx.png"))

    plt.figure(figureIndex+1)
    data_list=[]
    print (len(data_list))
    data_list.append(np.array(shared_rx))
    plt.hist(data_list, bins = 15,label= label+" shared links")
    plt.xlabel("Rx")
    # plt.ylabel('Number of data samples')
    plt.ylabel("Number of Slots")
    plt.yscale('log')
    plt.grid(True)
    plt.legend()  
    plt.savefig(os.path.join(os.getcwd(),label+"_pdf_rx.png"))

def plotAggregate(data,label,figureIndex):
    dedicated_etx = []
    shared_rx = []
    shared_etx=[]
    for m in data:
        s = data[m].get("Schedule")
        if s:                              
            for slot in s:
                if ( slot ['numTx']>0):
                    etx = round(float(slot ['numTx']+1)/float(slot ['numTxACK']+1),2)
                    if (slot['neighbor']!=  ' (None)' and slot ['shared']==0):
                        dedicated_etx.append(etx)
                        # print "dedicated eTx {} / {} = {}".format(slot ['numTx'], slot ['numTxACK'], etx)
                    if (slot ['shared']==1):
                        shared_etx.append(etx)
                        # print "shared    eTx {} / {} = {}".format(slot ['numTx'], slot ['numTxACK'], etx)
 
                if (slot ['shared']==1 and slot ['numRx']>0):
                    shared_rx.append(slot ['numRx'])
                    print "shared    rx  {}".format(slot ['numRx'])

    plt.figure(figureIndex)
    data_list=[]
    data_list.append(np.array(shared_rx))
    sorted_data=np.sort(data_list)
    counts, bin_edges = np.histogram (sorted_data, bins=30, density=True)
    cdf = np.cumsum (counts)
    plt.plot ( bin_edges[1:], cdf/cdf[-1],label= label)
    plt.xlabel("Rx")
    # plt.ylabel('Number of data samples')
    plt.ylabel("Portion of slots")
    plt.grid(True)
    plt.legend()  
    plt.savefig(os.path.join(os.getcwd(),"cdf_rx_all.png"))


plot(oqpskData,"oqpsk",0)
plot(ofdmData,"ofdm",2)
plot(fskData,"fsk",4)

plotAggregate(oqpskData,"oqpsk",6)
plotAggregate(ofdmData,"ofdm",6)
plotAggregate(fskData,"fsk",6)