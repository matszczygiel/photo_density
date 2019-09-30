#!/usr/bin/python3
import numpy as np
from numpy.polynomial.legendre import legval

l_max = 39
dt = 0.025
dr = 0.1
nr = 1001
rskip = 5

ntheta = 200

dsnap = 40
snap_max=35000
file_pre = "wf-3e13/real_prop_wf_"
file_pos = ".dat"

out_file_pre = "density/density_"
out_file_pos = ".dat"

rr = np.linspace(0.0, dr * nr, nr, dtype=float)[::rskip]
rr[0] = 0.00001
th = np.linspace(0.0, np.pi, ntheta, dtype=float)

snaps = np.arange(0, snap_max+1,dsnap)


target_max_l = 2*l_max

for snap in range(snaps.size):
    filename = file_pre + str(snaps[snap]) + file_pos
    print("Loading raw data: " + filename)
    wf_data = np.empty((l_max+1, nr), dtype=complex)[:, ::rskip]
    data = np.loadtxt(filename)
    for l in range(l_max+1):
        wf_data[l, :] = (data[l*nr: (l+1)*nr, 0] + 1.0j*data[l*nr: (l+1)*nr, 1])[::rskip]
        wf_data[l, :] *= rr**(-1) * np.sqrt((2 *l + 1) / 4.0 / np.pi)


    target_data = np.abs(legval(np.cos(th), wf_data, tensor=True))**2
        
    out_file = out_file_pre + str(snaps[snap]) + out_file_pos
    np.savetxt(out_file, target_data)




        










