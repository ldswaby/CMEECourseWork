############## PLOTTING ##############
# Input modelstats csv headers must be full model name immediately followed by 'AIC'/'BIC'
# Any changes to this format will require changes to be made on lines 29 and 40 
# (change 3 to however many chars now follow the full model names in the headers)
# ALso assumes only other cols besides ID are aic/bic vals.

rm(list = ls())

# Imports
suppressMessages(library(tidyverse))
suppressMessages(library(plyr))
suppressMessages(library(janitor))
suppressMessages(library(gridExtra))
suppressMessages(library(grid))
suppressMessages(library(scales))

# Load data
frData <- read.csv('../Data/CRat_prepped.csv', stringsAsFactors = FALSE)
frModStats <- read.csv('../Data/ModelStats.csv', stringsAsFactors = FALSE)

# Extract model information
model_count <- (length(frModStats)-6)/2 # assumes only other cols besides ID are aic/bic/rsqd vals and 5 coefficients (holl2 and 3)
ord <- c('Cubic', 'HollingI', 'HollingII', 'GFR')
model_names <- substr(names(frModStats[2:(1+model_count)]), 1, nchar(names(frModStats[2:(1+model_count)]))-4) #Assumes full model names precede the last 3 chars of header
model_names <- model_names[order(match(model_names, ord))] # Order

##############################################################################
######################### Overlayed plots ###################################
#############################################################################
cat('\nPlotting fits...')

## Functions ##
holling2 <- function(R, a, h){
  num <- a*R
  denom <- 1+a*h*R
  return(num/denom)
}

holling3 <- function(R, a, h){
  num <- a*R^2
  denom <- 1+a*h*R^2
  return(num/denom)
}


plotFits <- function(id){
  df <- subset(frData, ID == id)
  stats <- subset(frModStats, ID == id)
  
  try({
    ResDensity <- df$ResDensity
    N_TraitValue <- df$N_TraitValue
    x_units <- unique(df$ResDensityUnit)
    y_units <- unique(df$TraitUnit)
    
    # Fit models
    #Quad <- lm(y ~ poly(x, 2))
    Cube <- lm(N_TraitValue ~ poly(ResDensity, 3))
    
    # Generate a vector of the the x-axis variable
    x <- seq(from = min(ResDensity), to = max(ResDensity), by = ((max(ResDensity) - min(ResDensity))/100))
    
    
    # Calculate predicted lines and write points to dataframe
    y_cube <- predict.lm(Cube, data.frame(ResDensity = x))
    y_holl1 <- stats$a_Holl1 * x
    y_holl2 <- holling2(x, stats$a_Holl2, stats$h_Holl2)
    y_holl3 <- holling3(x, stats$a_Holl3, stats$h_Holl3)
    
    data_to_fit <- data.frame(x = x, y_cube = y_cube, y_holl1 = y_holl1, y_holl2 = y_holl2, y_holl3 = y_holl3)
    
    # Plot
    p <- ggplot(aes(x = ResDensity, y = N_TraitValue), data = df) +
      geom_point(shape=I(4)) + theme_bw() +
      ggtitle(paste("ID:", id)) +
      theme(plot.title = element_text(size=8, hjust = 1)) +
      theme(legend.position = 'right') +
      xlab(NULL) +
      ylab(NULL) +
      geom_line(aes(x = x, y = y_cube, colour = "Cubic"), data = data_to_fit, size = 0.4) +
      geom_line(aes(x = x, y = y_holl1, colour = "Type I"), data = data_to_fit, size = 0.4) + 
      geom_line(aes(x = x, y = y_holl2, colour = "Type II"), data = data_to_fit, size = 0.4) +
      geom_line(aes(x = x, y = y_holl3, colour = "Type III"), data = data_to_fit, size = 0.4) +
      scale_colour_manual("", breaks = c("Cubic", "Type I", "Type II", "Type III"), values = c("green4", "blue", "red", "purple")) 
    
    if (id == 39951){
      p <- p + annotate(geom = 'text', label = 'Cubic', x = -Inf, y = Inf, hjust = -0.3, vjust = 2)
    } else if (id == 39896){
      p <- p + annotate(geom = 'text', label = 'Type I', x = -Inf, y = Inf, hjust = -0.3, vjust = 2)
    } else if (id == 39894){
      p <- p + annotate(geom = 'text', label = 'Type II', x = -Inf, y = Inf, hjust = -0.3, vjust = 2)
    } else if (id == 39904){
      p <- p + annotate(geom = 'text', label = 'Type III', x = -Inf, y = Inf, hjust = -0.3, vjust = 2)
    } else {
      return(p)
    }
    
    return(p)
  }, silent = TRUE)
}

