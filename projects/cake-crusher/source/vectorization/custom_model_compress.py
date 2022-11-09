# custom model
import os
import pickle
from sklearn.decomposition import PCA
from custom_model_tf_idf import custom_vectorize

matrix = []
count = 0
train_path = "C:/Users/User/Desktop/dataset/20news-bydate-train/"

for category in os.listdir(train_path):
    count = 0
    for filename in os.listdir(train_path + category):
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
with open("../../assets/vectorized_train", "rb") as file:
    vectorized_train = pickle.load(file)
print(len(vectorized_train))
print(len(vectorized_train[0]))

# train PCA
pca = PCA(n_components=100)
fitted_pca = pca.fit(vectorized_train)
with open("../../assets/fitted_pca", "wb") as file:
    pickle.dump(fitted_pca, file)
