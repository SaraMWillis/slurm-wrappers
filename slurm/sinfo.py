#!/usr/bin/env python3

import subprocess

'''
------------------------------------------------------------------------------------------
                                    Get Partitions
Get valid partitions available on the cluster
'''
def get_partitions():
    p = subprocess.Popen(['sinfo --federation --format=%R --noheader'],stdout=subprocess.PIPE,shell=True)
    out,err = p.communicate()
    if err != None and err.decode("utf-8",'ignore') != "":
        print("Oops, something has gone wrong! Error occured running:\n\t'sinfo --federation --format=%R --noheader'\nThis could be a problem with your SLURM setup. Exiting.")
        sys.exit(1)
    output = out.decode('utf-8','ignore').split("\n")
    partitions = [i for i in output if i != '']
    return partitions
