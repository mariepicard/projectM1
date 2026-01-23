#! /usr/bin/env python3

import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("presence_linear.csv")
delta = df["Normalized cumulative neighbouring distance"]

nb_sketches = 4000

fig, axs = plt.subplots(1, 2)
axs[0].set_title("Normalized cumulative Hamming distance")
axs[0].set_ylabel("$\delta/s$")
axs[0].scatter(df.s, delta)


axs[1].set_title("Estimation of compression ratio RLE")
axs[1].set_ylabel("Compression ratio")
axs[1].plot(df.s, nb_sketches/(2*(1 + delta)), linestyle="--", label="lower bound : $\dfrac{|S|}{2(1+\delta/s)}$")
axs[1].plot(df.s, nb_sketches/delta, linestyle=":",label="higher bound : $\dfrac{|S|}{\delta / s}$")
axs[1].legend()
axs[1].set_ylim(0,85)



for i in range(2):
    axs[i].set_xlabel("s")
    
    #axs[i].set_xscale("log")
    axs[i].set_ylim(bottom=0)

plt.show()
