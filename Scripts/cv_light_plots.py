import numpy as np
import matplotlib as plt
from glob import glob

data = []
#Load data - multiple datasets
for file in glob("../CV Light/TiO2_24_CV_Light(*)",root_dir="."):
    set=np.loadtxt(file,skiprows=1)
    data.append(set) # Append all dataset

