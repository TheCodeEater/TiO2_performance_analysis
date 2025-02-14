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
