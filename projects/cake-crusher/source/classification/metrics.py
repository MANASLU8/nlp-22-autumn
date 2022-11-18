from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from confusion_matrix import confusion_matrix


def calculate_metrics(y_test, pred):
    conf_matrix = confusion_matrix(y_test, pred)
    print(conf_matrix.to_string())
    acc = accuracy(conf_matrix)
    acc_lib = round(accuracy_score(y_test, pred), 2)
    prec = precision(conf_matrix)
    prec_lib = round(precision_score(y_test, pred, average='weighted', zero_division=1), 2)
    rec = recall(conf_matrix)
    rec_lib = round(recall_score(y_test, pred, average='weighted'), 2)
    f1 = f1_scr(conf_matrix)
    f1_lib = round(f1_score(y_test, pred, average='weighted'), 2)
    print(f'Custom | Library Accuracy: {acc} | {acc_lib}')
    print(f'Custom | Library Precision: {prec} | {prec_lib}')
    print(f'Custom | Library Recall: {rec} | {rec_lib}')
    print(f'Custom | Library F1: {f1} | {f1_lib}\n')


def precision(df_conf_matrix):
    df = df_conf_matrix
    numerator_sum = 0
    denominator_sum = 0

    for index, row in df.iterrows():
        TP, FP, FN = 0, 0, 0
    #     TP = пересечение
        TP = df[index].iloc[index]
    #     FP = сумма столбца кроме TP
        FP = df.loc[df[index] != TP, index].sum()
    #     FN = сумма строки кроме TP
        for item in row:
            FN += item if item != TP else 0
    #     TN = сумма всех клеток, пропуская строку и столбец соотв. лейблу
        if (TP + FP) != 0:
            numerator_sum += TP / (TP + FP) * (TP + FN)
    #     numerator_sum += (TP + FP) * TP / (TP + FN)
    #     denominator_sum += TP + FP
    return round(numerator_sum / df.to_numpy().sum(), 2)


def recall(df_conf_matrix):
    df = df_conf_matrix
    numerator_sum = 0
    denominator_sum = 0

    for index, row in df.iterrows():
        TP, FP, FN = 0, 0, 0
        #     TP = пересечение
        TP = df[index].iloc[index]
        #     FP = сумма столбца кроме TP
        FP = df.loc[df[index] != TP, index].sum()
        #     FN = сумма строки кроме TP
        for item in row:
            FN += item if item != TP else 0
        #     TN = сумма всех клеток пропуская строку и столбец соотв. лейблу
        #TN = df.to_numpy().sum() - (FP + TP) - FN

        if (TP + FN) != 0:
            numerator_sum += TP / (TP + FN) * (TP + FN)
    #     numerator_sum += (TP + FP) * TP / (TP + FN)
    #     denominator_sum += TP + FP
    return round(numerator_sum / df.to_numpy().sum(), 2)


def f1_scr(df_conf_matrix):
    pre = precision(df_conf_matrix)
    rec = recall(df_conf_matrix)
    return round(2 * pre * rec / (pre + rec), 2)


def accuracy(df_conf_matrix):
    df = df_conf_matrix
    TP_sum = 0
    sum = df.to_numpy().sum()
    for index, row in df.iterrows():
        TP_sum += df[index].iloc[index]
    return round(TP_sum/sum, 2)


def training_time(t1, t2):
    return t2 - t1
