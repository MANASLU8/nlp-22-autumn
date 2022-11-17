import pandas as pd


def confusion_matrix(y_actu, y_pred):
    y_actu = pd.Series(y_actu, name='Actual')
    y_pred = pd.Series(y_pred, name='Reference')
    df_conf_matrix = pd.crosstab(y_actu, y_pred)
    for i in range(len(set(y_actu))):
        if i not in df_conf_matrix.columns:
            df_conf_matrix[i] = 0
    return df_conf_matrix
