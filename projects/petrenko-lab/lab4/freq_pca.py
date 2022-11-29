from sklearn.decomposition import PCA
from main import freq_vectorizer
import os
import pickle


vectors = []
train_path = "../lab1/20news-bydate-train/"
for category in os.listdir(train_path):
    limit = 0
    for filename in os.listdir(train_path + category):
        if limit == 100:
            with open("../assets/vectorized_train", "wb") as file:
                pickle.dump(vectors, file)
            break
        with open(train_path + category + '/' + filename) as file:
            vector = freq_vectorizer(file.read())
        vectors.append(vector)

with open("../assets/vectorized_train", "rb") as file:
    vectorized_train = pickle.load(file)
print(len(vectorized_train))


# fit PCA
pca = PCA(n_components=100)
pca_model = pca.fit(vectorized_train)

with open("../assets/pca_model", "wb") as file:
    pickle.dump(pca_model, file)
