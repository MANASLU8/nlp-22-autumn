# task 8
import os
from w2vec import w2vec_vectorize

test_path = "C:/Users/User/Desktop/dataset/20news-bydate-test/"
count = 0
for category in os.listdir(test_path):
    for filename in os.listdir(test_path + category):
        print(filename, count)
        count += 1
        with open(test_path + category + '/' + filename) as file:
            vector = w2vec_vectorize(file.read())
            embedding_str = ""
            for embedding in vector:
                embedding_str += '\t' + str(round(embedding, 6))
            print(category + '/' + filename + embedding_str + '\n')
            with open('../../assets/test_vectorized.tsv', 'a') as result_file:
                result_file.write(category + '/' + filename + embedding_str + '\n')
