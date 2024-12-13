# A simple program that shows how to save data to a file
import random                          # Just used to generate some random numbers

###########################################################
# CONFIGURATION
filename = "data.csv"                  # The file name of the file to be saved

decimal_comma = True                   # If decimal separator is a comma then set to true

data_delimiter = '\t'                  # The data delimiter

###########################################################
# PROGRAM
file = open(filename, 'w')             # Open the file in 'w' write mode

# Make some dummy data
for i in range(1000):
    value_i = random.randint(0, 100)   # Get a random integer number
    value_f = 123.456 * value_i        # Get a float number

    value_f_str = "%.2f" % value_f     # Round the float to two decimals and convert it into a string
    if decimal_comma == True:          # Replace . with , if wanted       
        value_f_str = value_f_str.replace('.', ',')
    
    # Format the data to a string and write it
    string = "%d%s%d%s%s\n" % (i, data_delimiter, value_i, data_delimiter, value_f_str)
    file.write(string)

file.close()                           # Close the file when the writing has been done
