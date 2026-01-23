#! /usr/bin/env python3

import numpy as np
import pandas as pd
import os
import sys
import glob
import json
import heapq

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
    return np.sum((M[i] - M[i + 1])**2)/2

input_dir = "json_files"
if len(sys.argv) > 1:
    input_dir = sys.argv[1]

inputs = sorted([f for f in glob.glob(input_dir + '/*')])

hashes = [extract_hashes_from_json(filename) for filename in inputs]
s = len(hashes[0])
all_hashes = sorted_union(hashes)
M = np.array([[elem in lst for elem in all_hashes]
        for lst in hashes], dtype=bool)
#pairdistances = pairwise_distances(M, M, hamming)
i_range = np.arange(len(M) -1)
"""
cumulative_distance = delta_i(i_range)

print(f"{s},{s/len(all_hashes)}, {cumulative_distance/s}")
"""
np.save(f"matrices/presence_matrix_s{s}_g{len(inputs)}.npy", M)
with open(f"matrices/union_sketches_s{s}_g{len(inputs)}.json", 'w') as f:
    json.dump(all_hashes, f)
