#!/usr/bin/env python3

import subprocess, json, time, datetime
from statistics import mean

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
    
    
    
'''
------------------------------------------------------------------------------------------
                                   Get User Job IDs
If the --user option is supplied, that user's job IDs are pulled and returned as a list
'''

def pending_job_statistics(system_summary_dict,system_specifications,job_state="PENDING"):
    
    search_value = {}
    exclude_reason_codes = ["Dependency","AssocGrpGRES","AssocGrpCPUMinutesLimit","QOSGrpCPUMinutesLimit","AssocGrpMemLimit","AssocGrpCpuLimit"]
    #exclude_reason_codes = []
    
    pending_jobs = {"Total":{"Count":0,"Times":[]}}
    for ntype, specs in system_specifications["node_types"].items():
        pending_jobs[ntype] = {"Count":0,"Times":[]}
        if ntype == "Standard Nodes":
            pass
        elif ntype =="GPU Nodes":
            search_value[specs["squeue Field"]] = {"Values":specs["GPU Values"].keys(),"NType":ntype}
        else:
            search_value[specs["squeue Field"]] = {"Values":specs["squeue Values"],"NType":ntype}
        
        
    current_timestamp = int(time.time())
    
    p = subprocess.Popen(["squeue --json"],stdout=subprocess.PIPE,shell=True)
    out,err = p.communicate()
    output = out.decode('utf-8','ignore')
    jobs_dict = json.loads(output)
    

    for job in jobs_dict["jobs"]:
        #print(job["billable_tres"],job["tres_req_str"],job["partition"])
        cpu_count = int(job["tres_req_str"].split("billing=")[-1].split(",")[0])
        partition=job["partition"]
        if partition not in pending_jobs["Total"].keys():
            pending_jobs["Total"][partition] = {"Count":0,"1_to_10":[],"11_to_50":[],"51_to_100":[],"101_to_1000":[],"1000+":[]} 
        if job["job_state"] == job_state:
            pending_jobs["Total"]["Count"] += 1
            pending_jobs["Total"][partition]["Count"] += 1
            if job["state_reason"] not in exclude_reason_codes:
                pending_jobs["Total"]["Times"].append(current_timestamp - job["submit_time"])
                pending_jobs["Total"][partition]["Count"]+=1
                if cpu_count < 11:
                    pending_jobs["Total"][partition]["1_to_10"].append(current_timestamp - job["submit_time"])
                elif cpu_count >= 11 and cpu_count < 51:
                    pending_jobs["Total"][partition]["11_to_50"].append(current_timestamp - job["submit_time"])
                elif cpu_count >= 51 and cpu_count < 101:
                    pending_jobs["Total"][partition]["51_to_100"].append(current_timestamp - job["submit_time"])
                elif cpu_count >= 101 and cpu_count < 1001:
                    pending_jobs["Total"][partition]["101_to_1000"].append(current_timestamp - job["submit_time"])
                elif cpu_count >= 1001:
                    pending_jobs["Total"][partition]["1000+"].append(current_timestamp - job["submit_time"])


            found=False
            for f,v in search_value.items():
                if job[f] in v["Values"]:
                    if partition not in pending_jobs[v["NType"]].keys():
                        pending_jobs[v["NType"]][partition] = {"Count":0,"1_to_10":[],"11_to_50":[],"51_to_100":[],"101_to_1000":[],"1000+":[]} 
                    pending_jobs[v["NType"]]["Count"] +=1
                    pending_jobs[v["NType"]][partition]["Count"] +=1 
                    if job["state_reason"] not in exclude_reason_codes:
                        pending_jobs[v["NType"]]['Times'].append(current_timestamp - job["submit_time"])
                        if cpu_count < 11:
                            pending_jobs[v["NType"]][partition]["1_to_10"].append(current_timestamp - job["submit_time"])
                        elif cpu_count >= 11 and cpu_count < 51:
                            pending_jobs[v["NType"]][partition]["11_to_50"].append(current_timestamp - job["submit_time"])
                        elif cpu_count >= 51 and cpu_count < 101:
                            pending_jobs[v["NType"]][partition]["51_to_100"].append(current_timestamp - job["submit_time"])
                        elif cpu_count >= 101 and cpu_count < 1001:
                            pending_jobs[v["NType"]][partition]["101_to_1000"].append(current_timestamp - job["submit_time"])
                        elif cpu_count >= 1001:
                            pending_jobs[v["NType"]][partition]["1000+"].append(current_timestamp - job["submit_time"])
                    found=True
                else:
                    pass
            if found == False:
                pending_jobs["Standard Nodes"]["Count"] +=1 
                pending_jobs["Standard Nodes"]["Times"].append(current_timestamp - job["submit_time"])


    for ntype,data in pending_jobs.items():
        if len(data['Times']) ==0:
            avg_pending = "N/A"
            data["Average Wait"] = avg_pending

        else:
            avg_pending = mean(data["Times"])
            td = datetime.timedelta(seconds=int(avg_pending))
            data["Average Wait"] = td
            data.pop("Times")
            for p,d in data.items():
                if p not in ["Count","Average Wait"]:
                    avg_1_to_10 = datetime.timedelta(seconds=int(mean(d["1_to_10"]))) if len(d["1_to_10"]) >0 else "N/A"
                    d["1_to_10"] = avg_1_to_10
                    avg_11_to_50 = datetime.timedelta(seconds=int(mean(d["11_to_50"]))) if len(d["11_to_50"]) >0 else "N/A"
                    d["11_to_50"] = avg_11_to_50 
                    avg_51_to_100 = datetime.timedelta(seconds=int(mean(d["51_to_100"]))) if len(d["51_to_100"]) >0 else "N/A"
                    d["51_to_100"] = avg_51_to_100
                    avg_101_to_1000 = datetime.timedelta(seconds=int(mean(d["101_to_1000"]))) if len(d["101_to_1000"]) >0 else "N/A"
                    d["101_to_1000"] = avg_101_to_1000
                    avg_1000_plus = datetime.timedelta(seconds=int(mean(d["1000+"]))) if len(d["1000+"]) >0 else "N/A"
                    d["1000+"] = avg_1000_plus
    del jobs_dict
    
    return pending_jobs

    
