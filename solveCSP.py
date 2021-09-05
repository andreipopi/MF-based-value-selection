
import constraint
import time
import numpy as np


def solve(configHotEncodingValueOrder):

    problem = constraint.Problem()
 
    #by means of the configHotEncodingValueOrder and the correctConfiguration, we recreate the domains of each variable
    #in the correct order
    domain1= [61, 102, 123, 142, 162, 241, 242, 208, 209, 243, 363]
    domain2= [18, 25, 27, 30, 32]
    domain3= [1, 2]
    domain4 =[1, 2]
    domain5 = [1, 2]
    domain6 = [1, 2]
    domain7=  [1, 2, 3, 4, 5, 6]
    domain8= [20, 30, 35, 50, 58, 78]
    domain9=  [445, 455, 460, 470, 475, 505, 530, 535, 560, 675, 700, 765, 840, 850, 860, 980, 1405]
    domain10 = [189, 399, 400, 469, 479, 499, 579, 581, 609, 659, 669, 749, 1129, 1649, 2149, 2329, 2749, 3229, 5219]
    
    #product table
    pc = np.array([
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


    orderV1 = []
    orderV2 = []
    orderV3 = []
    orderV4 = []
    orderV5 = []
    orderV6 = []
    orderV7 = []
    orderV8 = []
    orderV9 = []
    orderV10 = []


    #[1,223,1,4,1,24,]
    i = 0
    for index in configHotEncodingValueOrder:
        if(i <= 10):  
            orderV1.append(domain1[index]) #append to the order of V1, the domain value at the index in the indices_ordering learned order
        elif i >= 11 and i <= 15:
            orderV2.append(domain2[index])
        elif i >= 16 and i <= 17:
            orderV3.append(domain3[index])
        elif i >= 18 and i <= 19:
            orderV4.append(domain4[index])
        elif i >= 20 and i <= 21:
            orderV5.append(domain5[index]) 
        elif i >= 22 and i <= 23:
            orderV6.append(domain6[index])
        elif i >= 24 and i <= 29:
            orderV7.append(domain7[index])
        elif i >= 30 and i <= 35:
            orderV8.append(domain8[index])
        elif i >= 36 and i <= 52:
            orderV9.append(domain9[index])
        elif i >= 53 and i <= 71:
            orderV10.append(domain10[index])
        i = i+1 

    problem.addVariable("v1", orderV1)
    problem.addVariable("v2", orderV2)
    problem.addVariable("v3", orderV3)
    problem.addVariable("v4", orderV4)
    problem.addVariable("v5", orderV5)
    problem.addVariable("v6", orderV6)
    problem.addVariable("v7", orderV7)
    problem.addVariable("v8", orderV8)
    problem.addVariable("v9", orderV9)
    problem.addVariable("v10", orderV10)

    def kbConstraint(v1,v2,v3,v4,v5,v6,v7,v8,v9,v10):
        transaction = np.array([v1,v2,v3,v4,v5,v6,v7,v8,v9,v10])

        prod1 = (pc[0]== transaction).all()
        prod2 = (pc[1]== transaction).all()
        prod3 = (pc[2]== transaction).all()
        prod4 = (pc[3]== transaction).all()
        prod5 = (pc[4]== transaction).all()
        prod6 = (pc[5]== transaction).all()
        prod7 = (pc[6]== transaction).all()
        prod8 = (pc[7]== transaction).all()
        prod9 = (pc[8]== transaction).all()
        prod10 = (pc[9]== transaction).all()
        prod11 = (pc[10]== transaction).all()
        prod12 = (pc[11]== transaction).all()
        prod13 = (pc[12]== transaction).all()
        prod14 = (pc[13]== transaction).all()
        prod15 = (pc[14]== transaction).all()
        prod16 = (pc[15]== transaction).all()
        prod17 = (pc[16]== transaction).all()
        prod18 = (pc[17]== transaction).all()
        prod19 = (pc[18]== transaction).all()
        prod20 = (pc[19]== transaction).all()

        if prod1 or prod2 or prod3 or prod4 or prod5 or prod6 or prod7 or prod8 or prod9 or prod10 or prod11 or prod12 or prod13 or prod14 or prod15 or prod16 or prod17 or prod18 or prod19 or prod20:
            print("true")
            return True

        return False

    #if display < 25 then no touchscreen 
    def simpleConstraint(v1,v7):
        #if v2 < 32:
        #    if v3 != 1:
        if v1 == 242:
            if v7 != 4:
                return False
        return True


    problem.addConstraint(kbConstraint, ["v1","v2","v3","v4","v5","v6","v7","v8","v9","v10"])
    #problem.addConstraint(simpleConstraint, ["v1","v7"])
    start_time = time.time()
    solution = problem.getSolution()
    #print("--- %s seconds ---" % (time.time() - start_time))
    print(solution)
        
    solution_array = []

    if solution != None:
        solution_array = np.append(solution_array, solution['v1'])
        solution_array = np.append(solution_array, solution['v2'])
        solution_array = np.append(solution_array, solution['v3'])
        solution_array = np.append(solution_array, solution['v4'])
        solution_array = np.append(solution_array, solution['v5'])
        solution_array = np.append(solution_array, solution['v6'])
        solution_array = np.append(solution_array, solution['v7'])
        solution_array = np.append(solution_array, solution['v8'])
        solution_array = np.append(solution_array, solution['v9'])
        solution_array = np.append(solution_array, solution['v10'])

    return solution_array, (time.time() - start_time)


