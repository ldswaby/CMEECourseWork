#!/urs/bin/env python3

"""Script for fitting a polynomial of degree n and Holling's type I, II,
and III models to the functional response dataset"""

## Imports ##

import sys
import time
import lmfit
import argparse
import numpy as np
import pandas as pd
import multiprocessing
from smt.sampling_methods import LHS
import statsmodels.formula.api as smf

## Variables ##

data = pd.read_csv("../Data/CRat_prepped.csv")  # Load data
ids = data['ID'].unique()

## Functions ##

def AIC(N, Nvarys, rss):
    """Function to calculate AIC using same formula as the lmfit module.

    Arguments:
        N: Number of data points
        Nvarys: Number of free parameters
        rss: Residual sum of squares
    """
    return N * np.log(rss/N) + 2*Nvarys

def BIC(N, Nvarys, rss):
    """Function to calculate BIC using same formula as the lmfit module.

    Arguments:
        N: Number of data points
        Nvarys: Number of free parameters
        rss: Residual sum of squares
    """
    return N * np.log(rss/N) + np.log(N)*Nvarys

def fitPolynomial(df, n):
    """Fits polynomial of degree n to functional response data using numpy's
    polyfit.

    Arguments:
        df: dataframe containing functional response data in 'ResDensity' and
            'N_TraitValue' columns
        n: degree of polynomial to fit

    Output:
        aic: fit AIC value
        bic: fit BIC value
    """
    id_ = df['ID'].unique()[0]
    x = df['ResDensity']
    y = df['N_TraitValue']

    model = np.polyfit(x, y, n, full=True)
    predict = np.poly1d(model[0])

    # Calculate R-squared
    RSS = np.sum((y - predict(x))**2)
    TSS = np.sum((y - np.mean(y))**2)
    r_sqd = 1 - RSS/TSS

    if r_sqd == 1:
        # Drop ID due to insufficient data points
        print(f"WARNING: insufficient data for ID {id_}\tto fit polynomial of "
              f"degree {n}")
        return None, None

    # Obtain OLS stats
    stats = smf.ols(formula='N_TraitValue ~ predict(ResDensity)',
                    data=df).fit()

    aic = stats.aic
    bic = stats.bic

    return aic, bic

def fitHollingI(df):
    """Fits C. S. Holling's type I functional response model to data.

    Arguments:
        df: dataframe containing functional response data in 'ResDensity' and
            'N_TraitValue' columns

    Output:
        aic: fit AIC value
        bic: fit BIC value
        a: estimate for attack rate parameter
    """
    x = np.array(df['ResDensity'])
    y = np.array(df['N_TraitValue'])

    # x needs to be a column vector instead of a 1D vector
    x = x[:, np.newaxis]

    a, rss, _, _ = np.linalg.lstsq(x, y, rcond=None)

    aic = AIC(len(x), 1, rss[0])
    bic = BIC(len(x), 1, rss[0])

    return aic, bic, a[0]

def startValues(df):
    """Return sensible start values for parameters a (attack rate) and h
    (handling time) for C. S. Holling's type II and III functional response
    models.

    Arguments:
        df: dataframe containing functional response data in 'ResDensity' and
            'N_TraitValue' columns

    Outputs:
        h: an initial value estimate for the handling time
        a2: an initial value estimate for the attack rate in the type II model
        a3: an initial value estimate for the attack rate in the type III model
    """
    Fmax = max(df['N_TraitValue'])
    Nhalf = min(df['ResDensity'], key=lambda x: abs(x - 0.5*Fmax))

    # Handling time
    h = 1/Fmax  # As curve tends to 1/h

    # Attack rate
    a2 = Fmax/Nhalf   # a value for Holling type II
    a3 = Fmax/Nhalf**2   # a value for Holling type III

    return h, a2, a3

def residHoll2(params, x, y):
    """Returns residuals between observed data and predicted values on C. S.
    Holling's type II functional response model.

    Arguments:
        params: a parameters object storing initial value estimates for the
                attack rate and handling time.
        x: Resource density data values
        y: Corresponding N_TraitValue data values
    """
    v = params.valuesdict()  # Get an ordered dictionary of parameter values

    model = (v['a'] * x) / (1 + v['h'] * v['a'] * x)  # Holling II model

    # Return residuals
    return model - y

def residHoll3(params, x, y):
    """Returns residuals between observed data and predicted values on C. S.
    Holling's type III functional response model.

    Arguments:
        params: A parameters object storing initial value estimates for the
                attack rate and handling time.
        x: Resource density data values
        y: Corresponding N_TraitValue data values
    """
    v = params.valuesdict()  # Get an ordered dictionary of parameter values

    model = (v['a'] * x**2) / (1 + v['h'] * v['a'] * x**2)  # Holling II model

    # Return residuals
    return model - y

