#!/usr/bin/env python3

"""Script that plots the Lotka-Volterra model, taking arguments for the four
model parameters (r, a, z, e), the carrying capacity of the environment (K), and
 an arbitrary upper bound for the output x-axis (tN) from the command line."""

__author__ = 'Luke Swaby (lds20@ic.ac.uk)'
__version__ = '0.0.1'

## Imports ##
import argparse
import sys
import numpy as np
import scipy.integrate as integrate
import matplotlib.pylab as p

## Functions ##

def dCR_dt(RC0, t, r, a, z, e, K):
    """Returns the growth rate of consumer and resource
    population at any given time step using the Lotka-Volterra model.

    Arguments:
     - RC0 (array) : the densities of both populations at time t
     - t: time
     - r: Intrinsic (per-capita) growth rate of the 'resource population
          (/time).'
     - a: Encounter and consumption rate of the consumer on the resource
     - z: Mortality rate (/time).
     - e: The consumer’s efficiency (a fraction) in converting resource to
          consumer biomass.
     - K: Environment carrying capacity

    Output:
     - A numpy array containing the growth rate of the two populations
    """
    R = RC0[0]
    C = RC0[1]
    dRdt = r * R * (1 - R/K) - a * R * C
    dCdt = -z * C + e * a * R * C

    return np.array([dRdt, dCdt])

def main(r=1., a=0.1, z=1.5, e=0.75, K=50, tN=35):
    """Plot the Lotka-Volterra model with prey density dependence.
    """
    # Define the time vector
    t = np.linspace(0, tN, 1000)

    # Set the initial conditions for the two populations
    R0 = 10
    C0 = 5
    RC0 = np.array([R0, C0])

    # Numerically integrate this system forward from those starting conditions
    pops, infodict = integrate.odeint(dCR_dt, RC0, t,
                                      args=(r, a, z, e, K), full_output=True)

    print(infodict['message'])

    ## PLOT ##
    f1 = p.figure()  # open an empty figure object
    p.plot(t, pops[:, 0], 'g-', label='Resource density')  # Plot
    p.plot(t, pops[:, 1], 'b-', label='Consumer density')
    p.grid()
    p.legend(loc='best')
    p.xlabel('Time')
    p.ylabel('Population density')
    p.suptitle('Consumer-Resource population dynamics')
    p.title("r = %.2f,  a = %.2f,  z = %.2f,  e = %.2f, K = %d"
            % (r, a, z, e, K), fontsize=10)
    #p.show()  # To display the figure

    # Save figure
    f1.savefig('../Results/LV2_model.pdf')

    # Print final population density values
    print("Stabilised resource population density: %.2f" % pops[-1, 0])
    print("Stabilised consumer population density: %.2f" % pops[-1, 1])

    return 0

if __name__ == '__main__':

    # Use argparse to provide info about individual args and force dtypes
    parser = argparse.ArgumentParser(
        description="Script that plots the Lotka-Volterra model, taking "
                    "arguments for the four model parameters (r, a, z, e), "
                    "the carrying capacity of the environment (K), and an "
                    "arbitrary upper bound for the output x-axis (tN) from the "
                    "command line. Note that if no/insufficicient args are "
                    "provided then defaults will be used.")

    parser.add_argument('r', type=float, nargs='?',
                        help='Intrinsic (per-capita) growth rate of the '
                             'resource population (/time).')
    parser.add_argument('a', type=float, nargs='?',
                        help='Encounter and consumption rate of the consumer '
                             'on the resource.')
    parser.add_argument('z', type=float, nargs='?',
                        help='Mortality rate (/time).')
    parser.add_argument('e', type=float, nargs='?',
                        help='The consumer’s efficiency (a fraction) in '
                             'converting resource to consumer biomass.')
    parser.add_argument('K', type=float, nargs='?',
                        help='Carrying capacity.')
    parser.add_argument('tN', type=float, nargs='?',
                        help='Time interval to display in output plot.')

    args = parser.parse_args()

    if len(sys.argv) == 7:
        status = main(args.r, args.a, args.z, args.e, args.K, args.tN)
        sys.exit(status)
    else:
        print("WARNING: Incorrect arguments provided. "
              "(For more information see help page — 'python3 LV2.py -h')\n"
              "Defaults will be used:\n"
              "r = 1.\na = 0.1\nz = 1.5\ne = 0.75\nK = 50\ntN = 35")
        status = main()
        sys.exit(status)
