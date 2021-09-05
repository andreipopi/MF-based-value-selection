import numpy as np
from random import randrange
from sklearn.decomposition import NMF
import time
import math
from numpy import genfromtxt
import random
import solveCSP

import sys
domains = np.array([
                    [61, 102, 123, 142, 162, 241, 242, 208, 209, 243, 363],
                    [18, 25, 27, 30, 32],
                    [1,2],
                    [1,2],
                    [1,2],
                    [1,2],
                    [1, 2, 3, 4, 5, 6],
                    [20, 30, 35, 50, 58, 78],
                    [445, 455, 460, 470, 475, 505, 530, 535, 560, 675, 700, 765, 840, 850, 860, 980, 1405],
                    [189, 399, 400, 469, 479, 499, 579, 581, 609, 659, 669, 749, 1129, 1649, 2149, 2329, 2749, 3229, 5219]
                    ])
#STEP 1.1: Define 20 products as possible solutions from the product catalog of digital camera dataset:
#https://github.com/CSPHeuristix/CDBC/blob/master/CameraKB.java
#==================================================================
#solutions
productsConfigurations = np.array([
            [208,   32, 2,  2,  1,  2,  1,  30, 1405,   5219],
            [61,	25,	1,	2,	1,	1,	5,	30,	475,	659],
            [61,	18,	1,	1,	1,	1,	5,	20,	700,	189],
            [209,	32,	2,	2,	2,	1,	1,	58,	860,	2329],
            [243,	32,	1,	1,	1,	1,	3,	35,	850,	1649],
            [243,	32,	1,	2,	1,	1,	4,	35,	840,	2149],
            [363,	32,	1,	1,	1,	1,	4,	50,	980,	3229],
            [102,	30,	1,	1,	1,	1,	5,	30,	535,	400],
        	[142,	30,	1,	1,	1,	1,	2,	30,	455,	469],
    		[242,	30,	1,	1,	1,	2,	3,	30,	455,	581],
    		[242,	30,	1,	1,	1,	1,	4,	58,	460,	399],
        	[242,	30,	1,	1,	1,	1,	4,	30,	445,	499],
    		[123,	27,	1,	1,	1,	2,	6,	30,	560,	579],
    		[162,	30,	1,	1,	1,	2,	3,	30,	560,	469],
    		[241,	30,	1,	2,	1,	2,	3,	58,	505,	479],
    		[242,	32,	1,	2,	1,	2,	4,	58,	530,	609],
    		[242,	32,	2,	2,	1,	2,	4,	58,	470,	749],
    		[241,	32,	2,	2,	1,	2,	3,	58,	675,	669],
    		[242,	32,	1,	2,	2,	1,	4,	78,	765,	1129],
    		[162,	32,	1,	1,	1,	1,	5,	50,	765,	2749]
            ])

           

#==================================================================
#STEP 1.2:  Hold ID list of the expected solutions for each 265 users taken from the user dataset:
#https://github.com/CSPHeuristix/CDBC/blob/master/CameraKB_ConfigurationDataset.data
#==================================================================

data = genfromtxt("purchasedProducts.txt", delimiter=",")
#pruchased prducts ID for each user: already sorted by user ID 0-266
purchasedProducts = data[:,10] 
users = data[:,11]

#[userID, productID]
usersPurchases = np.c_[users,purchasedProducts]

usersPurchasesTest = usersPurchases[200:264, :] 
#==================================================================
# matrix [264 X 10 ]
productVariables = []
# matrix [264 X 72 ]
productVariablesHotEncodings = []