###### PRINT ALL FITS ########
#ids <- unique(frModStats$ID)
#pdf('../Results/ALLFITS.pdf')
#for (id in ids){
#  print(plotFits(id))
#}
#dev.off()
##############################

#pdf('../Results/typeIIIfilterfeeders.pdf')
#ids <- c(39883, 39899, 39901, 39904, 39949, 39973, 39987, 39993, 39997, 39999, 40006, 40017, 40035, 40061, 40064, 40099, 40105)
#for (id in ids){
#  print(plotFits(id))
#}
#dev.off()

pl <- lapply(c(39951, 39896, 39894, 39904), FUN = plotFits)

# Function to extract legend
# https://github.com/hadley/ggplot2/wiki/Share-a-legend-between-two-ggplot2-graphs
g_legend <- function(a.gplot){
  tmp <- ggplot_gtable(ggplot_build(a.gplot))
  leg <- which(sapply(tmp$grobs, function(x) x$name) == "guide-box")
  legend <- tmp$grobs[[leg]]
  return(legend) 
}

# Extract legend as a grob
leg = g_legend(pl[[1]])

demplots <- grid.arrange(
  arrangeGrob(grobs=lapply(pl, function(p) p + guides(colour=FALSE)), ncol=2,
              bottom=textGrob("Resource Density", gp=gpar(fontface="bold", fontsize=10)), 
              left=textGrob("Consumption Rate", gp=gpar(fontface="bold", fontsize=10), rot=90)),
  leg, 
  widths=c(9,1.5)
)

ggsave("../Results/ModelFits.pdf", demplots, width = 6.12, height = 5.42)

##################################################################################
######################### Prepare/Combine Data ###################################
##################################################################################
cat('\rCombining data...')

# Function for comparing model fits for each ID by both AIC and BIC.
compareModels <- function(row){
  id <- as.character(row[1])
  
  # Works for comparisons for any number of models
  AICs <- sort(row[2:(1+model_count)])
  BICs <- sort(row[(2+model_count):(1+2*model_count)])
  
  # Extract model names (assumes the only charcters following the model names are 
  # 'AIC' or 'BIC' - as such only clips last 3)
  mod_names <- substr(names(AICs), 1, nchar(names(AICs))-4)
  
  ## Find best fit(s) 
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
  
  # Name elements
  names(best_fits_aic) <- mod_names[1:length(best_fits_aic)]
  names(best_fits_bic) <- mod_names[1:length(best_fits_bic)]
  
  # Combine into strings
  AICBestFit <- paste(names(best_fits_aic), collapse = '/')
  BICBestFit <- paste(names(best_fits_bic), collapse = '/')
  
  return(c(id, AICBestFit, BICBestFit))
}

# Merge best fit results to model stats (using apply over ddply for speed, tested with Sys.time())
bestFits <- as.data.frame(t(apply(frModStats, 1, compareModels)))

# Rename cols                                       
colnames(bestFits) <- c('ID', 'BestModelAIC', 'BestModelBIC')                                          

# Function for extracting model with lowest AIC, rule of 2 ignored
NoRuleof2 <- function(vec){    
  bestfits <- strsplit(vec, '/') # Split strngs into vectors
  return(sapply(bestfits, function(x) x[1]))
}

# Add columns
bestFits$BestModelAIC_NoRule2 <- NoRuleof2(bestFits$BestModelAIC)
bestFits$BestModelBIC_NoRule2 <- NoRuleof2(bestFits$BestModelBIC)

# Reset column type
bestFits$ID <- as.integer(bestFits$ID)

