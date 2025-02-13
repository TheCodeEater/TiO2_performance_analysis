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

for light,dark in zip(light_dataset,dark_dataset):
    voltage_light=np.average(light)
    voltage_dark=np.average(dark)

    #Compute current density difference. this is the photocurrent
    photovoltage=voltage_light-voltage_dark

    #Arrange data in a matrix
    pos=proc.getxy(count)
    cd_mat[pos]=photovoltage

    count+=1

cd_mat=np.transpose(cd_mat) # Fix orientation of matrix
#Reflect

# Assign colors based on value (interpolation between maximum and minimum hue, fixed brightness and saturation)
# Create image
fig, ax = plt.subplots(1,2,subplot_kw={"projection": "3d"},figsize=(12,12))
plots=ax.flatten()

X=np.arange(0,8,1)
Y=X
X, Y = np.meshgrid(X, Y)
Z=cd_mat

#Smooth the dataset
#interpolate the matrix along a finer lattice
if doSmooth:
    xnew, ynew = np.mgrid[0:7:200j, 0:7:200j]
    tck = sp.interpolate.bisplrep(X, Y, Z, s=10)
    znew = sp.interpolate.bisplev(xnew[:,0], ynew[0,:], tck)

    X=xnew
    Y=ynew
    Z=znew

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
