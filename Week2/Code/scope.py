#!/urs/bin/env python3

"""Playing with global variables"""

__author__ = 'Luke Swaby (lds20@ic.ac.uk)'
__version__ = '0.0.1'

## 1

_a_global = 10

print("Outside the function, the value of _a_global is", _a_global)

def a_function():
    """Demonstrates global variables defined within functions can be re-used
    outside
    """
    global _a_global
    _a_global = 5
    _a_local = 4

    print("Inside the function, the value of _a_global is ", _a_global)
    print("Inside the function, the value _a_local is ", _a_local)

    return None

a_function()

print("Outside the function, the value of _a_global now is", _a_global)

## 2

def a_function():
    """Demonstrates global variables defined within functions is only set when
    function is called
    """
    _a_global = 10

    def _a_function2():
        """Set global variable
        """
        global _a_global
        _a_global = 20

    print("Before calling a_function, value of _a_global is ", _a_global)

    _a_function2()

    print("After calling _a_function2, value of _a_global is ", _a_global)

    return None

a_function()

print("The value of a_global in main workspace / namespace is ", _a_global)

## 3

_a_global = 10

def a_function():
    """Calling a global variable set in a function within a function
    """
    def _a_function2():
        """Set global variable
        """
        global _a_global
        _a_global = 20

    print("Before calling a_function, value of _a_global is ", _a_global)

    _a_function2()

    print("After calling _a_function2, value of _a_global is ", _a_global)

a_function()

print("The value of a_global in main workspace / namespace is ", _a_global)
