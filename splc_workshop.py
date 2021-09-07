import numpy as np
from random import randrange
from sklearn.decomposition import NMF
import time
import math
from numpy import genfromtxt
import random
import splc_workshop_csp
import sys


domain = [0,1]
domains = []
for i in range(0,263):
    domains.append(domain)

print(domains)

#DEFINE PRODUCT TABLE FROM FILE: 1000 product configurations
productsConfigurations = []

file = open("linuxFiles/products.txt")
next(file)
for line in file:
    desired_array = [int(numeric_string) for numeric_string in line.rstrip().split(",")]
    productsConfigurations.append(np.array(desired_array))
file.close()

# * * * * * * * * * * * * * * * * * * * * * * * * * 
#  PRODUCT TABLE: productsConfigurations.         *
# * * * * * * * * * * * * * * * * * * * * * * * * *
productsConfigurations = np.array(productsConfigurations)


# * * * * * * * * * * * * * * * * * * * * * * * * *
#  HISTORICAL TRANSACTIONS: purchased products    *
# * * * * * * * * * * * * * * * * * * * * * * * * *

#CREATE A SYNTHETIC HISTORICAL DATASET OF USER PURCHASES. (ASSUME 500 users)
#we assign a random product to each of the 500 users
purchasedProducts =[]

#for example this is the case: users=500, products=100
for i in range(0,500): #number of historical transactions available
    purchasedProducts.append(random.randint(0,999)) #number of products 



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# stepbystep code (code to generate a guiding file)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
stepbystep = open("stepByStep.txt", "a")
stepbystep.write("Synthetic historical dataset:\n")
index=0
for line in purchasedProducts[0:10]:
    stepbystep.write("User "+ str(index)+" purchesed product: "+ str(line))
    stepbystep.write("\n")
    index+=1

stepbystep.write("and so on...")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# end stepbystep code
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

users = range(0,500)




#==================================================================
#STEP 1.2:  Hold ID list of the expected solutions for each 265 users taken from the user dataset:
#https://github.com/CSPHeuristix/CDBC/blob/master/CameraKB_ConfigurationDataset.data
#==================================================================


#[userID, productID]
usersPurchases = np.c_[users,purchasedProducts]

#for userID in users:
    #print("userID:"+ str(userID) +"confirm:"+ str(usersPurchases[userID][0])+"bought:"+ str(usersPurchases[userID][1])+"confirm:"+str(purchasedProducts[userID]))




#now we need to create a matrix of historical transactions:
# first create a matrix of historical transactions of the shape:

# [500 X 263] rows:#users X columns:#values, then
#transform this into hot encoding -> [500 X 526]
productVariables = []
productVariablesHotEncodings = []

#for all users:
for user in range(0,500):
    purchasedProductID = int(usersPurchases[user][1])

    #STEP 2.1: Create a matrix with real values using the training data (NOT one-hot encoding matrix) -> 200x10
    #==================================================================
    if user == 0:#if needed because at index 0 the append works well but vstack gives an error
       productVariables= np.append(productVariables, productsConfigurations[purchasedProductID])
    else:
       productVariables = np.vstack([productVariables, productsConfigurations[purchasedProductID]])

    #==================================================================
 
    #STEP 3.1: Convert the dense matrix of 500 users (training data) into one-hot encoding matrix -> 200x(more than 10)
    #==================================================================
    oneHotRow = []
    i = 0 #index of the variable in configuration

    for var in productsConfigurations[purchasedProductID]:
        #create an array of size of the domain of the variable with index i
        #example: [0,0] in this case 2 for all variables
        
        oneHotVar = [0]*len(domains[i]) 
        #position of the 1 [000001000000], is the position
        #of the value var in the domain of the variable( domains[i])
        positionHotKey = domains[i].index(var)
        
        if positionHotKey != []:
            oneHotVar[positionHotKey] = 1
        oneHotRow = np.concatenate((oneHotRow,oneHotVar))
        i+= 1

    if user == 0:
        productVariablesHotEncodings = np.append(productVariablesHotEncodings, oneHotRow)
    else:
        productVariablesHotEncodings = np.vstack([productVariablesHotEncodings, oneHotRow])
    #==================================================================


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# stepbystep code
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

stepbystep.write("Based on the purchased items, we create the historical transaction set containing full valid transactions. \n")

for line in productVariables[0:10]:
    stepbystep.write(str(line))
    stepbystep.write("\n")


stepbystep.write("and so on...")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# end stepbystep code
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #




#print(len(productVariablesHotEncodings[0]))
#print(productVariables[0])
#print(productVariablesHotEncodings[0])

np.set_printoptions(threshold=np.inf)
np.set_printoptions(suppress=True)

#==================================================================
#trainingSet = productVariables[0:100, :]
#==================================================================
#====================================================================
#testSet = productVariables[100:200, :]
#====================================================================



#print(len(trainingSet))
#print(len(testSet))


f = open("Results/stats1.txt", "a")

