# Reference: https://www.geeksforgeeks.org/create-a-correlation-matrix-using-python/

import pandas as pd

# Create dataframe from file
dataframe = pd.read_csv('images/data.csv')

# Show dataframe
#print(dataframe)

# Use the corr() method on dataframe to create a correlation matrix
matrix = dataframe.corr()

# Print the correlation matrix
#print('The Correlation Matrix is: ')
#print(matrix)

with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 8,
                       'display.width', 20000,
                       ):
    with open('images/correlation', 'w', encoding = 'utf8') as correlation:
        correlation.write(str(matrix))
