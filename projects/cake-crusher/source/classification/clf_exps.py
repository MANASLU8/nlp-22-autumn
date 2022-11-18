import re
import pickle
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from metrics import calculate_metrics, training_time
from time import time


def get_vectors(path, surface: bool):
    X = []
    y = []
    pattern = r'(?<=[a-z])\.' if surface else r'\t'
    with open(path, 'r') as file:
        for line in file:
            vector = []
            split = re.split(pattern, line)
            label = split[0] if surface else re.split(r'/', split[0])[0]
            y.append(label)
            embeddings = re.split(r'\t', line)[1:]
            for embedding in embeddings:
                embedding = embedding if '\n' not in embedding else embedding[:-1]
                vector.append(embedding)
            X.append(vector)
    return X, y


def get_vectorized(surface: bool):
    X_train, y_train = get_vectors('../../assets/annotated-corpus/train-embeddings.tsv', surface)
    X_test, y_test = get_vectors('../../assets/annotated-corpus/test-embeddings.tsv', surface)

    return X_train, y_train, X_test, y_test
    # with open('../../assets/vec_data', 'wb') as file:
    #     pickle.dump(vec_data, file)

def svm_pipe(X_train, y_train, X_test, y_test, **params):
    clf = svm.SVC(**params)
    print("Training...")
    t1 = time()
    clf.fit(X_train, y_train)
    t2 = time()
    print(f'{clf} training time: {training_time(t1, t2)}')
    pred = clf.predict(X_test)
    # pred = [item.split()[-1] for item in pred]
    calculate_metrics(y_test, pred)


def main():
    X_train, y_train, X_test, y_test = get_vectorized(surface=True)
    X_train = np.array(X_train, dtype=float)
    X_test = np.array(X_test, dtype=float)
    encoder = LabelEncoder()
    y_train = encoder.fit_transform(y_train)
    y_test = encoder.fit_transform(y_test)

    # pca = PCA(2)
    # df = pca.fit_transform(X_train)
    # X_testa = pca.fit_transform(X_test)
    # model = KMeans(n_clusters=20)
    # label = model.fit_predict(df)
    # u_labels = np.unique(y_train)
    # for i in u_labels:
    #     plt.scatter(df[label == i, 0], df[label == i, 1], label=i)
    # plt.legend()
    # plt.show()

    svm_pipe(X_train, y_train, X_test, y_test, kernel='linear')
    svm_pipe(X_train, y_train, X_test, y_test, kernel='poly', C=1.0)
    svm_pipe(X_train, y_train, X_test, y_test, kernel='rbf', C=1.0, degree=3, gamma='auto')

    mlp_clf = MLPClassifier(max_iter=500) #activation='relu')
    print("Training...")
    t1 = time()
    mlp_clf.fit(X_train, y_train)
    t2 = time()
    print(f'{mlp_clf} training time: {training_time(t1, t2)}')
    pred = mlp_clf.predict(X_test)
    calculate_metrics(y_test, pred)


if __name__ == "__main__":
    main()
