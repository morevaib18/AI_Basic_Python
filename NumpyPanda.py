import array as arr
import numpy as np
import pandas as pd

a=arr.array('i',[2,4,6])

l=[123, 'Shiv']

# Numpy Array
# Vectorized Arithmetic
# Vectorized Comparison, operator
# lots of extra feature of scientific calculations
arr1=np.array([1,2,3], dtype=int)
arr2=np.array([0,4,5], dtype=int)
arr3=arr1 + arr2
print(arr3)
arr4=arr2>arr1
print(arr4)
print(np.mean(arr1))

# Pandas -- Panel Data i.e. Data shows in tabular format
arrdata= np.array([['Shiv',20], ['Raju',30], ['Hari',75], ['Amar',100]])
print(arrdata)

data={'Name':['Shiv','Raju','Hari','Amar'],'Age':[20,30,75,100]}
table1=pd.DataFrame(data)
print(table1)
print(table1['Age']>30)

#Normal Array for simple things
#Numpy Array - Vectorised, mean, median
#Pandas - In memory table, Pandas use Numpy