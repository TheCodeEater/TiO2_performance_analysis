import functools

#
# Config loader
#

#Load config here and set constants, to be later used by decorators
X_points=8
Y_points=8

#
# Config decorators
# Add config entries to kwargs
#

def LoadMatrixSize(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper
