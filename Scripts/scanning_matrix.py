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

print(scanSequence(8,8,1,1,True))
