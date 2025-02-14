import functools

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
