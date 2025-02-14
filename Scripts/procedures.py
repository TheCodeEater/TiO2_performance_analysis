import time
import re
from glob import glob
import numpy as np
import scipy as scp
from decorators import LoadMatrixSize

# Assign sequence position to x,y of point
@LoadMatrixSize
def getxy(linear_position,**kwargs):
    #Assigning variables
    X_max=kwargs["X_max"]
    Y_max=kwargs["Y_max"]

    #Works regardless of scan order
    x=linear_position // X_max

    #If coming back to zero after moving on x axis
    if kwargs["backToZero"]:
        y=linear_position % Y_max
        return (x,y)

    else: #otherwise use the algorithm
        r=linear_position % (Y_max*2)

        if Y_max <=r <= Y_max*2-1:
            y=Y_max-1-(r%Y_max)
        else:
            y=r

        return (x,y)

@LoadMatrixSize
def getlinearpos(x,y,**kwargs):
    #ensure the range is ok
    assert(x<=kwargs["X_max"])
    assert(y<=kwargs["Y_max"])
    linear_position=0

    #if coming back to 0
    if kwargs["backToZero"]:
        linear_position=x*kwargs["X_max"]+y #add a column for each x plus y offset inside the column
    else:
        #if on even column
        if x%2==0:
           linear_position=x*kwargs["X_max"]+y
        #if on odd column
        else:
            linear_position=x*kwargs["X_max"]+(kwargs["Y_max"]-1-y)

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