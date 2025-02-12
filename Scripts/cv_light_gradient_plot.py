import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import time

data_base = []
data_normalized = []
#Load data - multiple datasets
for file in glob("../CV Light/TiO2_24_CV_Light(*)",root_dir="."):
    voltage, we_current, vrhe, specific_current=np.loadtxt(file,skiprows=1,unpack=True)

    iv_ch={"x":voltage,"y":we_current}
    iv_normalized={"x":vrhe,"y":specific_current}

    data_base.append(iv_ch) # Append all dataset
    data_normalized.append(iv_normalized)

# Plot using a color gradient
colors=(
    "#003f5c",
    "#58508d",
    "#8a508f",
    "#bc5090",
    "#de5a79",
    "#ff6361",
    "#ff8531",
    "#ffa600"
)

#Plots
figure, ax = plt.subplots(nrows=2,ncols=4,figsize=(30,15)) #Plot data along cols (contains 8 plots, one for each row of the col assigned to the plot)
plots=ax.flatten()


# Col plots
for col in range(0,8): #for each column
    #Get column as lienar array
    column=data_base[col*8:(col+1)*8]#excludes last element
    #Reverse row if parity is odd (first column is 0)
    if col%2==1:
        column=reversed(column)

    i=0
    for row in column: #for each row, plot according to colors
        plots[col].plot(row["x"],row["y"],color=colors[i])
        plots[col].set(xlabel="Potential (V)",ylabel="Current (A)",title="Column {}".format(col+1))
        i=i+1


#Drawing
#matrix.legend()
#matrix.set(xlabel="Potential (V)",ylabel="WE Current(A)")
plt.savefig("../Artifacts/CV_Light_"+time.strftime("%Y%m%d-%H%M%S")+".png")
plt.show()

