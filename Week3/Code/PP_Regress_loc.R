# Script Name: PP_Regress_loc.R
# Author: Luke Swaby (lds20@ic.ac.uk), Jingkai Sun (ks3020@ic.ac.uk)
#         Acacia Tang (t.tang20@imperial.ac.uk), Dengku Tang (dengkui.tang20@imperial.ac.uk)

#load packages
library(dplyr)

#load data
MyDF <- read.csv("../Data/EcolArchives-E089-51-D1.csv")

#make grouping variables factors
MyDF$Type.of.feeding.interaction <- as.factor(MyDF$Type.of.feeding.interaction)
MyDF$Predator.lifestage <- as.factor(MyDF$Predator.lifestage)

#regression results
combinations <- as.matrix(unique(select(MyDF, Type.of.feeding.interaction, Location, Predator.lifestage))) # get all combinations of factors to analysize by
Results <- matrix(nrow = 0, ncol = 7)
for (i in 1:nrow(combinations)){
    subset <- filter(MyDF, Type.of.feeding.interaction == combinations[i,1], Location == combinations[i,2])
    subset <- filter(subset, Predator.lifestage == combinations[i,3])
    subset_lm <- summary(lm(log(Predator.mass) ~ log(Prey.mass), data = subset))
    if(nrow(subset_lm$coefficient) > 1){
        subset_results <- c(combinations[i,1], combinations[i,2], subset_lm$coefficients[2, 1], subset_lm$coefficients[1, 1], subset_lm$r.squared, subset_lm$fstatistic[1], subset_lm$coefficients[2, 4])
        Results <- rbind(Results, subset_results)
    }

}
colnames(Results) <- c("feeding type", "life stage", "regression slope", "regression intercept", "R2", "F-statistic value", "p-value")
write.csv(Results, "../Results/PP_Regress_loc_Results.csv", row.names = F)