# Join with main dataframe
statsWithFits <- left_join(frModStats, bestFits, by = "ID")
metadata <- frData[!duplicated(frData[,1]),][,-c(2,3)] # drop rows with duplicate IDs as metadata same for each ID, and delete N_TraitValue and ResDensity
ALLDATA <- right_join(metadata, statsWithFits, by = "ID") # create df of all relevant fields

################## Add columns for winning model(s) type #############################
# Function to determine whether winning model(s) are phenomenological or mechanistic
addBestModelType <- function(x){
  # Mechanistic
  mech <- c('HollingI', 'HollingII', 'HollingIII')
  mech2perms <- apply(expand.grid(mech, mech), 1, function(x) paste(x, collapse = '/'))
  mech3perms <- apply(expand.grid(mech, mech, mech), 1, function(x) paste(x, collapse = '/'))
  allmechs <- c(mech, mech2perms, mech3perms)
  # Phenomenological
  phnm <- c('Quadratic', 'Cubic')
  phnm2perms <- apply(expand.grid(phnm, phnm), 1, function(x) paste(x, collapse = '/'))
  phnm3perms <- apply(expand.grid(phnm, phnm, phnm), 1, function(x) paste(x, collapse = '/'))
  allphnms <- c(phnm, phnm2perms, phnm3perms)
  if (x %in% allmechs){ # all permutations
    return('Mechanistic')
  } else if (x %in% allphnms){ # all permutations
    return('Phenomenological')
  } else {
    return('TIE')
  }
}

# AIC
BestModelTypeAIC <- sapply(ALLDATA$BestModelAIC, addBestModelType, USE.NAMES = FALSE) # Rule of 2
BestModelTypeAIC_NoRule2 <- sapply(ALLDATA$BestModelAIC_NoRule2, addBestModelType, USE.NAMES = FALSE) # No rule of 2
ALLDATA$BestModelTypeAIC <- BestModelTypeAIC
ALLDATA$BestModelTypeAIC_NoRule2 <- BestModelTypeAIC_NoRule2

# BIC
BestModelTypeBIC <- sapply(ALLDATA$BestModelBIC, addBestModelType, USE.NAMES = FALSE) # Rule of 2
BestModelTypeBIC_NoRule2 <- sapply(ALLDATA$BestModelBIC_NoRule2, addBestModelType, USE.NAMES = FALSE) # No rule of 2
ALLDATA$BestModelTypeBIC <- BestModelTypeBIC
ALLDATA$BestModelTypeBIC_NoRule2 <- BestModelTypeBIC_NoRule2


################## Add FeedType metadata col ##########################
# Function for adding a column specifying whether the organism is a filter feeder
filterFeed <- function(vec){
  # Strip spaces and convert to lowercase
  stnd <- tolower(gsub(' ', '', vec, fixed = TRUE))
  filtfeeders <- c('rotifer', 'shrimp', 'copepod', 'daphnia', 'amphipod', 'krill', 
                   'euphasiid', 'amphipod', 'larva', 'larvae', 'maggot', 'bivalve', 
                   'appendicularian', 'polychaete', 'bladderwort', 'seastar', 
                   'webbuilder')
  pattern <- paste(filtfeeders, collapse = '|')
  result <- grepl(pattern, stnd)
  return(sapply(result, function(x) ifelse(isTRUE(x), 'Filter feeder', 'Non-filter feeder')))
}

ALLDATA$FilterFeeder <- filterFeed(ALLDATA$ConCommon)

######################################################################
######################### Plotting ###################################
######################################################################
cat('\rBar plots...')

