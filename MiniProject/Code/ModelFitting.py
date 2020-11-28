#!/urs/bin/env python3

"""Script for model fitting"""

## Imports ##
#from lmfit import Model
import statsmodels.formula.api as smf
#from lmfit import Minimizer, Parameters, report_fit
import lmfit
import numpy as np
import pandas as pd
import sys
import scipy as sc
#from scipy import stats
#import warnings
import time
#import concurrent.futures
#from multiprocessing import Process, Pool
import multiprocessing
from statistics import mean
#from itertools import product
#from functools import partial
#from smt.sampling_methods import LHS
#import warnings
from sklearn.metrics import r2_score  # because I'm lazy


# TODO:
#  1. Delete r_sqd stuff (and 'holler'/AIC/BIc funcs below thereafter)
#  2. Why is BIC giving so many to Holling II

## Variables ##
data = pd.read_csv("../Data/CRat_prepped.csv")  # Load data

##### FOR TESTING ########
#data = data.head(250)
#data = data[data['ID'] == 3]

#mask = data['ID'].isin([2, 3, 39949, 140, 351, 445])
#data = data.loc[mask]

##########################

ids = data['ID'].unique()

## Functions ##

def holler_II(x, a, h):
    """blabla"""
    return (a*x)/(1+h*a*x)

def holler_III(x, a, h, q):
    """blabla"""
    return (a*x**(q+1))/(1+h*a*x**(q+1))


def AIC(n, p, rss):
    """Calculate AIC value

    n = sample size
    p = number of free parameters
    rss = residual sum of squares
    """
    return n + 2 + n*np.log((2*np.pi)/n) + n*np.log(rss) + 2*p

def BIC(n, p, rss):
    """Calculate BIC value
    """
    return n + 2 + n*np.log((2*np.pi)/n) + n*np.log(rss) + p*np.log(n)


def fitPolynomial(df, n):
    """Fits polynomial of degree n to data x and y using numpy's polyfit
    """
    id_ = df['ID'].unique()[0]
    x = df['ResDensity']
    y = df['N_TraitValue']

    model = np.polyfit(x, y, n, full=True)
    predict = np.poly1d(model[0])
    r_sqd = r2_score(y, predict(x))

    stats = smf.ols(formula='N_TraitValue ~ predict(ResDensity)',
                    data=df).fit()

    aic = stats.aic
    bic = stats.bic

    if r_sqd == 1:
        print(f"ERROR: Insufficient data for ID {id_} to fit polynomial of "
              f"degree {n}.")
        aic = bic = r_sqd = None

    return aic, bic, r_sqd

def startValues(df):
    """return sensible start values for params
    """
    # h
    h = 1/max(df['N_TraitValue'])  # As curve tends to 1/h

    # a
    BelowMean = df[df['N_TraitValue'] < mean(df['N_TraitValue'])]

    if len(BelowMean) > 1:
        # If there is more than one datapoint below the mean
        slope1, _, r_val1, _, _ = sc.stats.linregress(BelowMean['ResDensity'],
                                                      BelowMean['N_TraitValue'])
        r_sqd1 = r_val1**2
    else:
        r_sqd1 = 0

    BelowMax = df[df['N_TraitValue'] < max(df['N_TraitValue'])]
    slope2, _, r_value2, _, _ = sc.stats.linregress(BelowMax['ResDensity'],
                                                 BelowMax['N_TraitValue'])
    r_sqd2 = r_value2**2

    a = slope1 if r_sqd1 > r_sqd2 else slope2

    return h, a

def residHoll2(params, x, y):
    """Returns residuals for Holling II functional response:

    Arguments:
     - params: parameters
     - x: Resource density data values
     - y: Corresponding N_TraitValue data values
    """
    # Get an ordered dictionary of parameter values
    v = params.valuesdict()

    # Holling II model
    model = (v['a'] * x) / (1 + v['h'] * v['a'] * x)

    # Return residuals
    return model - y


def residHoll3(params, x, y):
    """Returns residuals for Holling II functional response:

    Arguments:
     - params: parameters
     - x: Resource density data values
     - y: Corresponding N_TraitValue data values
    """
    # Get an ordered dictionary of parameter values
    v = params.valuesdict()

    # Holling II model
    model = (v['a'] * x**(v['q']+1)) / (1 + v['h'] * v['a'] * x**(v['q']+1))

    # Return residuals
    return model - y

