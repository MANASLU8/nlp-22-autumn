import re
import numpy as np
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from metrics import calculate_metrics, training_time
from time import time


def get_vectors(path, is_surface: bool):
    X = []
    y = []
    pattern = r'(?<=[a-z])\.' if is_surface else r'\t'
    with open(path, 'r') as file:
        for line in file:
            vector = []
            split = re.split(pattern, line)
            label = split[0] if is_surface else re.split(r'/', split[0])[0]
            y.append(label)
            embeddings = re.split(r'\t', line)[1:]
            for embedding in embeddings:
                embedding = embedding if '\n' not in embedding else embedding[:-1]
                vector.append(embedding)
            X.append(vector)
    return X, y


def get_vectorized_data(is_surface: bool):
    X_train, y_train = get_vectors('../../assets/annotated-corpus/train-embeddings.tsv', is_surface)
    X_test, y_test = get_vectors('../../assets/annotated-corpus/test-embeddings.tsv', is_surface)

    return X_train, y_train, X_test, y_test


def ml_pipe(X_train, y_train, X_test, y_test, **params):
    parameters = params
    clf_name = parameters['clf']
    del parameters['clf']
    clf = clf_name(**parameters)
    print(f"Training {clf}...")
    t1 = time()
    clf.fit(X_train, y_train)
    t2 = time()
    print(f"{clf} training time: {training_time(t1, t2)}")
    pred = clf.predict(X_test)
    # pred = [item.split()[-1] for item in pred]
    calculate_metrics(y_test, pred)


def main():
    is_surface_list = [False, True]
    n_components = (100, 70, 50)
    for is_surface in is_surface_list:
        for number in n_components:
            print(f"Type: {'surface' if is_surface else 'full'} N_components = {number}")

            X_train, y_train, X_test, y_test = get_vectorized_data(is_surface=is_surface)
            if number != 100:
                pca = PCA(n_components=number)
                X_train = pca.fit_transform(X_train)
                X_test = pca.transform(X_test)
                print('PCA transformed')
            X_train = np.array(X_train, dtype=float)
            X_test = np.array(X_test, dtype=float)
            encoder = LabelEncoder()
            y_train = encoder.fit_transform(y_train)
            y_test = encoder.fit_transform(y_test)

            ml_pipe(X_train, y_train, X_test, y_test, clf=SVC, kernel='linear')
            ml_pipe(X_train, y_train, X_test, y_test, clf=SVC, kernel='poly', C=1.0)
            ml_pipe(X_train, y_train, X_test, y_test, clf=SVC, kernel='rbf', C=1.0, degree=3, gamma='auto')

            ml_pipe(X_train, y_train, X_test, y_test, clf=MLPClassifier, max_iter=500)


if __name__ == "__main__":
    main()
