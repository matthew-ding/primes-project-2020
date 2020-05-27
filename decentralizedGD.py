from sympy import *
import numpy as np
from scipy.spatial.distance import cdist, euclidean
import pandas as pd

### HYPERPARAMETERS
d = 30  # number of dimensions
m = 8  # number of nodes
n = 100  # total number of datapoints

byzantine_set = [4, 5, 9]  # set of byzantine nodes
adjList = {0: [3], 1: [3], 2: [3], 3: [0, 1, 2, 4, 5],
           4: [3, 6], 5: [3, 6], 6: [4, 5, 7, 8, 9], 7: [6], 8: [6], 9: [6]}

# adjList = {0: [4, 5], 1: [4, 5], 2: [4, 5], 3: [4, 5],
#           4: [0, 1, 2, 3, 6], 5: [0, 1, 2, 3, 6], 6: [4, 5, 7], 7: [6]}


my_data = pd.read_csv('dataset.txt')  # , names=nm)

X_set = []  # list of all x matrices
Y_set = []  # list of all y vectors
theta_set = []  # list of all parameter vectors
gradient_set = []
cost_set = []

for i in range(m):
    # Setting up X-Values
    X = my_data.iloc[i * int(n / m):(i + 1) * int(n / m), 0:d]
    ones = np.ones([X.shape[0], 1])
    X = np.concatenate((ones, X), axis=1)
    X_set.append(X)

    # Setting up costs (y values), .values converts it from pandas.core.frame.DataFrame to numpy.ndarray
    y = my_data.iloc[i * int(n / m):(i + 1) * int(n / m), d:d + 1].values
    Y_set.append(y)

    # parameter arrays
    theta = np.zeros([1, d + 1])
    theta_set.append(theta)
    gradient_set.append(theta)

    cost_set.append([])


def geometric_median(X, eps=1e-5):
    y = np.mean(X, 0)

    while True:
        D = cdist(X, [y])
        nonzeros = (D != 0)[:, 0]

        Dinv = 1 / D[nonzeros]
        Dinvs = np.sum(Dinv)
        W = Dinv / Dinvs
        T = np.sum(W * X[nonzeros], 0)

        num_zeros = len(X) - np.sum(nonzeros)
        if num_zeros == 0:
            y1 = T
        elif num_zeros == len(X):
            return y
        else:
            R = (T - y) * Dinvs
            r = np.linalg.norm(R)
            rinv = 0 if r == 0 else num_zeros / r
            y1 = max(0, 1 - rinv) * T + min(1, rinv) * y

        if euclidean(y, y1) < eps:
            return y1

        y = y1


# compute cost
def computeCost(X, y, theta):
    tobesummed = np.power(((X @ theta.T) - y), 2)
    return np.sum(tobesummed) / (2 * len(X))


def gradientDescent(iters, alpha, target):
    while True:
        iters += 1

        for i in range(m):
            calculateGradient(X_set[i], Y_set[i], theta_set[i], i)


        for i in range(m):
            currentNeighborGrad = []
            for j in range(m):
                if j == i or j in adjList[i]:
                    currentNeighborGrad.append(gradient_set[i])

            currentNeighborGrad = np.array(currentNeighborGrad)
            gradient = geometric_median(currentNeighborGrad)
            theta_set[i] = theta_set[i] - alpha * gradient

            cost_set[i].append(computeCost(X_set[i], Y_set[i], theta_set[i]))

        if iters % 1 == 0:
            print("Cost at iteration " + str(iters+1) + ": " + str(cost_set[target][iters]))

        if iters != 0:
            if abs(cost_set[target][iters] - cost_set[target][iters - 1]) < precision:
                break

    return theta_set[target], cost_set[target]


def calculateGradient(X, y, theta, i):
    gradient = (1.0 / len(X)) * np.sum(X * (X @ theta.T - y), axis=0)

    if i in byzantine_set:
        gradient*=1.0

    gradient_set[i] = gradient


# set hyper parameters
alpha = 0.001
iters = -1
precision = 0.0000001
target = 5

g, cost = gradientDescent(iters, alpha, target)

finalCost = computeCost(X, y, g)
print("Converges, Final Cost: " + str(finalCost) + "\n")

g = g.tolist()[0]

for i in range(1, len(g)):
    print("Variable: x" + str(i) + ", Coefficient: " + str(g[i]))

print("Constant: " + str(g[0]))

