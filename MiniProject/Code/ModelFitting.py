#!/urs/bin/env python3

"""Script for model fitting"""

## Imports ##
#from lmfit import Model
import statsmodels.formula.api as smf
from lmfit import Minimizer, Parameters, report_fit
import numpy as np
import pandas as pd
import scipy as sc

## Functions ##

# Models

def holler_II(x, a, h):
    """blabla"""
    return (a*x)/(1+h*a*x)

def holler_III(x, a, h, q):
    """blabla"""
    return (a*x**(q+1))/(1+h*a*x**(q+1))

# Load data
data = pd.read_csv("../Data/CRat_prepped.csv")
#data.set_index('ID', inplace=True)

#ids = data.index.unique()

# Pre-allocate empty array
ModelStats = np.empty((len(ids), 16))

# func for extracting stats
def returnStats(df):
    """blabla
    """
    # Extract exp/resp variables
    x = df['ResDensity'].tolist()
    y = df['N_TraitValue'].tolist()

    # Quadratic Polynomial
    quad = np.poly1d(np.polyfit(x, y, 2))
    quad_stats = smf.ols(formula='N_TraitValue ~ quad(ResDensity)',
                         data=df).fit()
    # Cubic Polynomial
    cube = np.poly1d(np.polyfit(x, y, 3))
    cube_stats = smf.ols(formula='N_TraitValue ~ cube(ResDensity)',
                         data=df).fit()  # Obtain OLS stats

    stats = np.array([quad_stats.aic, cube_stats.aic, quad_stats.bic, cube_stats.bic])
    heads = ['QuadraticAIC', 'CubicAIC', 'QuadraticBIC', 'CubicBIC']

    newdf = pd.DataFrame([stats], columns=heads)

    return newdf

#import time
#start = time.time()

la = data.groupby('ID').apply(returnStats)  # Takes 5.457477 s to run.
la.reset_index(inplace=True)

#print("Takes %f s to run." % (time.time() - start))



##################################################################
import numpy as np
import numpy.lib.recfunctions
from scipy import ndimage

x = pd.DataFrame({'d' : [1.,1.,1.,2.,2.,2.],
                  'c' : np.tile(['a','b','c'], 2),
                  'v' : np.arange(1., 7.)})

x = np.rec.fromarrays(([1,1,1,2,2,2],['a','b','c']*2,range(1, 7)), names='d,c,v')

unique, groups = np.unique(x['d'], False, True)
uniques = range(unique.size)
mins = ndimage.minimum(x['v'], groups, uniques)[groups]
maxs = ndimage.maximum(x['v'], groups, uniques)[groups]

x2 = np.lib.recfunctions.append_fields(x, 'v2', (x['v'] - mins)/(maxs - mins + 0.0))


ids, groups = np.unique(data['ID'], False, True)
ids_no = range(ids.size)


##################################################################



# Populate with stats
for i, curve_id in enumerate(ids):
    sub = data[data.index == curve_id]
    x = sub['ResDensity'].tolist()
    y = sub['N_TraitValue'].tolist()

    # Fit and obtain coefficients
    quad = np.polyfit(x, y, 2)
    cube = np.polyfit(x, y, 3)

    # Convery to polynomial
    f_quad = np.poly1d(quad)
    f_cube = np.poly1d(cube)

    # Obtain OLS stats
    quad_stats = smf.ols(formula='N_TraitValue ~ f_quad(ResDensity)', data=sub).fit()
    cube_stats = smf.ols(formula='N_TraitValue ~ f_cube(ResDensity)', data=sub).fit()

    ModelStats[i, :] = [curve_id,  # ID
                        min(x), max(x),  # min/max values
                        quad[0], quad[1], quad[2],  # Quaratic coeffs
                        cube[0], cube[1], cube[2], cube[3],  # Cubic coeffs
                        quad_stats.aic, cube_stats.aic,  # AIC values
                        quad_stats.bic, cube_stats.bic,  # BIC values
                        quad_stats.rsquared, cube_stats.rsquared]  # R squared


# Convert to dataframe and add heads
heads = ('ID', 'Min_ResDensity', 'Max_ResDensity', 'Quad_coeff1', 'Quad_coeff2',
         'Quad_coeff3', 'Cube_coeff1', 'Cube_coeff2', 'Cube_coeff3',
         'Cube_coeff4', 'QuadAIC', 'CubeAIC', 'QuadBIC', 'CubeBIC', 'QuadR2',
         'CubeR2')
ModelStats = pd.DataFrame(ModelStats, columns=heads)
"""

# 2

heads = ('ID', 'Min_ResDensity', 'Max_ResDensity', 'Quad_coeffs',
         'Cube_coeffs', 'QuadAIC', 'CubeAIC', 'QuadBIC',
         'CubeBIC', 'QuadR2', 'CubeR2')
ModelStats = pd.DataFrame(columns=heads)

for i, curve_id in enumerate(ids):
    sub = data[data.index == curve_id]
    x = sub['ResDensity'].tolist()
    y = sub['N_TraitValue'].tolist()

    # Fit
    quad = np.polyfit(x, y, 2)
    cube = np.polyfit(x, y, 3)

    # ?
    f_quad = np.poly1d(quad)
    f_cube = np.poly1d(cube)

    # Obtain OLS stats
    quad_stats = smf.ols(formula='N_TraitValue ~ f_quad(ResDensity)', data=sub).fit()
    cube_stats = smf.ols(formula='N_TraitValue ~ f_cube(ResDensity)', data=sub).fit()

    ModelStats.loc[i] = [str(curve_id),  # ID
                         min(x), max(x),  # min/max values
                         ','.join(map(str, list(f_quad))),  # Quaratic coeffs
                         ','.join(map(str, list(f_cube))),  # Cubic coeffs
                         quad_stats.aic, cube_stats.aic,  # AIC values
                         quad_stats.bic, cube_stats.bic,  # BIC values
                         quad_stats.rsquared, cube_stats.rsquared]  # R squared
"""

# Write to CSV
ModelStats.to_csv('../Results/ModelStats.csv', index=False)

# Set vars
"""
x = data['ResDensity'].tolist()
y = data['N_TraitValue'].tolist()


holler2 = Model(holler_II)
holler3 = Model(holler_III)

holler2.param_names
holler2.independent_vars

params = holler2.make_params()

result = holler2.fit(y, params, x=x)
"""


