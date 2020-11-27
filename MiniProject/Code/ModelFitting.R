
# TODO:
# 
################### Clear workspace #######################
rm(list = ls())
graphics.off()

####################### Imports ###########################
library(tidyverse)
library(plyr)
#library(frair)

# Load Data
FRData <- read.csv("../Data/CRat_prepped.csv", stringsAsFactors = FALSE)
#dplyr::glimpse(FRData)

ids <- unique(FRData$ID)

returnStats <- function(df){
  # df <- subset(FRData, ID == 721)
  x <- df$ResDensity
  y <- df$N_TraitValue
  
  ###################################
  # TODO: Also a problem that N_TraitValue is not an integer?
  #frair_test(y~x, df) # Why is it saying: 'No evidence for any response!'
  #frair_fit(formula, data, response, start=list(), fixed=NULL)
  #frair_fit(y~x, df, response='typeI', start=list(a=0.1), fixed=list(T=40/24))
  ###################################
  
  # Fit models
  Quad <- try(lm(y ~ poly(x, 2)), silent = TRUE)
  Cube <- try(lm(y ~ poly(x, 3)), silent = TRUE)
  
  quadAIC <- ifelse(class(Quad) == "try-error", NA, AIC(Quad))
  cubeAIC <- ifelse(class(Cube) == "try-error", NA, AIC(Cube))
  quadBIC <- ifelse(class(Quad) == "try-error", NA, BIC(Quad))
  cubeBIC <- ifelse(class(Cube) == "try-error", NA, BIC(Cube))
  quadRsqd <- ifelse(class(Cube) == "try-error", NA, summary(Quad)$r.squared)
  cubeRsqd <- ifelse(class(Cube) == "try-error", NA, summary(Cube)$r.squared)
  
  # Return stats row vector
  return(c(quadAIC, cubeAIC, quadBIC, cubeBIC, quadRsqd, cubeRsqd))
}


#############
#OUT <- matrix(NA, nrow = 306, ncol = 7)
#ids <- unique(FRData$ID)
#for (i in 1:length(ids)){
#  sub <- subset(FRData, ID == ids[i])
#  x <- sub$ResDensity
#  y <- sub$N_TraitValue
#  Quad <- lm(y ~ poly(y, 2))
#  Cube <- lm(x ~ poly(y, 3))
#  OUT[i,] <- c(ids[i], AIC(Quad), AIC(Cube), BIC(Quad), BIC(Cube),
#           summary(Quad)$r.squared, summary(Cube)$r.squared)
#}
#OUT <- as.data.frame(OUT)
#colnames(OUT) <- c('ID', 'QuadAIC', 'CubeAIC', 'QuadBIC', 'CubeBIC', 'QuadR2',
#                   'CubeR2')
#############

# Write dataframe of important model stats for each ID
ModStats <- ddply(FRData, .(ID), .fun = returnStats)
heads = c('ID', 'QuadraticAIC', 'CubicAIC', 'QuadraticBIC', 'CubicBIC', 'QuadraticR2',
          'CubeR2') # Takes 1.787297 s to run.
colnames(ModStats) <- heads



# Write to CSV file
write.csv(ModStats, '../Data/ModelStats.csv', row.names = FALSE)