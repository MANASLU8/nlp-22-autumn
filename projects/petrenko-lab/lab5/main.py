from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
from time import time
from estimation import score
import numpy as np


def read_from_tsv():
    x_train = []
    y_train = []
    with open("../assets/train-embeddings1.tsv", "r") as file:
        for line in file:
            if len(line) < 100:
                continue
            train = line.split('\t')
            train = train[:-1] + [train[-1][:-1]]
            x_train.append(train[1:])
            y_train.append(train[0].split('/')[0])
    x_test = []
    y_test = []
    with open("../assets/test-embeddings1.tsv", "r") as file:
        for line in file:
            if len(line) < 100:
                continue
            test = line.split('\t')
            # убрать \n
            test = test[:-1] + [test[-1][:-1]]
            x_test.append(test[1:])
            y_test.append(test[0].split('/')[0])
    return x_train, y_train, x_test, y_test


def main():
    for i in range(3):
        x_train, y_train, x_test, y_test = read_from_tsv()
        if i != 0:
            n_components = 50
            if i == 2:
                n_components = 10
            pca = PCA(n_components=n_components)
            x_train = pca.fit_transform(x_train)
            x_test = pca.transform(x_test)

        svc_lin = SVC(kernel="linear", random_state=10)
        time1 = time()
        svc_lin.fit(x_train, y_train)
        time2 = time()
        pred_lin = svc_lin.predict(x_test)
        conf_matrix, accuracy, precision, recall, f1 = score(y_test, pred_lin)
        print(f'Model: {svc_lin}, training time: {time2-time1}\n\n', f'{conf_matrix.to_string()}\n\n',
              f'accuracy: {accuracy}\n', f'precision: {precision}\n', f'recall: {recall}\n', f'f1: {f1}\n\n')

        svc_poly = SVC(kernel="poly", random_state=10)
        time1 = time()
        svc_poly.fit(x_train, y_train)
        time2 = time()
        pred_poly = svc_poly.predict(x_test)
        conf_matrix, accuracy, precision, recall, f1 = score(y_test, pred_poly)
        print(f'Model: {svc_poly}, training time: {time2-time1}\n\n', f'{conf_matrix.to_string()}\n\n',
              f'accuracy: {accuracy}\n', f'precision: {precision}\n', f'recall: {recall}\n', f'f1: {f1}\n\n')

        svc_rbf = SVC(kernel="rbf", class_weight="balanced", decision_function_shape="ovr", random_state=10 )
        time1 = time()
        svc_rbf.fit(x_train, y_train)
        time2 = time()
        pred_rbf = svc_rbf.predict(x_test)
        conf_matrix, accuracy, precision, recall, f1 = score(y_test, pred_rbf)
        print(f'Model: {svc_rbf}, training time: {time2-time1}\n\n', f'{conf_matrix.to_string()}\n\n',
              f'accuracy: {accuracy}\n', f'precision: {precision}\n', f'recall: {recall}\n', f'f1: {f1}\n\n')

        for max_iter in [500, 1000, 1500]:
            mlp = MLPClassifier(max_iter=max_iter)
            encoder = LabelEncoder()
            x_train = np.array(x_train, dtype=float)
            x_test = np.array(x_test, dtype=float)
            y_train = encoder.fit_transform(y_train)
            y_test = encoder.transform(y_test)
            time1 = time()
            mlp.fit(x_train, y_train)
            time2 = time()
            pred_mlp = mlp.predict(x_test)
            conf_matrix, accuracy, precision, recall, f1 = score(y_test, pred_mlp)
            print(f'Model: {mlp}, training time: {time2-time1}\n\n', f'{conf_matrix.to_string()}\n\n',
                  f'accuracy: {accuracy}\n', f'precision: {precision}\n', f'recall: {recall}\n', f'f1: {f1}\n\n')


if __name__ == "__main__":
    main()
