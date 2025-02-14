import functools
"""!
    Generate a 2D scanning matrix
    Returns a list of coordinates relative to a given origin (usually a corner of the surface to scan)
    that identify a scanning order
"""

"""!
    Generate a scan sequence. All the values are in arbitrary units.
    If you want to change the main scan axis, just transpose the sample.
    
    @:param width the size on the X axis of the sample
    @:param height the size on the Y axis of the sample
    @:param step_x the increasing step on x axis
    @:param step_y the increasing step on y axis
    @:param back_to_zero wether to start the next Y axis scan at y=0 or from the last value
    
    Use absolute coordinates
    
"""
def scanSequence(width,height,step_x,step_y,backToZero):
    #Convert the parameters in terms of the discrete X,Y matrix
    #using units of step
    X_min=0
    X_max=width//step_x
    Y_min=0
    Y_max=height//step_y

    X_sequence=[]
    Y_sequence=[]

    #Move along the main axis
    for x in range(X_min,X_max):

        for y in range(Y_min,Y_max):
            #Set matching x value
            X_sequence.append(x)
            #Set matching Y value
            if backToZero:
                Y_sequence.append(y)
            else:
                if x%2==0:
                    Y_sequence.append(y)
                else:
                    Y_sequence.append(Y_max-y-1)

    sequence={"x":X_sequence,"y":Y_sequence}

    return sequence

"""!
    Convert a sequence dictionary in different x and y units
"""
def convertToAU(sequence,unit_x,unit_y):
    X=sequence["x"]
    Y=sequence["y"]

    X = [x*unit_x for x in X]
    Y = [y * unit_y for y in Y]

    return {"x":X,"y":Y}

"""!
    Turn existing sequence into relative 
"""
def toRelativeSequence(sequence):
    #Get the sequences
    X=sequence["x"]
    Y=sequence["y"]
    #Ensure len is ok
    assert(len(X)==len(Y))

    X_rel=[]
    Y_rel=[]

    #Add first element manually
    X_rel.append(X[0])
    Y_rel.append(Y[0])

    for i in range(1,len(X)):
        X_rel.append(X[i]-X[i-1])
        Y_rel.append(Y[i]-Y[i-1])

    #Reassemble the dict
    return {"x":X_rel,"y":Y_rel}


#
# DECORATORS
#

def makeRelative(f):
    def wrapper(*args,**kwargs):
        return toRelativeSequence(f(*args,**kwargs))
    return wrapper

def toAU(_func=None, *,unit_x,unit_y): #decorator with parameters. Assemble decorator with fixed par and return
    def decorator_toAU(f):
        @functools.wraps(f)
        def wrapper(*args,**kwargs):
            return convertToAU(f(*args,**kwargs),unit_x,unit_y)

        return wrapper
    if _func is None:
        return decorator_toAU
    else:
        return decorator_toAU(_func)

@makeRelative
@toAU(unit_x=5,unit_y=5)
def relativeSequence(*args):
    return scanSequence(*args)
