################################################################
################## Wrangling the Pound Hill Dataset ############
################################################################

############## Imports ##############
library(tidyverse)

############# Load the dataset ###############
# header = false because the raw data don't have real headers
MyData <- as.matrix(read_csv("../Data/PoundHillData.csv", col_names = F)) 

# header = true because we do have metadata headers
MyMetaData <- read_delim("../Data/PoundHillMetaData.csv", col_names = T, delim = ';')

############# Inspect the dataset ###############
dplyr::glimpse(MyData)
#utils::View(MyData) # Hashed out as it takes ages!

############# Transpose ###############
# To get those species into columns and treatments into rows 
MyData <- t(MyData) 
dplyr::glimpse(MyData)
#utils::View(MyData) # Hashed out as it takes ages!

############# Replace species absences with zeros ###############
MyData[is.na(MyData)] <- 0

############# Convert raw matrix to data frame ###############
TempData <- tibble::as_tibble(MyData[-1,]) 
colnames(TempData) <- MyData[1,] # assign column names from original data

############# Convert from wide to long format  ###############
MyWrangledData <- gather(TempData, Species, Count, -c(Cultivation, Block, Plot, Quadrat))

# Convert data back to factor/int type
MyWrangledData <- mutate_at(MyWrangledData, vars(colnames(MyWrangledData)), factor)
MyWrangledData <- mutate(MyWrangledData, Count = as.integer(Count))

############# Exploring the data ###############
dplyr::glimpse(MyWrangledData)
#utils::View(MyWrangledData) ## Hashed out as it takes ages!