import matplotlib.pyplot as plt
import numpy as np
import constants as c
from glob import glob
import procedures as proc
import re
import scipy as sp

#Set target potential
target_potential=1.1
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
for file in proc.get_sorted_filenames(c.FILEPATH_CV_LIGHT):
    junk, junk, voltage, current_density=np.loadtxt(file,skiprows=1,unpack=True)

    current_density = proc.reject_outliers(current_density, 31)

    iv={"x":voltage,"y":current_density}
    light_dataset.append(iv)

#Load dark current density data
for file in proc.get_sorted_filenames(c.FILEPATH_CV_DARK):
    junk, junk, voltage, current_density=np.loadtxt(file,skiprows=1,unpack=True)

    current_density = proc.reject_outliers(current_density, 31)

    iv={"x":voltage,"y":current_density}
    dark_dataset.append(iv)

#For each point, at a fixed potential, compute difference for both maximum and minimum
# Use normalized data

#Find potential - copy one array
potential_array=light_dataset[0]["x"]
#Remove reversing voltage part
#Get maximum potential value index
max_potential_index=np.argmax(potential_array)
#Trim the array
potential_array[:max_potential_index]

index=np.argmin(np.abs(potential_array - target_potential)) #index of the wanted potential in the dataset

count=0
cd_mat = np.zeros((8,8))

for light,dark in zip(light_dataset,dark_dataset):
    current_light=light["y"][index]
    current_dark=dark["y"][index]

    #Compute current density difference. this is the photocurrent
    photocurrent=current_light-current_dark


    #Arrange data in a matrix
    pos=proc.getXY(count)
    cd_mat[pos]=photocurrent
    #print("({},{})\n->Light: {}\n->Dark: {}\n->Delta: {}\nPoint: {}\n----".format(pos[0],pos[1],current_light,current_dark,photocurrent,count))

    count+=1

cd_mat=np.transpose(cd_mat) # Fix orientation of matrix

# Assign colors based on value (interpolation between maximum and minimum hue, fixed brightness and saturation)
# Create image
fig, ax = plt.subplots(subplot_kw={"projection": "3d"},figsize=(10,10))

X=np.arange(0,8,1)
Y=X
X, Y = np.meshgrid(X, Y)
Z=cd_mat

#Smooth the dataset
#interpolate the matrix along a finer lattice
X,Y,Z=proc.smoothMatrix(X,Y,Z)

surf = ax.contour(X,Y,Z, 100,cmap="gnuplot", antialiased=True)
ax.set(xlabel="X",ylabel="Y")

plt.suptitle("Current density map at {} V cell potential".format(target_potential))
plt.title("Towards positive voltages")
#plt.colorbar(label="mA/$cm^2$")

plt.savefig("../Artifacts/current_density_maps_contour/CD_CT_{}.png".format(proc.current_time()))
plt.show()
