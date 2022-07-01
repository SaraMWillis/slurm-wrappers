# SLURM Wrappers

> **⚠ Warning **  
> These scripts were developed for the University of Arizona's HPC center so some pieces may be specific to our setup. This is being worked on to make the scripts more customizable/portable.

> This branch will be changing soon. In the interests of simplicity/portability, I created the original scripts to be standalone. In the interests of maintainability, I'm working on creating libraries and config scripts

 


# Job Information
Retrieve running and past job data in a friendly format. Both scripts require job accounting data to be retrievable with ```sacct``` and ```scontrol```.

## ```past-jobs```
Get job IDs from the last ```<N>``` days. Usage: ```past-jobs -d <N>```. Example:
```
(elgato) [sarawillis@wentletrap bin]$ past-jobs -d 2

                      Jobs submitted by user sarawillis yesterday and today.                      

JobID    Start       User            JobName         Partition  Account    State       ExitCode
------------------------------------------------------------------------------------------------
296700   2022-03-31  sarawillis      interactive     standard   hpcteam    COMPLETED        0:0
296706   2022-03-31  sarawillis      test_exclus     standard   hpcteam    CANCELLED        0:0
296712   2022-03-31  sarawillis      interactive     standard   hpcteam    TIMEOUT          0:0
297690   2022-04-01  sarawillis      interactive     standard   hpcteam    COMPLETED        0:0
```

## ```job-history```
A simple wrapper for grabbing the history of completed and running jobs. 
```
(elgato) [sarawillis@wentletrap bin]$ job-history 296700

Job Overview
==================================================

Job Name             : interactive         
Job ID               : 296700              
Raw JobID            : 296700              
State                : COMPLETED
Exit Code            : 0:0                 
Derived Exit Code    : 0:0                 

Accounting
==================================================

User                 : sarawillis          
UID                  : 44571               
Account              : hpcteam             
Group                : hpcteam                         
Partition            : standard            
QOS                  : part_qos_standard   
Raw QOS              : 4                   
Priority             : 5004                

Time
==================================================

Time Limit           : 01:00:00            
Time Limit (Raw)     : 60                  
Time Elapsed         : 00:34:40            
Time Elapsed (raw)   : 2080                
CPU Time             : 00:34:40            
CPU Time (raw)       : 2080                
Submit Time          : 2022-03-31T12:47:51 
Eligible Time        : 2022-03-31T12:47:51 
Start Time           : 2022-03-31T12:47:52 
End Time             : 2022-03-31T13:22:32 

Resources*
==================================================

Cluster              : elgato              
Requsted Resources   : billing=1,cpu=1,mem=4G,node=1
Requested RAM        : 4G                  
Requested CPUs       : 1                   
Requested Nodes      : 1                   
Allocated Resources  : billing=1,cpu=1,mem=4G,node=1
Allocated Nodes      : 1                   
Allocated CPUs       : 1                   
Node List            : cpu37               

Files & Directories
==================================================

Working Directory    : /home/u21/sarawillis

Comments/Misc
==================================================

Flags                : SchedMain                       

* If there is a discrepancy between the resources you requested and the resources you were allocated, this may be due to memory requirements. See: https://public.confluence.arizona.edu/display/UAHPC/Compute+Resources#ComputeResources-ExampleResourceRequests
```

----------


# System Usage
## ```cluster-busy```
Developed for the HPC systems at the University of Arizona. This script allows users to query the average usage of each cluster. A highlighting option is available to view resource usage by partition using ```cluster-busy --partition=<partition_name>```. Example output for a single cluster:
```
====================================================================================================
                                                Puma                                                
====================================================================================================


                                             Resources                                              
____________________________________________________________________________________________________
Node Type            | Node Count | CPUs Total | CPUs Used | % Used | GPUs Total | GPUs Used | % Used
____________________________________________________________________________________________________
Standard             | 248        | 23808      | 22307     | 94.00% | N/A        | N/A       | N/A%  
GPU                  | 9          | 864        | 717       | 83.00% | 33         | 19        | 58.00%
HiMem                | 4          | 384        | 365       | 95.00% | N/A        | N/A       | N/A%  

                                             CPU Usage                                              
____________________________________________________________________________________________________
Standard:  [███████████████████████████████████████████████████████████████████████████░░░░░] (94.0%)
GPU     :  [██████████████████████████████████████████████████████████████████░░░░░░░░░░░░░░] (83.0%)
HiMem   :  [████████████████████████████████████████████████████████████████████████████░░░░] (95.0%)

                                             GPU Usage                                              
____________________________________________________________________________________________________
GPUs    :  [██████████████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] (58.0%)
```

