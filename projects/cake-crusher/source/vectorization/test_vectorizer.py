# task 8
import os
import gensim.models
from w2vec import w2vec_vectorize

model = gensim.models.Word2Vec.load('../../assets/w2v_model')
test_path = "C:/Users/User/Desktop/dataset/20news-bydate-test/"
result = ""
count = 0
for category in os.listdir(test_path):
    for filename in os.listdir(test_path + category):
        print(filename, count)
        count += 1
        with open(test_path + category + '/' + filename) as file:
            vector = w2vec_vectorize(file.read(), model)
            embedding_str = ""
            for embedding in vector:
                embedding_str += '\t' + str(round(embedding, 6))
            result += (category + '/' + filename + embedding_str + '\n')

with open('../../assets/annotated-corpus/test-embeddings.tsv', 'w') as result_file:
    result_file.write(result)
