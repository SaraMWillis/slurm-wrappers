#!/usr/bin/env python3

import sys 

'''
The goal with this subroutine is to get a summary overview of the cluster that can be displayed
in either text or graphical format. 

'''
def system_summary(system_dictionary,system_specifications):
    # Define some standard statistics we want to collect
    gpu_field = system_specifications["node_types"]["GPU Nodes"]["Field"]
    summary_dict = {"Total_Nodes": 0,
                    "Idle_Nodes": 0,
                    "Percent_Nodes_Idle":0,
                    "Down_Nodes": 0,
                    "Percent_Nodes_Down":0,
                    "Drain_Nodes": 0,
                    "Percent_Nodes_Drain":0,
                    "Total_Jobs":0,
                    "Total_CPUs": 0,
                    "CPUs_in_Use":0,
                    "Percent_CPUs_Used":0,
                    "GPUs_in_Use":0,
                    "Total_GPUs": 0,
                    "Percent_GPUs_Used":0,
                    "Node_Types": {}
    }
    for node,data in system_dictionary.items():
        if node in ["REASONS","MAX_CPUS"] :
            pass
        else:
            # We want specific information about the different nodes types, so we'll start
            # collecting this information in a dictionary 
            if data["Node_Type"] not in summary_dict["Node_Types"]:
                summary_dict["Node_Types"][data["Node_Type"]] = {"Count":1, "Down_Nodes":0,"Idle_Nodes":0,"Drain_Nodes":0, "Total_CPUs": int(data["CPUTot"]),"Total_GPUs": 0,"CPUs_in_Use":0,"GPUs_in_Use":0, "Total_Jobs":0}
            else:
                summary_dict["Node_Types"][data["Node_Type"]]["Count"] +=1
                summary_dict["Node_Types"][data["Node_Type"]]["Total_CPUs"] += int(data["CPUTot"])
                
            summary_dict["Total_Nodes"] +=1
            summary_dict["Total_CPUs"] += int(data["CPUTot"])
            if data["State"] == "DOWN":
                summary_dict["Down_Nodes"] +=1 
                summary_dict["Node_Types"][data["Node_Type"]]["Down_Nodes"] +=1 
            elif data["State"] == "DRAIN":
                summary_dict["Drain_Nodes"] += 1
                summary_dict["Node_Types"][data["Node_Type"]]["Drain_Nodes"] +=1 
            elif "JOBS" not in data.keys():
                summary_dict["Idle_Nodes"] += 1
                summary_dict["Node_Types"][data["Node_Type"]]["Idle_Nodes"] +=1 
                
            # We want jobs on up, down, and drain nodes, so we'll check whether jobs are on 
            # the relevant node again. The previous check won't work for this since it excludes
            # drain/down nodes, and I don't want to count those as idle nodes. 
            if "JOBS" in data.keys():
                total_jobs = len(data["JOBS"].keys())
                cpus_in_use = sum([int(i["CPUs"]) for i in data["JOBS"].values()])
                gpus_in_use = sum([int(i["GPUs"]) for i in data["JOBS"].values()])
            else:
                total_jobs = 0
                cpus_in_use = 0
                gpus_in_use = 0
            # Only nodes with GPUs have this value
            if gpu_field in data.keys():
                summary_dict["Total_GPUs"] += int(data[gpu_field ])
                summary_dict["Node_Types"][data["Node_Type"]]["Total_GPUs"] += int(data[gpu_field])
            summary_dict["Node_Types"][data["Node_Type"]]["CPUs_in_Use"] += cpus_in_use
            summary_dict["Node_Types"][data["Node_Type"]]["GPUs_in_Use"] += gpus_in_use
            summary_dict["Node_Types"][data["Node_Type"]]["Total_Jobs"] += total_jobs
            summary_dict["CPUs_in_Use"] += cpus_in_use
            summary_dict["GPUs_in_Use"] += gpus_in_use
            summary_dict["Total_Jobs"] += total_jobs
    
    # Now that we have our absolute counts, let's calculate some percentages
    summary_dict["Percent_Nodes_Idle"]=round((summary_dict["Idle_Nodes"]/summary_dict["Total_Nodes"])*100,2)
    summary_dict["Percent_Nodes_Down"]=round((summary_dict["Down_Nodes"]/summary_dict["Total_Nodes"])*100,2)
    summary_dict["Percent_Nodes_Drain"]=round((summary_dict["Drain_Nodes"]/summary_dict["Total_Nodes"])*100,2)
    summary_dict["Percent_CPUs_Used"]=round((summary_dict["CPUs_in_Use"]/summary_dict["Total_CPUs"])*100,2)
    if summary_dict["Total_GPUs"] != 0:
        summary_dict["Percent_GPUs_Used"]=round((summary_dict["GPUs_in_Use"]/summary_dict["Total_GPUs"])*100,2)
    else:
        summary_dict["Percent_GPUs_Used"] = "N/A"
    
    # Let's also calculate these values for each node type
    for node_type,values in summary_dict["Node_Types"].items():
        values["Percent_Nodes_Idle"] = round((values["Idle_Nodes"]/values["Count"])*100,2)
        values["Percent_Nodes_Down"] = round((values["Down_Nodes"]/values["Count"])*100,2)
        values["Percent_Nodes_Drain"] = round((values["Drain_Nodes"]/values["Count"])*100,2)
        values["Percent_CPUs_Used"]=round((values["CPUs_in_Use"]/values["Total_CPUs"])*100,2)
        if values["Total_GPUs"] ==0:
            values["Percent_GPUs_Used"]="N/A"
        else:
            values["Percent_GPUs_Used"]=round((values["GPUs_in_Use"]/values["Total_GPUs"])*100,2)
    return summary_dict