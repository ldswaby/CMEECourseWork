#!/urs/bin/env python3

"""Script for model fitting"""

## Imports ##
#from lmfit import Model
import statsmodels.formula.api as smf
from lmfit import Minimizer, Parameters, report_fit
import lmfit
import numpy as np
import pandas as pd
import sys
import scipy as sc
from scipy import stats
import warnings
import time
import concurrent.futures
from multiprocessing import Process, Pool
import multiprocessing
from statistics import mean
from itertools import product
from functools import partial
from smt.sampling_methods import LHS
import warnings
from sklearn.metrics import r2_score


# TODO:
#  1. Delete r_sqd stuff (and 'holler'/AIC/BIc funcs below thereafter)
#  2. Why is BIC giving so many to Holling II

## Variables ##
data = pd.read_csv("../Data/CRat_prepped.csv")  # Load data

##### FOR TESTING ########
#data = data.head(100)
# data = data[data['ID'] == 140]
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


def fit_polynomial(df, n):
    """Fits polynomial of degree n to data x and y using numpy's polyfit
    """
    x = df['ResDensity']
    y = df['N_TraitValue']

    try:
        model = np.polyfit(x, y, n, full=True)
        predict = np.poly1d(model[0])
        r_sqd = r2_score(y, predict(x))

        stats = smf.ols(formula='N_TraitValue ~ predict(ResDensity)',
                        data=df).fit()

        aic = stats.aic
        bic = stats.bic

    except IndexError:
        aic = bic = r_sqd = None

    return aic, bic, r_sqd

