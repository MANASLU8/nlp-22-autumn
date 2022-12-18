import pandas as pd
import numpy as np


def calc_confusion_matrix(test, pred):
    y_actu = pd.Series(test, name='Actual')
    y_pred = pd.Series(pred, name='Predicted')
    df_confusion = pd.crosstab(y_actu, y_pred)
    for i in range(len(set(y_actu))):
        if i not in df_confusion.columns:
            df_confusion[i] = 0
    df_confusion = df_confusion.reindex(sorted(df_confusion.columns), axis=1)
    return df_confusion


def score_accuracy(cm):
    sum_all = cm.values.sum()
    sum_correct = 0
    for index, row in cm.iterrows():
        try:
            sum_correct += cm[index].iloc[index]
        except:
            pass
    return round(sum_correct / sum_all, 2)


def score_recall(cm):
    # micro
    sum_false_neg = 0
    sum_true_pos = 0
    for index, row in cm.iterrows():
        true_pos = cm[index].iloc[index]
        sum_true_pos += cm[index].iloc[index]
        for value in row:
            if value != true_pos:
                sum_false_neg += value
    recall = sum_true_pos / (sum_true_pos + sum_false_neg)
    return round(recall, 2)


def score_precision(cm):
    # micro
    sum_true_pos = 0
    sum_false_pos = 0
    for index, row in cm.iterrows():
        true_pos = cm[index].iloc[index]
        sum_true_pos += true_pos
        column_sum = cm[index].sum()
        sum_false_pos += column_sum - true_pos
    precision = sum_true_pos / (sum_true_pos + sum_false_pos)
    return round(precision, 2)


def score_f1(precision, recall):
    return round((2 * precision * recall / (precision + recall)), 2)
