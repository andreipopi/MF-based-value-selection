import constraint
import time
import numpy as np
import sys




def initialize(stepbystep):
    #we create a problem and add the domain constraints which will be the same for all problems,
    #later, in solve(), we add the producttable constraint and we solve the problem.
    ###############  AUXILIARY FUNCTIONS  ################################

    ###############################################################################
    # MANDATORY RELATIONSHIPS
    ###############################################################################
    def mandatory():
        stepbystep.write("Mandatory Relationships \n")
        file1 = open('linuxFiles/mandatoryRelationships.txt')
        lines = file1.readlines()
        # Strips the newline character
        for line in lines:
            line = line.replace(' ','')
            line = line.replace("\n", "")
            listOfParameters = np.array(line.split(",") )
            #now listOfParameters has the two parameters for a mandatory constraint
            #as the second argument for addConstraint, we need to pass the correct variables like this:
            # get the index of parameter1 in listOfFeatures
            # use that index to get the correct v in vars
            # add constraint, for example:  addCOnstraint()
            index1 = list(listOfFeatures).index(listOfParameters[0])
            index2 = list(listOfFeatures).index(listOfParameters[1])
            #print("indeces",index1,"-",index2)
            stepbystep.write("("+"v"+str(index1)+" == 0 and "+"v"+str(index2)+" == 0) or ("+"v"+str(index1)+" == 1 and "+ "v"+str(index2)+" == 1) \n")
            prob.addConstraint(
                            lambda parameter1, parameter2: 
                                    (parameter1 == 0 and parameter2 == 0 ) or
                                    (parameter1 == 1 and parameter2 == 1  ),
                                    ("v"+str(index1),"v"+str(index2)), 
                                )
    
    ###############################################################################
    # OPTIONAL RELATIONSHIPS
    ###############################################################################
    #optional and requires can be both translated by the implication rules
    def optional(fileName):
        if fileName =="linuxFiles/optionalRelationships.txt":
            stepbystep.write("Optional Relationship \n")
        if fileName =="linuxFiles/requireConstraints.txt":
            stepbystep.write("Require Relationship \n")
        file1 = open(fileName)
        lines = file1.readlines()
        file1.close()
        # Strips the newline character
        for line in lines:
            line = line.replace(' ','')
            line = line.replace("\n", "")
            listOfParameters = np.array(line.split(",") )
        
            index1 = list(listOfFeatures).index(listOfParameters[0])
            index2 = list(listOfFeatures).index(listOfParameters[1])
            #print("indeces",index1,"-",index2)
            
            stepbystep.write("("+"v"+str(index1)+" == 0 and "+"v"+str(index2)+" == 0) or ("+"v"+str(index1)+" == 1 and "+ "v"+str(index2)+" == 1) or ("+"v"+str(index1)+"== 0 and "+ "v"+str(index2)+" == 1),("+"v"+str(index1)+","+"v"+str(index2)+") \n")

            print("("+"v"+str(index1)+" == 0 and "+"v"+str(index2)+" == 0) or ("+"v"+str(index1)+" == 1 and "+ "v"+str(index2)+" == 1) or ("+"v"+str(index1)+"== 0 and "+ "v"+str(index2)+" == 1),("+"v"+str(index1)+","+"v"+str(index2)+") \n")
            prob.addConstraint(
                            lambda parameter1, parameter2: 
                                    (parameter1 == 0 and parameter2 == 0 ) or
                                    (parameter1 == 1 and parameter2 == 1  )or
                                    (parameter1 == 0 and parameter2 == 1  ),
                                    ("v"+str(index1),"v"+str(index2)), 
                                )
    


    ###############################################################################
    # ALTERNATIVE RELATIONSHIPS
    ###############################################################################

    #considered the variable number of parameters for alternative constraints
    #we need to dynamically generate both indexes and expression for lambda
    def alternative():
        print("Alternative Relationship\n")
        stepbystep.write("Alternative Relationships \n")
        file1 = open('linuxFiles/alternativeRelationships.txt')
        lines = file1.readlines()

        # Strips the newline character
        for line in lines:
            line = line.replace(' ','')
            line = line.replace("\n", "")
            listOfParameters = np.array(line.split(",") )
        
            paramIndeces=[]#indeces of parameters that we can find in the vars array
            for param in listOfParameters:
                indexParam = list(listOfFeatures).index(param)
                paramIndeces.append( indexParam)
            #print(paramIndeces, "size",len(paramIndeces))
            
            #generate a list of parameters for the lambda function
            lambdaParameters = []
            count = 0
            for index in paramIndeces:
                lambdaParameters.append("parameter"+str(count))
                count+=1
            #print(lambdaParameters)
            #generate the correct list of variables involved in the python constraint for the addConstraintfunction
            #example:[v205,v261,v262]
            variables = []
            for index in paramIndeces:
                variables.append("v"+str(index))
        # print(variables)

            #now we need to create the expression for the alternative constraint
            ######CODE FORE POSITIVE PART:  P1 <=> P2    P1 = 0 and P2 =0
            expressionTotal  = ""
            expressionPartial = ""
            for i in range(1,len(lambdaParameters)):#starting at index 1, first parameter goes in the back of expression
                expressionPartial = "("+str(lambdaParameters[i])+"==0 and ("
                for j in range(1,len(lambdaParameters)):
                    if (lambdaParameters[j] != lambdaParameters[i]):
                        expressionPartial = expressionPartial+str(lambdaParameters[j])+"==1 and "
                expressionPartial = expressionPartial+ str(lambdaParameters[0])+"==0 ) == 0 )"
                if expressionTotal == "":
                    expressionTotal = expressionTotal+expressionPartial
                else:
                    expressionTotal = expressionTotal+" and "+expressionPartial
        

            expressionTotal = expressionTotal+" or "
            ######CODE FORE POSITIVE PART:  P1 <=> P2    P1 = 1 and P2 =1
            for i in range(1,len(lambdaParameters)):#starting at index 1, first parameter goes in the back of expression
                expressionPartial = " ("+str(lambdaParameters[i])+"==1 and ("
                for j in range(1,len(lambdaParameters)):
                    if (lambdaParameters[j] != lambdaParameters[i]):
                        expressionPartial = expressionPartial+str(lambdaParameters[j])+"==0 and "
                expressionPartial = expressionPartial+ str(lambdaParameters[0])+"==1 ) == 1 )"
            
                if i == 1: #concatenate with an end only if it is not the firs parameter
                    expressionTotal = expressionTotal+expressionPartial
                else:
                    expressionTotal = expressionTotal+" and "+expressionPartial
        
            
            print(expressionTotal+"\n")
            stepbystep.write(str(expressionTotal)+"\n")
            prob.addConstraint(
                            lambda *lambdaParameters: #to pass variable number of parameters
                                    expressionTotal,
                                    variables
                                )
    ###############################################################################
    # OR RELATIONSHIPS
    ###############################################################################
    def orRelationship():
        print("OR Relationship\n")
        stepbystep.write("OR Relationships \n")
        file1 = open('linuxFiles/orRelationships.txt')
        lines = file1.readlines()

        # Strips the newline character
        for line in lines:
            line = line.replace(' ','')
            line = line.replace("\n", "")
            listOfParameters = np.array(line.split(",") )
        
            paramIndeces=[]#indeces of parameters that we can find in the vars array
            for param in listOfParameters:
                indexParam = list(listOfFeatures).index(param)
                paramIndeces.append( indexParam)
            #print(paramIndeces, "size",len(paramIndeces))
            
            #generate a list of parameters for the lambda function
            lambdaParameters = []
            count = 0
            for index in paramIndeces:
                lambdaParameters.append("parameter"+str(count))
                count+=1
            #print(lambdaParameters)
            #generate the correct list of variables involved in the python constraint for the addConstraintfunction
            #example:[v205,v261,v262]
            variables = []
            for index in paramIndeces:
                variables.append("v"+str(index))
            #print(variables)

            #now we need to create the expression for the alternative constraint
            ######CODE FORE POSITIVE PART:  P1 <=> P2    P1 = 0 and P2 =0
            expressionTotal  = "("+str(lambdaParameters[0])+"==0 and ("
        
            for i in range(1,len(lambdaParameters) -1):#starting at index 1, first parameter goes in the back of expression
                expressionTotal = expressionTotal+str(lambdaParameters[i])+"==0 or "
            expressionTotal =expressionTotal + str(lambdaParameters[-1])+"==0 )) "
            
            expressionTotal =expressionTotal +" or ("

            expressionTotal  = expressionTotal +str(lambdaParameters[0])+"==1 and ("
            for i in range(1,len(lambdaParameters) -1):#starting at index 1, first parameter goes in the back of expression
                expressionTotal = expressionTotal+str(lambdaParameters[i])+"==1 or "
            expressionTotal =expressionTotal + str(lambdaParameters[-1])+"==1 )) "

            print(expressionTotal+"\n")
            stepbystep.write(str(expressionTotal)+"\n")
            prob.addConstraint(
                            lambda *lambdaParameters: 
                                    expressionTotal,
                                    variables
                                )
    def threeCNF():
        print("3CNF constraints\n")
        stepbystep.write("3CNF Constraints \n")
        file1 = open('linuxFiles/constraints.txt')
        lines = file1.readlines()
        # Strips the newline character
        for line in lines:
            line = line.replace(' ','')
            line = line.replace("\n", "")
            listOfParameters = np.array(line.split(",") )
            
            paramIndeces=[]#indeces of parameters that we can find in the vars array
            for param in listOfParameters:
                indexParam = list(listOfFeatures).index(param)
                paramIndeces.append( indexParam)
            #print(paramIndeces, "size",len(paramIndeces))
            
            #generate a list of parameters for the lambda function
            lambdaParameters = []
            count = 0
            for index in paramIndeces:
                lambdaParameters.append("parameter"+str(count))
                count+=1
            #print(lambdaParameters)
            #generate the correct list of variables involved in the python constraint for the addConstraintfunction
            #example:[v205,v261,v262]
            variables = []
            for index in paramIndeces:
                variables.append("v"+str(index))
            #print(variables)

            #now we need to create the expression for the  3cnf constraint
            ######CODE FORE POSITIVE PART:  P1 <=> P2    P1 = 0 and P2 =0
            expressionTotal  = "("+str(lambdaParameters[0])+"==0 or ("
        
            for i in range(1,len(lambdaParameters) -1):#starting at index 1, first parameter goes in the back of expression
                expressionTotal = expressionTotal+str(lambdaParameters[i])+"==1 or "
            expressionTotal =expressionTotal + str(lambdaParameters[-1])+"==1 )) "
            
            print(expressionTotal+"\n")
            stepbystep.write(str(expressionTotal)+"\n")
            #print(expressionTotal)
            prob.addConstraint(
                            lambda *lambdaParameters: 
                                    expressionTotal,
                                    variables
                                )


    prob = constraint.Problem()

    with open('linuxFiles/products.txt') as f:
        listOfFeatures = f.readline().rstrip().split(",") #the first line in the file is the list of features

    listOfFeatures = [x.strip(' ') for x in listOfFeatures] #remmove white spaces
    listOfFeatures = np.array(listOfFeatures)

    #ADDINT THESE CONSTRAINTS ONCE TO THE PROBLEM,
    #then for each transaction in each testset, the solve method is called and a producttable constraint is added.
    mandatory()
    optional("linuxFiles/optionalRelationships.txt")
    optional("linuxFiles/requireConstraints.txt")
    alternative()
    orRelationship()
    threeCNF()

    return prob

