############## PLOTTING ##############
# Input modelstats csv headers must be full model name immediately followed by 'AIC'/'BIC'
# Any changes to this format will require changes to be made on lines 29 and 40 
# (change 3 to however many chars now follow the full model names in the headers)
# ALso assumes only other cols besides ID are aic/bic vals.

rm(list = ls())

library(plyr)
library(tidyverse)

frData <- read.csv('../Data/CRat_prepped.csv', stringsAsFactors = FALSE)
frModStats <- read.csv('../Data/ModelStats.csv', stringsAsFactors = FALSE)



################################################################################
################################### ANALYSE ####################################
################################################################################
# TODO:
# 1. drop Rsqd rows. Should these be included at all?
#frModStats <- frModStats[,1:5]
# 2. When a model doesn't fit, should the whole curve be dismissed from
#    the anaysis or just that particular model for that particular curve?
# Drop rows with +/-Inf values (bad fits) and NAs
#frModStats <- frModStats[!is.infinite(rowSums(frModStats)),]
#frModStats <- na.omit(frModStats)
################################################################################

model_count <- (length(frModStats)-6)/2 # assumes only other cols besides ID are aic/bic/rsqd vals and 5 coefficients (holl2 and 3)
model_names <- substr(names(frModStats[2:(1+model_count)]), 1, nchar(names(frModStats[2:(1+model_count)]))-4) #Assumes full model names precede the last 3 chars of header

compareModels <- function(row){
  id <- as.character(row[1])
  # Works for comparisons for any number of models
  #model_count <- (length(row)-6)/2 # assumes only other cols besides ID are aic/bic vals
  AICs <- sort(row[2:(1+model_count)])
  BICs <- sort(row[(2+model_count):(1+2*model_count)]) # or just until length(row) if no other cols are added
  
  # Extract model names (assumes the only charcters following the model names are 
  # 'AIC' or 'BIC' - as such only clips last 3)
  mod_names <- substr(names(AICs), 1, nchar(names(AICs))-4)
  
  ##################### Find best fit ###########################
  # Initialise best fit charcter vectors (can't preallocate as final length unknown)
  best_fits_aic <- c(AICs[1])
  best_fits_bic <- c(BICs[1])
  
  add_aic <- TRUE
  add_bic <- TRUE
  
  for (i in 2:model_count){
    # Calculate diffs
    deltaAIC <- abs(AICs[i] - AICs[i-1])
    deltaBIC <- abs(BICs[i] - BICs[i-1])
    
    ## Check best according to AIC ##
    while (add_aic){
      if (deltaAIC <= 2){
        # If difference with previous AIC is less than or equal to two
        # then diff insignificant; add to list
        best_fits_aic[i] <- AICs[i]
        break
      } else {
        add_aic <- FALSE
      }
    }
    
    ## Check best according to BIC ##
    while (add_bic){
      if (deltaBIC <= 2){
        # If difference with previous BIC is less than or equal to two
        # Add to list
        best_fits_bic[i] <- BICs[i]
        break
      } else {
        add_bic <- FALSE
      }
    }
  }
  
  names(best_fits_aic) <- mod_names[1:length(best_fits_aic)]
  names(best_fits_bic) <- mod_names[1:length(best_fits_bic)]
  
  # Standardise order (as ties don't matter)
  order <- c('Quadratic', 'Cubic', 'HollingII', 'GFR')
  aic <- names(best_fits_aic)[order(match(names(best_fits_aic), order))]
  bic <- names(best_fits_bic)[order(match(names(best_fits_bic), order))]
  
  # Combine into strings
  AICBestFit <- paste(aic, collapse = '/')
  BICBestFit <- paste(bic, collapse = '/')
  
  return(c(id, AICBestFit, BICBestFit))
}

## Merge best fit results to model stats (using apply over ddply for speed, tested
# with Sys.time())
bestFits <- as.data.frame(t(apply(frModStats, 1, compareModels)))
colnames(bestFits) <- c('ID', 'AICBestFits', 'BICBestFits')
bestFits$ID <- as.integer(bestFits$ID)
statsWithFits <- left_join(frModStats, bestFits, by = "ID")

############### Add columns for winning model(s) type #############################
addBestModelType <- function(x){
  if (x %in% c('HollingII', 'GFR', 'HollingII/GFR')){
    return('Mechanistic')
  } else if (x %in% c('Quadratic', 'Cubic', 'Quadratic/Cubic')){
    return('Phenomenological')
  } else {
    return('TIE')
  }
}

BestModelTypeAIC <- sapply(statsWithFits$AICBestFits, addBestModelType, USE.NAMES = FALSE)
statsWithFits$BestModelTypeAIC <- BestModelTypeAIC

BestModelTypeBIC <- sapply(statsWithFits$BICBestFits, addBestModelType, USE.NAMES = FALSE)
statsWithFits$BestModelTypeBIC <- BestModelTypeBIC

aicTypeBreakdown <- table(statsWithFits$BestModelTypeAIC)
bicTypeBreakdown <- table(statsWithFits$BestModelTypeBIC)

