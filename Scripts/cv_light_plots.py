import numpy as np
import matplotlib.pyplot as plt
from glob import glob

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

for set in data_base:
    plt.plot(data=set,color="blue")

plt.legend()
plt.xlabel("V")
plt.ylabel("I")
plt.show()

