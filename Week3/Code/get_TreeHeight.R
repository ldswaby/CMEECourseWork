# Script Name: get_TreeHeight.R
# Author: Luke Swaby (lds20@ic.ac.uk), Jingkai Sun (ks3020@ic.ac.uk)
#         Acacia Tang (t.tang20@imperial.ac.uk), Dengku Tang (dengkui.tang20@imperial.ac.

require(tools)
rm(list = ls())

if (length(commandArgs(trailingOnly = TRUE)) == 1){
  fileName = commandArgs(trailingOnly = TRUE)
} else {
  fileName = "trees.csv"
}

noExtension = tools::file_path_sans_ext(fileName)
defaultDataDir = "../Data/" 
fileLocation = file.path(defaultDataDir, fileName)
trees_data = read.csv(fileLocation, header = T)

# Create TreeHeight Function
TreeHeight <- function(degrees, distance) {
  radians <- degrees * pi / 180
  height <- distance * tan(radians)
  print(height)

  return(height)
}

# Apply TreeHeight Function
trees_data$Height = TreeHeight(trees_data$Angle.degrees, trees_data$Distance.m)

# Save the output file as csv format
write.csv(trees_data, paste("../Results/", noExtension, "_treeheights.csv", sep = ""), row.names = F)
cat("The file has been saved in ", "../Results/", noExtension, "_treeheights.csv\n", sep = "")