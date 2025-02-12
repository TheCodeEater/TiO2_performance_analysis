import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import time
import constants as c
import procedures as proc

data_base = []
data_normalized = []
#Load data - multiple datasets
for file in proc.get_sorted_filenames("../CV Light/TiO2_24_CV_Light(*)"):
    voltage, we_current, vrhe, specific_current=np.loadtxt(file,skiprows=1,unpack=True)

    iv_ch={"x":voltage,"y":we_current}
    iv_normalized={"x":vrhe,"y":specific_current}

    data_base.append(iv_ch) # Append all dataset
    data_normalized.append(iv_normalized)


#General plots
i=0
for set in data_base:
    r=i%16
    if 8<=r<=15:
        r=7-(r%8)

    plt.plot(set["x"],set["y"],color=c.colors[r],ls="dotted")#,label="Riga {}".format(r+1))

    i=i+1




#Drawing
plt.legend()
plt.xlabel("Potential (V)")
plt.ylabel("WE Current(A)")
plt.savefig("../Artifacts/CV_Light_"+time.strftime("%Y%m%d-%H%M%S")+".png")
plt.show()

