# tasks 5-6
import os
import pickle

from sklearn.decomposition import PCA
from tf_idf import custom_vectorize
from w2vec import w2vec_vectorize
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

# text = "Hello world! How are you?"
#
# # w2vec
# w2vec_vectorized_text = w2vec_vectorize(text)
# print(w2vec_vectorized_text)

# custom model
matrix = []
count = 0
train_path = "C:/Users/User/Desktop/dataset/20news-bydate-train/"
with open("../../assets/vectorized_train", "rb") as file:
    matrix = pickle.load(file)
number_processed = len(matrix)
print(number_processed)
big_count = 0
for category in os.listdir(train_path):
    count = 0
    for filename in os.listdir(train_path + category):
        if big_count < number_processed:
            big_count += 1
            continue
        print(filename, count)
        count += 1
        with open(train_path + category + '/' + filename) as file:
            vector = custom_vectorize(file.read())
            #print(vector)
        matrix.append(vector)
        if count == 100:
            with open("../../assets/vectorized_train", "wb") as file:
                pickle.dump(matrix, file)
            break
# vector = custom_vectorize(text, format=False)
# matrix.append(vector)
# pca = PCA(n_components=100)
# a = pca.fit_transform(vector)
# print(a)
# custom_vectorized_text = np.array(custom_vectorized_text).reshape(1, -1)
# pca = PCA(n_components=100)
# composed = pca.fit_transform(custom_vectorized_text)
