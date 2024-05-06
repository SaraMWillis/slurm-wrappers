#!/usr/bin/env python3

import subprocess, sys, re
from formatting.slurm_output_reformatting import split_node_format

'''
------------------------------------------------------------------------------------------
                                 Pull Job Data
Uses "scontrol show job -d --oneliner" to grab detailed data on every job running on the 
cluster. Specs are pulled from these to determine the number of GPUs, CPUs, etc. reserved. 
Also pulls the job queue for the --partition option.
'''
def get_scontrol_job_data(system_specifications,target_job = None):
    fields = ["JobId","Partition","Restarts","EndTime","TimeLimit","NodeList","NumNodes","NumCPUs","NumTasks","TRES","JOB_GRES","Nodes","Features","CPU_IDs","TresPerNode"]
    job_data = {}
    if target_job == None:
        p = subprocess.Popen(['scontrol show job -d --oneliner | grep "JobState=RUNNING"'],stdout=subprocess.PIPE, shell=True)
    else:
        p = subprocess.Popen(['scontrol show job -d --oneliner '+target_job+' | grep "JobState=RUNNING"'],stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
    out,err = p.communicate()

    if err != None and err.decode("utf-8",'ignore') != "":
        print("Oops, something has gone wrong!\nIf you've included a Job ID, check that it's valid and try again.")
        sys.exit(1)
    
    # Split up space-delimited output into a job dictionary 
    output = out.decode('utf-8','ignore').split("\n")
    
    if len(output) <= 1:
        print("No jobs found")
        return {}
    for job in output:
        details = job.split(' ')
        for i in details:
            # Fields and their values are separated by "="
            job_entry = i.split("=")

            # We only care about the fields we've defined, so we ignore the rest
            gpu_field = system_specifications["node_types"]["GPU Nodes"]["GPU Alloc"]
            gpu_job_values = system_specifications["node_types"]["GPU Nodes"]["GPU Values"]
            
            if job_entry[0] in fields:
                if job_entry[0] == "JobId":
                    JobId = job_entry[1]
                    job_data[JobId] = {"Individual Nodes" : {},"GPUAlloc":0}
                elif job_entry[0] =="Nodes":
                    current_node = job_entry[1]
                    job_data[JobId]["Individual Nodes"][current_node] = None
                elif job_entry[0] == "CPU_IDs":
                    cpus_assigned = 0
                    ids = job_entry[1].split(',')
                    for ID_set in ids:
                        split_set = ID_set.split("-")
                        if len(split_set) == 1:
                            cpus_assigned +=1
                        else:
                            cpus_assigned += len(range(int(split_set[0]),int(split_set[1]))) + 1
                    job_data[JobId]["Individual Nodes"][current_node] = cpus_assigned
                
                # GPU Field 
                elif job_entry[0] == gpu_field:
                    gpu_value = job_entry[1]
                    if job_entry[1] not in gpu_job_values:
                        print("WARNING: GPU value '%s' which is not listed in the configuration file. Ignoring."%job_entry[1])
                        pass
                    job_data[JobId]["GPUAlloc"] = gpu_job_values[job_entry[1]]

                else:
                    entry_label = job_entry[0]
                    entry_data = job_entry[1]
                    job_data[JobId][entry_label] = entry_data
        # Catch all instances of node name reformatting so the jobs can be
        # matched 
        remove, add = [],[]
        for entry,cpus in job_data[JobId]["Individual Nodes"].items():
            nodes = split_node_format(entry,cpus)
            if "," in entry or "[" in entry:
                remove.append(entry)
                nodes = split_node_format(entry,cpus)
                add += nodes
        for entry in remove:
            job_data[JobId]["Individual Nodes"].pop(entry)
        for entry in add:
            job_data[JobId]["Individual Nodes"][entry[0]] = entry[1]
    return job_data
    
    
    
'''
------------------------------------------------------------------------------------------
                                  Get Node Data
Get all data from nodes and arrange into dictionary. This can be merged with the job data 
to get comprehensive information about system use.
'''
def get_scontrol_node_data(node_specifications):
    node_types = node_specifications["node_types"]
    cpu_limits = node_specifications["cpu_limits"]
    node_annotations = node_specifications["node_annotations"]

    max_cpus = 0
    # Used to collect the reasons nodes may be in the down/drain state
    node_data = {"REASONS":{}}
    n = 1
    fields = ["NodeName","CPUAlloc","CPUTot","AvailableFeatures","AllocTRES","CfgTRES","State","Reason","Partitions","Gres"]
    ufields = {}
    # node_types is defined as a global variable at the start of the script. This is to differentiate
    # standard, gpu, high memory, etc. nodes. 
    for i in node_types.items():
        k,v,f = i[0],i[1]["Value"],i[1]["Field"]
        # Setting the specific node type to none is how a node type is made the default categorization
        if f != None:
            # There may be multiple fields associated with a node type. This catches that case.
            if type(f) == list:
                for f_i in f:
                    ufields[f_i] = (v,k)
            else:
                ufields[f] = (v,k)
    uvalues = {}
    for i in node_types.items():
        k,v = i[0],i[1]["Value"]
        if v != None:
            uvalues[v] = k

    # Node information is collected from scontrol and arranged into a dictionary.            
    p = subprocess.Popen(['scontrol show nodes --all --oneliner'],stdout=subprocess.PIPE,shell=True)
    out,err = p.communicate()
    node_output = out.decode('utf-8','ignore').split("\n")
    for i in node_output:
        node_specs = i.split(" ")
        for j in node_specs:
            field = j.split("=")[0]
            if field in fields:
                # Since NodeName is the first field, this is where we add preliminary data.
                # Standard Nodes are the assumed default (this can be renamed in the user
                # options). This may be altered if other node specs defined in node_types
                # are found. 
                if field == "NodeName":
                    Node_Name = j.split("=")[-1]
                    node_data[Node_Name]={"Node_Type":node_types["Standard Nodes"]["Name"],"Annotation":None}
                    
                # Add annotations if field and value match user specifications
                if node_annotations != None and j.split("=")[1] in [i["Value"] for i in node_annotations.values()]:
                    for f,v in node_annotations.items():
                        if v["Field"] == field and v["Value"] == j.split("=")[1]:
                            if node_data[Node_Name]["Annotation"] ==None:
                                node_data[Node_Name]["Annotation"] = {f: {"Ascii": v["Ascii Symbol"],"UTF-8": v["UTF-8 Symbol"]} }
                            else:
                                node_data[Node_Name]["Annotation"][f] = {"Ascii": v["Ascii Symbol"],"UTF-8": v["UTF-8 Symbol"]} 
                # Next, we check if a specified node type was found
                if field in ufields.keys():
                    if ufields[field][0] in j:
                        # I know, this is nested chaos... I'm sorry
                        # All that's happening is that the node grouping
                        # is being checked to see if it should be changed
                        current_priority = node_types[node_data[Node_Name]["Node_Type"]]["Priority"]
                        check_priority = node_types[ufields[field][1]]["Priority"]
                        if check_priority > current_priority:
                            node_data[Node_Name]["Node_Type"] = ufields[field][1]

                # SLURM shows GPUs either in AllocTRES or CfgTRES. 
                gpu_field = node_specifications["node_types"]["GPU Nodes"]["Field"]
                if field == gpu_field:
                    if "gpu" in j:
                        gpu_count = j.split("gpu")[-1].split("=")[-1]
                        node_data[Node_Name][field] = gpu_count

                # This bit grabs why a node is down/draining
                # Reasons may include spaces and the node specs are space-delimited
                # (sigh), so this gets the full reason 
                elif field == "Reason":
                    reason = i.split("Reason=")[-1].split(" Comment=")[0] 
                    removal = re.search('\[[^\]]*\]',reason)
                    initiator = removal.group(0)
                    reason = reason.replace(initiator,"")
                    if reason not in node_data["REASONS"]:
                        node_data["REASONS"][reason]=n
                        node_data[Node_Name]["Reason"] =n
                        n+=1
                    else:
                        node_data[Node_Name]["Reason"] =node_data["REASONS"][reason]
                elif field == "State":
                    state = j.split("=")[-1]
                    if "DOWN" in state:
                        node_data[Node_Name]["State"] = "DOWN"
                    elif "DRAIN" in state:
                        node_data[Node_Name]["State"] = "DRAIN"
                    else:
                        node_data[Node_Name]["State"]="UP"
                elif field == "CPUTot":
                    cpu_count = int(j.split("=")[-1])
                    if cpu_limits != None and str(cpu_count) in cpu_limits.keys():
                        cpu_count = int(cpu_limits[str(cpu_count)])
                    if cpu_count > max_cpus:
                        max_cpus = cpu_count
                    node_data[Node_Name][field] = cpu_count
                    percentage = str(round(100*(int(node_data[Node_Name]["CPUAlloc"])/cpu_count),2))+"%"
                    percentage = " "*(6-len(percentage))+percentage
                    node_data[Node_Name]["CPU_PERCENT"] = percentage
                else:
                    node_data[Node_Name][field] = j.split("=")[-1]
    node_data["MAX_CPUS"] = max_cpus
    return node_data