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
def absScanSequence(width,height,**kwargs):
    #Convert the parameters in terms of the discrete X,Y matrix
    #using units of step
    X_min=0
    X_max=width//kwargs["step_x"]
    Y_min=0
    Y_max=height//kwargs["step_y"]

    X_sequence=[]
    Y_sequence=[]

    #Move along the main axis
    for x in range(X_min,X_max):

        for y in range(Y_min,Y_max):
            #Set matching x value
            X_sequence.append(x)
            #Set matching Y value
            if kwargs["backToZero"]:
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


def relScanSequence(width,height,**kwargs):
    return convertToAU(toRelativeSequence(absScanSequence(width,height,**kwargs)),kwargs["step_x"],kwargs["step_y"])