#for all users:
for user in range(0,264):
    purchasedProductID = int(usersPurchases[user][1])

    #STEP 2.1: Create a matrix with real values using the training data (NOT one-hot encoding matrix) -> 200x10
    #==================================================================
    if user == 0:#if needed because at index 0 the append works well but vstack gives an error
       productVariables= np.append(productVariables, productsConfigurations[purchasedProductID])
    else:
       productVariables = np.vstack([productVariables, productsConfigurations[purchasedProductID]])

    #==================================================================

    #STEP 3.1: Convert the dense matrix of 200 users (training data) into one-hot encoding matrix -> 200x(more than 10)
    #==================================================================
    oneHotRow = []
    i = 0 #index of the variable in configuration
    for var in productsConfigurations[purchasedProductID]:
        #create an array of size of the domain of the variable with index i
        #example: [0,0,0,0,0,0,0,0,...]of size of domain[i]
        oneHotVar = [1]*len(domains[i]) 
        #position of the 1 [000001000000], is the position
        #of the value var in the domain of the variable( domains[i])
        positionHotKey = domains[i].index(var)
        
        if positionHotKey != []:
            oneHotVar[positionHotKey] = 2
        oneHotRow = np.concatenate((oneHotRow,oneHotVar))
        i+= 1

    if user == 0:
        productVariablesHotEncodings = np.append(productVariablesHotEncodings, oneHotRow)
    else:
        productVariablesHotEncodings = np.vstack([productVariablesHotEncodings, oneHotRow])
    #==================================================================
    
np.set_printoptions(threshold=np.inf)
np.set_printoptions(suppress=True)

#STEP 1.3: Use the first 200 users data as the training data to build up the matrix (with all variables are assigned) 
#==================================================================
trainingSet = productVariables[0:200, :]
#==================================================================

#STEP 1.4: NEW PROBLEMS: Use the rest 65 users as the test data (new CSPs). Randomly remove some assignments from these configurations. There are 10 variables in total. You need to remove the same number of assignments from each configuration. 
#For each test, we need to have a different number of missing assignments in all 65 problems. The number of missing assignments will be in between 1-9. This means we have 9 test cases. 
#====================================================================
testSet = productVariables[200:264, :]
#====================================================================

def testCaseGenerate(missing):
    testCase = np.array(testSet)
    ranndomToErase =[]
    index = 0
    for row in testCase: 
        ranndomToErase = random.sample(range(0, 9), missing)

        for elem in ranndomToErase:
            testCase[index][elem] = 0
        index+=1
    return testCase

testCases= []
testCase1 = np.array(testCaseGenerate(1))
testCase2 = np.array(testCaseGenerate(2))
testCase3 = np.array(testCaseGenerate(3))
testCase4 = np.array(testCaseGenerate(4))
testCase5 = np.array(testCaseGenerate(5))
testCase6 = np.array(testCaseGenerate(6))
testCase7 = np.array(testCaseGenerate(7))
testCase8 = np.array(testCaseGenerate(8))
testCase9 = np.array(testCaseGenerate(9))

testCases = [testCase1, testCase2, testCase3, testCase4, testCase5, testCase6, testCase7, testCase8, testCase9]

f = open("stats1.txt", "a")

print("productCOnfigurations")
print(productsConfigurations)
print("purchasedProducts")
print(purchasedProducts)


#========================For both V1 and v3=========================

trainingSetHotEncoding = productVariablesHotEncodings[0:200, :]
testSetHotEncoding = productVariablesHotEncodings[200:265, :]

nmf = NMF()
#STEP 3.2: Factorize and record value ordering for each user in the training data
#==================================================================
W = nmf.fit_transform(trainingSetHotEncoding)
H = nmf.components_
denseMatrix = np.dot(W,H) #our dense matrix is: #200 X 72 
#================================================================

print(denseMatrix)


#RECORD VALUE ORDERING BASED ON THE FACTORIZED MARIX=============
indeces_vordering = [] #recording value orderings

