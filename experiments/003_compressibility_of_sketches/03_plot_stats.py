#! /usr/bin/env python3

import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("presence_linear.csv")
fig, axs = plt.subplots(1, 2)
fig.tight_layout()
axs[0].set_title("Normalized cumulative Hamming distance")
axs[0].set_ylabel("$\delta/s$")

to_plot = [df["Normalized cumulative neighbouring distance"],
           4000/(2*(1+df["Normalized cumulative neighbouring distance"]))]

axs[1].set_title("Lower bound of compression ratio")
axs[1].set_ylabel("$\dfrac{|S|}{2(1+\delta/s)}$")

for i in range(2):
    axs[i].set_xlabel("s")
    axs[i].scatter(df.s, to_plot[i])
    #axs[i].set_xscale("log")
    axs[i].set_ylim(bottom=0, top=max(to_plot[i])*1.2)

plt.show()
