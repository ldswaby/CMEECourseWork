#!/urs/bin/env python3

"""Script for model fitting"""

## Imports ##
#from lmfit import Model
import statsmodels.formula.api as smf
from lmfit import Minimizer, Parameters, report_fit
import lmfit
import numpy as np
import pandas as pd
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
#  1. Parameter optimization (and q start value estimation)
#  2. Why is Holling II/III so much worse than cubic? (plot)
#  3. Logging?

## Functions ##

t1 = time.perf_counter()

# Models

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
        #r_sqd = 1 - (np.sum((y - predict(x))**2))/(np.sum((y - np.mean(y))**2))
        #r_sqd = r2_score(y, predict(x))

        stats = smf.ols(formula='N_TraitValue ~ predict(ResDensity)', data=df).fit()

        aic = stats.aic
        bic = stats.bic
        #n = len(x)
        #rss = model[1][0]
        #p = n - len(model[0])
        #aic = AIC(n, p, rss)
        #bic = BIC(n, p, rss)

        # For plotting!
        #coef1, coef2, coef3, coef4 = model[0]

    except IndexError:
        aic, bic = None, None
        #coef1, coef2, coef3, coef4, aic, bic, r_sqd = None, None, None, None, None, None, None

    return aic, bic
    #return coef1, coef2, coef3, coef4, aic, bic, r_sqd


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

def fitHoll2(h, a, x, y, N):
    """Fit Holling II to data with start values  RANDOM UNIF DIST

    h: handling time
    a: attack rate
    x: ResDensity (vec)
    y: N_TraitValue (vec)
    N: no of parameter pairs to try
    """
    # Create ranges around params to test
    hrange = 0.8 * min(abs(h - 1e6), h)   # range around h to test
    arange = 0.8 * min(abs(a - 5e7), a)   # range around h to test

    # Set seed
    np.random.seed(0)

    #
    h_vals = [h] + [x for x in list(np.random.uniform(h - hrange, h + hrange, N))]
    a_vals = [a] + [x for x in list(np.random.uniform(a - arange, a + arange, N))]

    #h_vals = [h] + [np.exp(x) for x in list(np.random.uniform(np.log(1e-20), np.log(1e6), N))]
    #a_vals = [a] + [np.exp(x) for x in list(np.random.uniform(np.log(1e-20), np.log(5e7), N))]

    # Create 2 column array out of params
    paramsdf = pd.DataFrame(list(zip(h_vals, a_vals)), columns=['h', 'a'])

    # Initialize timer and counter
    timeout = time.time() + 5  # Set fitting time limit FOR EACH ID (5 seconds from now)
    groups = []
    i = 0

    # Fit until time runs out of all values have been tested
    while time.time() < timeout and i < N:
        params = paramsdf.loc[i]
        hi = params[0]
        ai = params[1]

        # store paramteters
        params_holl2 = Parameters()  # Create object for parameter storing
        params_holl2.add('h', value=hi, min=0, max=1e6)  # Add h param   1 week
        params_holl2.add('a', value=ai, min=0, max=5e7)  # Add a param   # Blue whale eats max 50 million krill per day # sett max just to outside bounds of possibility  e.g. whale eating how much and add 10%

        try:
            fit = lmfit.minimize(residHoll2, params_holl2, args=(x, y))

            h_best = fit.params['h'].value
            a_best = fit.params['a'].value

            #r_sqd = 1 - fit.redchi / np.var(y, ddof=2)
            #RSS = np.sum((y - holler_II(x, a_best, h_best)) ** 2)
            #TSS = np.sum((y - np.mean(y))**2)
            #r_sqd = 1 - RSS/TSS
            #print(r_sqd, r_sqd2)
            # Write stats to group tuple
            group = (h_best, a_best, fit.aic, fit.bic)
            groups.append(group)
            i += 1

        except ValueError:
            i += 1
            continue

    best_fit = min(groups, key=lambda t: t[2])  # take group with lowest AIC

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