def fitFuncResp(h, a, df, model, timeout):
    """Fit functinal response curves to input data.

    using uniform distribution
    across range centred
    RANDOM UNIF DIST

    Arguments:
    h: handling time
    a: attack rate
    x: ResDensity (vec)
    y: N_TraitValue (vec)
    N: no of parameter pairs to try
    """
    N = 1000  # Set max number of param combos/runs

    x = df['ResDensity']
    y = df['N_TraitValue']

    # Create ranges around params to test
    hrange = 0.8 * min(abs(h - 1e6), h)
    arange = 0.8 * min(abs(a - 5e7), a)

    # Generate random parameter samples
    # (uniform used over LHS as LHS unncessary here — runmax high so unlikely
    # to not cover the whole parameter space)
    np.random.seed(0)
    h_vals = [h] + list(np.random.uniform(h - hrange, h + hrange, N))
    a_vals = [a] + list(np.random.uniform(a - arange, a + arange, N))
    ##################
    paramsdf = pd.DataFrame(list(zip(h_vals, a_vals)), columns=['h', 'a'])
    ##################

    # Initialize timer, counter, and groups list
    i = 0
    groups = []
    t = time.time() + timeout  # Set fitting time limit for each ID

    # Fit until time runs out of all values have been tested
    # TODO: Cut if a lower aic hasn't been found in? no point, I'm using time constraints
    while time.time() < t and i < N:

        # Extract params to test
        testparams = paramsdf.loc[i]
        hi = testparams['h']
        ai = testparams['a']

        # Store paramteters
        params = lmfit.Parameters()
        params.add('h', value=hi, min=0, max=1e6)  # Add h param
        params.add('a', value=ai, min=0, max=5e7)  # Add a param

        if model == 'HollingII':

            # Attempt fit
            try:
                fit = lmfit.minimize(residHoll2, params, args=(x, y))
            except ValueError:
                i += 1
                continue

            # Extract otimised parameters
            h_best = fit.params['h'].value
            a_best = fit.params['a'].value

            # Calculate R-squared
            RSS = np.sum((y - holler_II(x, a_best, h_best)) ** 2)
            TSS = np.sum((y - np.mean(y)) ** 2)
            r_sqd = 1 - RSS / TSS

            # Create tuple to return
            group = (fit.aic, fit.bic, r_sqd, h_best, a_best)

        else:

            params.add('q', value=0)  # Add additional q param for GFR

            # Attempt fit
            try:
                fit = lmfit.minimize(residHoll3, params, args=(x, y))
            except ValueError:
                i += 1
                continue

            # Extract otimised parameters
            h_best = fit.params['h'].value
            a_best = fit.params['a'].value
            q_best = fit.params['q'].value

            # Calculate R-squared
            RSS = np.sum((y - holler_III(x, a_best, h_best, q_best)) ** 2)
            TSS = np.sum((y - np.mean(y)) ** 2)
            r_sqd = 1 - RSS / TSS

            # Create tuple to return
            group = (fit.aic, fit.bic, r_sqd, h_best, a_best, q_best)

        groups.append(group)
        i += 1

    best_fit = min(groups, key=lambda grp: grp[0])  # take group with lowest AIC

    return best_fit if groups else None

###############################################################################
def returnStats(id_):
    #i, id_ = 279, 140
    # id_ = 140
    # id_ = 39840
    # id_ = 39949
    df = data[data['ID'] == id_]

    # Holing I
    #holl1AIC, holl1BIC, holl1R2 = fitPolynomial(df, 1)
    #if None in [holl1AIC, holl1BIC, holl1R2]:
    #    print(f"Insufficient data to plot Holling II for ID '{id_}'.")

    # Quadratic Polynomial
    quadAIC, quadBIC, quadR2 = fitPolynomial(df, 2)
    if None in [quadAIC, quadBIC, quadR2]:
        return [None] * 14

    # Cubic Polynomial
    cubeAIC, cubeBIC, cubeR2 = fitPolynomial(df, 3)
    if None in [cubeAIC, cubeBIC, cubeR2]:
        return [None] * 14

    ######################### NON-LINEAR ###############################

    # Obtain sensible parameter starting values (catching any warnings thrown
    # by stats.linregress())
    #with warnings.catch_warnings():
    #    warnings.filterwarnings('error')
    #    try:
    #        h, a = startValues(df)
    #    except RuntimeWarning:
    #        print(f"startValues error at ID {id_}. Skipping.")
    #        return [None] * 15

    # Generate starting values
    h, a = startValues(df)

    # Holling II
    bestfit = fitFuncResp(h, a, df, 'HollingII', 5)
    if bestfit:
        holl2aic, holl2bic, holl2R2, h2, a2 = bestfit
    else:
        print(f"ERROR: Insufficient data for ID {id_} to fit Holling II model.")
        return [None] * 14

    # Generalised Functional Response
    bestfit = fitFuncResp(h, a, df, 'GFR', 5)
    if bestfit:
        gfraic, gfrbic, gfrR2, h3, a3, q3 = bestfit
    else:
        print(f"ERROR: Insufficient data for ID {id_} to fit Generalised "
              f"Functional Response model.")
        return [None] * 14

    statistics = [id_,
                  quadAIC, cubeAIC, holl2aic, gfraic,
                  quadBIC, cubeBIC, holl2bic, gfrbic,
                  #cubeR2, holl2R2, holl3R2, quadR2
                  h2, a2,
                  h3, a3, q3]

    return statistics

def main():
    """Run analysis
    """
    print('Fitting models to data...')

    # Apply function and filter out failed IDs
    with multiprocessing.Pool() as pool:
        rows = [row for row in pool.map(returnStats, ids) if None not in row]

    heads = ['ID',
             'Quadratic_AIC', 'Cubic_AIC', 'HollingII_AIC', 'GFR_AIC',
             'Quadratic_BIC', 'Cubic_BIC', 'HollingII_BIC', 'GFR_BIC',
             #'Cubic_Rsqd', 'HollingII_Rsqd', 'HollingIII_Rsqd',
             'h_Holl2', 'a_Holl2',
             'h_GFR', 'a_GFR', 'q_GFR']
    ModelStats = pd.DataFrame(rows, columns=heads)
    ModelStats['ID'] = ModelStats['ID'].astype(int)  # Convert ID col from float
    ModelStats.sort_values('ID', inplace=True)  # Order by ID

    # Write to CSV
    ModelStats.to_csv('../Data/ModelStats.csv', index=False)

    return 0

if __name__ == '__main__':
    status = main()
    sys.exit(status)