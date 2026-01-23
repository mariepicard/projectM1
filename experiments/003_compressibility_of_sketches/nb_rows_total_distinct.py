import numpy as np
import matplotlib.pyplot as plt

nb_rows = np.array([[1, 1, 1 , 1], #g, s, nb_rows_total, nb_rows_distinct
                    [1, 10, 10 , 1],
                    [1, 100, 100 , 1],
                    [1, 1000, 1000 , 1],
                    [1, 10000, 10000 , 1],
                    [10, 1, 2 , 2],
                    [10, 10, 12 , 5],
                    [10, 100, 125 , 31],
                    [10, 1000, 1223 , 119],
                    [10, 10000, 12150 , 315],
                    [100, 1, 2 , 2],
                    [100, 10, 13 , 9],
                    [100, 100, 161 , 93],
                    [100, 1000, 1538 , 577],
                    [100, 10000, 15029 , 3788],
                    [1000, 1, 3 , 3],
                    [1000, 10, 21 , 17],
                    [1000, 100, 249 , 192],
                    [1000, 1000, 2328 , 1379],
                    [1000, 10000, 22815 , 8983]])

fig, axs = plt.subplots(1, 2)
axs[0].set_title("number of total rows")
axs[1].set_title("number of distinct rows")
shapes = [':', '-', '--', '-.']
for i in range(4):
    lines = nb_rows[5*i:5*(i + 1),:]
    axs[0].plot(lines[:,1], lines[:,2], linestyle = shapes[i], label=f"g = {10**i}")
    axs[1].plot(lines[:,1], lines[:,3], linestyle = shapes[i], label=f"g = {10**i}")

for i in range(2):
    axs[i].legend()
    axs[i].set_xlabel("s")
    axs[i].set_ylabel("nb of rows")
    axs[i].set_xscale("log")
    axs[i].set_yscale("log")
    axs[i].set_ylim(0, 25000)

plt.tight_layout()
plt.show()
