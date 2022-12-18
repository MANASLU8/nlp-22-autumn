from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from scores import calc_confusion_matrix, score_accuracy, score_precision, score_recall, score_f1
from time import time
import numpy as np
import re


def main():
    # collect data from tsv lab4
    x_train, y_train, x_test, y_test = [], [], [], []
    for part in ["train", "test"]:
        #with open(f"../assets/{part}-embeddings.tsv") as f:
        with open(f"../assets/annotated-corpus/{part}-embeddings.tsv") as f:
            for row in f:
                line = re.split(r"\t", row)
                if part == "train":
                    y_train.append(re.split(r"/", line[0])[0])
                    x_train.append(line[1:-1])
                    x_train[-1].append(line[-1][:-1])
                else:
                    y_test.append(re.split(r"/", line[0])[0])
                    x_test.append(line[1:-1])
                    x_test[-1].append(line[-1][:-1])

    encoder = LabelEncoder()
    y_train = encoder.fit_transform(y_train)
    y_test = encoder.fit_transform(y_test)

    lin_svm = SVC(kernel="linear", random_state=1)
    t1 = time()
    lin_svm.fit(x_train, y_train)
    t2 = time()
    pred_lin = lin_svm.predict(x_test)
    conf_matrix = calc_confusion_matrix(y_test, pred_lin)
    accuracy = score_accuracy(conf_matrix)
    precision = score_precision(conf_matrix)
    recall = score_recall(conf_matrix)
    f1_score = score_f1(precision, recall)
    print(f"Training time: {t2 - t1} of model: {lin_svm}\n\n{conf_matrix.to_string()}\n\n"
          f"Accuracy: {accuracy}\nPrecision: {precision}\n"
          f"Recall: {recall}\nF1 Score: {f1_score}\n\n")


    rbf_svm = SVC(kernel="rbf", random_state=1)
    t1 = time()
    rbf_svm.fit(x_train, y_train)
    t2 = time()
    pred_rbf = rbf_svm.predict(x_test)
    conf_matrix = calc_confusion_matrix(y_test, pred_rbf)
    accuracy = score_accuracy(conf_matrix)
    precision = score_precision(conf_matrix)
    recall = score_recall(conf_matrix)
    f1_score = score_f1(precision, recall)
    print(f"Training time: {t2 - t1} of model: {rbf_svm}\n\n{conf_matrix.to_string()}\n\n"
          f"Accuracy: {accuracy}\nPrecision: {precision}\n"
          f"Recall: {recall}\nF1 Score: {f1_score}\n\n")

    poly_svm = SVC(kernel="poly", random_state=1)
    t1 = time()
    poly_svm.fit(x_train, y_train)
    t2 = time()
    pred_poly = poly_svm.predict(x_test)
    conf_matrix = calc_confusion_matrix(y_test, pred_poly)
    accuracy = score_accuracy(conf_matrix)
    precision = score_precision(conf_matrix)
    recall = score_recall(conf_matrix)
    f1_score = score_f1(precision, recall)
    print(f"Training time: {t2 - t1} of model: {poly_svm}\n\n{conf_matrix.to_string()}\n\n"
          f"Accuracy: {accuracy}\nPrecision: {precision}\n"
          f"Recall: {recall}\nF1 Score: {f1_score}\n\n")

    log_reg = LogisticRegression(random_state=1)
    x_train = np.array(x_train, dtype=float)
    x_test = np.array(x_test, dtype=float)
    t1 = time()
    log_reg.fit(x_train, y_train)
    t2 = time()
    pred_log_reg = log_reg.predict(x_test)
    conf_matrix = calc_confusion_matrix(y_test, pred_log_reg)
    accuracy = score_accuracy(conf_matrix)
    precision = score_precision(conf_matrix)
    recall = score_recall(conf_matrix)
    f1_score = score_f1(precision, recall)
    print(f"Training time: {t2 - t1} of model: {log_reg}\n\n{conf_matrix.to_string()}\n\n"
          f"Accuracy: {accuracy}\nPrecision: {precision}\n"
          f"Recall: {recall}\nF1 Score: {f1_score}\n\n")

    mlp = MLPClassifier(max_iter=500)
    t1 = time()
    mlp.fit(x_train, y_train)
    t2 = time()
    pred_mlp = mlp.predict(x_test)
    conf_matrix = calc_confusion_matrix(y_test, pred_mlp)
    accuracy = score_accuracy(conf_matrix)
    precision = score_precision(conf_matrix)
    recall = score_recall(conf_matrix)
    f1_score = score_f1(precision, recall)
    print(f"Training time: {t2 - t1} of model: {mlp}\n\n{conf_matrix.to_string()}\n\n"
          f"Accuracy: {accuracy}\nPrecision: {precision}\n"
          f"Recall: {recall}\nF1 Score: {f1_score}\n\n")

    # best model is MLP
    mlp = MLPClassifier(max_iter=1000)
    t1 = time()
    mlp.fit(x_train, y_train)
    t2 = time()
    pred_mlp = mlp.predict(x_test)
    conf_matrix = calc_confusion_matrix(y_test, pred_mlp)
    accuracy = score_accuracy(conf_matrix)
    precision = score_precision(conf_matrix)
    recall = score_recall(conf_matrix)
    f1_score = score_f1(precision, recall)
    print(f"Training time: {t2 - t1} of model: {mlp}\n\n{conf_matrix.to_string()}\n\n"
          f"Accuracy: {accuracy}\nPrecision: {precision}\n"
          f"Recall: {recall}\nF1 Score: {f1_score}\n\n")

    # с удалением некоторых фич
    cut_x_train = []
    cut_x_test = []
    throwed = [i for i in range(0, 101, 10)]
    for vector in x_train:
        new_vector = []
        new_vector.append([_ for i, _ in enumerate(vector) if i not in throwed])
        cut_x_train.append(new_vector[0])
    for vector in x_test:
        new_vector = []
        new_vector.append([_ for i, _ in enumerate(vector) if i not in throwed])
        cut_x_test.append(new_vector[0])
    print(len(cut_x_train))
    print(len(cut_x_train[101]))

    mlp = MLPClassifier(max_iter=1000)
    t1 = time()
    mlp.fit(cut_x_train, y_train)
    t2 = time()
    pred_mlp = mlp.predict(cut_x_test)
    conf_matrix = calc_confusion_matrix(y_test, pred_mlp)
    accuracy = score_accuracy(conf_matrix)
    precision = score_precision(conf_matrix)
    recall = score_recall(conf_matrix)
    f1_score = score_f1(precision, recall)
    print(f"Training time: {t2 - t1} of model: {mlp}\n\n{conf_matrix.to_string()}\n\n"
          f"Accuracy: {accuracy}\nPrecision: {precision}\n"
          f"Recall: {recall}\nF1 Score: {f1_score}\n\n")

    # с сокращением размерности
    for number in [10, 50, 75]:
        pca = PCA(n_components=number)
        x_train_pca = pca.fit_transform(x_train)
        x_test_pca = pca.transform(x_test)

        mlp = MLPClassifier(max_iter=1000)
        t1 = time()
        mlp.fit(x_train_pca, y_train)
        t2 = time()
        pred_mlp = mlp.predict(x_test_pca)
        conf_matrix = calc_confusion_matrix(y_test, pred_mlp)
        accuracy = score_accuracy(conf_matrix)
        precision = score_precision(conf_matrix)
        recall = score_recall(conf_matrix)
        f1_score = score_f1(precision, recall)
        print(f"Training time: {t2 - t1} of model: {mlp}\n\n{conf_matrix.to_string()}\n\n"
              f"Accuracy: {accuracy}\nPrecision: {precision}\n"
              f"Recall: {recall}\nF1 Score: {f1_score}\n\n")


if __name__ == "__main__":
    main()