print("productCOnfigurations")
print(productsConfigurations)
print("purchasedProducts")
print(purchasedProducts)


#========================For both V1 and v3=========================

trainingSetHotEncoding = productVariablesHotEncodings[0:425, :]
testSetHotEncoding = productVariablesHotEncodings[425:500, :] #######CORRECT THIS

print("trainset",len(trainingSetHotEncoding))
print("testSetHotEncodingSize",len(testSetHotEncoding))

nmf = NMF()
#STEP 3.2: Factorize and record value ordering for each user in the training data
#==================================================================
W = nmf.fit_transform(trainingSetHotEncoding) #########CHANGE CHANGE CHANGE CHANGE to trainingSetHotEncoding
H = nmf.components_
denseMatrix = np.dot(W,H) #our dense matrix is: #400 X 526
#================================================================

print("Dense Matrix Shape",denseMatrix.shape)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# stepbystep code
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
stepbystep.write("\n"+"DenseMatrix("+str(denseMatrix.shape)+"):\n")
for line in denseMatrix[0:10]:
    stepbystep.write(str(line)+"\n")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# stepbystep code
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#RECORD VALUE ORDERING BASED ON THE FACTORIZED MARIX=============
indeces_vordering = [] #recording value orderings

vorderings = []#orderings for all variables
for array in denseMatrix:
   
    vordering = []#ordering for current variable
    countDomain = 0#it will increase twice in the same loop, as each variable has exactly 2 elements in the domain
    countVariable = 0#it will only increase one and will help to choose the vordering
    storeVariableValues = []
    
    for key in array:
        # the vordering for the corresponding variable being checked right now  
        storeVariableValues.append(key)
        countDomain += 1
        if(countDomain > 1):
            countDomain = 0
            countVariable +=1
            vordering.append(storeVariableValues)
            storeVariableValues = []#reset vordering for next variable
            
    #vordering has shape (263, 2) : example:  [0.9999966689967302, 0.0], [1.0000010062232447, 0.0], [1.0000046401659777, 0.0], [0.9999990178878336, 0.0], [0.9999952061885831, 0.0], [0.9999736279907523, 0.0], [0.9999939302729934, 0.0], [1.0000043558417488, 0.0], [0.9999920816333303, 0.0], [0.0, 1.0000042518628558], [0.9999905684623245, 0.0], [0.9999994335937801, 0.0], [0.9999989137051305, 0.0]]
    vorderings.append(vordering) 
    #print(vorderings)
    #print(np.array(vorderings).shape)
    #print(countVariable)
    #print(vorderings[0])
    #print("length vorderings", len(vorderings))


#for each value order from the denseMatrix
#we create a row with new value order for each variable, stored in indeces_vordering
for vordering in vorderings: #vorderings has 20, so one vordering per transaction
    #print("vordering",vordering)
    newVordering = []
    for domain in vordering:
        order = list(np.argsort(domain))#we take the order as if the domain was sorted, because in our heuristic we want to take the highest value, i.e the hot key
        #print(order)
        newVordering.append(order)

        #print("lengt newvordering", len(newVordering))
    indeces_vordering.append(newVordering)

#indeces_vordering contains trainingSet # of rows.
#each row contains 263 arrays of shape [ , ], containing indexes as if the arrays obtain by MF were sorted.
#print(len(indeces_vordering))
#print(len(indeces_vordering[0]))
#print(indeces_vordering[-1])
#END RECORDING VALUE ORDERING=====================================3.2





##############################create testcases###############################

#print(testSetHotEncoding[0])

def testCaseHot(missing):
    testcase = np.copy(testSetHotEncoding)
    ranndomToErase =[]
    index = 0
    for row in testcase: 
        ranndomToErase = random.sample(range(0, 262), missing)
        for elem in ranndomToErase:
            #0   1   2  3  4   5      6     
            #01  23  45 67 89  10 11  12 13
            testcase[index][elem*2 ] = 2 #unassigned
            testcase[index][elem*2 +1] = 2 #unassigned
        index+=1
    return testcase


testcase1HotEncoding = testCaseHot(1)

testcase2HotEncoding = testCaseHot(5)
testcase3HotEncoding = testCaseHot(10)
testcase4HotEncoding = testCaseHot(25)
testcase5HotEncoding = testCaseHot(50)
testcase6HotEncoding = testCaseHot(90)
testcase7HotEncoding = testCaseHot(120)
testcase8HotEncoding = testCaseHot(160)
testcase9HotEncoding = testCaseHot(230)



testCasesHot =[]
testCasesHot.append(testcase3HotEncoding)
testCasesHot.append(testcase2HotEncoding)
testCasesHot.append(testcase3HotEncoding)
testCasesHot.append(testcase4HotEncoding)
testCasesHot.append(testcase5HotEncoding)
testCasesHot.append(testcase6HotEncoding)
testCasesHot.append(testcase7HotEncoding)
testCasesHot.append(testcase8HotEncoding)
testCasesHot.append(testcase9HotEncoding)



