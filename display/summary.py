#!/usr/bin/env python3

import sys
from display.print_header import print_header
from formatting.summarize_system_info import system_summary

def usage_bar(width,percent_used,used_block,blank_block,label,max_label_length):
    percent_length = 6
    bar_width = width - max_label_length - percent_length
    
    #formatting_string ="{0:%s}"%str(max_label_length)+": ["+"{1:%s"+"] "%str(bar_width)+"{2:%s}"%str(percent_length)
    formatting_string = "{0:%s}: [{1:%s}] {2:%s}"%(max_label_length,bar_width,percent_length)
    num_used_blocks = round(percent_used/100*bar_width)
    num_blank_blocks = bar_width-num_used_blocks
    bars = (num_used_blocks*used_block)+(num_blank_blocks*blank_block)
    percent = str(percent_used)+"%"
    print(formatting_string.format(label,bars,percent))
    #print(label+": ["+(num_used_blocks*used_block)+(num_blank_blocks*blank_block)+"] "+str(percent_used)+"%")
    return
    

def display_system_summary(merged,job_options,vis,system_specifications):
    
    vis.width = 100
    print_header(vis,job_options)
    
    # Get ascii or utf-8 symbols we'll use for visual display
    if vis.use_ascii == True:
        usage_block = vis.ascii_char
        blank_block = " "
    else:
        usage_block = vis.summary_utf8_char
        blank_block = vis.summary_utf8_blank

    # Get a summary of the system as a dictionary
    system_summary_dict = system_summary(merged,system_specifications)
    
    #print(system_summary_dict.keys())
    max_label_length = max([len(i) for i in system_summary_dict["Node_Types"].keys()])
    
    bar_widths = vis.width - 5
    
    ### Overview of total system
    print("Total Usage".center(vis.width," "))
    print("-"*vis.width)
    usage_bar(bar_widths,system_summary_dict["Percent_CPUs_Used"],usage_block,blank_block,"CPU",max_label_length)
    if system_summary_dict["Percent_GPUs_Used"] !="N/A":
        usage_bar(bar_widths,system_summary_dict["Percent_GPUs_Used"],usage_block,blank_block,"GPU",max_label_length)
        
    print("\n")
    for node_type,specs in system_summary_dict["Node_Types"].items():
        print(node_type.center(vis.width," "))
        print("-"*vis.width)
        usage_bar(bar_widths,system_summary_dict["Node_Types"][node_type]["Percent_CPUs_Used"],usage_block,blank_block,"CPU",max_label_length)
        if system_summary_dict["Node_Types"][node_type]["Percent_GPUs_Used"] != "N/A":
            usage_bar(bar_widths,system_summary_dict["Node_Types"][node_type]["Percent_GPUs_Used"],usage_block,blank_block,"GPU",max_label_length)
        print()
        #print(node_type,specs)
    sys.exit(0)
    print("Usage by Node Type".center(vis.width," "))
    print("-"*vis.width)
    #usage_bar(bar_widths,system_summary_dict["Percent_CPUs_Used"],usage_block,blank_block,"Standard")
    #usage_bar(bar_widths,system_summary_dict["Percent_CPUs_Used"],usage_block,blank_block,"High Memory")
    sys.exit(0)
    pcpus_in_use = round(system_summary_dict["Percent_CPUs_Used"]/100*vis.width)
    print(system_summary_dict["Percent_CPUs_Used"])
    print(pcpus_in_use)
    pcpus_idle = vis.width-round(pcpus_in_use)
    print(pcpus_idle)
    print("Total: ["+(pcpus_in_use*usage_block)+(pcpus_idle*blank_block)+"]")

    sys.exit(0)