def solve(prob,valueOrder,productConfigurations):
    
    def kbConstraint(*vars):
        transaction = []
        count = 0
        for v in vars:   
            count+=1
            transaction.append(v)
    
        #we want this transaction to be consistent with at least one of the products in the product table
        
        counttable=0
        consistent = 0
        for product in productTable:
            #print("product", product)
            #print("transactioN",transaction)
            
            comparison = (product == transaction).all()
            if comparison:
                consistent = 1
                print("is consistent"),
            counttable+=1

        print("counttable",counttable)
       # sys.exit()   

        if consistent == 1:
            return True
        
        return False
    ##################END AUXILIARY FUNCTIONS##########################






    ###################################################################
    #  M A I N 
    ###################################################################

    

    #print(listOfFeatures)
    #print(listOfFeatures.size)
    
    productTable = productConfigurations 

    domains =[]
    numberOfVariables = 263
    vars = []#list of variables, we have 263 of them

    #listOfFeatures: [Accessibility' ' Appearance' ' BrightnessAndLock' ' Displays1','   '    ]
    #vars:           [v0,              v1 ,          v2 ,                 v3,  ....  v262]
    #create a list of 263 variables with domain 0,1 and add them to the newprob
    

    for order in valueOrder: #we use the order of the closest neighbour (python will take the last element in the domain, which is the highest)
        domains.append(order)
    
    for i in range(0,numberOfVariables):
        vars.append("v"+str(i))
        prob.addVariable(vars[i],domains[i])



    #print("domains",domains)
    #print(prob._variables)

    #prob.addConstraint(kbConstraint, vars) #this constraint is created without lambda
   # kbConstraint()

    #print(prob._constraints)

    solution = prob.getSolution()
    #print("--- %s seconds ---" % (time.time() - start_time))
        
    #print("SOLAS",solution)
    solution_array = []

    if solution != None:
        for i in range(0,numberOfVariables):
            solution_array = np.append(solution_array, solution["v"+str(i)]) #we need to take the variables in order because for some reason python mixes them in the solution

        
            

    #print("solutionarray",solution_array)
       
    prob.reset()
    return solution_array #, (time.time() - start_time)
####################################################


######################## RELATIONSHIPS AND CONSTRAINT ##########################
######################## CREATION FROM FILES          ############################


