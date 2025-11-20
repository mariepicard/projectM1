#! /usr/bin/env python3

import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("presence_base10.csv")
fig, axs = plt.subplots(1, 2)
axs[0].set_title("Evolution of normalized cumulative Hamming distance")
axs[0].set_ylabel("$\delta/s$")
axs[0].scatter(df.s, df["Normalized cumulative neighbouring distance"]/2)

axs[1].set_title("Lower bound of compression ratio")
axs[1].set_ylabel("$\dfrac{|S|}{2(1+\delta/s)}$")
axs[1].scatter(df.s, 4000/(2*(1+df["Normalized cumulative neighbouring distance"]/2)))

for i in range(2):
    axs[i].set_xlabel("s")
    axs[i].set_xscale("log")
    axs[i].set_yscale("log")

plt.show()
