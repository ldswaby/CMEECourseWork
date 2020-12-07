#!/urs/bin/env python3

"""Script for model fitting"""

## Imports ##
import statsmodels.formula.api as smf
import lmfit
import numpy as np
import pandas as pd
import sys
import time
import multiprocessing
from sklearn.metrics import r2_score  # because I'm lazy
from smt.sampling_methods import LHS


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

    model = np.polyfit(x, y, n, full=True)
    predict = np.poly1d(model[0])
    r_sqd = r2_score(y, predict(x))

    if r_sqd == 1:
        print(f"WARNING: insufficient data for ID {id_}\tto fit polynomial of "
              f"order {n}")
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
    """return sensible start values for params (Rodenbaum method)
    """
    Fmax = max(df['N_TraitValue'])
    Nhalf = min(df['ResDensity'], key=lambda x: abs(x - 0.5*Fmax))

    # h
    h = 1/Fmax  # As curve tends to 1/h

    # a
    a2 = Fmax/Nhalf   # a value for Holling type II
    a3 = Fmax/Nhalf**2   # a value for Holling type III

    return h, a2, a3

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

    N = 20  # Fix max number of param combos/runs to try

    x = df['ResDensity']
    y = df['N_TraitValue']

    # Create ranges around params to test
    hrange = 0.8 * min(abs(h - 1e6), h)
    arange = 0.8 * min(abs(a - 5e7), a)

    # Generate random parameter samples (using LHS to ensure entire parameter
    # space is covered)
    limits = np.array([[h-hrange, h+hrange], [a-arange, a+arange]])
    sampling = LHS(xlimits=limits)

    #plist = sampling(N)
    #fig = plt.figure()
    #ax = fig.gca()
    #ax.set_xticks(np.arange(h-hrange, h+hrange, (2*hrange)/N))
    #ax.set_yticks(np.arange(a-arange, a+arange, (2*arange)/N))
    #plt.plot(plist[:, 0], plist[:, 1], 'o')
    #plt.xlabel('h')
    #plt.ylabel('a')
    #plt.grid()
    # Turn off tick labels
    #ax.set_yticklabels([])
    #ax.set_xticklabels([])
    #plt.show()

    # Create 2 column array out of param samples (try initial estimates first)
    paramslist = np.append(np.array([h, a]), sampling(N)).reshape(N + 1, 2)

    # Initialize timer, counter, and groups list
    i = 0
    groups = []
    t = time.time() + timeout  # Set fitting time limit for each ID

    # Fit until time runs out of all values have been tested
    # TODO: Cut if a lower aic hasn't been found in? no point, I'm using time constraints
    while time.time() < t and i <= N:

        # Extract params to test
        testparams = paramslist[i]
        hi = testparams[0]
        ai = testparams[1]

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
            # If model is Holling III...
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

    #print(f'max runs = {i}')

    best_fit = min(groups, key=lambda grp: grp[0])  # take group with lowest AIC

    return best_fit if groups else None

###############################################################################
def returnStats(id_):
    """Fits models to curve and returns fit comparison stats and parameter
    estimates.
    """
    df = data[data['ID'] == id_]
    #print(f'starting {id_}')

    # Quadratic Polynomial
    #quadAIC, quadBIC = fitPolynomial(df, 2)
    #if None in [quadAIC, quadBIC]:
    #    return [None] * 14

    # Cubic Polynomial
    cubeAIC, cubeBIC = fitPolynomial(df, 3)
    if None in [cubeAIC, cubeBIC]:
        return None

    # Holling type I
    holl1aic, holl1bic, a1 = fitHollingI(df)

    ######################### NON-LINEAR ###############################

    # Generate sensible starting values
    h, ahol2, ahol3 = startValues(df)

    # Holling II
    bestfit = fitFuncResp(h, ahol2, df, 'HollingII', 3)
    if bestfit:
        holl2aic, holl2bic, h2, a2 = bestfit
    else:
        print(f"WARNING: insufficient data for ID {id_} to fit Holling II "
              f"model.")
        return None

    # Generalised Functional Response
    bestfit = fitFuncResp(h, ahol3, df, 'HollingIII', 3)
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
    print('\033[FFitting models to data...')  # Overwrite previous line (R)

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