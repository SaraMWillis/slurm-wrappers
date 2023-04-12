#!/usr/bin/env python3

import re

    
    
'''
******************************************************************************************
------------------------------------------------------------------------------------------
                                  Splitting Node Names
Slurm tries to make for nice output by representing nodes in formats like:
cpu1,cpu31,cpu[45-46,48,51-55],cpu[57-58],cpu[59-60,63],cpu[70,74]...
which is a bummer to parse. These functions are dedicated to untangling this.
As far as I'm aware, there isn't a way to print node lists in long form with
scontrol. If I'm wrong on this, *please* let me know.

'''


# This bit catches the cases where a node name might be something like node01
# We need to pull the leading zero(s) and hang onto it/them. This is because to unpack
# node lists effectively, we'll need to generate a range of integers which will eliminate
# leading zeros. Trying to paste those indices back together with the node prefix will
# lead to an invalid node name causing a dictionary error later in this pipeline. 
def store_leading_zero(index):
    if index[0] != "0" or index == "0":
        prefix=""
    else:
        prefix = ""
        for i in range(0,len(index)+1):
            if index[i] =="0":
                prefix += index[i]
            else:
                break
    return prefix

# This section has been changed after discovering some edge cases that made the
# old version fail. This formatting is a nightmare to disentangle. I'll try to 
# annotate for future screaming matches with my computer:

# Tested on:
# r2u13n2,r2u25n1,r2u26n1,r2u28n1
# gpu[1-50,76,78-90]
# exp-1-[25-26],exp-2-[47-48],exp-3-[01-02,37-38],exp-4-[47-48],exp-5-[08-09,56],exp-8-[01-02],exp-14-[16-18],exp-30-20,exp-25-01
# r3u08n2,r3u12n2,r3u14n1,r3u16n2,r3u17n[1-2]

def split_node_format(NodeList,cpus):
    split_nodes = []
    # We split up our list of nodes into groups with the specific intent of 
    # separating node prefixes from their possible index ranges
    split_groups = [i for i in re.findall("([\w\[,\-]*)",NodeList) if i != ""]
    for i in split_groups:
        # Scrub the node name prefix of any leading commas
        if "," == i[0]:
            i = i[1:]
        # If there aren't any brackets, then the names are well-behaved and 
        # we can split them easily using commas. However, if there are brackets,
        # we need to unpack the index values. 
        if "[" in i:
            node_prefix,indices = i.split("[")
            # Unpack any clustered indices
            if "," in node_prefix:
                node_cluster = node_prefix.split(",")
                leading_nodes = node_cluster[:-1]
                node_prefix= node_cluster[-1]
                split_nodes += [(n,cpus) for n in leading_nodes]
            v_ranges = indices.split(",")
            # For each range of indices shown as 1-10, or 002-010 (bummer), we'll 
            # grab the leading zeros so that the indices can be converted to integers
            # and will then generate a range
            for r in v_ranges:
                r_split = r.split("-")
                if len(r_split) == 1:
                    split_nodes.append((node_prefix+r_split[0],cpus))
                else:
                    first_index, second_index = r_split
                    leading_val = store_leading_zero(first_index)
                    index_range = range(int(first_index),int(second_index)+1)
                    previous_index = index_range[0]
                    for index in index_range:
			# Another frustration here. If we transition from a single digit to double-digit
			# index, we might see: node[01-10], which will generate:
			# node01,node02,...,node010. We want to avoid this, so a length comparison is
			# used. It's (highly) probable another issue will crop up sometime. Sigh. 
                        if len(str(index)) > len(str(previous_index)) and leading_val != "":
                            leading_val = leading_val[1:]
                        split_nodes.append((node_prefix + leading_val + str(index),cpus))
        else:
            split_nodes += [(n,cpus) for n in i.split(",")]
    return split_nodes
    
    
    
'''
------------------------------------------------------------------------------------------
                                          Merge
Merge the jobs and nodes dictionary together to get comprehensive data on system use. 
'''
def merge(jobs_dictionary, nodes_dictionary):
    for job in jobs_dictionary.keys():
        for node,cpus in jobs_dictionary[job]["Individual Nodes"].items():
            if "JOBS" not in nodes_dictionary[node].keys():
                nodes_dictionary[node]["JOBS"] = {}
            nodes_dictionary[node]["JOBS"][job] = {"CPUs":cpus, "GPUs":jobs_dictionary[job]["GPUAlloc"],"EndTime":jobs_dictionary[job]["EndTime"],"Partition":jobs_dictionary[job]["Partition"],"Restarts":jobs_dictionary[job]["Restarts"]}
    return nodes_dictionary
    