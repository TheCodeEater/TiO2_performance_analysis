import matplotlib.pyplot as plt
import numpy as np
import constants as c
from glob import glob
import procedures as proc
import re
import scipy as sp

#Set smoothing
doSmooth=True
#Set origin position
zeroToObserver=True

#Load data - Both light and dark
#IV curve for each potential
dark_dataset = []
light_dataset = []

junk = []

#Load light current density data
for file in proc.get_sorted_filenames(c.FILEPATH_OCP_LIGHT):
    junk, voltage=np.loadtxt(file,skiprows=1,unpack=True)
    light_dataset.append(voltage)

#Load dark current density data
for file in proc.get_sorted_filenames(c.FILEPATH_OCP_DARK):
    junk,  voltage=np.loadtxt(file,skiprows=1,unpack=True)
    dark_dataset.append(voltage)

#Compute differences

count=0
cd_mat = np.zeros((8,8))

X,Y,cd_mat=proc.deltaAverageOCP(light_dataset,dark_dataset)


cd_mat=np.transpose(cd_mat) # Fix orientation of matrix
Z=cd_mat
#Reflect

# Assign colors based on value (interpolation between maximum and minimum hue, fixed brightness and saturation)
# Create image
fig, ax = plt.subplots(1,2,subplot_kw={"projection": "3d"},figsize=(10,6))
plots=ax.flatten()


#Smooth the dataset
#interpolate the matrix along a finer lattice
X,Y,Z=proc.smoothMatrix(X,Y,Z)

#Plot surface

surf = plots[0].plot_surface(X,Y,Z, cmap="gnuplot",
                       linewidth=0, antialiased=True)
ax[0].set(xlabel="X",ylabel="Y")

#Plot contour
surf2 = ax[1].contour(X,Y,Z, 100,cmap="gnuplot", antialiased=True)
ax[1].set(xlabel="X",ylabel="Y")

plt.suptitle("OCP photovoltage map (average)")
#plt.colorbar(label="mA/$cm^2$")

plt.savefig("../Artifacts/ocp_voltage_delta/OCP_dV_3D_{}.png".format(proc.current_time()))
plt.show()