def fitHoll3(h, a, x, y, N):
    """Fit Holling II to data with start values  RANDOM UNIF DIST

    h: handling time
    a: attack rate
    x: ResDensity (vec)
    y: N_TraitValue (vec)
    N: no of parameter pairs to try
    """
    # Create ranges around params to test
    hrange = 0.8 * min(abs(h - 1e6), h)  # range around h to test
    arange = 0.8 * min(abs(a - 5e7), a)  # range around h to test

    # Set seed
    np.random.seed(0)

    #
    h_vals = [h] + [x for x in list(np.random.uniform(h - hrange, h + hrange, N))]
    a_vals = [a] + [x for x in list(np.random.uniform(a - arange, a + arange, N))]

    #h_vals = [h] + [np.exp(x) for x in list(np.random.uniform(np.log(1e-20), np.log(1e6), N))]
    #a_vals = [a] + [np.exp(x) for x in list(np.random.uniform(np.log(1e-20), np.log(5e7), N))]

    # Create 2 column array out of params
    paramsdf = pd.DataFrame(list(zip(h_vals, a_vals)), columns=['h', 'a'])

    # Initialize timer and counter
    timeout = time.time() + 5  # Set fitting time limit FOR EACH ID (5 seconds from now)
    groups = []
    i = 0

    # Fit until time runs out of all values have been tested
    while time.time() < timeout and i < N:
        params = paramsdf.loc[i]
        hi = params[0]
        ai = params[1]

        # store paramteters
        params_holl3 = Parameters()  # Create object for parameter storing
        params_holl3.add('h', value=hi, min=0, max=1e6)  # Add h param   1 week
        params_holl3.add('a', value=ai, min=0, max=5e7)  # Add a param   # Blue whale eats max 50 million krill per day # sett max just to outside bounds of possibility  e.g. whale eating how much and add 10%
        params_holl3.add('q', value=0)

        try:
            fit = lmfit.minimize(residHoll3, params_holl3, args=(x, y))

            h_best = fit.params['h'].value
            a_best = fit.params['a'].value
            q_best = fit.params['q'].value

            #RSS = np.sum((y - holler_III(x, a_best, h_best, q_best)) ** 2)
            #TSS = np.sum((y - np.mean(y)) ** 2)
            #r_sqd = 1 - RSS / TSS
            # print(r_sqd, r_sqd2)
            # Write stats to group tuple
            group = (h_best, a_best, q_best, fit.aic, fit.bic)
            groups.append(group)
            i += 1

        except ValueError:
            i += 1
            continue

    best_fit = min(groups, key=lambda t: t[3])  # take group with lowest AIC

    return best_fit if groups else None


###############################################################################
# Load data
data = pd.read_csv("../Data/CRat_prepped.csv")
#data.set_index('ID', inplace=True)

##### FOR TESTING ########
#data = data.head(500)
#data = data[data['ID'] == 140]

##########################

ids = data['ID'].unique()

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

    ## Holing I
    #holl1AIC, holl1BIC = fit_polynomial(df, 1)
    #if None in [holl1AIC, holl1BIC]:
    #    print(f"Insufficient data to plot Holling II for ID '{id_}'.")

    # Quadratic Polynomial
    #quadAIC, quadBIC, quadR2 = fit_polynomial(x, y, 2)
    #if None in [quadAIC, quadBIC, quadR2]:
    #    print(f"Insufficient data to plot quadratic polynomial for ID '{id_}'.")

    # Cubic Polynomial
    cubeAIC, cubeBIC = fit_polynomial(df, 3)
    if None in [cubeAIC, cubeBIC]:
        print(f"Insufficient data to plot cubic polynomial for ID '{id_}'.")

    ######################### NON-LINEAR ###############################

    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            h, a = startValues(df)
        except RuntimeWarning:
            print(f"Insufficient data to fit for ID {id_}. Skipping.")
            return [id_] + [None] * 6

    # Holling II
    #h, a = optimizeParams(h, a, x, y, 30) # better values
    bestfit = fitHoll2(h, a, x, y, 1000)
    if bestfit:
        h2, a2, holl2aic, holl2bic = bestfit
    else:
        print(f"Insufficient data to plot Holling II for ID '{id_}'.")
        h2, a2, holl2aic, holl2bic = [None] * 4

    # Holling III
    bestfit = fitHoll3(h, a, x, y, 1000)
    if bestfit:
        h3, a3, q3, holl3aic, holl3bic = bestfit
    else:
        print(f"Insufficient data to plot Holling III for ID '{id_}'.")
        h3, a3, q3, holl3aic, holl3bic = [None] * 5

    statistics = [id_,
                  #holl1AIC,
                  #quadAIC,
                  cubeAIC,
                  holl2aic,
                  holl3aic,
                  #holl1BIC,
                  #quadBIC,
                  cubeBIC,
                  holl2bic,
                  holl3bic,
                  #holl1R2,
                  #quadR2,
                  #cubeR2,
                  #holl2R2,
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
         #'HollingIAIC',
         #'QuadraticAIC',
         'CubicAIC',
         'HollingIIAIC',
         'HollingIIIAIC',
         #'HollingIBIC',
         #'QuadraticBIC',
         'CubicBIC',
         'HollingIIBIC',
         'HollingIIIBIC'
         #'HollingIR^2',
         #'QuadraticR^2',
         #'CubicR^2',
         #'HollingIIR^2',
         #'HollingIIIR^2'
         ]
ModelStats = pd.DataFrame(rows, columns=heads)
ModelStats['ID'] = ModelStats['ID'].astype(int)  # Convert ID col from float
ModelStats.sort_values('ID', inplace=True)  # Order by ID

# Write to CSV
ModelStats.to_csv('../Data/ModelStats2.csv', index=False)
