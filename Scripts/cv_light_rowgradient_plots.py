import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import time
import constants as c

data_base = []
data_normalized = []
#Load data - multiple datasets
for file in glob("../CV Light/TiO2_24_CV_Light(*)",root_dir="."):
    voltage, we_current, vrhe, specific_current=np.loadtxt(file,skiprows=1,unpack=True)

    iv_ch={"x":voltage,"y":we_current}
    iv_normalized={"x":vrhe,"y":specific_current}

    data_base.append(iv_ch) # Append all dataset
    data_normalized.append(iv_normalized)


#Plots
figure, ax = plt.subplots(nrows=2,ncols=4,figsize=(30,15)) #Plot data along rows (contains 8 plots, one for each row of the col assigned to the plot)
plots=ax.flatten()


# Col plots
for row in range(0,8): #for each row
    #Get the row as linear array



    for row in column: #for each row, plot according to colors
        plots[col].plot(row["x"],row["y"],color=c.colors[i],label="Riga {}".format(i+1))
        i=i+1

    plots[col].set(xlabel="Potential (V)", ylabel="Current (A)", title="Column {}".format(col + 1))
    plots[col].legend()


#Drawing
#matrix.legend()
#matrix.set(xlabel="Potential (V)",ylabel="WE Current(A)")
plt.legend()
plt.savefig("../Artifacts/CV_Light_"+time.strftime("%Y%m%d-%H%M%S")+".png")
plt.show()

