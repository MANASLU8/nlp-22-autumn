from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import pickle
import re
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix


def ml_pipe(X_train, y_train, X_test, y_test, **params):
    parameters = params
    clf_name = parameters['clf']
    del parameters['clf']
    clf = clf_name(**parameters)
    print(f"Training {clf}...")
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(accuracy)
    conf_matrix = confusion_matrix(y_test, y_pred)
    print(conf_matrix)
    return clf


def main():

    with open('../../assets/file_to_vector', 'rb') as file:
        file_to_vector = pickle.load(file)

    X = []
    y = []
    for file in file_to_vector:
        X.append(file_to_vector[file])
        cls = re.split('/', file)[0]
        y.append(cls)

    X = np.array(X, dtype=float)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
    print(len(y_test))
    _ = ml_pipe(X_train, y_train, X_test, y_test, clf=SVC, probability=True)
    _ = ml_pipe(X_train, y_train, X_test, y_test, clf=RandomForestClassifier, class_weight='balanced')
    clf = ml_pipe(X_train, y_train, X_test, y_test, clf=MLPClassifier, max_iter=3000)

    with open('../../assets/mlp_clf', 'wb') as file:
        pickle.dump(clf, file)


if __name__ == "__main__":
    main()
