import os
import re
import pickle
import pandas as pd
import numpy as np
from math import log10
from util import text_by_sentence_tokenize

with open("../../assets/df_cropped_dictionary", "rb") as file:
    dictionary = pickle.load(file)


def custom_vectorize(text: str, compressed: bool):
    sentence_list = text_by_sentence_tokenize(text)
    # Матрица частот
    freq_df = pd.DataFrame(columns=dictionary.keys())
    for sentence in sentence_list:
    # из term-document matrix - найти и добавить dfs в словарь
    # из словаря - брать dfs
        str_sentence = ""
        for token in sentence:
            str_sentence += ' ' + token
        str_sentence = str_sentence[1:]
        freq_df.loc[str_sentence] = 0
        for token in sentence:
            try:
                freq_df.at[str_sentence, token] += 1
            except:
                pass

    # Матрица tf-idf
    tf_idf_df = freq_df
    with open("../../assets/token_list_by_file", "rb") as file:
        token_list_by_file = pickle.load(file)
    N = len(token_list_by_file) # общее число документов в train
    del token_list_by_file
    for index, row in tf_idf_df.iterrows():
        for token in dictionary:
            if row[token] != 0:
                tf_idf_df.at[index, token] = row[token] * log10((N + 1)/(dictionary[token][1] + 1))

    vectorized_doc = []
    for token in dictionary:
        vectorized_doc.append(round(tf_idf_df[token].mean(), 3))

    if compressed:
        with open("../../assets/fitted_pca", "rb") as file:
            fitted_pca = pickle.load(file)
        vector = np.array(vectorized_doc).reshape(1, -1)
        vectorized_doc = fitted_pca.transform(vector)[0]

    return vectorized_doc
