from sklearn.neural_network import MLPClassifier
import numpy as np
import matplotlib.pyplot as plt
import array


X = np.genfromtxt('train_x.csv',delimiter=',',dtype=None, names=True)
X = np.array(X).tolist()

y = np.genfromtxt('train_y.csv',delimiter=',',dtype=None, names=True)
y = np.array(y).tolist()


clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                   hidden_layer_sizes=(5, 2), random_state=1)

clf.fit(X, y)

test_X = np.genfromtxt('test_x.csv',delimiter=',',dtype=None, names=True)
test_X = np.array(test_X).tolist()

test_y = np.genfromtxt('test_y.csv',delimiter=',',dtype=None, names=True)
# test_y = np.array(test_y).tolist()


result_y = clf.predict(test_X)
result_y = np.asarray(result_y)
print(len(result_y))
print(result_y.__len__())
xaxis = np.arange(1,50001,1)
print(xaxis.__len__())

plt.plot(np.arange(1,50001,1), result_y, linewidth = 2)
plt.show()

plt.plot(np.arange(1,50001,1), test_y, linewidth = 2)
plt.show()
