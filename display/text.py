#!/usr/bin/env python3

import sys, datetime, math

from formatting.summarize_system_info import system_summary
from display.print_header import print_header
from slurm.squeue import pending_job_statistics


        
def display_text_summary(system_dictionary,job_options,vis,system_specifications):
    

    print_header(vis,job_options)
    
    system_summary_dict = system_summary(system_dictionary,system_specifications)

    
    format_string = "{0:25}: {1:>15} {2:>9}"
    print(format_string.format("Total System Hardware","Count","%"))
    print("="*vis.width)
    print(format_string.format("Total nodes",system_summary_dict["Total_Nodes"],""))
    print(format_string.format("Total down nodes",system_summary_dict["Down_Nodes"],"(%s%%)"%system_summary_dict["Percent_Nodes_Down"]))
    print(format_string.format("Total drain nodes",system_summary_dict["Drain_Nodes"],"(%s%%)"%system_summary_dict["Percent_Nodes_Drain"]))
    print(format_string.format("Total idle nodes",system_summary_dict["Idle_Nodes"],"(%s%%)"%system_summary_dict["Percent_Nodes_Idle"]))
    print()
    print(format_string.format("Total CPUs",system_summary_dict["Total_CPUs"],""))
    print(format_string.format("CPUs in use",system_summary_dict["CPUs_in_Use"],"(%s%%)"%system_summary_dict["Percent_CPUs_Used"]))
    print()
    print(format_string.format("Total GPUs",system_summary_dict["Total_GPUs"],""))
    if system_summary_dict["Total_GPUs"] != 0:
        print(format_string.format("GPUs in use",system_summary_dict["GPUs_in_Use"],"(%s%%)"%system_summary_dict["Percent_GPUs_Used"]))
    print("\n")
    print("="*vis.width)
    print("Breakdown by Node Type")
    print("="*vis.width)
    for node_type,values in system_summary_dict["Node_Types"].items():
        print(node_type)
        print("-"*vis.width)
        print(format_string.format("Total nodes", values["Count"],""))
        print(format_string.format("Total down nodes",values["Down_Nodes"],"(%s%%)"%values["Percent_Nodes_Down"]))
        print(format_string.format("Total drain nodes",values["Drain_Nodes"],"(%s%%)"%values["Percent_Nodes_Drain"]))
        print()
        print(format_string.format("Total CPUs",values["Total_CPUs"],""))
        print(format_string.format("CPUs in Use",values["CPUs_in_Use"],"(%s%%)"%values["Percent_CPUs_Used"]))
        if values["Total_GPUs"] != 0:
            print(format_string.format("Total GPUs",values["Total_GPUs"],""))
            print(format_string.format("GPUs in Use",values["GPUs_in_Use"],"(%s%%)"%values["Percent_GPUs_Used"]))
        print("\n")
        
    sys.exit(0) 
    pending_jobs = pending_job_statistics(system_summary_dict,system_specifications)
    print(pending_jobs)
    head_format_string = "{0:25}  {1:>15} {2:>9}"
    print("\n"+"="*vis.width)
    print("Pending Job Data".center(vis.width," "))
    print("="*vis.width)
    print("All Pending Jobs".center(vis.width," "))
    print(head_format_string.format("Partition","Count","Average Wait"))
    print("-"*vis.width)
    #print(pending_jobs["Total"]["Count"])
    print(format_string.format("All",pending_jobs["Total"]["Count"],str(pending_jobs["Total"]["Average Wait"])))
    for p,v in pending_jobs["Total"].items():
        if p not in ["Count","Average Wait"]:
            print(format_string.format(p,v["Count"],""))
    #print(format_string.format("   -1 to 10 CPUs","",pending_jobs["Total"][]))
    print()
    for jtype,data in pending_jobs.items():
        if jtype == "Total":
            pass
        else:
            print(jtype)
            print("-"*vis.width)
            print(format_string.format("Job count",pending_jobs[jtype]["Count"],""))
            print(format_string.format("Average wait time",str(pending_jobs[jtype]["Average Wait"]).split(".")[0],""))
            print()
    print("\n\n\n")
    
    sys.exit(0)