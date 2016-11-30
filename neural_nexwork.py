import numpy as np
import matplotlib.pyplot as plt


X = np.array(([3,5],[5,1],[10,2]) , dtype = float)
y = np.array(([75],[82],[93]) , dtype = float)
X = X/np.amax(X, axis = 0)
y = y/100

def sigmoid(z):
    # apply sigmoid activaiton function
    return 1/(1+np.exp(-z))
testInput = np.arange(-6,6,0.1)
plt.plot(testInput, sigmoid(testInput), linewidth = 2)
plt.show()

class Neural_network(object):
    def _init_(self):
        self.inputLayerSize = 2
        self.outputLayerSize = 1
        self.hiddenLayerSize = 3

        # setting the weight
        self.W1 = np.random.randn(self.inputLayerSize, \
                                self.hiddenLayerSize)
        self.W2 = np.random.randn(self.hiddenLayerSize, \
                                self.outputLayerSize)

    def forward(self, X):
        #propagate inputs through network
        self.z2 = np.dot(X,self.W1)
        self.a2 = self.sigmoid(self.z2)
        self.z3 = np.dot(self.a2, self.W2)
        yHat = self.sigmoid(self.z3)
        return yHat
    def sigmoid(self, z):
        #Apply sigmoid actvation funtion to scalar, vector or array
        return 1/(1+np.exp(-z))
NN = Neural_network()
yHat = NN.forward(X)

weightsToTry = np.linspace(-10, 10, 1000)
costs = np.zeros(1000)
costs[i] = 0.5*sum((y-yHat)**2)

def sigmoidPrime(z):
    #Deriviative of Sigmoid Function
    return np.exp(-z)/((1+np.exp(-z))**2)

def costFunctionPrime(self, X, y):
    self.yHat = self.forward(X)

    delta3 = np.multiply(-(y-self.yHat), self.sigmoidPrime(self.z3))
    dJdW2 = np.dot(self.a2.T, delta3)

    delta2 = np.dot(delta3, self.W2.T)*self.sigmoidPrime(self.z2)
    dJdW1 = np.dot(X.T, delta2)

    return dJdW1, dJdW2

NN = Neural_network()
cost1 = NN.costFunction(X,y)

dJdW1, dJdW2 = NN.costFunctionPrime(X,y)
NN.W1 = NN.W1 - scalar*dJdW1
NN.W2 = NN.W1 - scalar*dJdW1
cost3 = NN.costFunction(X,y)
print cost3 ,cost2