# Function for plotting the breakdown of best fits according to both AIC and BIC, 
# and with and withut the Rule of Two applied...
plotBestFits <- function(df, fac){
  # Evaluate args
  if(!fac %in% c('Model', 'Model Type')) return("fac must be one of: 'Model', 'Type'")
  
  # no of levels
  no <- ifelse(fac=='Model Type', 2, model_count)
  
  # define levels
  if (fac == 'Model Type'){
    lvls <- c('Phenomenological', 'Mechanistic')
    aicBreakdown <- table(ALLDATA[,'BestModelTypeAIC_NoRule2'])
    bicBreakdown <- table(ALLDATA[,'BestModelTypeBIC_NoRule2'])
    aicBreakdownRO2 <- table(ALLDATA[,'BestModelTypeAIC'])
    bicBreakdownRO2 <- table(ALLDATA[,'BestModelTypeBIC'])
  } else { # if fac == 'Model'
    lvls <- model_names
    aicBreakdown <- table(ALLDATA[,'BestModelAIC_NoRule2'])
    bicBreakdown <- table(ALLDATA[,'BestModelBIC_NoRule2'])
    aicBreakdownRO2 <- table(ALLDATA[,'BestModelAIC'])
    bicBreakdownRO2 <- table(ALLDATA[,'BestModelBIC'])
  }
  
  fitdata <- data.frame(Level = rep(lvls, times = 4), 
                        Estimator = rep(c('AIC', 'BIC'), each = 2*no),
                        RO2 = rep(c('Rule of Two', 'No Rule of Two'), times = 2, each=no),
                        Count = rep(NA, times = 4*no))
  
  # Load count of how many IDs were definititvely best fit by each model (draws excluded)
  for (i in 1:nrow(fitdata)){
    lvl <- fitdata[i,'Level']
    stat <- fitdata[i,'Estimator']
    ro2 <- fitdata[i,'RO2']
    if (ro2 == 'No Rule of Two'){
      if (stat == 'AIC'){
        fitdata[i,'Count'] <- ifelse(is.na(aicBreakdown[lvl]), 0, aicBreakdown[[lvl]])
      } else {
        fitdata[i,'Count'] <- ifelse(is.na(bicBreakdown[lvl]), 0, bicBreakdown[[lvl]])
      }
    } else {
      if (stat == 'AIC'){
        fitdata[i,'Count'] <- ifelse(is.na(aicBreakdownRO2[lvl]), 0, aicBreakdownRO2[[lvl]])
      } else {
        fitdata[i,'Count'] <- ifelse(is.na(bicBreakdownRO2[lvl]), 0, bicBreakdownRO2[[lvl]])
      }
    }
  }
  
  nro2 <- sum(fitdata$Count[1:no])
  nnotro2 <- sum(fitdata$Count[(no+1):(2*no)])
  fitdata$Total <- rep(c(nro2, nnotro2), each = no) # Add total
  fitdata$Percentage <- (fitdata$Count/fitdata$Total)*100 # Add percentage of IDs best fit
  # when the rule of 2 is applied there will be different totals (as ties are ignored)
  
  # Plot
  p <- ggplot(data = fitdata, aes(x = factor(Level, levels = lvls), y = Percentage, fill = Estimator)) + 
    facet_wrap(~RO2) +
    geom_bar(stat="identity", position = 'dodge2') +
    labs(x = fac, y = 'Best Fits (%)') + 
    theme_bw() +  theme(aspect.ratio=1) +
    theme(legend.title = element_text(face="bold")) +
    geom_text(aes(label=paste(round(Percentage), '% (', Count, ')', sep = '')), position=position_dodge(width=0.9), vjust=-0.5, cex = 6-no) +
    scale_fill_brewer(palette="Paired") +
    scale_y_continuous(limits=c(0,max(fitdata$Percentage)*1.02))
  
  return(p)
}

######### Model Comparison ##########
p1 <- plotBestFits(ALLDATA, 'Model')
ggsave("../Results/ModelComparisonBar.pdf", p1, width=11, height=5)

###### Model Type Comparison ########
p2 <- plotBestFits(ALLDATA, 'Model Type')
ggsave("../Results/TypeComparisonBar.pdf", p2, width=11, height=5)


###################################################################################
############################# Trend Exploration ###################################
###################################################################################
cat('\Tabulations...')
############################# Foraging Movement ###################################
# Consumer 
con_mvmt <- ALLDATA %>%
            tabyl(Con_ForagingMovement, BestModelAIC_NoRule2) %>% # create table
            adorn_totals("row") %>% # add total counts
            adorn_percentages("row") %>% # add percentages
            adorn_pct_formatting(rounding = "half up", digits = 0) %>% # round to 2dp
            adorn_ns() %>% # add counts
            dplyr::rename("Consumer Foraging Movement" = "Con_ForagingMovement") # rename columns

write.csv(con_mvmt, file = '../Results/Consumer_Movement.csv', quote = FALSE, row.names = FALSE)

