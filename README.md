# SLURM Wrappers

> **⚠ Warning **  
> These scripts were developed for the University of Arizona's HPC center so some pieces may be specific to our setup. These cases are being worked on to make the scripts more customizable/portable.
> Update: nodes-busy now runs in tests on [Bridges2](https://www.psc.edu/resources/bridges-2/user-guide-2/)

## Executables

### Jobs
#### ```job-history```
A simple wrapper for grabbing data for completed and running jobs.

----------


### System Usage
#### ```cluster-busy```
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

#### ```nodes-busy```
Developed for the HPC systems at University of Arizona. High memory nodes are differentiated from standard nodes with ```AvailableFeatures=hi_mem```.

https://user-images.githubusercontent.com/24305667/142665361-8bfcc98a-d9e9-4f78-83ee-760123645927.mp4


#### ```system-busy```
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



