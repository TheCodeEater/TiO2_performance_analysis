import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import time
import constants as c
import procedures as proc
import scipy as sp
from decorators import LoadMatrixSize

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

@LoadMatrixSize
def generatePlots(dataset,**kwargs):
    #Create convenient variables
    X_max=kwargs["X_max"]
    Y_max=kwargs["Y_max"]
    backToZero=kwargs["backToZero"]
    del kwargs["X_max"]
    del kwargs["Y_max"]
    del kwargs["backToZero"]

    # Plot for each column
    for column_index in range(0,X_max): #for each column
        #Get column as linear array
        column=dataset[column_index*X_max:(column_index+1)*X_max]#excludes last element, which is part of the next column (or out of bound if last col)

        #check if we are going back to the start or do a snake like route
        if backToZero==False:
        #Reverse row if parity is odd (first column is 0)
            if column_index%2==1:
                column=reversed(column)

        row_index=0
        for row in column: #for each row, plot according to colors
            plots[column_index].plot(row["x"],row["y"],color=c.colors[row_index],label="Row {}".format(row_index+1))
            row_index+=1

        #Set labels and title
        plots[column_index].set(**kwargs,
                   title="Column {}".format(column_index + 1))
        plots[column_index].legend()

generatePlots(data_base,xlabel="Potential (V)", ylabel="Current (A)",xlim=c.CRG_XLIM,ylim=c.CRG_YLIM)

#Drawing
plt.legend()
plt.savefig("../Artifacts/cv_light_column_gradient/CV_Light_COL_"+time.strftime("%Y%m%d-%H%M%S")+".png")
plt.show()

