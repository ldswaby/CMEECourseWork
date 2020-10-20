# A simple script to illustrate R input-output. 

MyData <- read.csv('../Data/trees.csv', header = T) # Import with headers
write.csv(MyData, '../Results/MyData.csv') # Write to CSV
write.table(MyData[1,], file = '../Results/MyData.csv', append = T) # Append to it
write.csv(MyData, '../Results/MyData.csv', row.names = T) # Write row names
write.table(MyData, '../Results/MyData.csv', col.names = F) # Ignore col names
print("Script complete!")
