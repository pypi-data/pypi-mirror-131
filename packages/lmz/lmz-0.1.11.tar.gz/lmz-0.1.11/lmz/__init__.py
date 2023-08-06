from itertools import zip_longest

def Map(*x,**y):
    return list(map(*x,**y))

def Zip(*x,**y):
    return list(zip(*x,**y))

def Filter(*x,**y):
    return list(filter(*x,**y))

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def Grouper(*x,**y):
    return list(grouper(*x,**y))


def iterselect(iterable, n):
    while n>0:
        next(iterable)
        n-=1
    return next(iterable)




def Range(*x):
    # loi = length or int
    loi = lambda y: y if isinstance(y,int) else len(y)
    #x[0] = loi(x[0])
    #if len(x) > 1:
    #    x[1] = loi(x[1])
    return list(range(*map(loi,x)))

def Transpose(x):
    return list(zip(*x))
