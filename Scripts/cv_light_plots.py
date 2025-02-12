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


#General plots
i=0
for set in data_base:
    r=i%8
    if 8<=r<=15:
        r=7-(r%8)

    plt.plot(set["x"],set["y"],color=colors[r],ls="dotted")

    i=i+1




#Drawing
plt.legend()
plt.xlabel("Potential (V)")
plt.ylabel("WE Current(A)")
plt.savefig("../Artifacts/CV_Light_"+time.strftime("%Y%m%d-%H%M%S")+".png")
plt.show()

