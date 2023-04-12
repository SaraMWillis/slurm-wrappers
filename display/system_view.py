#!/usr/bin/env python3

import datetime, math

from formatting.usage_bar import scale, highlight, usage_bar, format_string
from formatting.sorting import sort_node_types

'''
------------------------------------------------------------------------------------------
##########################################################################################
                                Display Subroutines                                
##########################################################################################
------------------------------------------------------------------------------------------
                                  Print Header
                                  
******************************************************************************************

Print header for the output. Not a whole lot going on here aside from displaying the
current time, giving the output a nice header, and double-checking that utf-8 encoding
is enabled. 
'''
def print_header(width,job_options,vis):
    ENDCOLOR = vis.ENDCOLOR
    cycle = vis.color_cycle()
    
    # Formats the current day/time into something that can be displayed nicely
    # The time_spacing is used to center the message.
    today = datetime.datetime.now()
    time_string = "%s"%today.strftime("%a %b %d, %I:%M:%S %p (MST) %G")
    time_string_length = len(time_string)
    time_spacing = math.ceil(width/2) - math.ceil(time_string_length/2)

    # Similar to above, heading_spacing is used to center the header string
    heading_string = " System Status "
    heading_spacing = math.ceil(width/2) - math.ceil((len(heading_string)+2)/2)
    
    if job_options.use_ascii == False:
        block = vis.utf8_char
    else:
        block = vis.ascii_char
        
    print("="*width)
    
    # if anything is wonky with the user's environment (e.g. the python encoding 
    # variable is set to use ascii, this will catch it. 
    try:
        print("\n"+" "*heading_spacing +  block + heading_string + block)
    except UnicodeEncodeError:
        block = vis.ascii_char
        job_options.use_ascii = True
        print("\n"+" "*heading_spacing +  block + heading_string + block)
        
    print(" "*time_spacing + time_string)
    
    if job_options.partition != None:
        partition_string = "Highlighting resources reserved by the %s partition"%job_options.partition
        partition_spacing = math.ceil(width/2) - math.ceil(len(partition_string)/2)
        print(cycle[0]+" "*partition_spacing + partition_string + ENDCOLOR)
    elif job_options.user != None:
        user_string = "Highlighting resources reserved by user: %s"%job_options.user
        user_spacing = math.ceil(width/2) - math.ceil(len(user_string)/2)
        print(cycle[0]+" "*user_spacing + user_string + ENDCOLOR)
    elif job_options.group != None:
        group_string = "Highlighting resources reserved by group: %s"%job_options.group
        group_spacing = math.ceil(width/2) - math.ceil(len(group_string)/2)
        print(cycle[0]+" "*group_spacing + group_string + ENDCOLOR)
    return job_options
    
    
