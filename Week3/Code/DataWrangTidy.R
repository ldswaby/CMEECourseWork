################################################################
################## Wrangling the Pound Hill Dataset ############
################################################################
rm(list=ls())

############## Imports ##############
require(tidyverse)

############# Load the dataset ###############
# header = false because the raw data don't have real headers
MyData <- as.matrix(read_csv("../data/PoundHillData.csv", col_names = F)) 

# header = true because we do have metadata headers
MyMetaData <- read_delim("../data/PoundHillMetaData.csv", col_names = T, delim = ';')

############# Inspect the dataset ###############
dplyr::glimpse(MyData)
utils::View(MyData)

############# Transpose ###############
# To get those species into columns and treatments into rows 
MyData <- t(MyData) 
dplyr::glimpse(MyData)
utils::View(MyData)

############# Replace species absences with zeros ###############
MyData[is.na(MyData)] = 0

############# Convert raw matrix to data frame ###############
TempData <- tibble::as_tibble(MyData[-1,]) 
colnames(TempData) <- MyData[1,] # assign column names from original data

############# Convert from wide to long format  ###############
MyWrangledData <- gather(TempData, Species, Count, -c(Cultivation, Block, Plot, Quadrat))

MyWrangledData[, "Cultivation"] <- as.factor(MyWrangledData[, "Cultivation"])
MyWrangledData[, "Block"] <- as.factor(MyWrangledData[, "Block"])
MyWrangledData[, "Plot"] <- as.factor(MyWrangledData[, "Plot"])
MyWrangledData[, "Quadrat"] <- as.factor(MyWrangledData[, "Quadrat"])
MyWrangledData[, "Count"] <- as.integer(MyWrangledData[, "Count"])

dplyr::glimpse(MyWrangledData)
utils::View(MyWrangledData)