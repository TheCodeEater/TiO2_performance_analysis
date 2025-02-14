import time
import re
from glob import glob
import numpy as np
import scipy as scp
# Assign sequence position to x,y of point

def getxy(linear_position,**kwargs):
    #Assigning variables
    X_max=kwargs["X_max"]
    Y_max=kwargs["Y_max"]

    x=linear_position // X_max

    r=linear_position % Y_max*2

    if Y_max <=r <= Y_max*2-1:
        y=Y_max-1-(r%Y_max)
    else:
        y=r

    return (x,y)

def getlinearpos(x,y):
    #Position if Y was 0

    #if on even column
    if x%2==0:
        linear_position=x*8+y
    #if on odd column
    else:
        linear_position=x*8+(7-y)

    return linear_position

def current_time():
    return time.strftime("%Y%m%d-%H%M%S")

def get_file_number(file):
    # For each file, match position and put in the list
    pos = re.search(r"\((\d+)\)", file)
    pos = int(pos.group(1))
    return pos
def get_sorted_filenames(path):
    filenames = glob(path, root_dir=".")
    return sorted(filenames, key=get_file_number)

def reject_outliers(data, m=2):
    return scp.ndimage.median_filter(data,m)