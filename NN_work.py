from sklearn.neural_network import MLPClassifier
import numpy as np


X = np.genfromtxt('PT0026_M_x.csv',delimiter=',',dtype=None, names=True)
X = np.array(X).tolist()

y = np.genfromtxt('PT0026_M_y.csv',delimiter=',',dtype=None, names=True)
y = np.array(y).tolist()


clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                   hidden_layer_sizes=(5, 2), random_state=1)

clf.fit(X, y)

print(clf.predict([[2., 2.,1.5,3.5, 2.5,0.8], [2., 2.,1.5,3.5, 2.5,0.8]]))

