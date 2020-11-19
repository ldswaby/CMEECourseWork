#!/usr/bin/env python3

"""Playing with the Lotka-Volterra model"""

__author__ = 'Luke Swaby (lds20@ic.ac.uk)'
__version__ = '0.0.1'

## Imports ##
import numpy as np
import scipy.integrate as integrate
import matplotlib.pylab as p

## Assign some parameter values ##

## Functions ##

def dCR_dt(pops, t=0, r=1., a=0.1, z=1.5, e=0.75):
    """Returns the growth rate of consumer and resource
    population at any given time step using the Lotka-Volterra model.

    Arguments:
     - RC0 (array) : the densities of both populations at time t

    Output:
     - a numpy array containing the growth rate of the populations
    """
    R = pops[0]
    C = pops[1]
    dRdt = r * R - a * R * C
    dCdt = -z * C + e * a * R * C

    return np.array([dRdt, dCdt])

def main():
    """Run functions
    """

    # Define the time vector
    t = np.linspace(0, 15, 1000)

    # Set the initial conditions for the two populations
    R0 = 10
    C0 = 5
    RC0 = np.array([R0, C0])

    # Numerically integrate this system forward from those starting conditions
    pops, infodict = integrate.odeint(dCR_dt, RC0, t, full_output=True)

    print(infodict['message'])

    ## PLOT 1 ##
    f1 = p.figure()  # open an empty figure object
    p.plot(t, pops[:, 0], 'g-', label='Resource density')  # Plot
    p.plot(t, pops[:, 1], 'b-', label='Consumer density')
    p.grid()
    p.legend(loc='best')
    p.xlabel('Time')
    p.ylabel('Population density')
    p.title('Consumer-Resource population dynamics')
    #p.show()  # To display the figure

    # Save figure
    f1.savefig('../Results/LV_model.pdf')

    ## PLOT 2 ##
    f2 = p.figure()
    p.plot(pops[:, 0], pops[:, 1], 'r-')
    p.grid()
    p.xlabel('Resource density')
    p.ylabel('Consumer density')
    p.title('Consumer-Resource population dynamics')

    # Save figure
    f2.savefig('../Results/LV_model2.pdf')

if __name__ == '__main__':
    main()