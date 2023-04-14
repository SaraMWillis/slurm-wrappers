#!/usr/bin/env python3

from slurm.sinfo import get_partitions

'''
******************************************************************************************
------------------------------------------------------------------------------------------
                                Single Node Display
If the --node=<node_name> option is used, a single usage bar will appear with color-coded
blocks that display resources reserved on that node by job. This information includes CPU
count, GPU count (if applicable), job partition, job end time, and number of job 
interrupts. 
'''

def single_node_display(node,node_dictionary,use_ascii,vis,node_specifications):
    node_annotations = node_specifications['node_annotations']

    # First, we'll check that the node name actually exists on the system
    if node not in node_dictionary.keys():
        print("Oops! Node not found on cluster. Check your input and try again.")
        usage(1)

    # If utf-8 encoding isn't supported in the user's environment, we'll switch to ascii
    message = "Displaying usage info for node: %s"%node
    if use_ascii == True:
        block = vis.ascii_char
    else:
        block = vis.utf8_char
    try:
        print("\n%s %s %s"%(block, message,block))
    except UnicodeEncodeError:
        block = vis.ascii_char
        use_ascii = True
        print("\n%s %s %s"%(block, message,block))
    horizontal_line = "="*(len(message) + 4)
    print(horizontal_line)

    # Grab data about this specific node 
    node_specific_dictionary = node_dictionary[node]
    state = node_specific_dictionary['State']
    node_type = node_specific_dictionary["Node_Type"]
    allowed_partitions=get_partitions()
 
    # If this node is down, we'll find out and display why
    if state in ["DOWN","DRAIN"]:
        for r,index in node_dictionary["REASONS"].items():
           if node_specific_dictionary["Reason"] == index:
               reason = r
               break

    # Since we're only interested in one node, let's dump the rest
    del node_dictionary

    # The goal now is to display all the CPUs reserved by individual user jobs. Each
    # unique user job will receive its own color so they can be distinguished. We'll 
    # build the usage bar here.
    total_cpus = int(node_specific_dictionary["CPUTot"])
    color_index = 0
    color_cycle = vis.color_cycle()
    cpu_usage_bar = "["
    try:
        for job,data in node_specific_dictionary["JOBS"].items():
            color = color_cycle[color_index]
            node_specific_dictionary["JOBS"][job]["color"] = color
            num_cpus = int(data["CPUs"])
            cpu_usage_bar += color + block * num_cpus + vis.ENDCOLOR
            color_index += 1
    except KeyError:
        pass
    used_cpus = int(node_specific_dictionary["CPUAlloc"])
    unused_cpus = total_cpus - used_cpus
    cpu_usage_bar = cpu_usage_bar + " "*unused_cpus+ "]"
    used_gpus = 0

    # Get GPUs if applicable
    if node_type == "GPU Nodes":
        total_gpus = int(node_specific_dictionary["CfgTRES"])
        gpu_usage_bar = "["
        try:
            for job,data in node_specific_dictionary["JOBS"].items():
                color = data["color"]
                num_gpus = int(data["GPUs"])
                used_gpus += num_gpus
                gpu_usage_bar += color + block * num_gpus + vis.ENDCOLOR
        except KeyError:
            pass
        unused_gpus = total_gpus - used_gpus
        gpu_usage_bar = gpu_usage_bar + " "*unused_gpus +"]"
        gpu_percentage_usage = str(round(100*(used_gpus/total_gpus),2)) + "%"
    percentage_usage = str(round(100*(used_cpus/total_cpus),2)) + "%"


    # Print Node Data
    DOWNCOLOR = vis.DOWNCOLOR
    ENDCOLOR = vis.ENDCOLOR
    if state in ["DOWN","DRAIN"]:
        print(DOWNCOLOR+"State: %s -- %s"%(state,reason)+ENDCOLOR)
    else:
        print("State: %s"%state)
    print("Node Type: %s"%node_type)
    print("Allowed Partitions: %s"%','.join(allowed_partitions))
    print("Number of jobs running: %s"%color_index)
    print("CPUs Available: %s | CPUs Used: %s | Percent Utilized: %s"%(total_cpus,used_cpus,percentage_usage))
    if node_type == "GPU":
        print("GPUs Available: %s | GPUs Used: %s | Percent Utilized: %s\n"%(total_gpus,used_gpus,gpu_percentage_usage))
    
    # If this node has specific annotations, they are printed here
    if node_specific_dictionary["Annotation"] != None:
        print("\nNode Annotations:")
        for key,ann in node_specific_dictionary["Annotation"].items():
            if use_ascii == True:    
                print("{0:3}: {1:50}".format(ann["Ascii"],node_annotations[key]["Message"]))
            else:
                print("{0:3}: {1:50}".format(ann["UTF-8"],node_annotations[key]["Message"]))
    print(horizontal_line+"\n")
   
    # Slightly different formatting options for 
    if node_type =="GPU Nodes":
        format_string = "{0:"+str(len(node))+"} {1:"+str(total_cpus+3)+"} {2:"+str(total_gpus+3)+"}"
        print(format_string.format("Node","CPU Usage","GPU Usage"))
        print("%s:%s  %s"%(node,cpu_usage_bar,gpu_usage_bar))
    else:
        format_string = "{0:"+str(len(node))+"} {1:"+str(total_cpus+3)+"}"
        print(format_string.format("Node","CPU Usage"))
        print("%s:%s"%(node,cpu_usage_bar))
    print("\nJobs")
    print(horizontal_line)
    if node_type == "GPU":
        job_formatting_string = "{0:10} {1:8} {2:10} {3:4} {4:4} {5:8} {6:15}"
        print(job_formatting_string.format("Color","Job ID","Partition","CPUs","GPUs","Restarts","End Date/Time"))
    else:
        job_formatting_string = "{0:10} {1:8} {2:10} {3:4} {4:8} {5:15}"
        print(job_formatting_string.format("Color","Job ID","Partition","CPUs","Restarts","End Date/Time"))
    try:
        for job,data in node_specific_dictionary["JOBS"].items():
            color = data["color"]
            identifier = color + block + ENDCOLOR + 9*" "
            end_time = data["EndTime"].replace("T","/")
            if node_type == "GPU":
                print(job_formatting_string.format(identifier, str(job), data["Partition"],str(data["CPUs"]),str(data["GPUs"]),data["Restarts"],end_time))
            else:
                print(job_formatting_string.format(identifier, str(job), data["Partition"],str(data["CPUs"]),data["Restarts"],end_time))
    except KeyError:
        print(DOWNCOLOR+"\nNo jobs to display"+vis.ENDCOLOR)
    print()