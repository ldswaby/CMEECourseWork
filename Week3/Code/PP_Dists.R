###############################################
#### Investigating Body Mass Distributions ####
###############################################

# Imports
#library(plyr)
library(tidyverse)

# Load data
MyDF <- read.csv("../Data/EcolArchives-E089-51-D1.csv", header = TRUE)

# Inspect data
dplyr::glimpse(MyDF)

# Subset
MyDF <- MyDF[,c('Predator.mass', 'Prey.mass', 'Type.of.feeding.interaction')]

# Add mass ratio column and rename Predator.mass column for pdf output name
MyDF$SizeRatio <- MyDF$Prey.mass/MyDF$Predator.mass
#MyDF <- rename(MyDF, c('Predator.mass' = 'Pred.mass'))
names(MyDF)[names(MyDF) == 'Predator.mass'] <- 'Pred.mass'

# Write subplots to pdfs
for (col in c('Pred.mass', 'Prey.mass', 'SizeRatio')){
  field <- strsplit(col, split = '.', fixed = T)[[1]][1]
  pdf(sprintf('../Results/%s_Subplots.pdf', field), 11.7, 8.3)
  
  # Set titles/axis labels
  if (col == 'SizeRatio'){
    xlb <- 'log10(SizeRatio)'
    titl <- 'Size Ratio Subplots by Feeding Type'
  } else {
    xlb <- sprintf('log10(%s Mass (g))', field)
    titl <- sprintf('%s Mass Subplots by Feeding Type', field)
  }
  
  # Set up page
  par(mfcol = c(2,3), mfg = c(1,1), oma=c(1.5,2,1,1))
  
  # Plot
  for (i in unique(MyDF$Type.of.feeding.interaction)){
    Sub <- subset(MyDF, Type.of.feeding.interaction == i)
    hist(log10(Sub[,col]), 
         xlab = xlb,
         ylab = 'Count',
         col = 'lightblue',
         main = str_to_title(i))
    mtext(titl, outer=TRUE,  cex=1, line=-0.5)
  }
  graphics.off()
}

##########################################################
##################### Using ggplot #######################
##########################################################
# library(ggplot2)

#for (col in c('Pred.mass', 'Prey.mass', 'SizeRatio')){
#  field <- strsplit(col, split = '.', fixed = T)[[1]][1]
#  
#  if (col == 'SizeRatio'){
#    xlb <- 'log10(SizeRatio)'
#    titl <- 'Size Ratio Subplots by Feeding Type'
#  } else {
#    xlb <- sprintf('log10(%s Mass (g))', field)
#    titl <- sprintf('%s Mass Subplots by Feeding Type', field)
#  }
#  
#  p <- (ggplot(MyDF, aes(x = log10(MyDF[,col]), fill = Type.of.feeding.interaction)) + 
#          geom_histogram(colour = 'black') + 
#          facet_wrap(.~Type.of.feeding.interaction, scales = 'free') +
#          theme(legend.position = 'none') + 
#          labs(title = titl) + 
#          ylab("Count") + 
#          xlab(xlb)
#        )
#
#  pdf(sprintf('../Results/%s_Subplots.pdf', field), 11.7, 8.3)
#  print(p)
#  graphics.off()
#}
##########################################################
##########################################################

##### Write CSV #####

## Calculate stats ##

# Pred
Log.pred.mass.mean <- tapply(log10(MyDF[,'Pred.mass']), MyDF$Type.of.feeding.interaction, FUN = mean)
Log.pred.mass.median <- tapply(log10(MyDF[,'Pred.mass']), MyDF$Type.of.feeding.interaction, FUN = median)

# Prey
Log.prey.mass.mean <- tapply(log10(MyDF[,'Prey.mass']), MyDF$Type.of.feeding.interaction, FUN = mean)
Log.prey.mass.median <- tapply(log10(MyDF[,'Prey.mass']), MyDF$Type.of.feeding.interaction, FUN = median)

# Ratio
Log.SizeRatio.mean <- tapply(log10(MyDF[,'SizeRatio']), MyDF$Type.of.feeding.interaction, FUN = mean)
Log.SizeRatio.median <- tapply(log10(MyDF[,'SizeRatio']), MyDF$Type.of.feeding.interaction, FUN = median)

# Initialize stats matrix
Stats <- matrix(1:35, nrow = 5, ncol = 7)

# Load matrix
Stats[,1] <- c('Insectivorous','Piscivorous','Planktivorous','Predacious',
               'Predacious/Piscivorous')
#Stats[,1] <- Feeding.interactions  # not in right order!

# Is there a way to do this in a single step? A function analogous to 'enumerate'?
Stats[,2] <- as.vector(Log.pred.mass.mean)
Stats[,3] <- as.vector(Log.pred.mass.median)
Stats[,4] <- as.vector(Log.prey.mass.mean)
Stats[,5] <- as.vector(Log.prey.mass.median)
Stats[,6] <- as.vector(Log.SizeRatio.mean)
Stats[,7] <- as.vector(Log.SizeRatio.median)

# Convert to DataFrame
Out <- as.data.frame(Stats)

# Add header
colnames(Out) <- c('Feeding.Type', 'Log10.Pred.Mass.Mean', 'Log10.Pred.Mass.Median', 
                   'Log10.Prey.Mass.Mean', 'Log10.Prey.Mass.Median', 
                   'Log10.SizeRatio.Mean', 'Log10.SizeRatio.Median')

# Write CSV output
write.csv(Out, '../Results/PP_Results.csv', row.names = FALSE)