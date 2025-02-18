import matplotlib.pyplot as plt
import numpy as np
import constants as c
from glob import glob
import procedures as proc
import re
import scipy as sp
from matplotlib.ticker import FuncFormatter

#Request target potential
target_potential=float(input("Insert target potential") or 1.1)

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

#Find requested potential index - copy one array
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
    print("({},{})\n->Light: {}\n->Dark: {}\n->Delta: {}\nPoint: {}\n----".format(pos[0],pos[1],current_light,current_dark,photocurrent,count))

    count+=1

#Compute smooth version
X=np.arange(0,8,1)
Y=X
X, Y = np.meshgrid(X, Y)
Z=cd_mat

#Smooth the dataset
#interpolate the matrix along a finer lattice
X,Y,Z=proc.smoothMatrix(X,Y,Z)

#Drawing
#Transpose for correct drawing
cd_mat=np.transpose(cd_mat)
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

cont_plot = ax[2].contour(X,Y,np.transpose(Z), 60,cmap="gnuplot", antialiased=True)

#ax[2].set_xticks(ticks, np.arange(8))
#ax[2].set_yticks(ticks, np.arange(8))

#General figure properties and scale
fig.suptitle("Current density map at {} V cell potential\nTowards positive voltages".format(target_potential))
#fig.colorbar(pixel_plot,label="mA/$cm^2$")
fig.colorbar(pixel_plot,label="mA/$cm^2$")
fig.colorbar(smooth_plot,label="mA/$cm^2$")
fig.colorbar(cont_plot,label="mA/$cm^2$")

plt.savefig("../Artifacts/current_density_maps/CD_{}.png".format(proc.current_time()))
plt.show()
