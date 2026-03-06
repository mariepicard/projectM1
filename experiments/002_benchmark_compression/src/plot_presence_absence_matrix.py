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

def delta_i(M, i):
    return np.sum((M[:,i] - M[:,i + 1])**2)/2

def color(elt, lst):
    try :
        return colors[lst.index(elt) % c]
    except ValueError:
        return [255, 255, 255]

def split_matrix(M):
    M_dense = []
    M_sparse = []
    for row in M:
        if np.count_nonzero(row) > len(row)//2:
            M_dense.append(row)
        else:
            M_sparse.append(row)
    return np.array(M_dense), np.array(M_sparse)
        

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

with open("output_file.csv", "w") as output_file:
    s = len(hashes[0])
    all_hashes = sorted_union(hashes)
    if colored:
        M = np.array([[color(elem, lst) for lst in hashes] for elem in all_hashes], dtype=int)
    else :
        M = np.array([[not elem in lst for lst in hashes] for elem in all_hashes], dtype=int)
        # split matrix
        M_dense, M_sparse = split_matrix(M)

        # re-normal
        i_range = np.arange(len(M[0]) - 1)

        print(f"{s}, {s/len(all_hashes)}, {1 - np.count_nonzero(M_dense)/(len(M_dense)*len(M_dense[0]))}, {1 - np.count_nonzero(M_sparse)/(len(M_sparse)*len(M_sparse[0]))}", file=output_file)
        """

        print(f"Sparse matrix : delta = {delta_i(M_dense, i_range)} \n density = {1 - np.count_nonzero(M_dense)/(len(M_dense)*len(M_dense[0]))}")
        print(f"Dense matrix : delta = {delta_i(M_sparse, i_range)} \n density = {1 - np.count_nonzero(M_sparse)/(len(M_sparse)*len(M_sparse[0]))}")
              
        cumulative_distance = delta_i(M, i_range)
        print(f"{s},{s/len(all_hashes)}, {cumulative_distance}")
        M = np.array([[[c, c, c] for c in row] for row in M], dtype=float)
        """
    
if plot:
    plt.style.use('grayscale')
    fig, axs = plt.subplots(1, 3)
    fig.suptitle(sdir)
    axs[0].set_title("full matrix")
    axs[0].matshow(M)
    axs[1].set_title("sparse half")
    axs[1].matshow(M_dense)
    axs[2].set_title("dense half")
    axs[2].matshow(M_sparse)

    plt.show()
    
    plt.title(f"Presence-absence matrix for {sdir} - {len(hashes)} sketches - s = {s}")
    plt.xlabel("sketch")
    plt.ylabel("hash")
    plt.imshow(M)
    plt.show()



#np.save(f"presence_matrix_{s}.npy", M)
with open(f"union_sketches_s{s}_S_{len(all_hashes)}.json", 'w') as f:
    json.dump(all_hashes, f)