def startValues(df):
    """return sensible start values for params
    """
    # h
    h = 1/max(df['N_TraitValue'])  # As curve tends to 1/h

    # a
    BelowMean = df[df['N_TraitValue'] < mean(df['N_TraitValue'])]
    slope1, _, r_value1, _, _ = stats.linregress(BelowMean['ResDensity'],
                                                 BelowMean['N_TraitValue'])
    r_sqd1 = r_value1**2

    BelowMax = df[df['N_TraitValue'] < max(df['N_TraitValue'])]
    slope2, _, r_value2, _, _ = stats.linregress(BelowMax['ResDensity'],
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

def fitHoll2(h, a, x, y, timeout):
    """Fit Holling II to data with start values  RANDOM UNIF DIST

    h: handling time
    a: attack rate
    x: ResDensity (vec)
    y: N_TraitValue (vec)
    N: no of parameter pairs to try
    """
    N = 1000  # Set max number of runs

    # Create ranges around params to test
    hrange = 0.8 * min(abs(h - 1e6), h)
    arange = 0.8 * min(abs(a - 5e7), a)

    # Generate random parameter samples
    np.random.seed(0)
    h_vals = [h] + list(np.random.uniform(h - hrange, h + hrange, N))
    a_vals = [a] + list(np.random.uniform(a - arange, a + arange, N))

    #h_vals = [h] + [np.exp(x) for x in list(np.random.uniform(np.log(1e-20), np.log(1e6), N))]
    #a_vals = [a] + [np.exp(x) for x in list(np.random.uniform(np.log(1e-20), np.log(5e7), N))]

    # Create 2 column array out of params
    paramsdf = pd.DataFrame(list(zip(h_vals, a_vals)), columns=['h', 'a'])

    # Initialize timer and counter
    t = time.time() + timeout  # Set fitting time limit
    groups = []
    i = 0

    # Fit until time runs out of all values have been tested
    while time.time() < t and i < N:
        params = paramsdf.loc[i]
        hi = params['h']
        ai = params['a']

        # Store paramteters
        params_holl2 = Parameters()
        params_holl2.add('h', value=hi, min=0, max=1e6)  # Add h param
        params_holl2.add('a', value=ai, min=0, max=5e7)  # Add a param

        # Attempt fit
        try:
            fit = lmfit.minimize(residHoll2, params_holl2, args=(x, y))

            h_best = fit.params['h'].value
            a_best = fit.params['a'].value

            #r_sqd = 1 - fit.redchi / np.var(y, ddof=2)
            RSS = np.sum((y - holler_II(x, a_best, h_best)) ** 2)
            TSS = np.sum((y - np.mean(y))**2)
            r_sqd = 1 - RSS/TSS
            #print(r_sqd, r_sqd2)
            # Write stats to group tuple
            group = (fit.aic, fit.bic, r_sqd, h_best, a_best)
            groups.append(group)
            i += 1

        except ValueError:
            i += 1
            continue

    best_fit = min(groups, key=lambda t: t[0])  # take group with lowest AIC

    return best_fit if groups else None

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


def fitHoll3(h, a, x, y, timeout):
    """Fit Holling II to data with start values  RANDOM UNIF DIST

    h: handling time
    a: attack rate
    x: ResDensity (vec)
    y: N_TraitValue (vec)
    N: no of parameter pairs to try
    """
    N = 1000  # Set max number of runs

    # Create ranges around params to test
    hrange = 0.8 * min(abs(h - 1e6), h)
    arange = 0.8 * min(abs(a - 5e7), a)

    # Generate random parameter samples
    np.random.seed(0)
    h_vals = [h] + list(np.random.uniform(h - hrange, h + hrange, N))
    a_vals = [a] + list(np.random.uniform(a - arange, a + arange, N))

    #h_vals = [h] + [np.exp(x) for x in list(np.random.uniform(np.log(1e-20), np.log(1e6), N))]
    #a_vals = [a] + [np.exp(x) for x in list(np.random.uniform(np.log(1e-20), np.log(5e7), N))]

    # Create 2 column array out of params
    paramsdf = pd.DataFrame(list(zip(h_vals, a_vals)), columns=['h', 'a'])

    # Initialize timer and counter
    t = time.time() + timeout  # Set fitting time limit FOR EACH ID (5 seconds from now)
    groups = []
    i = 0

    # Fit until time runs out of all values have been tested
    while time.time() < t and i < N:
        params = paramsdf.loc[i]
        hi = params['h']
        ai = params['a']

        # store paramteters
        params_holl3 = Parameters()  # Create object for parameter storing
        params_holl3.add('h', value=hi, min=0, max=1e6)  # Add h param
        params_holl3.add('a', value=ai, min=0, max=5e7)  # Add a param
        params_holl3.add('q', value=0)  # Add q param

        # Attempt fit
        try:
            fit = lmfit.minimize(residHoll3, params_holl3, args=(x, y))

            h_best = fit.params['h'].value
            a_best = fit.params['a'].value
            q_best = fit.params['q'].value

            RSS = np.sum((y - holler_III(x, a_best, h_best, q_best)) ** 2)
            TSS = np.sum((y - np.mean(y)) ** 2)
            r_sqd = 1 - RSS / TSS
            # print(r_sqd, r_sqd2)
            # Write stats to group tuple
            group = (fit.aic, fit.bic, r_sqd, h_best, a_best, q_best)
            groups.append(group)
            i += 1

        except ValueError:
            i += 1
            continue

    best_fit = min(groups, key=lambda t: t[0])  # take group with lowest AIC

    return best_fit if groups else None


###############################################################################
def returnStats(id_):
    #i, id_ = 279, 140
    # id_ = 140
    # id_ = 39840
    # id_ = 39835
    #print(id_)
    df = data[data['ID'] == id_]
    # Extract exp/resp variables
    x = df['ResDensity']
    y = df['N_TraitValue']

    #if len(df) < 3:
    #    print(f'Insufficient data for R2 to fit {id_}')
    #    return [None] * 10

    # Holing I
    #holl1AIC, holl1BIC, holl1R2 = fit_polynomial(df, 1)
    #if None in [holl1AIC, holl1BIC, holl1R2]:
    #    print(f"Insufficient data to plot Holling II for ID '{id_}'.")

    # Quadratic Polynomial
    #quadAIC, quadBIC, quadR2 = fit_polynomial(x, y, 2)
    #if None in [quadAIC, quadBIC, quadR2]:
    #    print(f"Insufficient data to plot quadratic polynomial for ID '{id_}'.")

    # Cubic Polynomial
    #cubeAIC, cubeBIC, cubeR2 = fit_polynomial(df, 3)
    cubeAIC, cubeBIC, cubeR2 = fit_polynomial(df, 3)
    if None in [cubeAIC, cubeBIC, cubeR2]:
        print(f"Insufficient data to plot cubic polynomial for ID '{id_}'.")

    ######################### NON-LINEAR ###############################

    # Obtain sensible parameter starting values (catching any warnings thrown
    # by stats.linregress())
    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            h, a = startValues(df)
        except RuntimeWarning:
            print(f"startValues error at ID {id_}. Skipping.")
            return [None] * 12

    # Holling II
    bestfit = fitHoll2(h, a, x, y, 10)
    if bestfit:
        holl2aic, holl2bic, holl2R2, h2, a2 = bestfit
    else:
        print(f"Insufficient data to plot Holling II for ID '{id_}'.")
        h2 = a2 = holl2aic = holl2bic = holl2R2 = None

    # Holling III
    bestfit = fitHoll3(h, a, x, y, 10)
    if bestfit:
        holl3aic, holl3bic, holl3R2, h3, a3, q3 = bestfit
    else:
        print(f"Insufficient data to plot Holling III for ID '{id_}'.")
        holl3aic = holl3bic = holl3R2 = h3 = a3 = q3 = None

    statistics = [id_,
                  cubeAIC, holl2aic, holl3aic,
                  cubeBIC, holl2bic, holl3bic,
                  h2, a2,
                  h3, a3, q3]

    #print(f'{id_} done!')

    return statistics

def main():
    """Run analysis
    """
    # Apply function and filter out failed IDs
    with multiprocessing.Pool() as pool:
        rows = [row for row in pool.map(returnStats, ids) if None not in row]

    heads = ['ID',
             'Cubic_AIC', 'HollingII_AIC', 'HollingIII_AIC',
             'Cubic_BIC', 'HollingII_BIC', 'HollingIII_BIC',
             'h_Holl2', 'a_Holl2',
             'h_Holl3', 'a_Holl3', 'q_Holl3']
    ModelStats = pd.DataFrame(rows, columns=heads)
    ModelStats['ID'] = ModelStats['ID'].astype(int)  # Convert ID col from float
    ModelStats.sort_values('ID', inplace=True)  # Order by ID

    # Write to CSV
    ModelStats.to_csv('../Data/STATS_test.csv', index=False)

    return 0

if __name__ == '__main__':
    status = main()
    sys.exit(status)








"""
def returnStats(id_):
    #i, id_ = 279, 140
    # id_ = 140
    # id_ = 39840
    # id_ = 39835
    print(id_)
    df = data[data['ID'] == id_]
    # Extract exp/resp variables
    x = df['ResDensity']
    y = df['N_TraitValue']

    if len(df) < 3:
        print(f'Insufficient data for R2 to fit {id_}')
        return [None] * 10

    # Holing I
    holl1AIC, holl1BIC, holl1R2 = fit_polynomial(df, 1)
    if None in [holl1AIC, holl1BIC, holl1R2]:
        print(f"Insufficient data to plot Holling II for ID '{id_}'.")

    # Quadratic Polynomial
    #quadAIC, quadBIC, quadR2 = fit_polynomial(x, y, 2)
    #if None in [quadAIC, quadBIC, quadR2]:
    #    print(f"Insufficient data to plot quadratic polynomial for ID '{id_}'.")

    # Cubic Polynomial
    cubeAIC, cubeBIC, cubeR2 = fit_polynomial(df, 3)
    if None in [cubeAIC, cubeBIC, cubeR2]:
        print(f"Insufficient data to plot cubic polynomial for ID '{id_}'.")

    ######################### NON-LINEAR ###############################

    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            h, a = startValues(df)
        except RuntimeWarning:
            print(f"Insufficient data to fit for ID {id_}. Skipping.")
            return [id_] + [None] * 9

    # Holling II
    #h, a = optimizeParams(h, a, x, y, 30) # better values
    bestfit = fitHoll2(h, a, x, y, 1000)
    if bestfit:
        h2, a2, holl2aic, holl2bic, holl2R2 = bestfit
    else:
        print(f"Insufficient data to plot Holling II for ID '{id_}'.")
        h2, a2, holl2aic, holl2bic, holl2R2 = [None] * 5

    # Holling III
    #h3, a3 = optimizeParams(h, a, x, y, 'hollingIII')

    #bestfit = fitHoll3(h, a, x, y, 1000)
    #if bestfit:
    #    holl3aic, holl3bic, h3, a3 = bestfit
    #else:
    #    print(f"Insufficient data to plot Holling III for ID '{id_}'.")
    #    holl3aic, holl3bic, h3, a3 = None, None, None, None

    statistics = [id_,
                  holl1AIC,
                  #quadAIC,
                  cubeAIC,
                  holl2aic,
                  #holl3aic,
                  holl1BIC,
                  #quadBIC,
                  cubeBIC,
                  holl2bic,
                  #holl3bic,
                  holl1R2,
                  #quadR2,
                  cubeR2,
                  holl2R2,
                  # holl3bic
                  ]

    print(f'{id_} done!')

    return statistics

pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
# Filter out None rows
rows = [row for row in pool.map(returnStats, ids) if None not in row]
pool.close()
pool.join()

#ModelStats = ModelStats[~np.isnan(ModelStats).any(axis=1)]  # Remove NaN rows
heads = ['ID',
         'HollingIAIC',
         #'QuadraticAIC',
         'CubicAIC',
         'HollingIIAIC',
         #'HollingIIIAIC',
         'HollingIBIC',
         #'QuadraticBIC',
         'CubicBIC',
         'HollingIIBIC',
         #'HollingIIIBIC'
         'HollingIR^2',
         #'QuadraticR^2',
         'CubicR^2',
         'HollingIIR^2',
         #'HollingIIIR^2'
         ]
ModelStats = pd.DataFrame(rows, columns=heads)
ModelStats['ID'] = ModelStats['ID'].astype(int)  # Convert ID col from float
ModelStats.sort_values('ID', inplace=True)  # Order by ID

# Write to CSV
ModelStats.to_csv('../Data/ModelStats2.csv', index=False)
"""