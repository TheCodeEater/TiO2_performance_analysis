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

proc.generatePlots(data_base,plots,xlabel="Potential (V)", ylabel="Current (A)",xlim=c.CRG_XLIM,ylim=c.CRG_YLIM)

#Drawing
plt.legend()
plt.savefig("../Artifacts/cv_light_column_gradient/CV_Light_COL_"+time.strftime("%Y%m%d-%H%M%S")+".png")
plt.show()