# Resource 
res_mvmt <- ALLDATA %>%
            tabyl(Res_ForagingMovement, BestModelAIC_NoRule2) %>% # create table
            adorn_totals("row") %>% # add total counts
            adorn_percentages("row") %>% # add percentages
            adorn_pct_formatting(rounding = "half up", digits = 0) %>% # round to 2dp
            adorn_ns() %>% # add counts
            dplyr::rename("Resource Foraging Movement" = "Res_ForagingMovement") # rename columns

write.csv(res_mvmt, file = '../Results/Resource_Movement.csv', quote = FALSE, row.names = FALSE)

################################# Habitat #######################################
habitat <- ALLDATA %>%
          tabyl(Habitat, BestModelAIC_NoRule2) %>% # create table
          adorn_totals("row") %>% # add total counts
          adorn_percentages("row") %>% # add percentages
          adorn_pct_formatting(rounding = "half up", digits = 0) %>% # round to 2dp
          adorn_ns() # add counts

write.csv(habitat, file = '../Results/Habitat.csv', quote = FALSE, row.names = FALSE)

############################# Experiment Type ###################################
labfield <- ALLDATA %>%
            tabyl(LabField, BestModelAIC_NoRule2) %>% # create table
            adorn_totals("row") %>% # add total counts
            adorn_percentages("row") %>% # add percentages
            adorn_pct_formatting(rounding = "half up", digits = 0) %>% # round to 2dp
            adorn_ns()  %>% # add counts
            dplyr::rename("Experiment Type" = 'LabField')

write.csv(labfield, file = '../Results/LabField.csv', quote = FALSE, row.names = FALSE)

############################# Dimensionality ###################################
# Consumer Movement
con_mvmt_dim <- ALLDATA %>%
                tabyl(Con_MovementDimensionality, BestModelAIC_NoRule2) %>% # create table
                adorn_totals("row") %>% # add total counts
                adorn_percentages("row") %>% # add percentages
                adorn_pct_formatting(rounding = "half up", digits = 0) %>% # round to 2dp
                adorn_ns() %>% # add counts
                dplyr::rename("Consumer Movement Dimensionality" = 'Con_MovementDimensionality')

write.csv(con_mvmt_dim, file = '../Results/ConMvmtDim.csv', quote = FALSE, row.names = FALSE)

# Resource Movement
res_mvmt_dim <- ALLDATA %>%
                tabyl(Res_MovementDimensionality, BestModelAIC_NoRule2) %>% # create table
                adorn_totals("row") %>% # add total counts
                adorn_percentages("row") %>% # add percentages
                adorn_pct_formatting(rounding = "half up", digits = 0) %>% # round to 2dp
                adorn_ns() %>% # add counts
                dplyr::rename("Resource Movement Dimensionality" = 'Res_MovementDimensionality')
  
write.csv(res_mvmt_dim, file = '../Results/ResMvmtDim.csv', quote = FALSE, row.names = FALSE)

# Consumer-Resource Detection
con_res_detect <- ALLDATA %>%
                  tabyl(Con_RESDetectionDimensionality, BestModelAIC_NoRule2) %>% # create table
                  adorn_totals("row") %>% # add total counts
                  adorn_percentages("row") %>% # add percentages
                  adorn_pct_formatting(rounding = "half up", digits = 0) %>% # round to 2dp
                  adorn_ns() %>% # add counts
                  dplyr::rename("Consumer-Resource Detection Dimensionality" = 'Con_RESDetectionDimensionality')
  
write.csv(con_res_detect, file = '../Results/ConResDetectDim.csv', quote = FALSE, row.names = FALSE)

# Resource-Consumer Detection
res_con_detect <- ALLDATA %>%
                  tabyl(Res_CONDetectionDimensionality, BestModelAIC_NoRule2) %>% # create table
                  adorn_totals("row") %>% # add total counts
                  adorn_percentages("row") %>% # add percentages
                  adorn_pct_formatting(rounding = "half up", digits = 0) %>% # round to 2dp
                  adorn_ns() %>% # add counts
                  dplyr::rename("Resource-Consumer Detection Dimensionality" = 'Res_CONDetectionDimensionality')

