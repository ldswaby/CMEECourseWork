#########################################
#### Visualizing Regression analyses ####
#########################################

# Imports
library(plyr)
library(tidyverse)

# Load data
MyDF <- read.csv("../Data/EcolArchives-E089-51-D1.csv", header = TRUE)

# Inspect data
dplyr::glimpse(MyDF)

# Subset Data 
MyDF <- MyDF[,c('Predator.mass', 'Prey.mass', 'Predator.lifestage','Type.of.feeding.interaction')]

# Remove spaces
MyDF[MyDF=="larva / juvenile"] <- "larva/juvenile"

# Plot
p <- ggplot(MyDF, aes(x = Prey.mass, y = Predator.mass, 
                      colour = Predator.lifestage)) + 
        facet_wrap(.~Type.of.feeding.interaction, scales = 'free') +
        facet_grid(Type.of.feeding.interaction~.) + # Split plots by feeding interaction
        geom_point(shape=I(3)) + theme_bw() + # Cross points + white background
        theme(legend.position = 'bottom', legend.title = element_text(face="bold")) + 
        ylab("Predator Mass in grams") + 
        xlab('Prey Mass in grams') +
        theme(aspect.ratio = 0.5) +
        geom_smooth(method = "lm", size = 0.5, fullrange = TRUE) + # Adds lm trendlines
        guides(colour = guide_legend(nrow = 1)) +   # Places the legend all on one line
        scale_x_log10() + scale_y_log10()  # Scale axes
        
# Write plot to pdf
pdf('../Results/PP_Regress.pdf', 8.3, 11.7)
print(p)
graphics.off()

### Create DF ###

# Define function to extract required statistics from a linear model
returnStats <- function(x){
  summ <- summary(x)
  
  # Extract stats
  m <- coef(x)[[2]]  # Gradient
  yint <- coef(x)[[1]]  # Intercept
  rsqd <- summ$r.squared  # R squared
  f <- summ$fstatistic  # F-statistic
  if (!is.null(f[[1]])){
    f_stat <- f[[1]]
  } else {
    f_stat <- NA
  }
  p_value <- coef(summary(x))[8]  # p-value
  
  return(c(m, yint, rsqd, f_stat, p_value))
}

# Create list of linear models
lm_out <- dlply(MyDF, .(Type.of.feeding.interaction, Predator.lifestage), 
                function(x) lm(log(Predator.mass)~log(Prey.mass), data = x))

# Write summative stats of linear models to dataframe
df_out <- ldply(lm_out, .fun = returnStats)

# Rename columns
colnames(df_out)[3:7] <- c('Gradient', 'Intercept', 'R-Squared', 'F-Statistic', 'p-value')

# Write to csv
write.csv(df_out, "../Results/PP_Regress_Results.csv", row.names = FALSE)