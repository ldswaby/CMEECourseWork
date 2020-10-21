# This function calculates heights of trees given distance of each tree 
# from its base and angle to its top, using  the trigonometric formula 
#
# height = distance * tan(radians)
#
# ARGUMENTS
# degrees:   The angle of elevation of tree
# distance:  The distance from base of tree (e.g., meters)
#
# OUTPUT
# The heights of the tree, same units as "distance"

Trees <- read.csv('../Data/trees.csv')

TreeHeight <- function(degrees, distance){
    radians <- degrees * pi / 180
    height <- distance * tan(radians)
    print(paste("Tree height is:", height))
  
    return (height)
}

Tree.Height.m <- TreeHeight(Trees$Angle.degrees, Trees$Distance.m)
write.csv(cbind(Trees, Tree.Height.m), '../Results/TreeHts.csv')