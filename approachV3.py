
print("===================APPROACH V3========================")
#=========================APPROACH V3=========================

f.write("APPROACH3=====================")
#print(productVariablesHotEncodings[190:201, :])



#==================================================================
testcaseIndex = 0

for testcase in testCasesHot:
   
    f.write("TestCase:"+str(testcaseIndex)+"\n")
    solution = np.array([])

    #avgSolvingTimeHot = 0
    avgConsistencyHot = 0
    avgPredictionQualityHot = 0

    userID = 0

    for transaction in testcase: 


        problem = splc_workshop_csp.initialize(stepbystep)

        #compute min distance user
        min_distance_user_ID = closestNeighbourDense(transaction,denseMatrix)
        #min_distance_valueOrder is the (increasing sorted) value order that the closest user used for his configuration
        min_distance_valueOrder = indeces_vordering[min_distance_user_ID]

        
        #correctConfiguration is the actual configuration purchased by the user in the test set
        correctConfiguration = productVariables[userID+425] #since our test dataset starts at 150, we just sum the current id and we get the correct element in the test set

        #print(min_distance_valueOrder)


        #creating the value order by keeping the assigned variables
        #and assigning unassigned ones to the ones in the closest neighbour
        ##############################################################
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
            
        #now we need to assign the missing variable/s a 0 or 1

        
        #A final solution would be the transaction, with replaced values for the missing assignments from
        #the closest neighbour so from (valueOrder)
        
        varIndex = 0
        for variable in solutionHot:
            
            if variable[0] ==2: #if the first element is a 2, it means the variable is unassigned
                indexOfHighestValue = min_distance_valueOrder[varIndex][1] #get the index of the highest value(the one that was assigned) from the closest neighbour value ordering
                #if index of highest value value = 0, then the hot encoding becomes [1,0]
                #if index of hghest value = 1 then hot encoding becomes [0,1]: it means closest neighbour assigned 1 to that variable
                if indexOfHighestValue == 0:
                    solutionHot[varIndex] = [1,0]
                if indexOfHighestValue == 1:
                    solutionHot[varIndex] = [0,1]

            varIndex +=1

        #############################################################

        #WRONG#solution = splc_workshop_csp.solve(problem, min_distance_valueOrder,productsConfigurations) #, time
        solution = splc_workshop_csp.solve(problem, solutionHot,productsConfigurations) #, time


        
        #print("min distance value order",min_distance_valueOrder)
        #print("transaction",transaction)
        #print("neighbourvalueorder",min_distance_valueOrder)
        #print("solution",solution)
        #print("correct",correctConfiguration)
       # sys.exit()


        #print("Solution", solution,"UserID", userID)
        #avgSolvingTimeHot += time

        #if the CSP solution is not empty
        if solution != []:

            consistent = True #it means the solver found a solution satysfing the constraints
            
            if consistent: 
                avgConsistencyHot += 1
                
                #only if the solution is consistent we check its prediction quality
                if (solution == correctConfiguration).all():  #correctConfiguration is actually purchased configuration(in testdata)
                    avgPredictionQualityHot += 1 
    
        userID += 1

    #avgSolvingTimeHot = avgSolvingTimeHot/ len(testcase)
    avgConsistencyHot = avgConsistencyHot /len(testcase)
    avgPredictionQualityHot = avgPredictionQualityHot /len(testcase)
  
   
    #print("average solving time", avgSolvingTimeHot)
    print("average consistency", avgConsistencyHot)
    print("average prediction", avgPredictionQualityHot)

    testcaseIndex +=1
    #f.write("AVG solving time:"+str(avgSolvingTimeHot)+"\n")
    f.write("AVG consistency:"+str(avgConsistencyHot)+"\n")
    f.write("AVG prediction:"+str(avgPredictionQualityHot)+"\n")