def fitFuncResp(h, a, df, model, timeout, N):
    """Fits Holling's type II and III functinal response models to input data.

    Arguments:
        h: Handling time initial value estimate
        a: Attack rate initial value estimate
        df: dataframe containing functional response data in 'ResDensity' and
            'N_TraitValue' columns
        timeout: Maximum time to spend fitting
        N: Maximum number of parameter combinations to try

    Outputs:
        best_fits: tuple of fit statistics and parameter estimates for the best
        fit (i.e. with the lowest AIC score)
    """
    valid = {'HollingII', 'HollingIII'}
    if model not in valid:
        raise ValueError(f"model must be one of: {', '.join(valid)}.")

    x = df['ResDensity']
    y = df['N_TraitValue']

    # Create ranges around params to test
    hrange = 0.8 * min(abs(h - 1e6), h)
    arange = 0.8 * min(abs(a - 5e7), a)

    # Generate random parameter samples using LHS to ensure maximal coverage
    # of the parameter space
    limits = np.array([[h-hrange, h+hrange], [a-arange, a+arange]])
    sampling = LHS(xlimits=limits)

    # Create 2 column array out of param samples (try initial estimates first)
    paramslist = np.append(np.array([h, a]), sampling(N)).reshape(N + 1, 2)

    # Initialize timer, counter, and groups list
    i = 0
    groups = []
    t = time.time() + timeout  # Set fitting time limit for each ID

    # Fit until time runs out of all values have been tested
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

    best_fit = min(groups, key=lambda grp: grp[0])  # take group with lowest AIC

    return best_fit if groups else None

def returnStats(id_):
    """Fits cubic polynomial and C. S. Holling's type I, II, and III functional
    response models to data and returns row list of fit statistics and parameter
    estimates.

    Arguments:
        id_: ID of data set to fit to

    Output:
        statistics: row list of the id_, the AIC and BIC values for the fitted
                        models, and estimates for their parameters.
    """
    df = data[data['ID'] == id_]

    ### LINEAR ###

    # Cubic Polynomial
    cubeAIC, cubeBIC = fitPolynomial(df, 3)
    if None in [cubeAIC, cubeBIC]:
        return None

    # Holling type I
    holl1aic, holl1bic, a1 = fitHollingI(df)

    ### NON-LINEAR ###

    # Generate sensible starting values for C. S. Holling higher order models
    h, ahol2, ahol3 = startValues(df)

    # Holling II
    bestfit = fitFuncResp(h, ahol2, df, 'HollingII', timeout=3, N=30)
    if bestfit:
        holl2aic, holl2bic, h2, a2 = bestfit
    else:
        print(f"WARNING: insufficient data for ID {id_} to fit Holling II "
              f"model.")
        return None

    # Generalised Functional Response
    bestfit = fitFuncResp(h, ahol3, df, 'HollingIII', timeout=3, N=30)
    if bestfit:
        holl3aic, holl3bic, h3, a3 = bestfit
    else:
        print(f"WARNING: insufficient data for ID {id_} to fit Generalised "
              f"Functional Response model.")
        return None

    statistics = [id_,
                  cubeAIC, holl1aic, holl2aic, holl3aic,
                  cubeBIC, holl1bic, holl2bic, holl3bic,
                  a1,
                  h2, a2,
                  h3, a3]

    return statistics

def main(outpath):
    """Run analysis

    Arguments:
        outpath: CSV file path string to write output statistics
    """
    print('\033[FFitting models to data...')  # Overwrite previous line (R)

    # Apply function and filter out failed IDs
    with multiprocessing.Pool() as pool:
        rows = list(filter(None, pool.map(returnStats, ids)))

    heads = ['ID',
             'Cubic_AIC', 'HollingI_AIC', 'HollingII_AIC', 'HollingIII_AIC',
             'Cubic_BIC', 'HollingI_BIC', 'HollingII_BIC', 'HollingIII_BIC',
             'a_Holl1',
             'h_Holl2', 'a_Holl2',
             'h_Holl3', 'a_Holl3']
    ModelStats = pd.DataFrame(rows, columns=heads)
    ModelStats['ID'] = ModelStats['ID'].astype(int)  # Convert ID col from float
    ModelStats.sort_values('ID', inplace=True)  # Order by ID

    # Write to CSV
    ModelStats.to_csv(outpath, index=False)

    return 0

if __name__ == '__main__':

    ## Parse Arguments ##
    parser = argparse.ArgumentParser(
        description="Script for fitting a polynomial of degree n and Holling's "
                    "type I, II, and III models to the functional response "
                    "dataset")
    parser.add_argument("-o", "--outpath", default="../Data/ModelStats.csv",
                        help="CSV file path string to write output "
                             "statistics.")
    args = parser.parse_args()

    status = main(args.outpath)  # run functions
    sys.exit(status)