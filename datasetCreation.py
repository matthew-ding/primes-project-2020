import numpy as np
import random

file = open("dataset.txt", "w")
file1 = open("coefficient.txt", "w")

d = 1000  # number of dimensions in input
n = 10000  # number of datapoints
sparseCoefficient = True

for i in range(d):
    file.write("x" + str(i + 1) + ",")

file.write("Cost" + "\n")

coefficients = []  # stores list of parameters (size d)
for i in range(d + 1):
    if sparseCoefficient:
        x = random.randrange(7)

        if x != 0:
            coefficients.append(0)
        else:
            coefficients.append(random.uniform(-10, 10))
    else:
        coefficients.append(random.uniform(-10, 10))

for i in range(d + 1):
    if i == d:
        file1.write("Constant: " + str(coefficients[i]) + "\n")
    else:
        file1.write("Variable: x" + str(i + 1) + ": " + str(coefficients[i]) + "\n")

for j in range(n):
    cost = 0
    line = ""
    for i in range(d + 1):
        if i == d:
            cost += coefficients[i]
        else:
            parameter = random.uniform(-10, 10)
            line += str(parameter) + ","
            cost += parameter * coefficients[i]

    file.write(str(line) + str(cost + np.random.normal(0, 2)) + "\n")