# Preallocate dataframe containing no. of datapoints best explained by each model
typefitdata <- data.frame(ModelType = rep(c('Phenomenological', 'Mechanistic'), times = 2), 
                      Estimator = rep(c('AIC', 'BIC'), each = 2),
                      Count = rep(NA, times = 4))

for (i in 1:nrow(typefitdata)){
  modtype <- typefitdata[i,'ModelType']
  stat <- typefitdata[i,'Estimator']
  if (stat == 'AIC'){
    typefitdata[i,'Count'] <- ifelse(is.na(aicTypeBreakdown[modtype]), 0, aicTypeBreakdown[[modtype]])
  } else {
    typefitdata[i,'Count'] <- ifelse(is.na(bicTypeBreakdown[modtype]), 0, bicTypeBreakdown[[modtype]])
  }
}


############ What percentage of the data is best fit by what model? ################
plotBestFits <- function(df, title){
  n <- nrow(df) 
  
  aicBreakdown <- table(df$AICBestFits)
  bicBreakdown <- table(df$BICBestFits)
  
  # Preallocate dataframe containing no. of datapoints best explained by each model
  fitdata <- data.frame(Model = rep(model_names, times = 2), 
                        Estimator = rep(c('AIC', 'BIC'), each = model_count),
                        Count = rep(NA, times = 2*model_count))
  
  # Load count of how many IDs were definititvely best fit by each model (draws excluded)
  for (i in 1:nrow(fitdata)){
    mod <- fitdata[i,'Model']
    stat <- fitdata[i,'Estimator']
    if (stat == 'AIC'){
      fitdata[i,'Count'] <- ifelse(is.na(aicBreakdown[mod]), 0, aicBreakdown[[mod]])
    } else {
      fitdata[i,'Count'] <- ifelse(is.na(bicBreakdown[mod]), 0, bicBreakdown[[mod]])
    }
  }
  
  # Plot
  ggplot(data = fitdata, aes(x = factor(Model), y = Count, fill = Estimator)) + 
    geom_bar(stat="identity", position = 'dodge') +
    ggtitle(title) +
    labs(x = 'Model', y = 'Best fits') + 
    theme_bw() +
    theme(legend.title = element_text(face="bold")) +
    geom_text(aes(label=paste(Count, ' (', round((Count/n)*100, 1), '%)', sep = '')), position=position_dodge(width=0.9), vjust=-0.5, cex = 2) +
    expand_limits(y = max(fitdata$Count)*1.02) +
    scale_fill_brewer(palette="Paired")
}

plotBestFits(statsWithFits, 'All Data')

##################### PASSIVE CONSUMERS #############################
pasvID <- unique(subset(frData, Con_ForagingMovement == "sessile")$ID)
pasvCons <- statsWithFits[statsWithFits$ID %in% pasvID,]
plotBestFits(pasvCons, "Passive Consumers")

##################### ACTIIVE CONSUMERS #############################
actvID <- unique(subset(frData, Con_ForagingMovement == "active")$ID)
actvCons <- statsWithFits[statsWithFits$ID %in% actvID,]
plotBestFits(actvCons, "Active Consumers")

#plotFits <- function(df){
  # df <- subset(frData, ID == 39909)
#  try({
#    id <- unique(df$ID)
    
#    x <- df$ResDensity
#    y <- df$N_TraitValue
#    x_units <- unique(df$ResDensityUnit)
#    y_units <- unique(df$TraitUnit)
    
    # Fit models
#    Quad <- lm(y ~ poly(x, 2))
#    Cube <- lm(y ~ poly(x, 3))
    
    # Generate a vector of the the x-axis variable
#    xvals <- seq(from = min(x), to = max(x), by = ((max(x) - min(x))/100))
    
    # Calculate predicted lines and write points to dataframe
#    y_quad <- predict.lm(Quad, data.frame(x = xvals))
#    y_cube <- predict.lm(Cube, data.frame(x = xvals))
#    data_to_fit <- data.frame(x = xvals, y_quad = y_quad, y_cube = y_cube)
    
    # Plot
#    p <- ggplot(aes(x = ResDensity, y = N_TraitValue), data = df) +
#      geom_point() + theme_bw() +
#      ggtitle(paste("ID:", id)) +
#      theme(legend.position = 'bottom') +
#      xlab(sprintf("log(Resource Density) (%s)", x_units)) +
#      ylab(sprintf("Trait Value (%s)", y_units)) +
#      geom_line(aes(x = x, y = y_quad, colour = "Quadratic"), data = data_to_fit) + 
#      geom_line(aes(x = x, y = y_cube, colour = "Cubic"), data = data_to_fit) +
#      scale_colour_manual("", breaks = c("Quadratic", "Cubic"), values = c("red", "blue"))
    
#    return(p)
#  }, silent = TRUE)
#}

# Create list of plots of curves
#plot_list <- dlply(frData, .(ID), plotFits)

# Print to pdf
#pdf('../Results/lala.pdf')
#for (i in 1:length(plot_list)){
#  print(plot_list[[i]])
#}
#dev.off()