outerIndex = 0
for array in denseMatrix:
    index = 0

    vordering1 = []
    vordering2 = []
    vordering3 = []
    vordering4 = []
    vordering5 = []
    vordering6 = []
    vordering7 = []
    vordering8 = []
    vordering9 = []
    vordering9 = []
    vordering10 = []

    tmp = []
    ordering = []
    for number in array: #for each value assignment in a line
        if(index <= 10):  
            #vordering1 = np.append(vordering1, number) 
            vordering1.append(number)
        elif index >= 11 and index <= 15:
            vordering2.append(number)
        elif index >= 16 and index <= 17:
            vordering3.append(number)
        elif index >= 18 and index <= 19:
            vordering4.append(number)
        elif index >= 20 and index <= 21:
            vordering5.append(number)
        elif index >= 22 and index <= 23:
            vordering6.append(number)
        elif index >= 24 and index <= 29:
            vordering7.append(number)
        elif index >= 30 and index <= 35:
            vordering8.append(number)
        elif index >= 36 and index <= 52:
            vordering9.append(number)
        elif index >= 53 and index <= 71:
            vordering10.append(number)
        index = index+1
        #print(my_formatter.format(number)+'  ', end = '')

    vordering1 = np.array(vordering1)
    vordering2 = np.array(vordering2)
    vordering3 = np.array(vordering3)
    vordering4 = np.array(vordering4)
    vordering5 = np.array(vordering5)
    vordering6 = np.array(vordering6)
    vordering7 = np.array(vordering7)
    vordering8 = np.array(vordering8)
    vordering9 = np.array(vordering9)
    vordering10 = np.array(vordering10)

    tmp= np.append(np.argsort(vordering1), np.argsort(vordering2))

    tmp = np.append(tmp, np.argsort(vordering3))
    tmp = np.append(tmp, np.argsort(vordering4)) 
    tmp = np.append(tmp, np.argsort(vordering5)) 
    tmp = np.append(tmp, np.argsort(vordering6)) 
    tmp = np.append(tmp, np.argsort(vordering7)) 
    tmp = np.append(tmp, np.argsort(vordering8)) 
    tmp = np.append(tmp, np.argsort(vordering9))
    tmp = np.append(tmp, np.argsort(vordering10)) 
    
    indeces_vordering.append(tmp)
   
    outerIndex = outerIndex +1
#END RECORDING VALUE ORDERING=====================================3.2

indeces_vordering = np.array(indeces_vordering)
print("\n")
print("indices")
print(indeces_vordering.shape)
print("last indeces ordering", indeces_vordering[-1])


def testCaseHot(missing):
    testCaseHotEncoding = testSetHotEncoding
    ranndomToErase =[]
    index = 0
    for row in testCaseHotEncoding: 
        ranndomToErase = random.sample(range(0, 9), missing)
        for elem in ranndomToErase:
            if elem == 0:
                testCaseHotEncoding[index][0:11] = 0
            elif elem == 1:
                testCaseHotEncoding[index][11:16] = 0
            elif elem == 2:
                testCaseHotEncoding[index][16:18] = 0
            elif elem == 3:
                testCaseHotEncoding[index][18:20] = 0
            elif elem == 4:
                testCaseHotEncoding[index][20:22] = 0
            elif elem == 5:
                testCaseHotEncoding[index][22:24] = 0
            elif elem == 6:
                testCaseHotEncoding[index][24:30] = 0
            elif elem == 7:
                testCaseHotEncoding[index][30:36] = 0
            elif elem == 8:
                testCaseHotEncoding[index][36:53] = 0
            elif elem == 9:
                testCaseHotEncoding[index][53:72] = 0    
        index+=1
        print("row",row)
    return testCaseHotEncoding

testcase1HotEncoding = np.array(testCaseHot(1))
print("last HOT TEST ENCODING......---", testcase1HotEncoding[63])

testcase2HotEncoding = np.array(testCaseHot(2))
testcase3HotEncoding = np.array(testCaseHot(3))
testcase4HotEncoding = np.array(testCaseHot(4))
testcase5HotEncoding = np.array(testCaseHot(5))
testcase6HotEncoding = np.array(testCaseHot(6))
testcase7HotEncoding = np.array(testCaseHot(7))
testcase8HotEncoding = np.array(testCaseHot(8))
testcase9HotEncoding = np.array(testCaseHot(9))

print("finished")

testCasesHot = [testcase1HotEncoding, testcase2HotEncoding,testcase3HotEncoding, testcase4HotEncoding, testcase5HotEncoding, testcase6HotEncoding, testcase7HotEncoding, testcase8HotEncoding, testcase9HotEncoding]



