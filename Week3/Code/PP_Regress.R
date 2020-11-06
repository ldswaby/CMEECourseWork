#########################################
#### Visualizing Regression analyses ####
#########################################

# Imports
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
p <- ggplot(MyDF, aes(x = log2(Prey.mass), y = log2(Predator.mass), 
                      colour = Predator.lifestage)) + 
        facet_wrap(.~Type.of.feeding.interaction, scales = 'free') +
        facet_grid(Type.of.feeding.interaction~.) +
        geom_point(shape=I(3)) + theme_bw() +
        theme(legend.position = 'bottom') + 
        ylab("Predator Mass in grams") + 
        xlab('Prey Mass in grams') +
        theme(aspect.ratio = 0.5) +
        geom_smooth(method = "lm", size = 0.5, fullrange = TRUE)

# Write plot to pdf
pdf('../Results/PP_Regress.pdf', 8.3, 11.7)
print(p)
graphics.off()

### Create DF ###
feeding.int <- unique(MyDF$Type.of.feeding.interaction)

Feeding_type <- Predator_lifestage <- Intercept <- Slope <- r_squared <- p_value <- f_statistics <- c(0)

Feeding.interaction.type <- Predator_lifestage <- Intercept <- Gradient <- R_squared <- p_value <- f_stat <- c(0)

count <- 0
i <- 0

while (i <= length(feeding.int)){
  i <- i + 1
  Sub <- subset(MyDF, Type.of.feeding.interaction == feeding.int[i])
  for (ls in unique(Sub$Predator.lifestage)){
    
    Sub2 <- subset(Sub, Predator.lifestage == ls)
    mod <- lm(log(Predator.mass) ~ log(Prey.mass), data = Sub2)
    count <- count + 1
    Feeding.interaction.type[count] <- as.character(feeding.int[i])
    Predator_lifestage[count] <- ls
    model = lm(log(Predator.mass) ~ log(Prey.mass), data = Sub2)
    
    Intercept[count] <- model$coefficients[[1]]
    Gradient[count] <- model$coefficients[[2]]
    R_squared[count] <- summary(mod)$r.squared
    
    f <- summary(mod)$fstatistic 
    
    if (!is.null(f[[1]])){
      f_stat[count] <- f[[1]]
    } else {
      f_stat[count] <- NA
    }
    
    p_value[count] <- summary(mod)$coefficients[8]
    reg.sum <- data.frame(Feeding.interaction.type, Predator_lifestage, Intercept, Gradient, R_squared, f_stat, p_value)
  }
}

write.csv(reg.sum, "../Results/PP_Regress_Results.csv", row.names = F)