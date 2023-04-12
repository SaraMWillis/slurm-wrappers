#!/usr/bin/env python3

import subprocess

'''
------------------------------------------------------------------------------------------
                                   Get User Job IDs
If the --user option is supplied, that user's job IDs are pulled and returned as a list
'''
def get_user_jobids(username,group):
    user_job_data = []
    if username != None:
        p = subprocess.Popen(['squeue --noheader --states=RUNNING -o %A --user '+username],stdout=subprocess.PIPE, shell=True)
    elif group != None:
        p = subprocess.Popen(['squeue --noheader --states=RUNNING -o %A --account '+group],stdout=subprocess.PIPE, shell=True)
    out,err = p.communicate()
    user_jobs = out.decode('utf-8','ignore').split("\n")
    for job in user_jobs:
        formatted_job = [i for i in job.split(" ") if i != ""]
        if len(formatted_job) != 0:
            JobID = formatted_job[0]
            Job_Components = JobID.split("_")
            Job_Base = Job_Components[0]
            try:
                # IDs are reformatted in the event of job arrays
                Job_indices = Job_Components[1].replace("[","").replace("]","")
                Indices_boundaries = Job_indices.split("-")
                Full_indices = range(int(Indices_boundaries[0]),int(Indices_boundaries[1])+1)
                for index in Full_indices:
                    Full_job_id = Job_Base+"_"+str(index)
                    user_job_data.append(Full_job_id)
            except IndexError:
                user_job_data.append(JobID)
    return user_job_data