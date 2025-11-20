#! /usr/bin/env python3
import matplotlib.pyplot as plt
import pandas as pd
import sys

args = sys.argv

if len(args) != 4 :
    sys.exit("Incorrect number of arguments")

path=args[1]
label=args[2]
title = args[3]

original_file_sizes = pd.read_csv(path+"/sketch_file_sizes.csv")

fig, axs = plt.subplots(1, 2)
fig.suptitle(title)
axs[0].set_title("XZ compression ratio")
axs[1].set_title("GZIP compression ratio")
for i in range(2):
    axs[i].set_xlabel("Preset")
    axs[i].set_ylabel("Compression ratio")
    axs[i].set_ylim(0,85)

for _,row in original_file_sizes.iterrows():
    l = row[label]
    og_mem = row["size"]
    mem_l = pd.read_csv(path+"/memory_"+str(l)+".csv")
    quality = mem_l.preset
    axs[0].scatter(quality, og_mem/mem_l["XZ memory usage"], label=f"{label} = {l}")
    axs[1].scatter(quality, og_mem/mem_l["GZIP memory usage"], label=f"{label} = {l}")
axs[0].legend()
axs[1].legend()
plt.show()
