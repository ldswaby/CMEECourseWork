def buggyfunc(x):
    y = x
    for i in range(x):
        y -= 1
        z = x/y
    return z

buggyfunc(20)