#! /usr/bin/env python3

import numpy as np
import pandas as pd
import os
import glob
import json

def extract_hashes_from_json(filename):
    df = pd.read_json(filename)
    return set(df.sketches[0]["hashes"])

def delta_i(i):
    return np.sum((M[i] - M[i + 1])**2)/2

inputs = sorted([f for f in glob.glob('json_files/*')])

hashes = [extract_hashes_from_json(filename) for filename in inputs]
s = len(hashes[0])
all_hashes = list(set().union(*hashes))
M = np.array([[1 if elem in lst else 0 for elem in all_hashes]
        for lst in hashes], dtype=int)
#pairdistances = pairwise_distances(M, M, hamming)
i_range = np.arange(len(M) -1)
cumulative_distance = delta_i(i_range)

print(f"{s},{s/len(all_hashes)}, {cumulative_distance/s}")
np.save(f"matrices/presence_matrix_{s}.npy", M)
with open(f"matrices/union_sketches_{s}.json", 'w') as f:
    json.dump(all_hashes, f)
