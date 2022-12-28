# task 8
import os
import gensim.models
from w2vec import w2vec_vectorize

model = gensim.models.Word2Vec.load('../../assets/w2v_model')
train_path = "C:/Users/User/Desktop/dataset/20news-bydate-train/"
result = ""
count = 0
for category in os.listdir(train_path):
    for filename in os.listdir(train_path + category):
        print(filename, count)
        count += 1
        with open(train_path + category + '/' + filename) as file:
            vector = w2vec_vectorize(file.read(), model)
            embedding_str = ""
            for embedding in vector:
                embedding_str += '\t' + str(round(embedding, 6))
            #print(category + '/' + filename + embedding_str + '\n')
            result += (category + '/' + filename + embedding_str + '\n')

with open('../../assets/annotated-corpus/train-embeddings.tsv', 'w') as result_file:
    result_file.write(result)
