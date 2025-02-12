import numpy as np
import constants as c
from glob import glob

#Load data - Both light and dark
dark = []
light = []
junk = []

#Load light current density data
for file in glob("../CV Light/TiO2_24_CV_Light(*)",root_dir="."):
    junk, junk, voltage, current_density=np.loadtxt(file,skiprows=1,unpack=True)

    iv={"x":voltage,"y":current_density}
    light.append(iv)

#Load dark current density data
for file in glob("../CV Dark/TiO2_24_CV_Dark(*)",root_dir="."):
    junk, junk, voltage, current_density=np.loadtxt(file,skiprows=1,unpack=True)

    iv={"x":voltage,"y":current_density}
    dark.append(iv)

#For each point, at a fixed potential, compute difference for both maximum and minimum
# Use normalized data

#Find potential - temporary hard-coded
pot_index=5




# Assign colors based on value (interpolation between maximum and minimum hue, fixed brightness and saturation)

# Create image