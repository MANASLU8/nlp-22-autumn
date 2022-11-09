# tasks 5-6
import pickle
from custom_model_tf_idf import custom_vectorize
from w2vec import w2vec_vectorize
import numpy as np
from util import cos_sim
from time import time


# with open('user_text.txt', 'r') as file:
#     text = file.read()
# with open("../../assets/fitted_pca", "rb") as file:
#     fitted_pca = pickle.load(file)
# vector = custom_vectorize(text, compressed=False)
# vector = np.array(vector).reshape(1, -1)
# compressed_custom_v = fitted_pca.transform(vector)
# print(compressed_custom_v[0])
# print(len(compressed_custom_v[0]))
# w2vec_vectorized_text = w2vec_vectorize(text)
# result = cos_sim(compressed_custom_v[0], w2vec_vectorized_text)
# print(result)
# "Studies show that a speaker is considered to be knowledgeable when they respond immediately.",
# "Studies demonstrate that a speaker is seen as more intelligent when they give an instant response.",

with open('user_text1.txt', 'r') as file:
    text1 = file.read()
with open('user_text2.txt', 'r') as file:
    text2 = file.read()
sentences1 = ["We are very accustomed to the art of speaking.",
              "We realize that moments of silence can be pretty uncomfortable.",
              text1]
sentences2 = ["We are used to the art of communicating.",
              "They favor things that are easy to understand over things that are difficult to make sense of.",
              text2]
index = 0
for i, j in zip(sentences1, sentences2):
    index += 1
    t0 = time()
    custom1 = custom_vectorize(i, compressed=True)
    custom2 = custom_vectorize(j, compressed=True)
    t1 = time()
    custom_mean_time = round((t1 - t0) / 2, 2)

    t0 = time()
    w2vec1 = w2vec_vectorize(i)
    w2vec2 = w2vec_vectorize(j)
    t1 = time()
    w2vec_mean_time = round((t1 - t0) / 2, 2)

    custom_sim = cos_sim(custom1, custom2)
    w2vec_sim = cos_sim(w2vec1, w2vec2)

    print(f'{index}. time: {custom_mean_time} sec %% Custom cosine similarity is {custom_sim}')
    print(f'{index}. time: {w2vec_mean_time} sec %% Word2vec cosine similarity is {w2vec_sim}\n')
