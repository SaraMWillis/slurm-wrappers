# SLURM Wrappers


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






