#############################
# Conditionals
#############################
def foo_1(x):
    """returns half of input
    """
    return x ** 0.5

def foo_2(x, y):
    """
    :param x: int
    :param y: int
    :return: the larger of the two
    """
    if x > y:
        return x
    return y

def foo_3(x, y, z):
    """
    :param x: int
    :param y: int
    :param z: int
    :return: swaps each element with the next if
    it is larger.
    """
    if x > y:
        tmp = y
        y = x
        x = tmp
    if y > z:
        tmp = z
        z = y
        y = tmp
    return [x, y, z]

def foo_4(x):
    """
    :param x: int
    :return: factorial of x
    """
    result = 1
    for i in range(1, x + 1):
        result = result * i
    return result

def foo_5(x):
    """a recursive function that calculates the factorial of x
    """
    if x == 1:
        return 1
    return x * foo_5(x - 1)

def foo_6(x): #
    """"calculate the factorial of x in a different way
    """
    facto = 1
    while x >= 1:
        facto = facto * x
        x = x - 1
    return facto