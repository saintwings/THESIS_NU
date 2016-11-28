import numpy
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
# fix random seed for reproducibility

seed = 7
numpy.random.seed(seed)
# load pima indians dataset
dataset = numpy.loadtxt("./Postures/posture_test.csv", delimiter=",")
# split into input (X) and output (Y) variables
X = dataset[:,0:7]
Y = dataset[:,7]

print X
print Y

encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y)
# baseline model
def create_larger():
	# create model
	model = Sequential()
	model.add(Dense(14, input_dim=7, init='normal', activation='relu'))
	model.add(Dense(7, init='normal', activation='relu'))
	model.add(Dense(1, init='normal', activation='sigmoid'))
	# Compile model
	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model
# evaluate model with standardized dataset
estimator = KerasClassifier(build_fn=create_larger, nb_epoch=100, batch_size=7, verbose=1)
kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
results = cross_val_score(estimator, X, encoded_Y, cv=kfold)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
