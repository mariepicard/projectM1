#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import subprocess


lst_s = [10**k for k in range(5)]
lst_g = [10**k for k in range(4)]

ratios_lst = np.zeros((len(lst_g), len(lst_s)))
for i in range(len(lst_g)):
    for j in range(len(lst_s)):
        g = lst_g[i]
        s = lst_s[j]
        subprocess.run(["src/sub_matrix.sh", "inputs/part_54/neisseria_gonorrhoeae__01", str(g), str(s)], check=True)
        subprocess.run(["src/presence_matrix.py", f"json_files_sub/s{s}_g{g}"], check=True)
        M = np.load(f"matrices/presence_matrix_s{s}_g{g}.npy")
        no_redundancy = np.unique(M, axis=1)
        print(f"g = {g}, s = {s}, {len(M[0])} rows total, {len(no_redundancy[0])} distinct rows")
        np.savez(f"matrices/no_redundancy_{s}.npz", no_redundancy)
        ratios_lst[i][j] = np.round(len(no_redundancy[0])/len(M[0]), decimals=3)

fig, ax = plt.subplots()
im = ax.imshow(ratios_lst)

# Show all ticks and label them with the respective list entries
ax.set_xticks(range(len(lst_s)), labels=lst_s,
              rotation=45, ha="right", rotation_mode="anchor")
ax.set_yticks(range(len(lst_g)), labels=lst_g)

# Loop over data dimensions and create text annotations.
for i in range(len(lst_g)):
    for j in range(len(lst_s)):
        text = ax.text(j, i, ratios_lst[i, j],
                       ha="center", va="center", color=("w" if ratios_lst[i, j] < 0.5 else "black"))

ax.set_title("Ratio of distinct rows per total nb of rows")
ax.set_xlabel("s")
ax.set_ylabel("g")
fig.tight_layout()
plt.show()

"""

plt.plot(lst_s, ratios)
plt.title("Ratio of distinct rows")
plt.xlabel("s")
plt.ylabel("nb of distinct rows / total nb of rows")
plt.xscale("log")
plt.ylim(0, 1)
plt.show()
"""