## ```nodes-busy```
Developed for the HPC systems at University of Arizona. 
> Update: ```nodes-busy``` now runs in tests on: 
>   - [Bridges2](https://www.psc.edu/resources/bridges-2/user-guide-2/)
>   - [Expanse](https://www.sdsc.edu/services/hpc/expanse/)
>   - [Stampede2](https://portal.tacc.utexas.edu/user-guides/stampede2#introduction)
>   - [University of Arizona](https://public.confluence.arizona.edu/display/UAHPC)



https://user-images.githubusercontent.com/24305667/161330606-3f122a90-232a-4f9b-b614-63245204d263.mp4

### User Customization
It's now possible to customize this script to add node annotations, change the groupings/naming of node types, and add limits to the CPU display.

The header of the script describes how to do this:

```
Need to make some adjustments? Options exist here to add annotations to nodes

# Options described below with instructions

'''
Node Annotations:
----------------
Add annotations next to a specific node type. E.g., UArizona's system adds an annotation for 
buy-in nodes. The format for this should be a dictionary with the following entries:

{AnnotationDescription: {"Ascii Symbol": "symbol here", "UTF-8 Symbol": "symbol here", "Field": "scontrol field", "Value": "field value", "Message": "display message at bottom of output"}}

This will annotate specific nodes with something like (assuming ascii symbol = **):

NodeName1 [####   ] x% **
NodeName2 [####   ] x%
...
** Node annotation message

If annotations are not desired, set node_annotations = None
'''
global node_annotations
node_annotations = {"HiPri": {"Ascii Symbol":"*","UTF-8 Symbol":u'\u271A',"Field":"Partitions","Value":"windfall,high_priority","Message":"Buy-in nodes. Only accept high_priority and windfall jobs"},
                    }
'''
Node Types:
----------------
node_types allows you to separate nodes into clusters that are displayed together. It relies on finding 
a specified value in a "scontrol show nodes --all" field. 

These groupings also have a priority value associated with them. This priority controls how to sort nodes 
that have more than one node type. For example,
if a node was both a GPU node and buy-in, the priority value would determine whether that node was displayed in
the buy-in group or the gpu group. Higher priority values indicate higher group priority. In this case, based
on the configuration below, because buy-in nodes have priority 4 > gpu nodes priority 2, this node would be
displayed in the buy-in group. 

--> The first entry in the dictionary below ("Standard Nodes") should be kept, it is the default grouping for
all nodes. Additionally, the Field and Value entries should be kept None. However, the Name can be changed
which is what's displayed. GPU Nodes should also be kept since this is used for display purposes. The name 
Can be changed if desired.
'''
global node_types
node_types = {"Standard Nodes"    : {"Name" :"Standard Nodes"    ,"Field": None                  ,"Value":None                    ,"Priority":0},
              "GPU Nodes"         : {"Name" : "GPU Nodes"        ,"Field":["AllocTRES","CfgTRES"],"Value":"gpu"                   ,"Priority":2},
              "High Memory Nodes" : {"Name" : "High Memory Nodes","Field":"AvailableFeatures"    ,"Value":"hi_mem"                ,"Priority":3}
              }

'''
CPU Limits:
----------------
This was built into the script for University of Arizona's systems. We have nodes with 96 CPUs
where two are reserved for system use. This leaves 94 available for users to schedule. If there are
machines where fewer CPUs are schedulable than exist on the system, this variable's format should be:
cpu_limits = {physical_cpus1:schedulable_cpus1,physical_cpus2:schedulable_cpus2,...}
if this is not applicable, set cpu_limits to None.
'''
global cpu_limits
cpu_limits = {"96":"94"}
'''
```






## ```system-busy```
Provides a text-based summary of a cluster's usage.
```
(puma) [sarawillis@wentletrap nodes-busy-devel]$ system-busy

Tue Dec 07, 11:44:30 AM (MST) 2021

Total Number of Nodes      :        261
Total Number of Idle Nodes :         23

Total Number of Jobs       :       1227

Total Number of CPUs       :      25056
CPUs in Use                :      19377
Percent Utilization        :     77.33%

Standard Nodes
=================
Total Standard Nodes       :        248
Total Standard CPUs        :      23808
Standard CPUs In Use       :      18562
Percent Utilization        :     77.97%

GPU Nodes
=================
Total GPU Nodes            :          9
Total GPU CPUs             :        864
GPU CPUs In Use            :        479
Percent Utilization        :     55.44%

High Memory Nodes
=================
Total High Mem Nodes       :          4
Total High Mem CPUs        :        384
High Mem CPUs In Use       :        336
Percent Utilization        :      87.5%

Idle Nodes:
=================
r1u10n1,r1u17n1,r1u33n1,r1u33n2,r1u34n1,r1u34n2,r1u35n1,r1u35n2,r2u16n1,r2u30n2,r2u34n1,r3u06n2,r3u13n2,r3u14n1,r3u16n1,r3u17n1,r3u26n1,r3u26n2,r3u27n2,r3u31n2,r3u33n2,r3u35n1,r4u40n1
```



