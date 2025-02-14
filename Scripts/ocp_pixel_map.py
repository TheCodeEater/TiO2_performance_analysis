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

X_max,Y_max=proc.getXYMax()

#Load light current density data
for file in proc.get_sorted_filenames(c.FILEPATH_OCP_LIGHT):
    junk, voltage=np.loadtxt(file,skiprows=1,unpack=True)
    light_dataset.append(voltage)

#Load dark current density data
for file in proc.get_sorted_filenames(c.FILEPATH_OCP_DARK):
    junk,  voltage=np.loadtxt(file,skiprows=1,unpack=True)
    dark_dataset.append(voltage)

#Compute differences
X,Y,Z=proc.deltaAverageOCP(light_dataset,dark_dataset)

#Compute smooth
xnew, ynew, znew = proc.smoothMatrix(X,Y,Z)

#Create subplots
fig,ax = plt.subplots(1,3,figsize=(20,5))

# Assign colors based on value (interpolation between maximum and minimum hue, fixed brightness and saturation)
# Draw 2d pixel
#Set correct orientation for pixel
#cd_mat=np.transpose(cd_mat)

pixel_plot=ax[0].imshow(
  np.transpose(Z), cmap='gnuplot', interpolation='nearest',origin="lower")

# Draw 2d smoothed
smooth_plot=ax[1].imshow(
    znew, cmap='gnuplot', interpolation='nearest',origin="lower")

#Set scale formatted for smoothed
ticks = np.linspace(0, 200, 8)

ax[1].set_xticks(ticks, np.arange(8))
ax[1].set_yticks(ticks, np.arange(8))

# Contour plot

cont_plot = ax[2].contour(xnew,ynew,np.transpose(znew), 80,cmap="gnuplot", antialiased=True)

plt.suptitle("OCP photovoltage map (average of last 10)")
plt.colorbar(pixel_plot,label="V")
plt.colorbar(smooth_plot,label="V")
plt.colorbar(cont_plot,label="V")


plt.savefig("../Artifacts/ocp_voltage_delta/OCP_2D_{}.png".format(proc.current_time()))
plt.show()
