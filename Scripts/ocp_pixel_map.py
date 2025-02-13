import matplotlib.pyplot as plt
import numpy as np
import constants as c
from glob import glob
import procedures as proc
import re

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

#Drawing
# Assign colors based on value (interpolation between maximum and minimum hue, fixed brightness and saturation)
# Create image
pixel_plot=plt.Figure()

#Transpose for correct drawing
cd_mat=np.transpose(cd_mat)

pixel_plot=plt.imshow(
  cd_mat, cmap='gnuplot', interpolation='nearest',origin="lower")

plt.suptitle("OCP photovoltage map (average)")
plt.colorbar(label="V")

plt.savefig("../Artifacts/ocp_voltage_delta/OCP_2D_{}.png".format(proc.current_time()))
plt.show()
