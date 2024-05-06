#!/usr/bin/env python3

import datetime, math

def print_header(vis,job_options):
    width = vis.width
    # Formats the current day/time into something that can be displayed nicely
    # The time_spacing is used to center the message.
    today = datetime.datetime.now()
    time_string = "%s"%today.strftime("%a %b %d, %I:%M:%S %p (MST) %G")
    time_string_length = len(time_string)
    time_spacing = math.ceil(width/2) - math.ceil(time_string_length/2)

    # Similar to above, heading_spacing is used to center the header string
    heading_string = " System Status "
    heading_spacing = math.ceil(width/2) - math.ceil((len(heading_string)+2)/2)
    
    if job_options.use_ascii == False:
        block = vis.utf8_char
    else:
        block = vis.ascii_char
        
    print("="*width)
    
    # if anything is wonky with the user's environment (e.g. the python encoding 
    # variable is set to use ascii, this will catch it. 
    try:
        print("\n"+" "*heading_spacing +  block + heading_string + block)
    except UnicodeEncodeError:
        block = vis.ascii_char
        job_options.use_ascii = True
        print("\n"+" "*heading_spacing +  block + heading_string + block)
        
    print(" "*time_spacing + time_string)
    print("="*width)
    return