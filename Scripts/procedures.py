import time
# Assign sequence position to x,y of point

def getxy(linear_position):
    x=linear_position // 8

    r=linear_position % 16

    if 8<=r<=15:
        y=7-(r%8)
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