# tasks 5-6
import pickle
from custom_model_tf_idf import custom_vectorize
from w2vec import w2vec_vectorize
import numpy as np
from util import cos_sim

with open("../../assets/fitted_pca", "rb") as file:
    fitted_pca = pickle.load(file)

with open('user_text.txt', 'r') as file:
    text = file.read()

# custom model
vector = custom_vectorize(text)
vector = np.array(vector).reshape(1, -1)
compressed_custom_v = fitted_pca.transform(vector)
print(compressed_custom_v[0])
print(len(compressed_custom_v[0]))

# w2vec model
w2vec_vectorized_text = w2vec_vectorize(text)

# comparison
result = cos_sim(compressed_custom_v, w2vec_vectorized_text)
print(result)

