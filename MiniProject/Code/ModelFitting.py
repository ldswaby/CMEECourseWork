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
#data = data.head(500)
#data = data[data['ID'] == 3]

#mask = data['ID'].isin([2, 3, 39949, 140, 351, 445])
#data = data.loc[mask]

##########################

ids = data['ID'].unique()

## Functions ##

def AIC(N, Nvarys, rss):
    """Function to calc in same way as lmfit
    """
    return N * np.log(rss/N) + 2*Nvarys

def BIC(N, Nvarys, rss):
    """Function to calc in same way as lmfit
    """
    return N * np.log(rss/N) + np.log(N)*Nvarys

def fitPolynomial(df, n):
    """Fits polynomial of degree n to data x and y using numpy's polyfit
    """
    id_ = df['ID'].unique()[0]
    x = df['ResDensity']
    y = df['N_TraitValue']

    #if len(df) < n:
    #    print(f"WARNING: insufficient data for ID {id_}\tto fit polynomial of "
    #          f"order {n}.")
    #    return None, None

    model = np.polyfit(x, y, n, full=True)
    predict = np.poly1d(model[0])
    r_sqd = r2_score(y, predict(x))

    if r_sqd == 1:
        print(f"WARNING: insufficient data for ID {id_}\tto fit polynomial of "
              f"order {n}.")
        return None, None

    stats = smf.ols(formula='N_TraitValue ~ predict(ResDensity)',
                    data=df).fit()

    aic = stats.aic
    bic = stats.bic

    #rss = model[1][0] if len(model[1]) else 0
    #aic = AIC(len(x), len(model[0]), rss)
    #bic = BIC(len(x), len(model[0]), rss)

    return aic, bic

def fitHollingI(df):
    """Fits holling Type 1, returning a coefficient
    """
    id_ = df['ID'].unique()[0]
    x = np.array(df['ResDensity'])
    y = np.array(df['N_TraitValue'])

    # x needs to be a column vector instead of a 1D vector
    x = x[:, np.newaxis]

    a, rss, _, _ = np.linalg.lstsq(x, y, rcond=None)

    #predict = np.poly1d(np.append(a, 0))  # force y-intercept to 0
    #stats = smf.ols(formula='N_TraitValue ~ predict(ResDensity)',
    #                data=df).fit()

    aic = AIC(len(x), 1, rss[0])
    bic = BIC(len(x), 1, rss[0])

    return aic, bic, a[0]

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

#def startValues2(df, model):
#    """return sensible start values for params (Rodenbaum method)
#    """
#    Fmax = max(df['N_TraitValue'])
#    Nhalf = min(df['ResDensity'], key=lambda x: abs(x - 0.5*Fmax))

    # h
#    h = 1/Fmax  # As curve tends to 1/h

    # a
#    a2 = Fmax/Nhalf   # a value for Holling type II
#    a3 = Fmax/Nhalf**2   # a value for Holling type III

#    return h, a2, a3

def HollingII(x, a, h):
    """blabla"""
    return (a*x)/(1+h*a*x)

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

#def GFR(x, a, h, q):
#    """blabla"""
#    return (a*x**(q+1))/(1+h*a*x**(q+1))

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
    model = (v['a'] * x**2) / (1 + v['h'] * v['a'] * x**2)

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
    valid = {'HollingII', 'HollingIII'}
    if model not in valid:
        raise ValueError(f"model must be one of: {', '.join(valid)}.")

    N = 1000  # Fix max number of param combos/runs

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
            try:
                # Attempt fit
                fit = lmfit.minimize(residHoll2, params, args=(x, y))
            except ValueError:
                i += 1
                continue

        else:
            # If model is Generalised Functional Response...
            try:
                # Attempt fit
                fit = lmfit.minimize(residHoll3, params, args=(x, y))
            except ValueError:
                i += 1
                continue

        # Extract otimised parameters
        h_best = fit.params['h'].value
        a_best = fit.params['a'].value

        # Create tuple to return
        group = (fit.aic, fit.bic, h_best, a_best)

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
    #id_ = 39876
    df = data[data['ID'] == id_]
    #print(f'starting {id_}')

    # Quadratic Polynomial
    #quadAIC, quadBIC = fitPolynomial(df, 2)
    #if None in [quadAIC, quadBIC]:
    #    return [None] * 14

    #
    # Cubic Polynomial
    cubeAIC, cubeBIC = fitPolynomial(df, 3)
    if None in [cubeAIC, cubeBIC]:
        return None

    # Holing I
    holl1aic, holl1bic, a1 = fitHollingI(df)
    # if None in [holl1AIC, holl1BIC, holl1R2]:
    #    print(f"Insufficient data to plot Holling II for ID '{id_}'.")

    ######################### NON-LINEAR ###############################

    # Generate sensible starting values
    h, a = startValues(df)

    # Holing I
    #holl1aic, holl1bic, a1 = fitFuncResp(h, a, df, 'HollingI', 2)

    # Holling II
    bestfit = fitFuncResp(h, a, df, 'HollingII', 5)
    if bestfit:
        holl2aic, holl2bic, h2, a2 = bestfit
    else:
        print(f"WARNING: insufficient data for ID {id_} to fit Holling II "
              f"model.")
        return None

    # Generalised Functional Response
    bestfit = fitFuncResp(h, a, df, 'HollingIII', 5)
    if bestfit:
        holl3aic, holl3bic, h3, a3 = bestfit
    else:
        print(f"WARNING: insufficient data for ID {id_} to fit Generalised "
              f"Functional Response model.")
        return None

    statistics = [id_,
                  cubeAIC, holl1aic, holl2aic, holl3aic,
                  cubeBIC, holl1bic, holl2bic, holl3bic,
                  #cubeR2, holl2R2, holl3R2, quadR2
                  a1,
                  h2, a2,
                  h3, a3]

    return statistics

def main():
    """Run analysis
    """
    print('\nFitting models to data...\n')

    # Apply function and filter out failed IDs
    with multiprocessing.Pool() as pool:
        rows = list(filter(None, pool.map(returnStats, ids)))

    heads = ['ID',
             'Cubic_AIC', 'HollingI_AIC', 'HollingII_AIC', 'HollingIII_AIC',
             'Cubic_BIC', 'HollingI_BIC', 'HollingII_BIC', 'HollingIII_BIC',
             #'Cubic_Rsqd', 'HollingII_Rsqd', 'HollingIII_Rsqd',
             'a_Holl1',
             'h_Holl2', 'a_Holl2',
             'h_Holl3', 'a_Holl3']
    ModelStats = pd.DataFrame(rows, columns=heads)
    ModelStats['ID'] = ModelStats['ID'].astype(int)  # Convert ID col from float
    ModelStats.sort_values('ID', inplace=True)  # Order by ID

    # Write to CSV
    ModelStats.to_csv('../Data/ModelStats.csv', index=False)

    #print('\nDone!')

    return 0

if __name__ == '__main__':
    status = main()
    sys.exit(status)