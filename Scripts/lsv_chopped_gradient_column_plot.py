import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import time
import constants as c
import procedures as proc
import scipy as sp

chopped = []

#Load data - voltage and current
for file in proc.get_sorted_filenames(c.FILEPATH_CHOPPED):
    voltage, we_current, junk,junk=np.loadtxt(file,skiprows=1,unpack=True)
    # Do not reject outliers, peaks are the norm here
    iv={"x":voltage,"y":we_current}
    chopped.append(iv)


#Create subplots for each column
figure, ax = plt.subplots(nrows=2,ncols=4,figsize=(30,15)) #Plot data along cols (contains 8 plots, one for each row of the col assigned to the plot)
plots=ax.flatten()


# Plot for each column
for col in range(0,8): #for each column
    #Get column as linear array
    column=chopped[col*8:(col+1)*8]#excludes last element, which is part of the next column (or out of bound if last col)
    #Reverse row if parity is odd (first column is 0)
    if col%2==1:
        column=reversed(column)

    row_count=0
    for row in column: #for each row, plot according to colors
        plots[col].plot(row["x"],row["y"],color=c.colors[row_count],label="Row {}".format(row_count+1))
        row_count+=1

    #Set labels and title
    plots[col].set(xlabel="Potential (V)", ylabel="Current (A)",
                   title="Column {}".format(col + 1),
                   xlim=c.CHOP_XLIM,ylim=c.CHOP_YLIM)
    plots[col].legend()


#Drawing
plt.legend()
plt.savefig("../Artifacts/chopped_column_gradient/Chop_COL_"+time.strftime("%Y%m%d-%H%M%S")+".png")
plt.show()

