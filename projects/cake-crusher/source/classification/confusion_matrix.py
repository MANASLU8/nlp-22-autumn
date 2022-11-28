import pandas as pd


def confusion_matrix(y_actual, y_pred):
    y_actual = pd.Series(y_actual, name='Actual')
    y_pred = pd.Series(y_pred, name='Reference')
    df_conf_matrix = pd.crosstab(y_actual, y_pred)

    for i in range(len(set(y_actual))):
        if i not in df_conf_matrix.columns:
            df_conf_matrix[i] = 0
    df_conf_matrix = df_conf_matrix.reindex(sorted(df_conf_matrix.columns), axis=1)

    return df_conf_matrix
