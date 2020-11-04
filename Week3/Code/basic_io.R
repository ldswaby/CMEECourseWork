# A simple script to illustrate R input-output. 

MyData <- read.csv('../Data/trees.csv', header = TRUE) # Import with headers
write.csv(MyData, '../Results/MyData.csv') # Write to CSV
write.table(MyData[1,], file = '../Results/MyData.csv', append = TRUE) # Append to it
write.csv(MyData, '../Results/MyData.csv', row.names = TRUE) # Write row names
write.table(MyData, '../Results/MyData.csv', col.names = FALSE) # Ignore col names
print("Script complete!")