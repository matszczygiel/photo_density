#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, ticker


resolution=200

l_max = 39
dt = 0.025
dr = 0.1
nr = 1001
rskip = 5
rcap = 67.4

ntheta = 200

dsnap = 40
snap_max=35000

file_pre = "density/density_"
file_pos = ".dat"

out_file_pre = "snaps/snap_t_"
out_file_pos = ".png"


rr = np.linspace(0.0, dr * nr, nr, dtype=float)[::rskip][1:]
th = np.linspace(0.0, np.pi, ntheta, dtype=float)

snaps = np.arange(0, snap_max+1,dsnap)

loactor = ticker.LogLocator(numticks=400)
colormap = cm.jet

clim  = (10**(-50), 10**(-1))

for snap in range(snaps.size):
    filename = file_pre + str(snaps[snap]) + file_pos
    print("Loading density data: " + filename)
    dens_data = np.loadtxt(filename)[1:, :]

#-- Plot... ------------------------------------------------
    plt.clf()
    axs = plt.subplot(111, polar=True)
    axs.set_rticks([rcap])    
    axs.set_thetagrids([0, 90, 180, 270])
    p = axs.contourf(th, rr, dens_data, 100, locator=loactor, cmap=colormap)
    p.set_clim(clim)
    p = axs.contourf(np.full(th.shape, 2*np.pi)-th, rr, dens_data, 100, locator=loactor, cmap=colormap)
    p.set_clim(clim)
    cbar = plt.colorbar(p, ax=axs)
    
    out_file = out_file_pre + str(int(dt*snaps[snap])*10).zfill(6) + out_file_pos
    plt.title("t = " + str((dt*snaps[snap])).zfill(5) + " au")
    plt.savefig(out_file, dpi=resolution)
