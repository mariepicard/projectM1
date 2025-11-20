#! /usr/bin/env

import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("output/compression_stats.csv")
df_xz = df.query("Command == 'xz'")
df_gz = df.query("Command == 'gzip'")
fig, axs = plt.subplots(2)

axs[0].set_title("Time usage (s)")
axs[0].scatter(df_xz.param,df_xz["elapsed time(user)"], label="XZ time")
axs[0].scatter(df_gz.param,df_gz["elapsed time(user)"], label="GZIP time")
axs[0].set_xlabel("Quality parameter")
axs[0].set_ylabel("User time (s)")


axs[0].legend()


axs[1].set_title("Memory usage (B)")
axs[1].scatter(df_xz.param,df_xz["peak memory consumption"], label="XZ memory")
axs[1].scatter(df_gz.param,df_gz["peak memory consumption"], label="GZIP memory")
axs[0].set_xlabel("Quality parameter")
axs[0].set_ylabel("Peak memory usage (B)")
axs[1].legend()
plt.show()
