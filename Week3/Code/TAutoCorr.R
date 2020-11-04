rm(list=ls())
graphics.off()

#Load Data
load('../Data/KeyWestAnnualMeanTemperature.RData')

# Compute Autocorrelation
AutoCorr <- cor(ats$Temp[-100], ats$Temp[-1])

#####################################
## ALTERNATIVE? ##
#require(dplyr)
#acf(ats$Temp, lag.max = 1, plot = F)
#####################################

# Repeat calculation for 10000 permuatations of Temp vector
Corrs <- rep(0, 10000)
for (i in 1:10000){
  d <- sample(ats$Temp)
  Corrs[i] <- cor(d[-100], d[-1])
}

# Compute approximate p-value
p <- sum(Corrs>AutoCorr)/10000

### Visualisations ###
pdf('TempRplot.pdf')
qplot(ats$Temp[-100], ats$Temp[-1],
      xlab = expression(paste("Temperature ",degree,"C (t)")),
      ylab = expression(paste("Temperature ",degree,"C (t+1)")),
      asp = 0.5, size = I(0.5)
      ) + geom_smooth(method = "lm", color = 'red', size = 0.5)
graphics.off()