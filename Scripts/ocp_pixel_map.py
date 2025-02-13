import matplotlib.pyplot as plt
import numpy as np
import constants as c
from glob import glob
import procedures as proc
import re
import scipy as sp

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

#Compute smooth version
X=np.arange(0,8,1)
Y=X
X, Y = np.meshgrid(X, Y)
Z=cd_mat

#Smooth the dataset
#interpolate the matrix along a finer lattice
xnew, ynew = np.mgrid[0:7:200j, 0:7:200j]
tck = sp.interpolate.bisplrep(X, Y, Z, s=10)
znew = sp.interpolate.bisplev(xnew[:,0], ynew[0,:], tck)

X=xnew
Y=ynew
Z=znew

#Create subplots
fig,ax = plt.subplots(1,3,figsize=(20,5))

# Assign colors based on value (interpolation between maximum and minimum hue, fixed brightness and saturation)
# Draw 2d pixel

pixel_plot=ax[0].imshow(
  cd_mat, cmap='gnuplot', interpolation='nearest',origin="lower")

# Draw 2d smoothed
smooth_plot=ax[1].imshow(
    Z, cmap='gnuplot', interpolation='nearest',origin="lower")

#Set scale formatted for smoothed
ticks = np.linspace(0, 200, 8)

ax[1].set_xticks(ticks, np.arange(8))
ax[1].set_yticks(ticks, np.arange(8))

# Contour plot

cont_plot = ax[2].contour(X,Y,np.transpose(Z), 80,cmap="gnuplot", antialiased=True)

plt.suptitle("OCP photovoltage map (average)")
plt.colorbar(pixel_plot,label="V")
plt.colorbar(smooth_plot,label="V")
plt.colorbar(cont_plot,label="V")


plt.savefig("../Artifacts/ocp_voltage_delta/OCP_2D_{}.png".format(proc.current_time()))
plt.show()
