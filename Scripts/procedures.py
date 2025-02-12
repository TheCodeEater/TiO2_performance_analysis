
# Assign sequence position to x,y of point

def getxy(linear_position):
    x=linear_position // 8

    r=linear_position % 16

    if 8<=r<=15:
        y=7-(r%8)
    else:
        y=r

    return (x,y)
