import matplotlib.pyplot as plt
import numpy as np
import constants as c
from glob import glob
import procedures as proc

#Set target potential
target_potential=1

#Load data - Both light and dark
#IV curve for each potential
dark_dataset = []
light_dataset = []

junk = []

#Load light current density data
for file in glob("../CV Light/TiO2_24_CV_Light(*)",root_dir="."):
    junk, junk, voltage, current_density=np.loadtxt(file,skiprows=1,unpack=True)

    iv={"x":voltage,"y":current_density}
    light_dataset.append(iv)

#Load dark current density data
for file in glob("../CV Dark/TiO2_24_CV_Dark(*)",root_dir="."):
    junk, junk, voltage, current_density=np.loadtxt(file,skiprows=1,unpack=True)

    iv={"x":voltage,"y":current_density}
    dark_dataset.append(iv)

#For each point, at a fixed potential, compute difference for both maximum and minimum
# Use normalized data

#Find potential - temporarily hard-coded
potential_array=light_dataset[0]["x"]

index=np.argmin(np.abs(potential_array - target_potential)) #index of the wanted potential in the dataset

count=0
cd_mat = np.zeros((8,8))

for light,dark in zip(light_dataset,dark_dataset):
    current_light=light["y"][index]
    current_dark=dark["y"][index]

    #Compute current density difference. this is the photocurrent
    photocurrent=current_light-current_dark


    #Arrange data in a matrix
    pos=proc.getxy(count)
    cd_mat[pos]=photocurrent

    count+=1

# Assign colors based on value (interpolation between maximum and minimum hue, fixed brightness and saturation)
# Create image

pixel_plot=plt.Figure()
#pixel_plot.add_axes()
pixel_plot=plt.imshow(
  cd_mat, cmap='gnuplot', interpolation='nearest')

plt.title("Current density map at {} V cell potential".format(target_potential))
plt.colorbar()

plt.savefig("../Artifacts/current_density_maps/CD_{}.png".format(proc.current_time()))
plt.show()
