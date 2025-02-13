import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import time
import constants as c
import procedures as proc

#Ask for the point to plot
print("Type the xy coordinates of the point to examine")

x_pos=input("X:\n")
y_pos=input("Y:\n")

linear_pos=proc.getlinearpos(x_pos,y_pos)

data_base = []
data_normalized = []

#Load data - multiple datasets
file= proc.get_sorted_filenames(c.FILEPATH_CV_LIGHT)[linear_pos]
voltage, we_current, vrhe, specific_current=np.loadtxt(file,skiprows=1,unpack=True)

specific_current=proc.reject_outliers(specific_current,31)

iv_ch={"x":vrhe,"y":specific_current}
iv_normalized={"x":vrhe,"y":specific_current}

data_base.append(iv_ch) # Append all dataset
data_normalized.append(iv_normalized)


#Plot the single curve
#Extract the dataset from the list
set=data_base[0]
plt.plot(set["x"],set["y"],color=c.colors[linear_pos],ls="dotted")


#Drawing
plt.legend()
plt.xlabel("Potential (V)")
plt.ylabel("WE Current(A)")
plt.savefig("../Artifacts/CV_Light_"+time.strftime("%Y%m%d-%H%M%S")+".png")
plt.show()

