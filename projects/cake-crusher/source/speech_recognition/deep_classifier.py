from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from classification import ml_pipe
import re
import pickle
import numpy as np


with open('../../assets/file_to_vector', 'rb') as file:
    file_to_vector = pickle.load(file)

X = []
y = []
for file in file_to_vector:
    cls = re.split('/', file)[0]
    if cls in ['Maths', 'Physics']:
        X.append(file_to_vector[file])
        y.append(cls)

X = np.array(X, dtype=float)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

_ = ml_pipe(X_train, y_train, X_test, y_test, clf=RandomForestClassifier, class_weight='balanced')
clf = ml_pipe(X_train, y_train, X_test, y_test, clf=MLPClassifier, max_iter=3000)

with open('../../assets/deep_mlp_clf', 'wb') as file:
    pickle.dump(clf, file)