#CLOSEST Neighbour for APPROACH V1 (only difference wrt V3 is that it uses the denseMatrix, it will be the same method with an extra parameter matrix in the future )
#==================================================================
def closestNeighbourDense(new_transaction, denseMatrix):
    #compute the closest neighbour
    min_distance = 144 #max distance 2x72
    min_distance_user = 0
    #Euclidean distance
    i = 0
    for user in denseMatrix:
        sum = 0
        j = 0
        for vi in new_transaction:
            sum = sum+ (new_transaction[j] - user[j])**2
            j+=1 
        distance = math.sqrt(sum)
        if distance < min_distance:
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

        neighoburIndex = closestNeighbourDense(transaction,denseMatrix)
             
        #min_distance_valueOrder is the (increasing sorted) value order that the closest user used for his configuration
        
        #indeces_vordering[neighbourIndex] = [ 9,5,1,10,5,1,5,6,4,2,3    ........x72    ]
        #contains the index order such that the array it got from would be sorted
        #if we get the last element for each variable (chunch of elements in the array), 
        valueOrder = indeces_vordering[neighoburIndex]
        print(valueOrder)

        #solution = np.array([domains[0][valueOrder[10]]])
        #solution = np.append(solution,domains[1][valueOrder[15]])
        #solution = np.append(solution,domains[2][valueOrder[17]])
        #solution = np.append(solution,domains[3][valueOrder[19]])
        #solution = np.append(solution,domains[4][valueOrder[21]])
        #solution = np.append(solution,domains[5][valueOrder[23]])
        #solution = np.append(solution,domains[6][valueOrder[29]])
        #solution = np.append(solution,domains[7][valueOrder[35]])
        #solution = np.append(solution,domains[8][valueOrder[52]])
        #solution = np.append(solution,domains[9][valueOrder[71]])


        #valueOrder
        #transaction

        print("value order", valueOrder)
        print(" transaction", transaction)

        var1 = np.array([])
        var2 =  np.array([])
        var3 =  np.array([])
        var4 =  np.array([])
        var5 =  np.array([])
        var6 =  np.array([])
        var7 =  np.array([])
        var8 =  np.array([])
        var9 =  np.array([])
        var10 =  np.array([])

        #REBUILD THE SOLUTION FROM HOT ENCODING
        index = 0
        for number in transaction: #for each value assignment in a line
            if(index <= 10):  
                var1 = np.append(var1, number)
            elif index >= 11 and index <= 15:
                var2 = np.append(var2, number)
            elif index >= 16 and index <= 17:
                var3 = np.append(var3, number)
            elif index >= 18 and index <= 19:
                var4 = np.append(var4, number)
            elif index >= 20 and index <= 21:
                var5 = np.append(var5, number)
            elif index >= 22 and index <= 23:
                var6 = np.append(var6, number)
            elif index >= 24 and index <= 29:
                var7 = np.append(var7, number)
            elif index >= 30 and index <= 35:
                var8 = np.append(var8, number)
            elif index >= 36 and index <= 52:
                var9 = np.append(var9, number)
            elif index >= 53 and index <= 71:
                var10 = np.append(var10, number)
            index = index+1


        #now we need to assign the missing variable/s a 2 or a 1
        indexOfHighestValue = domains[0].index(domains[0][valueOrder[10]])
        i = 0
        for value in var1:
            if value == 0: 
                if i == indexOfHighestValue:
                    var1[i] =2
                else:
                    var1[i] =1
            i+=1
        
        indexOfHighestValue = domains[1].index(domains[1][valueOrder[15]])
        i = 0
        for value in var2:
            if value == 0: 
                if i == indexOfHighestValue:
                    var2[i] =2
                else:
                    var2[i] =1
            i+=1
        

        indexOfHighestValue = domains[2].index(domains[2][valueOrder[17]])
        i = 0
        for value in var3:
            if value == 0: 
                if i == indexOfHighestValue:
                    var3[i] =2
                else:
                    var3[i] =1
            i+=1


        indexOfHighestValue = domains[3].index(domains[3][valueOrder[19]])
        i = 0
        for value in var4:
            if value == 0: 
                if i == indexOfHighestValue:
                    var4[i] =2
                else:
                    var4[i] =1
            i+=1
        
        indexOfHighestValue = domains[4].index(domains[4][valueOrder[21]])
        i = 0
        for value in var5:
            if value == 0: 
                if i == indexOfHighestValue:
                    var5[i] =2
                else:
                    var5[i] =1
            i+=1

        indexOfHighestValue = domains[5].index(domains[5][valueOrder[23]])
        i = 0
        for value in var6:
            if value == 0: 
                if i == indexOfHighestValue:
                    var6[i] =2
                else:
                    var6[i] =1
            i+=1
        
        indexOfHighestValue = domains[6].index(domains[6][valueOrder[29]])
        i = 0
        for value in var7:
            if value == 0: 
                if i == indexOfHighestValue:
                    var7[i] =2
                else:
                    var7[i] =1
            i+=1
        
        indexOfHighestValue = domains[7].index(domains[7][valueOrder[35]])
        i = 0
        for value in var8:
            if value == 0: 
                if i == indexOfHighestValue:
                    var8[i] =2
                else:
                    var8[i] =1
            i+=1
        indexOfHighestValue = domains[8].index(domains[8][valueOrder[52]])
        i = 0
        for value in var9:
            if value == 0: 
                if i == indexOfHighestValue:
                    var9[i] =2
                else:
                    var9[i] =1
            i+=1
        
        indexOfHighestValue = domains[9].index(domains[9][valueOrder[71]])
        i = 0
        for value in var10:
            if value == 0: 
                if i == indexOfHighestValue:
                    var10[i] =2
                else:
                    var10[i] =1
            i+=1

        print("var1", var1,"var2", var2, "var3",var3,"var4",var4,"var5",var5)
        #we rebuild the solution from the value orderings contained in the "var" variables
        solutionPartial = np.array([])
        
        h = 0
        for value in var1:
            print(value)
            if value == 2:
                #solutionPartial.append(domains[0][h])
                solutionPartial = np.append(solutionPartial, domains[0][h])
            h += 1
       
        h = 0
        for value in var2:
            if value == 2:
                #solutionPartial.append(domains[1][h])
                solutionPartial = np.append(solutionPartial, domains[1][h])
            h += 1
            
        h = 0
        for value in var3:
            if value == 2:
                #solutionPartial.append(domains[2][h])
                solutionPartial = np.append(solutionPartial, domains[2][h])
            h += 1
            
        h = 0
        for value in var4:
            if value == 2:
                #solutionPartial.append(domains[3][h])
                solutionPartial = np.append(solutionPartial, domains[3][h])
            h += 1
            
        h = 0
        for value in var5:
            if value == 2:
                #solutionPartial.append(domains[4][h])
                solutionPartial = np.append(solutionPartial, domains[4][h])
            h += 1

        h = 0
        for value in var6:
            if value == 2:
                #solutionPartial.append(domains[5][h])
                solutionPartial = np.append(solutionPartial, domains[5][h])
            h += 1

        h = 0
        for value in var7:
            if value == 2:
                #solutionPartial.append(domains[6][h])
                solutionPartial = np.append(solutionPartial, domains[6][h])
            h += 1

        h = 0
        for value in var8:
            if value == 2:
                #solutionPartial.append(domains[7][h])
                solutionPartial = np.append(solutionPartial, domains[7][h])
            h += 1
            
        h = 0
        for value in var9:
            if value == 2:
                #solutionPartial.append(domains[8][h])
                solutionPartial = np.append(solutionPartial, domains[8][h])
            h += 1

        h = 0
        for value in var10:
            if value == 2:
                #solutionPartial.append(domains[9][h])
                solutionPartial = np.append(solutionPartial, domains[9][h])
            h += 1



        #print("solution partial ", solutionPartial)

        #ADD only the missing values to the solution and the rest must be the already selected values 

        correctConfiguration = productsConfigurations[int(purchasedProducts[userID+200])]


        consistent = False
        #check whether it is consistent
        #if solution[0] == 242:
        #   if solution[6] == 4:


        for configuration in productsConfigurations:
            if(configuration == solutionPartial).all():
                consistent = True
        #for configuration in productsConfigurations:
        #   if(configuration == solutionPartial).all():
        #if solutionPartial[1] < 32:
        #    if solutionPartial[2] != 1:
        #if solutionPartial[0] == 242:
        #if solutionPartial[6] != 4:
        #    consistent = False
        #else:
        #    consistent = True
            
        if consistent: 
            avgConsistencyHot += 1
                
            #only if the solution is consistent we check its prediction quality
            if (solutionPartial == correctConfiguration).all():  #correctConfiguration is the value in the testData
                avgPredictionQualityHot += 1 
        
        userID +=1
                
    avgSolvingTimeHot = avgSolvingTimeHot/ len(t)
    avgConsistencyHot = avgConsistencyHot /len(t)
    avgPredictionQualityHot = avgPredictionQualityHot /len(t)
  
    print("average solving time", avgSolvingTimeHot)
    print("average consistency", avgConsistencyHot)
    print("average prediction", avgPredictionQualityHot)

    testcaseIndex +=1
    f.write("AVG solving time:"+str(avgSolvingTimeHot)+"\n")
    f.write("AVG consistency:"+str(avgConsistencyHot)+"\n")
    f.write("AVG prediction:"+str(avgPredictionQualityHot)+"\n")