write.csv(res_con_detect, file = '../Results/ResCosDetectDim.csv', quote = FALSE, row.names = FALSE)

######################### FILTER FEEDERS #########################

plotBestFits <- function(df, fac){
  # Evaluate args
  if(!fac %in% c('Model', 'Model Type')) return("fac must be one of: 'Model', 'Type'")
  
  # no of levels
  no <- ifelse(fac=='Model Type', 2, model_count)
  
  # define levels
  if (fac == 'Model Type'){
    lvls <- c('Phenomenological', 'Mechanistic')
    aicBreakdown <- table(ALLDATA$BestModelTypeAIC_NoRule2, ALLDATA$FilterFeeder)
    bicBreakdown <- table(ALLDATA$BestModelTypeBIC_NoRule2, ALLDATA$FilterFeeder)
  } else { # if fac == 'Model'
    lvls <- model_names
    aicBreakdown <- table(ALLDATA$BestModelAIC_NoRule2, ALLDATA$FilterFeeder)
    bicBreakdown <- table(ALLDATA$BestModelBIC_NoRule2, ALLDATA$FilterFeeder)
  }
  
  fitdata <- data.frame(Level = rep(lvls, times = 4), 
                        Estimator = rep(c('AIC', 'BIC'), each = 2*no),
                        FeedType = rep(c('Filter feeder', 'Non-filter feeder'), times = 2, each=no),
                        Count = rep(NA, times = 4*no))
  
  # Load count of how many IDs were definititvely best fit by each model (draws excluded)
  for (i in 1:nrow(fitdata)){
    lvl <- fitdata[i,'Level']
    stat <- fitdata[i,'Estimator']
    feedtype <- fitdata[i,'FeedType']
    if (stat == 'AIC'){
      fitdata[i,'Count'] <- ifelse(is.na(aicBreakdown[lvl, feedtype]), 0, aicBreakdown[[lvl, feedtype]])
    } else {
      fitdata[i,'Count'] <- ifelse(is.na(bicBreakdown[lvl, feedtype]), 0, bicBreakdown[[lvl, feedtype]])
    }
  }
  
  nfilt <- sum(fitdata$Count[1:no])
  nnonfilt <- sum(fitdata$Count[(no+1):(2*no)])
  fitdata$Total <- rep(c(nfilt, nnonfilt), each = no) # Add total
  fitdata$Percentage <- round((fitdata$Count/fitdata$Total)*100) # Add percentage of IDs best fit
  # when the rule of 2 is applied there will be different totals (as ties are ignored)
  
  # Plot
  p <- ggplot(data = fitdata, aes(x = factor(Level, levels = lvls), y = Percentage, fill = Estimator)) + 
    facet_wrap(~FeedType) +
    geom_bar(stat="identity", position = 'dodge2') +
    labs(x = fac, y = 'Best Fits (%)') + 
    theme_bw() +  theme(aspect.ratio=1) +
    theme(legend.title = element_text(face="bold")) +
    geom_text(aes(label=paste(round(Percentage), '% (', Count, ')', sep = '')), position=position_dodge(width=0.9), vjust=-0.5, cex = 6-no) +
    scale_fill_brewer(palette="Paired") +
    scale_y_continuous(limits=c(0,max(fitdata$Percentage)*1.02))
  
  return(p)
}









