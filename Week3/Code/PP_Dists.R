# Imports
require(plyr)
require(tidyverse)

# Load data
MyDF <- read.csv("../Data/EcolArchives-E089-51-D1.csv", header = TRUE)

# Inspect data
dplyr::glimpse(MyDF)

# Subset
MyDF <- MyDF[,c('Predator.mass', 'Prey.mass', 'Type.of.feeding.interaction')]

# Add mass ratio column and rename Predator.mass column for pdf output name
MyDF$SizeRatio <- MyDF$Prey.mass/MyDF$Predator.mass
MyDF <- rename(MyDF, c('Predator.mass' = 'Pred.mass'))

### TAPPLY ###
#for (col in c('Predator.mass', 'Prey.mass', 'SizeRatio')){
#  field = strsplit(x, split = '.', fixed = T)[[1]][1]
#  pdf(sprintf('../Results/%s_Subplots.pdf', field), 11.7, 8.3)
#  par(mfrow = c(2,3))
#  par(mfg = c(1,1))
#  tapply(log10(MyDF[,col]), MyDF$Type.of.feeding.interaction, FUN = hist)
#  graphics.off()
#}

# Obtain list of feeding types
Feeding.interactions <- unique(MyDF$Type.of.feeding.interaction)

# Write subplots to pdfs
for (x in c('Pred.mass', 'Prey.mass', 'SizeRatio')){
  field <- strsplit(x, split = '.', fixed = T)[[1]][1]
  pdf(sprintf('../Results/%s_Subplots.pdf', field), 11.7, 8.3)
  par(mfcol = c(2,3))
  par(mfg = c(1,1))
  
  for (i in Feeding.interactions){
    Sub <- subset(MyDF, Type.of.feeding.interaction == i)
    if (x == 'SizeRatio'){
      hist(log10(Sub[,x]), 
           xlab = 'log10(SizeRatio)',
           ylab = 'Count',
           col = 'lightblue',
           main = str_to_title(i))
    } else {
      hist(log10(Sub[,x]), 
           xlab = sprintf('log10(%s Mass (g))', field),
           ylab = 'Count',
           col = 'lightblue',
           main = str_to_title(i))
    }
    #mtext("Predator Subplots", side=3, outer=TRUE, line=-2)
  }
  graphics.off()
}

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
Stats[,1] <- c('insectivorous','piscivorous','planktivorous','predacious',
               'predacious/piscivorous')
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
colnames(Out) <- c('Feeding.type', 'Log10.pred.mass.mean', 'Log10.pred.mass.median', 
                   'Log10.prey.mass.mean', 'Log10.prey.mass.median', 
                   'Log10.SizeRatio.mean', 'Log10.SizeRatio.median')

# Write CSV output
write.csv(Out, '../Results/PP_Results.csv', row.names = FALSE)