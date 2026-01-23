#! /usr/bin/env python

import json
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import glob

intsz=64

def usage():
    print(f"Usage : \n\t{sys.argv[0]} <json_filename>", file=sys.stderr)
    sys.exit(1)

if len(sys.argv) != 2:
    usage()

filename = sys.argv[1]
lst_s = [1, 10, 100, 1000, 10000]
lst_sz = []
try :
    with open(filename, 'r') as file:
        data = json.load(file)
        mx = data[-1]
        n = len(data)
        elias_fano_sz = math.ceil((2*n + n*(math.log2(mx/n)))/8)
        og_sz = n*intsz/8
        lst_sz.append(og_sz/elias_fano_sz)
        print(f"Elias Fano size : {elias_fano_sz} B")
        print(f"Compression rate : {og_sz/elias_fano_sz}")
        M = np.zeros((intsz, n))
        for i in range(n):
            hsh = data[i]
            for j in range(intsz):
                M[intsz-1-j][i] = 1 - hsh%2
                hsh = hsh//2
        img = np.array([[[M[i,j], M[i,j], M[i,j]] for i in range(len(M))] for j in range(len(M[0]))])
        plt.xlabel("Bit in the hash (high-order bits left, low-order bits right)")
        plt.ylabel("hash")
        plt.title(f"{Path(filename).stem}")
        plt.imshow(img, interpolation='nearest')
        plt.axvline(x=(intsz -0.5 - math.ceil(math.log2(mx)) + math.ceil(math.log2(n))), color='r', label="limit between high and low entropy bits", linewidth=5.0)
        #plt.legend()
        plt.show()

except FileNotFoundError:
    print(f"Error : {filename} was not found", sys.stderr)
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error : {filename} is ill-formed - could not be decoded", sys.stderr)
    sys.exit(1)