#CLOSEST Neighbour for APPROACH V1 (only difference wrt V3 is that it uses the denseMatrix, it will be the same method with an extra parameter matrix in the future )
#==================================================================
def closestNeighbourDense(new_transaction, denseMatrix):
    #compute the closest neighbour
    min_distance = 1200 #max distance 263*2
    min_distance_user = 0
    i = 0

    for denseTransaction in denseMatrix:
        distance = np.linalg.norm(denseTransaction-new_transaction) #Euclidean distance
        if distance < min_distance:
            #max_distance = distance 
            min_distance = distance
            min_distance_user = i
        i+=1
    return min_distance_user




#===========================APPROACH V1=============================
f.write("APPROACHV1\n")

avgSolvingTimeHot = 0
avgConsistencyHot = 0
avgPredictionQualityHot = 0

testcaseIndex = 0
for t in testCasesHot:

    f.write("TestCase:"+str(testcaseIndex)+"\n")

    userID = 0
    for transaction in t:


        print("test transaction", transaction)
        closestneighoburIndex = closestNeighbourDense(transaction,denseMatrix)
             
        #min_distance_valueOrder is the (increasing sorted) value order that the closest user used for his configuration
        
        #indeces_vordering[neighbourIndex] = [ 9,5,1,10,5,1,5,6,4,2,3    ........x72    ]
        #contains the index order such that the array it got from would be sorted
        #if we get the last element for each variable (chunch of elements in the array), 
        variablesValueOrders = indeces_vordering[closestneighoburIndex]
        print("value order of closest neighbour", variablesValueOrders)

        
        
        #REBUILD THE SOLUTION FROM HOT ENCODING

        #we take the transaction, we want to keep the assigned variables
        #and to recommend variable assignments based on the value order of the closest neighbour for missing assignments
        solutionHot = []
        storeVariableValues = []
        for key in transaction:
            storeVariableValues.append(int(key))
            countDomain += 1
            if(countDomain > 1):
                countDomain = 0
                countVariable +=1
                solutionHot.append(storeVariableValues)
                storeVariableValues = []#reset vordering for next variable
            
        print("solution before changing 2",solutionHot)

        #now we need to assign the missing variable/s a 0 or 1

        
        #A final solution would be the transaction, with replaced values for the missing assignments from
        #the closest neighbour so from (valueOrder)
        
        print("valueOrderSize", len(variablesValueOrders))
        print("solutionSize",len(solutionHot))
        varIndex = 0
        for variable in solutionHot:
            
            if variable[0] ==2: #if the first element is a 2, it means the variable is unassigned
                indexOfHighestValue = variablesValueOrders[varIndex][1] #get the index of the highest value(the one that was assigned) from the closest neighbour value ordering
                #if index of highest value value = 0, then the hot encoding becomes [1,0]
                #if index of hghest value = 1 then hot encoding becomes [0,1]: it means closest neighbour assigned 1 to that variable
                if indexOfHighestValue == 0:
                    solutionHot[varIndex] = [1,0]
                if indexOfHighestValue == 1:
                    solutionHot[varIndex] = [0,1]

            varIndex +=1

        print("solutionSize",len(solutionHot))
        print("solution after changing 2",solutionHot)


        #build final solution (no hot encoding)
        solution = []
        for hotencoding in solutionHot:
            if hotencoding[0] == 1:
                solution.append(0)
            if hotencoding[1] == 1:
                solution.append(1)
            
        #print("solution",solution)

        #print("solution partial ", solutionPartial)

        #ADD only the missing values to the solution and the rest must be the already selected values 

       # correctConfiguration = productsConfigurations[int(purchasedProducts[userID+400])]


        correctConfiguration = productVariables[userID+425] #number depends on where the test set starts

        consistent = False
        #check whether it is consistent
        #if solution[0] == 242:
        #   if solution[6] == 4:


        #we want to check whether the calculated solution is consistent
        #we call the solver with the calculated values

        


        for configuration in productsConfigurations:
            if(configuration == solution).all():
                consistent = True
        
            
        if consistent: 
            avgConsistencyHot += 1
                
            #only if the solution is consistent we check its prediction quality
            if (solution == correctConfiguration).all():  #correctConfiguration is the value in the testData
                avgPredictionQualityHot += 1 
        
        userID +=1
                
    #avgSolvingTimeHot = avgSolvingTimeHot/ len(t)
    avgConsistencyHot = avgConsistencyHot /len(t)
    avgPredictionQualityHot = avgPredictionQualityHot /len(t)
  
    #print("average solving time", avgSolvingTimeHot)
    print("average consistency", avgConsistencyHot)
    print("average prediction", avgPredictionQualityHot)

    testcaseIndex +=1
    #f.write("AVG solving time:"+str(avgSolvingTimeHot)+"\n")
    f.write("AVG consistency:"+str(avgConsistencyHot)+"\n")
    f.write("AVG prediction:"+str(avgPredictionQualityHot)+"\n")

#=========================END APPROACH V1=======================

