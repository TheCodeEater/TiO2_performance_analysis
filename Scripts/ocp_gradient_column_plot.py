import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import time
import constants as c
import procedures as proc
import scipy as sp

#Load data - Both light and dark
#IV curve for each potential
dark_dataset = []
light_dataset = []

#Load light current density data
for file in proc.get_sorted_filenames(c.FILEPATH_OCP_LIGHT):
    time, voltage=np.loadtxt(file,skiprows=1,unpack=True)

    ocp_t={"x":time,"y":voltage}
    light_dataset.append(ocp_t)

#Load dark current density data
for file in proc.get_sorted_filenames(c.FILEPATH_OCP_DARK):
    time,  voltage=np.loadtxt(file,skiprows=1,unpack=True)
    ocp_t = {"x": time, "y": voltage}
    dark_dataset.append(ocp_t)

#Compute differences - NO AVERAGE

count=0
cd_mat = np.zeros((8,8))

for light,dark in zip(light_dataset,dark_dataset):
    voltage_light=np.average(light)
    voltage_dark=np.average(dark)

    #Compute current density difference. this is the photocurrent
    photovoltage=voltage_light-voltage_dark

    #Arrange data in a matrix
    pos=proc.getxy(count)
    cd_mat[pos]=photovoltage

    count+=1

cd_mat=np.transpose(cd_mat) # Fix orientation of matrix


#Create subplots for each column
figure, ax = plt.subplots(nrows=2,ncols=4,figsize=(30,15)) #Plot data along cols (contains 8 plots, one for each row of the col assigned to the plot)
plots=ax.flatten()


# Plot for each column
for col in range(0,8): #for each column
    #Get column as linear array
    column=data_base[col*8:(col+1)*8]#excludes last element, which is part of the next column (or out of bound if last col)
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
                   xlim=c.CRG_XLIM,ylim=c.CRG_YLIM)
    plots[col].legend()


#Drawing
plt.legend()
plt.savefig("../Artifacts/cv_light_column_gradient/CV_Light_COL_"+time.strftime("%Y%m%d-%H%M%S")+".png")
plt.show()

