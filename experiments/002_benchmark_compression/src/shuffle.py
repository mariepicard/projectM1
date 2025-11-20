#! /usr/bin/env python3

import os
import random
import sys

args = sys.argv

if len(args) == 3 or len(args) == 2:

    directory = args[1]
    unique_identifier = 0
    if len(args) == 3:
        unique_identifier = args[2]
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    random.shuffle(files)

    for idx, filename in enumerate(files):
        name, ext = os.path.splitext(filename)
        new_name = f"shuffled_{unique_identifier}_{idx:06d}{ext}"
        
        src = os.path.join(directory, filename)
        dst = os.path.join(directory, new_name)
        
        os.rename(src, dst)
else :
    print (f"Usage : {args[0]} <path_to_directory> [identifier=0]")