plotBestFits <- function(df, fac){
  # Evaluate args
  if(!fac %in% c('Model', 'Model Type')) return("fac must be one of: 'Model', 'Type'")

  # no of levels
  no <- ifelse(fac=='Model Type', 2, model_count)
  
  # define levels
  if (fac == 'Model Type'){
    lvls <- c('Phenomenological', 'Mechanistic')
    aicBreakdown <- table(ALLDATA[,'BestModelTypeAIC_NoRule2'], ALLDATA$FilterFeeder)
    bicBreakdown <- table(ALLDATA[,'BestModelTypeBIC_NoRule2'], ALLDATA$FilterFeeder)
    aicBreakdownRO2 <- table(ALLDATA[,'BestModelTypeAIC'], ALLDATA$FilterFeeder)
    bicBreakdownRO2 <- table(ALLDATA[,'BestModelTypeBIC'], ALLDATA$FilterFeeder)
  } else { # if fac == 'Model'
    lvls <- model_names
    aicBreakdown <- table(ALLDATA[,'BestModelAIC_NoRule2'], ALLDATA$FilterFeeder)
    bicBreakdown <- table(ALLDATA[,'BestModelBIC_NoRule2'], ALLDATA$FilterFeeder)
    aicBreakdownRO2 <- table(ALLDATA[,'BestModelAIC'], ALLDATA$FilterFeeder)
    bicBreakdownRO2 <- table(ALLDATA[,'BestModelBIC'], ALLDATA$FilterFeeder)
  }
  
  fitdata <- data.frame(Level = rep(lvls, times = 8), 
                        Estimator = rep(c('AIC', 'BIC'), each = 2*no, times = 2),
                        FeedType = rep(c('Filter feeder', 'Non-filter feeder'), times = 4, each=no),
                        RO2 = rep(c('Rule of Two', 'No Rule of Two'), each = 4*no),
                        Count = rep(NA, times = 8*no))
  
  # Load count of how many IDs were definititvely best fit by each model (draws excluded)
  for (i in 1:nrow(fitdata)){
    lvl <- fitdata[i,'Level']
    stat <- fitdata[i,'Estimator']
    ro2 <- fitdata[i,'RO2']
    feedtype <- fitdata[i,'FeedType']
    if (ro2 == 'No Rule of Two'){
      if (stat == 'AIC'){
        fitdata[i,'Count'] <- ifelse(is.na(aicBreakdown[lvl, feedtype]), 0, aicBreakdown[[lvl, feedtype]])
      } else {
        fitdata[i,'Count'] <- ifelse(is.na(bicBreakdown[lvl, feedtype]), 0, bicBreakdown[[lvl, feedtype]])
      }
    } else {
      if (stat == 'AIC'){
        fitdata[i,'Count'] <- ifelse(is.na(aicBreakdownRO2[lvl, feedtype]), 0, aicBreakdownRO2[[lvl, feedtype]])
      } else {
        fitdata[i,'Count'] <- ifelse(is.na(bicBreakdownRO2[lvl, feedtype]), 0, bicBreakdownRO2[[lvl, feedtype]])
      }
    }
  }
  
  n <- as.vector(sapply(split(fitdata$Count, ceiling(seq_along(fitdata$Count)/no)), sum)) # Split count col into 4s and add each to get relative total
  fitdata$Total <- rep(n, each = no)
  fitdata$Percentage <- round((fitdata$Count/fitdata$Total)*100) # Add percentage of IDs best fit
  # when the rule of 2 is applied there will be different totals (as ties are ignored)
  
  # Plot
  p <- ggplot(data = fitdata, aes(x = factor(Level, levels = lvls), y = Percentage, fill = Estimator)) + 
    labs(x = fac, y = 'Best Fits (%)') + 
    theme_bw() +
    theme(legend.title = element_text(face="bold")) +
    scale_fill_brewer(palette="Paired") +
    scale_y_continuous(limits=c(0,max(fitdata$Percentage)*1.02))
  
  # Facet wrap depending on plot required
  if (fac == 'Model Type'){ 
    fitdatanew <- subset(fitdata, RO2 == 'Rule of Two')
    p <- p + facet_wrap(~FeedType) + geom_bar(stat="identity", position = 'dodge') +
      geom_text(data = fitdatanew, aes(label=paste(round(Percentage), '% (', Count, ')', sep = '')), position=position_dodge(width=0.9), vjust=-0.5, cex = 3.5-0.5*no)
  } else {
    p <- p + facet_grid(RO2 ~ FeedType) + geom_bar(stat="identity", position = 'dodge2') +
      geom_text(aes(label=paste(round(Percentage), '% (', Count, ')', sep = '')), position=position_dodge(width=0.9), vjust=-0.5, cex = 3.5-0.5*no) 
  }
  
  return(p)
}

mod <- plotBestFits(ALLDATA, 'Model')

type <- plotBestFits(ALLDATA, 'Model Type')


ggsave('../Results/TYPE.pdf', type, width=7.5, height=4)
ggsave('../Results/MOD.pdf', mod, width=7.5, height=7.5)


