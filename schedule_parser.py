import collections
import fskData

data= fskData.data
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



temp ={}
adjacent_pairs = []
bad_neighbors =  {}
my_neighbors = {}
all_neighbors = []
for m in data:
    my_neighbors = {}
    neigbors = data[m].get("Neighbors")
    if neigbors:
        for n in neigbors:
            my_neighbors [n['addr']]=n
            all_neighbors.append (n['addr'])

    s = data[m].get("Schedule")
    if s:                              
        for slot in s:
            if (slot ['numTx']>slot ['numTxACK']):
                print "packet loss {}".format(slot ['numTx']-slot ['numTxACK'])

                if ( slot['neighbor'] in bad_neighbors):
                    bad_neighbors [slot['neighbor']]['loss'].append (slot ['numTx']-slot ['numTxACK'])
                else:
                    bad_neighbors [slot['neighbor']] ={'loss': [slot ['numTx']-slot ['numTxACK']],
                    'desc': my_neighbors [slot['neighbor']]
                    }

            n = slot ['neighbor']
            if (n!=  ' (None)' and slot ['shared']==0):
                slot_usage_count.append(slot ['slotOffset'])
                
                if n == ' (anycast)':
                    r = res_anycast_usage_map.get((slot ['slotOffset'],slot ['channelOffset']))
                    if (r):
                        res_anycast_usage_map [slot ['slotOffset'],slot ['channelOffset']]  +=1
                        # print "***conflict {},{},{},{}".format(m,n,slot ['slotOffset'],slot ['channelOffset'])
                    else:
                        res_anycast_usage_map [slot ['slotOffset'],slot ['channelOffset']]  = 1
                else:
                    r = res_p2p_usage_map.get((slot ['slotOffset'],slot ['channelOffset']))
                    if (r):
                        res_p2p_usage_map [slot ['slotOffset'],slot ['channelOffset']]  +=1
                        #del res_p2p_awkward_usage_map [slot ['slotOffset'],slot ['channelOffset']] 
                    else:
                        res_p2p_usage_map [slot ['slotOffset'],slot ['channelOffset']]  = 1
                        #res_p2p_awkward_usage_map [slot ['slotOffset'],slot ['channelOffset']]  = n

                if n != ' (anycast)':
                    if(are_adjacent(m,n)):
                        n_short_addr = n[-11:-6].replace('-','')
                        adjacent_pairs.append([m,n_short_addr])
print "*********"
print res_p2p_usage_map
print "*********"
print "all  neighbors"
print (set(all_neighbors))
print "*********"
print "bad neighbors"
# print bad_neighbors
print ("addr\trank\t#nodes\tlosstotal\tloss")
for n in bad_neighbors:
    print ("{}\t{}\t{}\t{}\t{}".format(
        bad_neighbors[n]["desc"] ['addr'],
        bad_neighbors[n]["desc"] ['DAGrank'],
        len(bad_neighbors[n]['loss']),
        sum(bad_neighbors[n]['loss']),
        bad_neighbors[n]['loss']
    ))


print "Number of total motes in the network:"
print len(data.keys())

print "Number of adjacent pairs in the network:"
print len(adjacent_pairs)


print "\n\n----- Anycast Resource Conflict Measurements-----"

res_anycast_usage_count = res_anycast_usage_map.values()
counter=collections.Counter(res_anycast_usage_count)

print "Resource usage histogram:"
print(counter)

print "Minimum count of resource conflicts in the network:"
arr = get_conflicts(res_anycast_usage_count)
print (sum(arr))

print "Total number of nodes affected with resource conflicts:"
# [4, 4, 2, 1, 2]
#print(counter.keys())
print(len(arr))


print "\n\n----- P2P Resource Conflict Measurements-----"
res_p2p_usage_count = res_p2p_usage_map.values()
counter=collections.Counter(res_p2p_usage_count)
print "Conflicting Resources"
print res_p2p_usage_map.keys() 
print("{" + "\n".join("{!r}: {!r},".format(k, v) for k, v in res_p2p_usage_map.items()) + "}")

print list

print "Resource usage histogram:"
print(counter)

print "Minimum count of resource conflicts in the network:"
arr = get_conflicts(res_p2p_usage_count)
print (sum(arr))

print "Total number of nodes affected with resource conflicts:"
# [4, 4, 2, 1, 2]
#print(counter.keys())
print(len(arr))

print "\n\n----- P2P Asymmetric Resource Allocation Measurements-----"
res_p2p_awkward_usage_count = res_p2p_awkward_usage_map.values()
counter=collections.Counter(res_p2p_awkward_usage_count)

print "Resource usage histogram:"
print(counter)

print "Minimum count of resource conflicts in the network:"
arr = get_conflicts(res_p2p_awkward_usage_count)
print (sum(arr))

print "Total number of nodes affected with resource conflicts:"
# [4, 4, 2, 1, 2]
#print(counter.keys())
print(len(arr))

print "----- Slot Conflict Estimation from data -----"
estimate_conflict (data.keys())

print "----- Resource Conflict Estimation from mote_list-----"
motes =["b5d8",
"b48d",
"b622",
"b640",
"b629",
"b646",
"b647",
"b602",
"b61c",
"b61a",
"b5e7",
"b462",
"b498",
"b5a9",
"b557",
"b558",
"b588",
"b53d",
"b5a3",
"b4aa",
"b55b",
"b648",
"b57e",
"b595",
"b63a",
"b638",
"b593",
"b618",
"b5b5",
"b5f8",
"b5b7",
"b58c",
"b60b",
"b5f1",
"b5f3",
"b5f2",
"b5bf",
"b605",
"b563",
"b571",
"b565",
"b612"]
estimate_conflict(motes)

