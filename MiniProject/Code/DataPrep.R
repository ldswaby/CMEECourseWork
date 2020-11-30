###########################################################
########### Data Wrangling for CMEE Miniproject ###########
###########################################################

# TODO:
# 1. Check units are consistent for each dataset
# 2. Filter out 0s in N_TraitValue col
# 3. Check for NAN / NA values
# 4. Range of each column very large - scale with log? 
#    Or does is not matter as units are consistent for each dataset?
# 5. HOW TO REMOVE OUTLIERS FROM INDV DATASETS?
# 6. Datasets with loads of different y values per x value
#    (these are generally curves with low resource densities)

####################### Imports ###########################
suppressMessages(library(tidyverse))
suppressMessages(library(plyr))

################### Clear workspace #######################
rm(list = ls())
graphics.off()

################## Load/Inspect Data ######################
FuncRespData <- read.csv("../Data/CRat.csv", stringsAsFactors = FALSE)
#dplyr::glimpse(FuncRespData)

# response variable: N_TraitValue: The number of resources consumed per consumer per unit time
# explanatory variable: ResDensity: resource abundance

############## Trim problematic datasets ##################

# Subset cols
ReqCols <- c('ID', 'ResDensity', 'N_TraitValue', 'ResDensityUnit', 'TraitUnit', 'ConTaxa', 'ResTaxa', 'Habitat', 'Con_ForagingMovement', 'Res_ForagingMovement')
FuncRespData <- FuncRespData[,ReqCols] 

# Drop rows corresponding to IDs with discrepant/irreconsilable measurment units used
DiscrepantUnits <- function(df){
  # Homogenize string characteristics that do not affect units
  # (whitespace and case).
  uniqueResUnits <- unique(tolower(gsub(" ", "", df$ResDensityUnit, fixed = TRUE)))
  uniqueTraitUnits <- unique(tolower(gsub(" ", "", df$TraitUnit, fixed = TRUE)))
  # Return ID where discrepant units found
  if (length(uniqueResUnits) > 1 | length(uniqueTraitUnits) > 1){
    return(unique(df$ID))
  }
}

DiscrepantIDs <- dlply(FuncRespData, .(ID), DiscrepantUnits)
FuncRespData <- FuncRespData[!(FuncRespData$ID %in% DiscrepantIDs),]

# Standardise case/terminology
FuncRespData$Con_ForagingMovement <- tolower(FuncRespData$Con_ForagingMovement)
FuncRespData$Res_ForagingMovement <- tolower(FuncRespData$Res_ForagingMovement)
FuncRespData[FuncRespData == "sessile"] <- "passive"

# Drop rows containing NA values (just in case)
FuncRespData <- na.omit(FuncRespData)

# Drop rows containing 0 values
#NonZeroRows <- apply(FuncRespData, 1, function(row) all(row != 0))
FuncRespData <- FuncRespData[!(FuncRespData$N_TraitValue==0 | FuncRespData$ResDensity==0),]

################### Write to CSV file ##################### 
write.csv(FuncRespData, '../Data/CRat_prepped.csv', row.names = FALSE)
