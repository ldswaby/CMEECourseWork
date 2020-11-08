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
map('world', fill = TRUE, col="lightgreen")
map.axes(cex.axis=0.8)

# Plot points
points(gpdd$long, gpdd$lat, pch=1, col="red", cex=0.2)

# Looking at the map, what biases might you expect in any analysis based 
# on the data represented? include your answer as a comment at the end of your 
# R script.

# Nearly all the observations in the sample were made in the viscinity of 
# Europe/North America (lat 25-70, long -135-40), with only one in the Southern 
# Hemisphere and two east of the 40th meridian east. Almost all observations 
# were also made terrestrially. This indicates a strong sampling bias that could 
# invalidate results of any generalisation of the data to a wider region.

