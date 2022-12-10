import pandas as pd
import numpy as np


def confusion_matrix(test, pred):
    df = pd.crosstab(test, pred, rownames=['Actual'], colnames=['Predicted'])
    for index, row in df.iterrows():
        if index not in df.columns:
            df[index] = 0
    return df

def calc_accuracy(conf_matrix_df):
    sum_all = conf_matrix_df.values.sum()
    pos = 0
    for index, row in conf_matrix_df.iterrows():
        try:
            pos += conf_matrix_df[index].loc[index]
        except:
            pass
    return round(pos/sum_all, 2)

def calc_precision(conf_matrix_df):
    # Нахождение precision для каждого класса, затем усреднение найденных precision
    return round((np.diag(conf_matrix_df) / np.sum(conf_matrix_df, axis=0)).mean(axis=0), 2)

def calc_recall(conf_matrix_df):
    # Нахождение recall для каждого класса, затем усреднение найденных recall
    return round((np.diag(conf_matrix_df) / np.sum(conf_matrix_df, axis=1)).mean(axis=0), 2)

def calc_f1(precision, recall):
    return round((2 * precision * recall / (precision + recall)), 2)


def score(test, pred):
    conf_matrix = confusion_matrix(test, pred)
    accuracy = calc_accuracy(conf_matrix)
    precision = calc_precision(conf_matrix)
    recall = calc_recall(conf_matrix)
    f1 = calc_f1(precision, recall)
    return conf_matrix, accuracy, precision, recall, f1