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

#Load data - Dark only. Pick high frequencies only
resistances = [] #real part is ohmic resistance

#Load light current density data
for file in proc.get_sorted_filenames(c.FILEPATH_EIS_DARK):
    junk, real_z, junk2=np.loadtxt(file,skiprows=1,unpack=True)
    resistances.append(real_z[0])#pick highest frequency


#Compute differences

count=0
cd_mat = np.zeros((8,8))

for value in resistances:
    #Arrange data in a matrix
    pos=proc.getxy(count)
    cd_mat[pos]=value

    count+=1

cd_mat=np.transpose(cd_mat) # Fix orientation of matrix
#Reflect

# Assign colors based on value (interpolation between maximum and minimum hue, fixed brightness and saturation)
# Create image
fig, ax = plt.subplots(subplot_kw={"projection": "3d"},figsize=(10,10))
X=np.arange(0,8,1)
Y=X
X, Y = np.meshgrid(X, Y)
Z=cd_mat

#Smooth the dataset
#interpolate the matrix along a finer lattice
if doSmooth:
    xnew, ynew = np.mgrid[0:7:200j, 0:7:200j]
    tck = sp.interpolate.bisplrep(X, Y, Z, s=100)
    znew = sp.interpolate.bisplev(xnew[:,0], ynew[0,:], tck)

    X=xnew
    Y=ynew
    Z=znew

#if zeroToObserver:
 #   plt.gca().invert_xaxis()
#else:
 #   plt.gca().invert_yaxis()

surf = ax.plot_surface(X,Y,Z, cmap="gnuplot",
                       linewidth=0, antialiased=True)
ax.set(xlabel="X",ylabel="Y")

plt.suptitle("EIS Re(Z) map at 100 kHz (maximum frequency)")
#plt.colorbar(label="mA/$cm^2$")

plt.savefig("../Artifacts/ocp_voltage_delta/OCP_dV_3D_{}.png".format(proc.current_time()))
plt.show()
