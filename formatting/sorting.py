#!/usr/bin/env python3

'''
------------------------------------------------------------------------------------------
                                   Sort Node Types
Takes each node type defined by the user and sorts into a list based on cpu usage. Also
returns max cpus and max gpus on the cluster for formatting purposes.
'''
def sort_node_types(node_specs,node_types):
    max_cpus = 0
    max_gpus = 0 

    sorted_specs = {}
    
    for ntype in node_types.keys():
        sorted_specs[ntype] = []
        
    for key, data in node_specs.items():
        if key in ("REASONS","MAX_CPUS"):
            pass
        else:
            Node_Type = data["Node_Type"]
            CPUAlloc = int(data["CPUAlloc"])
            TotalCPU = int(data["CPUTot"])
            if TotalCPU > max_cpus:
                max_cpus = TotalCPU
            if Node_Type in node_types.keys():
                sorted_specs[Node_Type].append((key,CPUAlloc))
            try:
                TotalGPU = int(data["CfgTRES"])
            except KeyError:
                TotalGPU = 0
            if TotalGPU > max_gpus:
                max_gpus = TotalGPU
                
    for i in sorted_specs.values():
        i.sort(key=lambda x: x[1], reverse=True)
    return sorted_specs, max_cpus, max_gpus