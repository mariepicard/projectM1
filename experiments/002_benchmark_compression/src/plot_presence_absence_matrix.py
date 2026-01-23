#! /usr/bin/env python3

import numpy as np
import pandas as pd
import os
import glob
import json
import heapq
import matplotlib.pyplot as plt
import sys

colors=[[255, 89, 94],
        [255, 202, 58],
        [138, 201, 38],
        [25, 130, 196],
        [106, 76, 147]]
c = len(colors)

def usage():
    print(f"\t Usage : {sys.argv[0]} <directory in json_files_subs> [mode='no plot' | 'bw' | 'colored']", file=sys.stderr)
    sys.exit(1)

def sorted_union(lists):
    merged = heapq.merge(*lists)
    result = []

    prev = object()
    for x in merged:
        if x != prev:
            result.append(x)
            prev = x

    return result

def extract_hashes_from_json(filename):
    df = pd.read_json(filename)
    return list(df.sketches[0]["hashes"])

def delta_i(i):
    return np.sum((M[:,i] - M[:,i + 1])**2)/2

def color(elt, lst):
    try :
        return colors[lst.index(elt) % c]
    except ValueError:
        return [255, 255, 255]
        

sdir = ""
inputs=[]
colored = False
plot=False
try :
    sdir = sys.argv[1]
    inputs = sorted([f for f in glob.glob(f'json_files_sub/{sdir}/*')])

    if len(sys.argv) == 3:
        if sys.argv[2] == 'colored':
            plot = True
            colored = True
        elif sys.argv[2] == 'bw':
            plot = True

except:
    usage()

hashes = [extract_hashes_from_json(filename) for filename in inputs]
s = len(hashes[0])
all_hashes = sorted_union(hashes)
if colored:
    M = np.array([[color(elem, lst) for lst in hashes] for elem in all_hashes], dtype=int)
else :
    M = np.array([[not elem in lst for lst in hashes] for elem in all_hashes], dtype=int)
    i_range = np.arange(len(M[0]) - 1)
    cumulative_distance = delta_i(i_range)
    print(f"{s},{s/len(all_hashes)}, {cumulative_distance/s}")
    M = np.array([[[c, c, c] for c in row] for row in M], dtype=float)
    
if plot:
    plt.title(f"Presence-absence matrix for {sdir} - {len(hashes)} sketches - s = {s}")
    plt.xlabel("sketch")
    plt.ylabel("hash")
    plt.imshow(M)
    plt.show()



#np.save(f"presence_matrix_{s}.npy", M)
with open(f"union_sketches_s{s}_S_{len(all_hashes)}.json", 'w') as f:
    json.dump(all_hashes, f)