'''
******************************************************************************************
------------------------------------------------------------------------------------------
                                Display Node Type
'''                                
def display_node_type(node_specs,ntype,nval,job_options,vis,cpu_limits):
    #partition,user,group, node,all_nodes,color_random, use_ascii= job_options
    # Get vis options
    ENDCOLOR = vis.ENDCOLOR
    DOWNCOLOR = vis.DOWNCOLOR
    DOWNUSEDCOLOR = vis.DOWNUSEDCOLOR
    width = vis.width
    max_cpus = vis.max_cpus
    max_gpus = vis.max_gpus
    

    # Get user options
    user = job_options.user
    group=job_options.group
    partition=job_options.partition
    all_nodes = job_options.all_nodes

    # Choose usage block based on whether ascii is needed
    if job_options.use_ascii == True:
        block = vis.ascii_char
    else:
        block = vis.utf8_char

    # Color cycle for highlighting usage 
    cycle = vis.color_cycle()
    # If a particular node type isn't found, the header/non-existent values aren't
    # displayed
    if len(nval) == 0:
        pass
    else:
        print("\n"+ntype+"\n"+"="*width)
        node_specs = highlight(nval,node_specs,partition,user,group)
        jobs_found = False
        for data in nval:
            node,CPUAlloc = data
            highlighted = node_specs[node]["highlighted_cpus"]
            highlighted_gpus = node_specs[node]["highlighted_gpus"]
            if node_specs[node]["Annotation"] ==None:
                annotate=""
            elif job_options.use_ascii == True:
                annotate=[]
                for ann in node_specs[node]["Annotation"].values():
                    annotate.append(ann["Ascii"])
                    vis.valid_annotations.add(ann["Ascii"])
                annotate = ",".join(annotate)
            else:
                annotate=[]
                for ann in node_specs[node]["Annotation"].values():
                    annotate.append(ann["UTF-8"])
                    vis.valid_annotations.add(ann["UTF-8"])
                annotate = ",".join(annotate)
            
            # Add bit about annotation here. Specifically related to "annotate" Will ignore until user options are more well-defined
            if (user != None or group != None) and highlighted == 0 and all_nodes==False:
                pass
            else:
                jobs_found = True
                total_cpus = node_specs[node]["CPUTot"]
                percentage = node_specs[node]["CPU_PERCENT"]
                if cpu_limits != None and total_cpus in cpu_limits.keys():
                    total_cpus = cpu_limits[total_cpus]
                #percentage = str(round(100*(int(CPUAlloc)/int(total_cpus)),2))+"%"
                #percentage = " "*(6-len(percentage))+percentage
                state = node_specs[node]["State"]
                usage = usage_bar(block,CPUAlloc,highlighted,total_cpus,state,vis)
                
                # Check to see if this is a GPU node
                try:
                    total_gpus = int(node_specs[node]["CfgTRES"])
                except KeyError:
                    total_gpus = 0
                # Even if this is a GPU node, GPUs may not be used. Catch this case here.
                try:
                    total_gpus_used = sum([int(job["GPUs"]) for job in node_specs[node]["JOBS"].values()])
                except KeyError:
                    total_gpus_used = 0
                if total_gpus != 0:
                    gpu_usage = usage_bar(block,total_gpus_used,highlighted_gpus,total_gpus,state,vis)+" "*(int(max_gpus)-int(total_gpus)+2)
                    gpu_percentage = str(round(100*(int(total_gpus_used)/int(total_gpus)),2))+"%"
                    gpu_percentage = " "*(6-len(gpu_percentage))+gpu_percentage
                
                
                if state not in ["DOWN","DRAIN"]:
                    if total_gpus == 0:
                        formatting_string = format_string(False,False,max_cpus,DOWNCOLOR,ENDCOLOR)
                        print(formatting_string.format(node,usage,percentage,annotate))
                    else:
                        formatting_string = format_string(False,True,max_cpus,DOWNCOLOR,ENDCOLOR,max_gpus)
                        print(formatting_string.format(node,usage,percentage,gpu_usage,gpu_percentage,annotate))
                else:
                    reason = node_specs[node]["Reason"]
                    if total_gpus == 0:
                        formatting_string = format_string(True,False,max_cpus,DOWNCOLOR,ENDCOLOR)
                        print(formatting_string.format(node,usage,percentage,state,reason,annotate))
                    else:
                        formatting_string = format_string(True,True,max_cpus,DOWNCOLOR,ENDCOLOR,max_gpus)
                        print(formatting_string.format(node,usage,percentage,gpu_usage,gpu_percentage,state,reason,annotate))
        if jobs_found == False and user != None:
            print("No user jobs found")
        if jobs_found == False and group != None:
            print("No jobs matching %s group"%group)
        elif jobs_found == False and user == None:
            print("No nodes found")
            

'''
******************************************************************************************
------------------------------------------------------------------------------------------
                                      Display
Goes through the whole process of sorting data, highlighting, checking user options, 
getting usage bar, and printing headers/formatting etc. 
'''
def system_display(node_specs,job_options,vis,node_specifications):
    node_types = node_specifications["node_types"]
    cpu_limits = node_specifications["cpu_limits"]
    node_annotations = node_specifications["node_annotations"]
    # Some color options defined in the vis class at the beginning of this script. Used for
    # highlighting selected users, groups, and partitions, or picking out down/draining
    # nodes.
    ENDCOLOR = vis.ENDCOLOR
    DOWNCOLOR = vis.DOWNCOLOR
    DOWNUSEDCOLOR = vis.DOWNUSEDCOLOR
    cycle = vis.color_cycle()
    max_cpus = node_specs["MAX_CPUS"]
    if job_options.scale == True and max_cpus != job_options.scaled_width:
        job_options.scale_ratio = job_options.scaled_width/max_cpus
        node_specs=scale(node_specs,job_options,vis)
        vis.utf8_char=vis.scale_utf8_char

    # We sort nodes based on CPU usage. This makes it so when all nodes are displayed, 
    # CPU usage will be shown in decending order
    sorted_specs, max_cpus, max_gpus = sort_node_types(node_specs,node_types)
    
    # Added new submodule to print the header as its own bit. Attempting to make this whole
    # display section less redundant/less of a mess.
    width = max_cpus + max_gpus + 30

    vis.width = width
    vis.max_cpus = max_cpus
    vis.max_gpus = max_gpus
    
    job_options = print_header(vis.width,job_options,vis)
    # Goes through each node type and prints a visualization of usage
    for ntype, nval in sorted_specs.items():
        display_node_type(node_specs,ntype,nval,job_options,vis,cpu_limits)
    
    # prints reasons why nodes are down or draining. 
    if len(node_specs["REASONS"].items()) != 0:
        print("\n\nDown/Drain* Node Reasons")
        print("="*width)
        for i,j in node_specs["REASONS"].items():
            print("[%s] %s"%(j,i))
        print("\n* Nodes in the DRAIN state will wait for all running jobs to complete\nand will not accept new jobs without manual intervention\n")
    
    if len(vis.valid_annotations) != 0:
        print("\nNode Annotations"+"\n"+"="*width)
        for a,v in node_annotations.items():
            if job_options.use_ascii == True:
                a_s = v["Ascii Symbol"]
            else:
                a_s = v["UTF-8 Symbol"]
            if a_s in vis.valid_annotations:
                print("{0:4} {1:50}".format(a_s,v["Message"]))
    return