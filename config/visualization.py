#!/usr/bin/env python3

import random

'''
------------------------------------------------------------------------------------------
                                   Vis Options
******************************************************************************************
Contains colors and utf-8/ascii characters that are used in the output
'''
class VisOptions:
    def __init__(self,seed, use_ascii):
        
        # Seed option determines if display colors are randomized
        self.seed = seed
        self.use_ascii = use_ascii
        self.width = 0
        self.max_cpus= 0
        self.max_gpus=0
        self.valid_annotations = set({})

    # The different color options are for highlighting resources used by a 
    # group/user/partition, if requested. Additionally, nodes in the DOWN/DRAIN
    # state will be highlighted with the DOWNCOLOR.
    COLOR="\033[38;5;%dm"
    DOWNCOLOR="\033[0;31m"
    DOWNUSEDCOLOR=COLOR%int(181)
    ENDCOLOR="\033[0m"

    # Blocks used to display resource usage. Want to use a different utf-8 character?
    # https://www.w3schools.com/charsets/ref_utf_geometric.asp
    utf8_char = u'\u258B'
    ascii_char = '#'
    scale_utf8_char = u'\u2592'
    
    # A range of randomized colors is also generated for color-coding different jobs
    # if the "--node=nodename" option is given. This is generally deterministic, 
    # unless the --randomize flag is used. 
    def color_cycle(self):
        cycle = [self.COLOR%i for i in range(0,256)]
        if self.seed == None:
            random.seed(110)
        if self.seed != None:
            random.seed(seed)
        random.shuffle(cycle)
        return cycle