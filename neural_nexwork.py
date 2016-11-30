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

print sigmoid(1)

class Neural_network(object):
    def _init_(self, activication = "tanh"):
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
