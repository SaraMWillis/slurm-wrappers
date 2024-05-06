#!/usr/bin/env python3 

import math
from slurm.squeue import get_user_jobids

'''
******************************************************************************************
------------------------------------------------------------------------------------------
                                         Usage Bar
Create a usage bar for each node, highlighting any CPUs or GPUs based on user options
'''
def usage_bar(usage_block,num_used,num_highlighted,total_cpus,state,vis):
    if state in ["DOWN","DRAIN"]:
        HIGHLIGHTCOLOR=vis.DOWNUSEDCOLOR
        UNHIGHLIGHTCOLOR = vis.DOWNCOLOR
    else:
        HIGHLIGHTCOLOR = vis.color_cycle()[0]
        UNHIGHLIGHTCOLOR = vis.ENDCOLOR
    used = int(num_used)
    highlighted = int(num_highlighted)
    unhighlighted = used - num_highlighted
    total_cpus = int(total_cpus)
    blank = total_cpus - used

    usage = UNHIGHLIGHTCOLOR+"["+usage_block*unhighlighted+HIGHLIGHTCOLOR+usage_block*highlighted+UNHIGHLIGHTCOLOR+" "*blank+"]"+vis.ENDCOLOR
    return usage
    
'''
------------------------------------------------------------------------------------------
                                        Highlight
In case --user or --partition has been included, the CPUs/GPUs associated with the request
need to be highlighted with a color. This grabs the number that need to be highlighted
'''
def highlight(node_list, node_dictionary, partition, user,group):
    if partition != None:
        for data in node_list:
            node,CPUAlloc = data
            highlighted_cpus = 0
            highlighted_gpus = 0
            try:
                for job,job_data in node_dictionary[node]["JOBS"].items():
                    if job_data["Partition"] == partition:
                        highlighted_cpus += int(job_data["CPUs"])
                        highlighted_gpus += int(job_data["GPUs"])
                    else:
                        pass
            except KeyError:
                highlighted_cpus = 0
                highlighted_gpus = 0
            node_dictionary[node]["highlighted_cpus"] = highlighted_cpus
            node_dictionary[node]["highlighted_gpus"] = highlighted_gpus
    elif user != None or group != None:
        user_job_list = get_user_jobids(user,group)
        for data in node_list:
            node,CPUAlloc = data
            highlighted_cpus =0
            highlighted_gpus =0
            try:
                for job, job_data in node_dictionary[node]["JOBS"].items():
                    if job in user_job_list:
                        highlighted_cpus += int(job_data["CPUs"])
                        highlighted_gpus += int(job_data["GPUs"])
                    else:
                        pass
            except KeyError:
                highlighted_cpus = 0
                highlighted_gpus = 0
            node_dictionary[node]["highlighted_cpus"] = highlighted_cpus
            node_dictionary[node]["highlighted_gpus"] = highlighted_gpus
    else:
        for data in node_list:
            node,CPUAlloc = data
            highlighted_cpus = 0
            highlighted_gpus = 0
            node_dictionary[node]["highlighted_cpus"] = highlighted_cpus
            node_dictionary[node]["highlighted_gpus"] = highlighted_gpus

    return node_dictionary
    
'''
------------------------------------------------------------------------------------------
                                      Scale

'''
def scale(node_specs,job_options,vis):

    scale_factor = job_options.scale_ratio
    for node,value in node_specs.items():
        if node in ("REASONS","MAX_CPUS"):
            pass
        else:
            true_fraction = float(value["CPUAlloc"])/float(value["CPUTot"])
            new_tot = math.ceil(int(value["CPUTot"])*scale_factor)
            scaled_usage = round(new_tot*true_fraction)

            value["CPUAlloc"] = scaled_usage
            value["CPUTot"] = new_tot
            if len(value)> 1 and "JOBS" in value.keys():
                for job,job_specs in value["JOBS"].items():
                    scaled_cpus = round(int(job_specs["CPUs"])*scale_factor)
                    value["JOBS"][job]["CPUs"] = scaled_cpus

    return node_specs
    
'''
------------------------------------------------------------------------------------------
                                   Format String
Create a formatted string for printing output.
'''
def format_string(down,gpu,max_cpus,DOWNCOLOR,ENDCOLOR,max_gpus=None):
    if down == True and gpu == False:
        formatting_string = DOWNCOLOR + "{0:9}:{1:"+str(max_cpus+2)+"}"+DOWNCOLOR+" {2:>5} {3:6}[{4:1}] {5:2}"+ENDCOLOR
    elif down == False and gpu == False:
        # Expecting input (node name, usage bar, percentage)
        formatting_string = formatting_string ="{0:9}:{1:"+str(max_cpus+2)+"} {2:*>5} {3:2}"
    elif down == True and gpu == True:
        # Expecting input (node name, usage bar, percentage, GPU usage bar, GPU percentage, state, reason index)
        formatting_string = DOWNCOLOR+"{0:9}:{1:"+str(max_cpus+2)+"}"+DOWNCOLOR+" {2:>5} {3:"+str(max_gpus+2)+"} "+DOWNCOLOR+"{4:>5} {5:6}[{6:1}] {7:2}" + ENDCOLOR
    elif down == False and gpu == True:
        # Expecting input (node name, usage bar, percentage, GPU usage bar, GPU percentage)
        formatting_string = "{0:9}:{1:"+str(max_cpus+2)+"} {2:>6} {3:"+str(int(max_gpus)+3)+"} {4:<6} {5:2}"
    return formatting_string