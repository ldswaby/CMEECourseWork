############## PLOTTING ##############
# Input modelstats csv headers must be full model name immediately followed by 'AIC'/'BIC'
# Any changes to this format will require changes to be made on lines 29 and 40 
# (change 3 to however many chars now follow the full model names in the headers)
# ALso assumes only other cols besides ID are aic/bic vals.

rm(list = ls())

library(plyr)
library(tidyverse)

Data <- read.csv('../Data/CRat_prepped.csv', stringsAsFactors = FALSE)
ModStats <- read.csv('../Data/STATS.csv', stringsAsFactors = FALSE)
#mergedData <- dplyr::left_join(frData, frModStats, by = "ID")
##################################################################################
ids <- unique(ModStats$ID)

holling2 <- function(h, a, R){
  num <- a*R
  denom <- 1+a*h*R
  return(num/denom)
}

pdf('../Results/modelplots.pdf')
for (id in ids){
  #id <- 39835
  sub <- subset(Data, ID == id)
  stats <- subset(ModStats, ID == id)
  x <- sub$ResDensity
  y <- sub$N_TraitValue
  
  # Models
  try(Cube <- lm(y ~ poly(x, 3)), silent = T)
  Holl1 <- lm(y ~ x)
  # x axis
  xvals <- seq(from = min(x), to = max(x), by = ((max(x) - min(x))/100))
  # y axis
  y_holl1 <- predict.lm(Holl1, data.frame(x = xvals))
  try(y_cube <- predict.lm(Cube, data.frame(x = xvals)), silent = T)
  y_holl2 <- holling2(stats$h_Holl2, stats$a_Holl2, xvals)
  
  # Plot
  plot(x, y)
  lines(xvals, y_holl1, col = 2, lwd = 2.5)
  try(lines(xvals, y_cube, col = 3, lwd = 2.5), silent = T)
  lines(xvals, y_holl2, col = 4, lwd = 2.5)
  legend("topleft", legend = c("Holling I", "Cubic", "Holling II"), lwd=2, lty=1, col=2:4)
}
dev.off()

holling3 <- function(R, a, h, q){
  num <- a*R^(q+1)
  denom <- 1+a*h*R^(q+1)
  return(num/denom)
}
