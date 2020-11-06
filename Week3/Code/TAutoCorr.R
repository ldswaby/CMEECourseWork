####################################
#### Autocorrelations Practical ####
####################################

# Imports
library(ggplot2)

# Load Data
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

# Plot
pl <- qplot(ats$Temp[-100], ats$Temp[-1],
            xlab = expression(paste("Temperature ",degree,"C (t-1)")),
            ylab = expression(paste("Temperature ",degree,"C (t)")),
            asp = 0.5, size = I(0.5)) + 
            geom_smooth(method = "lm", color = 'red', size = 0.5)

#### DENSITY PLOT TO DEMONSTRATE P ######
corrpl <- qplot(Corrs, geom = "density", xlab = "Correlation Coefficients",
                ylab = "Density", fill = "red", alpha = 0.5, asp = 0.5) + 
            theme(legend.position = "none") + 
            geom_vline(xintercept = AutoCorr, size = 0.5, colour = 'orange') + 
            geom_text(aes(x=AutoCorr, label="Autocorr Coeff. = 0.326\n", y=2), angle=90, size=3)

# Write to pdf
pdf('../Results/AutoCorrScatter.pdf')
print(pl)
graphics.off()

pdf('../Results/AutoCorrDensity.pdf')
print(corrpl)
graphics.off()
