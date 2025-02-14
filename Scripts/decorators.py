import functools
import numpy as np
import scipy as sp

#
# Config loader
#

#Load config here and set constants, to be later used by decorators
X_points=8
Y_points=8
backToZero=False

#
# Config decorators
# Add config entries to kwargs
#

def LoadMatrixSize(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        kwargs["X_max"]=X_points
        kwargs["Y_max"]=Y_points
        kwargs["backToZero"]=backToZero
        return f(*args, **kwargs)

    return wrapper

def Smooth(finesseX=200,finesseY=200,s_factor=10):
    def smooth_decorator(f):
        @functools.wraps(f)
        def wrapper(*args,**kwargs):
            X,Y,Z=f(*args,**kwargs)

            xnew, ynew = np.mgrid[0:X_points-1:finesseX, 0:X_points-1:finesseY]
            tck = sp.interpolate.bisplrep(X, Y, Z, s=s_factor)
            znew = sp.interpolate.bisplev(xnew[:, 0], ynew[0, :], tck)

            return (xnew,ynew,znew)

        return wrapper
    return smooth_decorator