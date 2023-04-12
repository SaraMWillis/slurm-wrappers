#!/usr/bin/env python3

import getopt, sys
from display.usage import usage
from display._version import *

'''
------------------------------------------------------------------------------------------
                                     Job Options
Parses flags. Flags determine what's displayed and how it's displayed. Recently added 
scale/width option. Some flags are mutually exclusive. These are described when running the
program using --help. 
'''
class Args:
    def __init__(self,argv):
        ERRORCOLOR="\033[0;31m"
        ENDCOLOR = "\033[0m"
        self.argv = argv
        
        self.partition=self.user=self.group=self.node=None
        self.all_nodes=self.color_random=self.use_ascii=self.scale=False
        self.scale_ratio=1
        try:
            opts,args = getopt.getopt(argv, "harvsw:p:u:n:g:",["help","all","version","randomize","ascii","partition=","user=","group=","node=","scale","width="])
            if len(opts) ==0:
                return
        except getopt.GetoptError:
            print(ERRORCOLOR+"Unrecognized Option"+ENDCOLOR)
            usage(1)
        for opt, arg in opts:
            if opt in ("-h","--help"):
                usage(0)
            elif opt in ("-v","--version"):
                print("Version    : "+version)
                print("Date       : "+date)
                print("Author     : "+author)
                print("Institution: "+institution)
                sys.exit(0)
            elif opt in ("-p","--partition"):
                self.partition = arg.lower()
            elif opt in ("-u","--user"):
                self.user = arg.lower() 
            elif opt in ("-n","--node"):
                self.node = arg.lower()
            elif opt in ("-a","--all"):
                self.all_nodes = True
            elif opt in ("-g","--group"):
                self.group = arg.lower()
            elif opt in ("-r","--randomize"):
                self.color_random = True
            elif opt == "--ascii":
                self.use_ascii=True
            elif opt in ("-s","--scale"):
                self.scale = True
                self.scaled_width=70
            elif opt in ("-w","--width"):
                try:
                    self.scale = True
                    self.scaled_width=int(arg)
                except ValueError:
                    print(ERRORCOLOR + "Width must be an integer"+ENDCOLOR)
                    usage(1)
            else:
                print(ERRORCOLOR+"Unrecognized option."+ENDCOLOR)
                usage(1)
        if [self.partition,self.user,self.group,self.node].count(None) < 3:
            print(ERRORCOLOR+"Too many options specified"+ENDCOLOR)
            usage(1)
        if self.node != None and self.scale == True:
            print(ERRORCOLOR+"Oops! Options --scale and --node are mutually exclusive. Please include one or the other"+ENDCOLOR)
            usage(1)