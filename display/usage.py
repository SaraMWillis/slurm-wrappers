#!/usr/bin/env python3

import sys
from slurm.sinfo import get_partitions

'''
------------------------------------------------------------------------------------------
                                      Usage
Only used to print the usage message. Exits with provided value after print
'''
def usage(exit_value):
    print("=============================================================================================")
    print("Usage: nodes-busy [--OPTION=VALUE|--VIS_OPTIONS|--help]")
    print("\nValid OPTION/VALUE combinations : Only one OPTION/VALUE can be specified")
    print("  --partiton=<partition*>       : Highlights all CPUs/GPUs reserved by specified partition")
    print("  --user=<netid>                : Highlights all CPUs/GPUs reserved by <netid>'s jobs")
    print("  --group=<gid>                 : Highlights all CPUs/GPUs reserved by <gid>'s jobs")
    print("  --node=<nodename>**           : Displays detailed usage of specified node")
    print("\nValid VIS_OPTIONS               : Optional. More than one can be selected")
    print("  --ascii                       : Use ascii encoding instead of utf-8. Can resolve formatting")
    print("                                : issues (e.g. in OOD terminals)")
    print("  --random                      : Just for fun, mix up the color display")
    print("  --all                         : Include all system nodes in --user and --group output")
    print("  --scale**                     : Scales node sizes down to 80 characters")
    print("  --width=<n>**                 : Scales node sizes to <n> characters")
    print("\n*Valid partitions: "+",".join(get_partitions())+"\n")
    print("**Scale/width options are mutually exclusive with --node option")
    sys.exit(exit_value)