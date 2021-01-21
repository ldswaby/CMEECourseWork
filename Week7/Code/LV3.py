#!/usr/bin/env python3

"""Script that plots a discrete-time version of the Lotka-Volterra model,
taking arguments for the model parameters (r, a, z, e), the carrying capacity
of the environment (K), and an arbitrary upper bound for the output x-axis
(tN) from the command line."""

__author__ = 'Luke Swaby (lds20@ic.ac.uk), ' \
             'Jinkai Sun (jingkai.sun20@imperial.ac.uk), ' \
             'Acacia Tang (t.tang20@imperial.ac.uk), ' \
             'Dengku Tang (dengkui.tang20@imperial.ac.uk)'
__version__ = '0.0.1'

## Imports ##
import argparse
import sys
import numpy as np
import matplotlib.pylab as p

## Functions ##

def discreteLV(r0, c0, t, r, a, z, e, K):
    """Returns the growth rate of consumer and resource
    population at any given time step using the Lotka-Volterra model.

    Arguments:
     - r0 (array) : inital resource density
     - c0 (array) : inital consumer density
     - t: time array
     - r: Intrinsic (per-capita) growth rate of the 'resource population
          (/time).'
     - a: Encounter and consumption rate of the consumer on the resource
     - z: Mortality rate (/time).
     - e: The consumer’s efficiency (a fraction) in converting resource to
          consumer biomass.
     - K: Environment carrying capacity

    Output:
     - A numpy array containing the desnities of the two populations at each
       time step
    """

    RC = np.zeros((len(t), 2), dtype='float')  # Pre-allocate array to hold data
    RC[0] = r0, c0  # Set intial conditions

    for i in range(len(t)-1):
        Rnext = RC[i][0] * (1 + r * (1 - RC[i][0] / K) - a * RC[i][1])
        Cnext = RC[i][1] * (1 - z + e * a * RC[i][0])

        # Set upper and lower population limits (0:K)
        for ix, pop in enumerate([Rnext, Cnext]):
            if pop > K:
                RC[i + 1][ix] = K
            elif pop < 0:
                RC[i + 1][ix] = 0
                break  # extinction
            else:
                RC[i + 1][ix] = pop

    return RC

def main(r=1, a=0.1, z=1.5, e=0.75, K=30, tN=35):
    """Plot discrete version of the Lotka-Volterra model with random gaussian
    fluctuation in resource’s growth rate at each time-step.

    Arguments:
     - r: Intrinsic (per-capita) growth rate of the 'resource population
          (/time).'
     - a: Encounter and consumption rate of the consumer on the resource
     - z: Mortality rate (/time).
     - e: The consumer’s efficiency (a fraction) in converting resource to
          consumer biomass.
     - K: Environment carrying capacity.
     - tN: Time interval to display in output plot.

    Output:
     - Plot of population density against time: '../Results/LV3_model.pdf'
    """

    # Define the time vector
    t = np.linspace(0, tN, 1000)

    # Set the initial conditions for the two populations
    R0 = 10
    C0 = 5

    # Run LV function and extract results
    RC = discreteLV(R0, C0, t, r, a, z, e, K)
    res = [x[0] for x in RC]
    cons = [x[1] for x in RC]

    ## PLOT ##
    f = p.figure()
    p.plot(t, res, 'g-', label='Resource density')
    p.plot(t, cons, 'b-', label='Consumer density')
    p.grid()
    p.legend(loc='best')
    p.xlabel('Time')
    p.xlim(left=0, right=3)
    p.ylabel('Population density')
    p.suptitle('Consumer-Resource population dynamics')
    p.title("r = %.2f,  a = %.2f,  z = %.2f,  e = %.2f, K = %d"
            % (r, a, z, e, K), fontsize=10)
    #p.show()
    f.savefig('../Results/LV3_model.pdf')

    # Print final population density values
    print("Stabilised resource population density: %.2f" % RC[-1][0])
    print("Stabilised consumer population density: %.2f" % RC[-1][1])

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
