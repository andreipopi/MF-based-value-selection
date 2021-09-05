



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
        correctConfiguration = productVariables[userID+200] #since our test dataset starts at 150, we just sum the current id and we get the correct element in the test set

        #print(min_distance_valueOrder)


        #passing to the solver the 
        #and 
        #table of


        solution = splc_workshop_csp.solve(problem, min_distance_valueOrder,productsConfigurations) #, time
       

        
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

