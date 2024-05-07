# Slurm Wrappers

> Updated on 04/12/2023 to have a more modular setup. More updates coming.


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

## ```nodes-busy```
Developed for the HPC systems at University of Arizona. 
> Update: ```nodes-busy``` now runs in tests on: 
>   - [Bridges2](https://www.psc.edu/resources/bridges-2/user-guide-2/)
>   - [Expanse](https://www.sdsc.edu/services/hpc/expanse/)
>   - [Stampede2](https://portal.tacc.utexas.edu/user-guides/stampede2#introduction)
>   - [University of Arizona](https://public.confluence.arizona.edu/display/UAHPC)



https://user-images.githubusercontent.com/24305667/161330606-3f122a90-232a-4f9b-b614-63245204d263.mp4

### User Customization

```






