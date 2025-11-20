#! /usr/bin/env python3

import numpy as np
import pandas as pd
import os
import glob
from scipy.spatial.distance import hamming
import json
#from sklearn.metrics.pairwise import pairwise_distances

        
def extract_hashes_from_json(filename):
    df = pd.read_json(filename)
    return df.sketches[0]["hashes"]

inputs = [f for f in glob.glob('json_files/*')]

hashes = [extract_hashes_from_json(filename) for filename in inputs]
s = len(hashes[0])
all_hashes = list(set().union(*hashes))
M = np.array([[1 if elem in lst else 0 for elem in all_hashes]
        for lst in hashes])
#pairdistances = pairwise_distances(M, M, hamming)
distances = np.array([hamming(M[i],M[i + 1]) for i in range(len(M) - 1)])

print(f"{s},{(s/len(all_hashes))**2}, {np.sum(distances)/s}")
np.save(f"matrices/presence_matrix_{s}.npy", M)
with open(f"matrices/union_sketches_{s}.json", 'w') as f:
    json.dump(all_hashes, f)
