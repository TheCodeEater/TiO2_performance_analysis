import matplotlib as mpl
import numpy as np


# Extract 8 colors from coolwarm palette
values = np.linspace(0, 1, 8)

# Get colors from the coolwarm colormap
colors = [mpl.colormaps["coolwarm"](value) for value in values]
# Color palettes
#colors=(
 #   "red",
 #   "orange",
  #  "gold",
  #  "green",
  #  "teal",
  #  "blue",
  #  "purple",
  #  "pink"
#)

# Filename patterns

FILEPATH_CV_LIGHT="../CV Light/TiO2_24_CV_Light(*)"
FILEPATH_CV_DARK="../CV Dark/TiO2_24_CV_Dark(*)"

#Axis limits
#For row and column gradients
CRG_XLIM=[-0.7, 1.6]
CRG_YLIM=[-1.2e-6, 3e-6]