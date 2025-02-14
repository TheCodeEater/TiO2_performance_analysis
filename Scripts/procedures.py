import time
import re
from glob import glob
import numpy as np
import scipy as sp
from decorators import LoadMatrixSize, Smooth

# Assign sequence position to x,y of point
@LoadMatrixSize
def getXY(linear_position, **kwargs):
    #Assigning variables
    X_max=kwargs["X_max"]
    Y_max=kwargs["Y_max"]

    assert(linear_position<=X_max*Y_max)

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
def getLinearPosition(x, y, **kwargs):
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

@LoadMatrixSize
def getBlankSampleMatrix(**kwargs):
    return np.zeros((kwargs["X_max"],kwargs["Y_max"]))

@LoadMatrixSize
def getXYMax(**kwargs):
    return (kwargs["X_max"],kwargs["Y_max"])

def current_time():
    return time.strftime("%Y%m%d-%H%M%S")

#@Smooth
def deltaOCP(light_dataset,dark_dataset):
    Z_matrix = getBlankSampleMatrix() #get empty matrix for z data

    count = 0
    for light,dark in zip(light_dataset,dark_dataset):
        voltage_light=np.average(light[-10:])
        voltage_dark=np.average(dark[-10:])

        #Compute current density difference. this is the photocurrent
        photovoltage=voltage_light-voltage_dark

        #Arrange data in a matrix
        pos=getXY(count)
        Z_matrix[pos]=photovoltage

        count+=1

    #Compute XY axis
    X = np.arange(0, 8, 1)
    Y = X
    X, Y = np.meshgrid(X, Y)

    return (X,Y,Z_matrix)

def smoothMatrix(X,Y,Z,finesseX=200j,finesseY=200j,s_factor=10):
    X_max,Y_max=getXYMax()

    xnew, ynew = np.mgrid[0:X_max - 1:finesseX, 0:Y_max - 1:finesseY]
    tck = sp.interpolate.bisplrep(X, Y, Z, s=s_factor)
    znew = sp.interpolate.bisplev(xnew[:, 0], ynew[0, :], tck)

    return (xnew,ynew,znew)

def get_file_number(file):
    # For each file, match position and put in the list
    pos = re.search(r"\((\d+)\)", file)
    pos = int(pos.group(1))
    return pos
def get_sorted_filenames(path):
    filenames = glob(path, root_dir=".")
    return sorted(filenames, key=get_file_number)

def reject_outliers(data, m=2):
    return sp.ndimage.median_filter(data,m)