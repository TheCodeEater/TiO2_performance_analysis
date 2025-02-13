import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import time
import constants as c
import procedures as proc
import scipy as sp

data_base = []
data_normalized = []
#Load data - multiple datasets
for file in proc.get_sorted_filenames(c.FILEPATH_CV_LIGHT):
    voltage, we_current, vrhe, specific_current=np.loadtxt(file,skiprows=1,unpack=True)

    we_current=proc.reject_outliers(we_current,31)

    iv_ch={"x":voltage,"y":we_current}
    iv_normalized={"x":vrhe,"y":specific_current}

    data_base.append(iv_ch) # Append all dataset
    data_normalized.append(iv_normalized)


#Create subplots for each column
figure, ax = plt.subplots(nrows=2,ncols=4,figsize=(30,15)) #Plot data along cols (contains 8 plots, one for each row of the col assigned to the plot)
plots=ax.flatten()


# Plot for each column
for row_index in range(0,8): #for each row
    # Create empty row
    row=[]
    # Get the row as a linear array, picking all x value (column) for fixed y (row)
    for col_index in range(0,8):
        linear_pos=proc.getlinearpos(col_index,row_index)
        row.append(data_base[linear_pos]) #pick all values on the same row but different columns

    #plot
    col_count=0
    for column in row: #for each column point that is on the row, plot
        plots[row_index].plot(column["x"],column["y"],color=c.colors[col_count],label="Column {}".format(col_count+1))
        col_count+=1

    #Set labels and title
    plots[row_index].set(xlabel="Potential (V)", ylabel="Current (A)",
                         title="Row {}".format(row_index + 1),
                         xlim=c.CRG_XLIM,ylim=c.CRG_YLIM)
    plots[row_index].legend()


#Drawing
plt.legend()
plt.savefig("../Artifacts/cv_light_row_gradient/CV_Light_ROW_"+time.strftime("%Y%m%d-%H%M%S")+".png")
plt.show()

