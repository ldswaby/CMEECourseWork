#TODO: No functions, but no script-level docstring either. 2 pts deducted

#TODO: No such file or directory: '../Sandbox/testout.txt'
#############################
# FILE OUTPUT
#############################
# Save the elements of a list to a file
list_to_save = range(100)

f = open('../Sandbox/testout.txt', 'w')
for i in list_to_save:
    f.write(str(i) + '\n')  # Add a new line at the end

f.close()