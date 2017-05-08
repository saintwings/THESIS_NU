import numpy as np
from sklearn import datasets
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, explained_variance_score
from sklearn.utils import shuffle

# Load housing data
data = datasets.load_boston()

# Shuffle the data
X, y = shuffle(data.data, data.target, random_state=7)

print(X[0],type(X))
print(y[0],type(y))