#!/usr/bin/env python3

import sys, os
from slurm.sinfo import get_partitions

'''
------------------------------------------------------------------------------------------
                                      Usage
Only used to print the usage message. Exits with provided value after print
'''
def usage(exit_value):
    command = sys.argv[0]
    print("=============================================================================================")
    print("Usage: %s [--option[=value]]"%command)
    print("\nValid option/value combinations   : Only one OPTION/VALUE can be specified")
    print("  --partiton=<partition*>         : Highlights all CPUs/GPUs reserved by specified partition")
    print("  --user=<netid>                  : Highlights all CPUs/GPUs reserved by <netid>'s jobs")
    print("  --group=<gid>                   : Highlights all CPUs/GPUs reserved by <gid>'s jobs")
    print("  --node=<nodename>**             : Displays detailed usage of specified node")
    print("\nVisualization options             : Optional. More than one can be selected")
    print("  --ascii                         : Use ascii encoding instead of utf-8. Can resolve formatting")
    print("                                  : issues (e.g. in OOD terminals)")
    print("  --text                          : Display nodes-busy information as a text summary")
    print("  --random                        : Just for fun, mix up the color display")
    print("  --all                           : Include all system nodes in --user and --group output")
    print("  --scale                         : Scales node sizes down to 80 characters")
    print("  --width=<n>                     : Scales node sizes to <n> characters")
    print("\nInfo")
    print("  --help                          : Display this message")
    print("  --version                       : Display version number")
    print("\n*Valid partitions: "+",".join(get_partitions())+"\n")
    sys.exit(exit_value)
    
def short_usage(message,exit_value):
    print("\n"+ message)
    print("\nFor help, use %s")