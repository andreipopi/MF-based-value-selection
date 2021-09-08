import numpy as np
from random import randrange
import math
from numpy import genfromtxt
import random
import sys





file = open("linuxFiles/manyProducts.txt")
lines = file.readlines()


randomProductTable = open("randomProductTable.txt", "a")


for i in range(1000):
    randomint = random.randint(0,43892)
    print(randomint)
    randomProductTable.write(lines[randomint])

    

randomProductTable.close()

print(len(lines))

