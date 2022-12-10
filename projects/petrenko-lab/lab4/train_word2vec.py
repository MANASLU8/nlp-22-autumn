import os
from word2vector import word2vec_vectorize


train_path = "../lab1/20news-bydate-train/"
result = ""
count = 0
for category in os.listdir(train_path):
    for filename in os.listdir(train_path + category):
        print(filename, count)
        count += 1
        with open(train_path + category + '/' + filename) as file:
            vector = word2vec_vectorize(file.read())
            row = ""
            for embedding in vector:
                row += '\t' + str(round(embedding, 5))
            result += (category + '/' + filename + row + '\n')
with open('../assets/train-embeddings.tsv', 'w') as result_file:
    result_file.write(result)
