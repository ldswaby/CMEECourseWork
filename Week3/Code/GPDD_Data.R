#################
#### Mapping ####
#################

# Import packages
library(tidyverse)
library(maps)

# Load and inspect data
load('../Data/GPDDFiltered.RData')
dplyr::glimpse(gpdd)

# Plot map
map('world', fill = FALSE)
map.axes(cex.axis=0.8)
points(gpdd$long, gpdd$lat, pch=1, col="red", cex=0.1)

# Looking at the map, what biases might you expect in any analysis based 
# on the data represented? include your answer as a comment at the end of your 
# R script.

# Looking at the map, it seems that all species in the sample were collected 
# from Europe/North America (lat -28.75-69, long -135-143), suggesting a strong
# sampling bias that could invalidate results of any generalisation of the
# data to a wider region.