#=========================END APPROACH V1=======================




print("===================APPROACH V3========================")
#=========================APPROACH V3=========================


f.write("APPROACH3=====================")
#print(productVariablesHotEncodings[190:201, :])



#In the SPLC paper we describe that we take the nearest neighbour from R', not from R
#STEP 3.3: For a new problem, calculate the nearest neighbor from R' and apply the value ordering to solve the new problem
#==================================================================
def closestNeighbour(new_transaction):
    #compute the closest neighbour
    min_distance = 144 #max distance 2x72
    min_distance_user = 0
        #Euclidean distance
    i = 0
    #for user in trainingSetHotEncoding:
    for user in denseMatrix:
        sum = 0
        j = 0
        for vi in new_transaction:
            sum = sum+ (new_transaction[j] - user[j])**2
            j+=1 
        distance = math.sqrt(sum)
        if distance < min_distance:
            min_distance = distance 
            min_distance_user = i
        i+=1
    return min_distance_user
#==================================================================


#STEP 3.4: Record the performance criteria: runtime to solve, consistency (always 1), and prediction quality (compare with the expected solution for this new user).
#==================================================================
testcaseIndex = 0
for testcase in testCasesHot:

    #print(testcase)
    f.write("TestCase:"+str(testcaseIndex)+"\n")
    solution = np.array([])

    avgSolvingTimeHot = 0
    avgConsistencyHot = 0
    avgPredictionQualityHot = 0

    userIndex = 0

    for transaction in testcase:

        #compute min distance user
        min_distance_user_ID = closestNeighbour(transaction)
        #min_distance_valueOrder is the (increasing sorted) value order that the closest user used for his configuration
        min_distance_valueOrder = indeces_vordering[min_distance_user_ID]

        #correctConfiguration is the actual configuration purchased by the user in the test set
        correctConfiguration = productsConfigurations[int(purchasedProducts[userIndex+200])]

        solution, time = solveCSP.solve(min_distance_valueOrder)
        print("Solution", solution,"count", userIndex)
        avgSolvingTimeHot += time

        #if the CSP solution is not empty
        if solution != []:

            consistent = True #it means the solver found a solution satysfing the constraints

            #consistent = False
            #check whether it is consistent
            #for configuration in productsConfigurations:
                
            #if(configuration == solution).all():
                # consistent = True
            
            if consistent: 
                avgConsistencyHot += 1
                
                #only if the solution is consistent we check its prediction quality
                if (solution == correctConfiguration).all():  #correctConfiguration is actually purchased configuration(in testdata)
                    avgPredictionQualityHot += 1 
             
        userIndex += 1

    avgSolvingTimeHot = avgSolvingTimeHot/ len(testcase)
    avgConsistencyHot = avgConsistencyHot /len(testcase)
    avgPredictionQualityHot = avgPredictionQualityHot /len(testcase)
  
    print("average solving time", avgSolvingTimeHot)
    print("average consistency", avgConsistencyHot)
    print("average prediction", avgPredictionQualityHot)

    testcaseIndex +=1
    f.write("AVG solving time:"+str(avgSolvingTimeHot)+"\n")
    f.write("AVG consistency:"+str(avgConsistencyHot)+"\n")
    f.write("AVG prediction:"+str(avgPredictionQualityHot)+"\n")