import pandas as pd



# Load/inspect data
data = pd.read_csv("../Data/CRat.csv")
data.head()

# Subset cols
ReqCols = ['ID', 'ResDensity', 'N_TraitValue', 'ResDensityUnit', 'TraitUnit']
data = data[ReqCols]
data.set_index('ID', inplace=True)


# Check data types
data.dtypes

# Check for missing values
data.isna().any()