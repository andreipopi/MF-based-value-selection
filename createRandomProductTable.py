import numpy as np
from random import randrange
import math
from numpy import genfromtxt
import random
import sys
import csptestversion



productsConfigurations = []

file = open("linuxFiles/randomProductTable.txt")
next(file)
for line in file:
    desired_array = [int(numeric_string) for numeric_string in line.rstrip().split(",")]
    productsConfigurations.append(np.array(desired_array))
file.close()


randomProductTable = open("randomProductTable2.txt", "a")

problem1 = csptestversion.initialize()

j=0
while j < 1000:


    transaction = []

    #create a transaction of 263 variables picked randomly
    for i in range(263):
        randbit = random.randint(0,1)
        transaction.append(randbit)

    print(transaction)
    #transform the transaction in one hot encoding
    oneHotRow = []
    i = 0 #index of the variable in configuration

    for var in transaction:
        #create an array of size of the domain of the variable with index i
        #example: [0,0] in this case 2 for all variables
        
        oneHotVar = [0,0]
        #position of the 1 [000001000000], is the position
        #of the value var in the domain of the variable( domains[i])
        positionHotKey = [0,1].index(var)
        
        if positionHotKey != []:
            oneHotVar[positionHotKey] = 1
        oneHotRow.append(oneHotVar)#((oneHotRow,oneHotVar))
        i+= 1

    consistent = False

    solution_array = csptestversion.solve(problem1, oneHotRow,productsConfigurations) #, time

    if len(solution_array) >0:
        consistent = True
        randomProductTable.write(str(transaction)[1:-1]+"\n")
        j+=1

    problem1.reset


print(oneHotRow)



#randomProductTable.close()

#print(len(lines))

