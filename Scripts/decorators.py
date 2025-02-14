import functools

#
# Config loader
#

#Load config here and set constants, to be later used by decorators

#
# Config decorators
#

def LoadConfig(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper
