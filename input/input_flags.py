#!/usr/bin/env python3

import getopt, sys, shutil, os, yaml
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
    def __init__(self,argv,formatting_specifications):
    
        #script_dir = os.path.dirname(os.path.abspath(__file__))
        #yml_file = os.path.join(script_dir,"../config/output_formatting.yml")
        #yml_file = "../config/output_formatting.yml"
        
        #with open(yml_file, 'r') as file:
        #    formatting_specifications = yaml.safe_load(file)
            
            
        ERRORCOLOR=bytes(formatting_specifications["Color"]["Error Color"], 'utf-8').decode('unicode-escape')


        ENDCOLOR = formatting_specifications["Color"]["No Color"].encode().decode('unicode-escape')
        
        if (formatting_specifications["Scaling"]["Auto-Scale"] in (True,False)) == False:
            print(ERRORCOLOR+"Auto-Scale value in formatting configuration file is not True/False.\nAuto-Scale = %s\nPlease check the following file: %s"%(formatting_specifications["Scaling"]["Auto-Scale"],yml_file)+ENDCOLOR)
            sys.exit(1)
        else:
            MAXWIDTH=int(formatting_specifications["Scaling"]["Max Width"])
            self.TERMINAL_WIDTH=shutil.get_terminal_size().columns
            self.scale = formatting_specifications["Scaling"]["Auto-Scale"]
            self.scale_ratio=1
            if self.TERMINAL_WIDTH < MAXWIDTH:
                self.scaled_width=self.TERMINAL_WIDTH - 50
            else:
                self.scaled_width = MAXWIDTH - 50
            if self.scaled_width < 10:
                self.scaled_width = 10

        self.argv = argv
        
        self.partition=self.user=self.group=self.node=None
        self.all_nodes=self.color_random=self.use_ascii=False
        
        # Default behavior is to display a visual of all the nodes on the system. 
        self.display_all = True
        self.single_node = False
        self.text        = False
        self.summary     = False
        

        try:
            opts,args = getopt.getopt(argv, "harvtsw:p:u:n:g:",["help","all","version","randomize","ascii","summary","text","partition=","user=","group=","node=","no-scale","scale","width="])
            if len(opts) ==0:
                return
        except getopt.GetoptError:
            print(ERRORCOLOR+"Unrecognized Option"+ENDCOLOR)
            usage(1)
        if "--scale" in [i[0] for i in opts] and "--no-scale" in [i[0] for i in opts]:
            print(ERRORCOLOR+"The use of --scale and --no-scale are mutually exclusive. Please choose only one option." + ENDCOLOR)
            sys.exit(1)

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
                self.single_node = True
                self.display_all = False
                self.scale=False
                self.node = arg.lower()
            elif opt in ("-a","--all"):
                self.all_nodes = True
            elif opt in ("-g","--group"):
                self.group = arg.lower()
            elif opt in ("-r","--randomize"):
                self.color_random = True
            elif opt == "--ascii":
                self.use_ascii=True
            elif opt in ("--no-scale"):
                self.scale = False
            elif opt in ("-s","--scale"):
                self.scale = True
            elif opt in ("-t","--text"):
                self.text = True
                self.display_all = False
            elif opt in ("--summary"):
                self.summary = True
                self.display_all = False
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
        if [self.display_all, self.single_node, self.text, self.summary].count(True) > 1:
            print(ERRORCOLOR + "Too many options specified."+ ENDCOLOR)
            usage(1)
        if self.node != None and self.scale == True:
            print(ERRORCOLOR+"Oops! Options --scale and --node are mutually exclusive. Please include one or the other"+ENDCOLOR)
            usage(1)