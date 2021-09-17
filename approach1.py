
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

        # * * * * * * * * * * * * * * * * * * * *
        # variablesValueOrders=nearest neighbour
        # * * * * * * * * * * * * * * * * * * * *

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
                #countVariable +=1
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

        consistent = False

        problem1 = splc_workshop_csp_approach1.initialize(stepbystep)

        solution_array = splc_workshop_csp_approach1.solve(problem1, solutionHot,productsConfigurations) #, time


        if len(solution_array) >0:
            consistent = True
        
        #for configuration in productsConfigurations:
        #    if(configuration == solution).all():
        #        consistent = True
      

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

        correctConfiguration = productVariables[userID+350] #number depends on where the test set starts

      
        #check whether it is consistent
        #if solution[0] == 242:
        #   if solution[6] == 4:


        #we want to check whether the calculated solution is consistent
        #we call the solver with the calculated values


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