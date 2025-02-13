import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import time
import constants as c
import procedures as proc

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


#Plot everything at once
linear_pos=0
for set in data_base:
    #convert linear position to coordinates
    x,y=proc.getxy(linear_pos)
    #use y coord to find color
    plt.plot(set["x"],set["y"],color=c.colors[y],ls="dotted")#,label="Riga {}".format(r+1))

    linear_pos+=1

#Custom legend
legend_elements=[]

for row in range(0,8): #for each row
    legend_elements.append(plt.Line2D([0],[0],color=c.colors[row],label="Row {}".format(row+1)))


#Drawing
plt.legend(handles=legend_elements)
plt.xlabel("Potential (V)")
plt.ylabel("WE Current(A)")
plt.savefig("../Artifacts/cv_light_all/CV_Light_ALL_"+time.strftime("%Y%m%d-%H%M%S")+".png")
plt.show()

