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
FILEPATH_OCP_DARK="../OCP Dark/TiO2_24_OCP_Dark(*)"
FILEPATH_OCP_LIGHT="../OCP Light/TiO2_24_OCP_Light(*)"
FILEPATH_EIS_DARK="../EIS Dark/TiO2_24_EIS_Dark(*)"
FILEPATH_CHOPPED="../LSV Chopped/TiO2_24_LSV_Chopped(*)"

#Axis limits
#For row and column gradients
CRG_XLIM=[-0.7, 1.6]
CRG_YLIM=[-1.2e-6, 3e-6]

OCP_XLIM=[-0.1,10]
OCP_YLIM=[-0.28,-0.01]

CHOP_XLIM=[-0.8,1.8]
CHOP_YLIM=[-5e-6,4e-6]