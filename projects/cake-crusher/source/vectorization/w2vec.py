import pickle
import gensim.models
import re
import nltk
import os
import numpy as np
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
from util import text_by_sentence_tokenize

stops = set(stopwords.words("english"))
with open("../../assets/cropped_dictionary", "rb") as file:
    dictionary = pickle.load(file)


# предложения документов train без стоп-слов и пунктуации для word2vec
def make_sentence_list_by_file():
    sentence_list_by_file = dict()
    data_path = '../../assets/annotated-corpus/'
    set_name = 'train'
    print('Collecting train sentences...')
    for category in os.listdir(data_path + set_name):
        for filename in os.listdir(data_path + set_name + '/' + category):
            sentence_list = []
            token_list = []
            with open(data_path + set_name + '/' + category + '/' + filename) as file:
                for line in file:
                    if line != '\n':
                        token = re.split(r'\t', line)[0]
                        # punctuation cleaner
                        if re.fullmatch(r'[\'!()\\\-\[\]{};@?<>:\",./^&*_|+`%#=~]+', token) \
                                or token in stops or token not in dictionary:
                            continue
                        token_list.append(token)
                    else:
                        sentence_list.append(token_list)
                        token_list = []
            sentence_list_by_file[category + '/' + filename] = sentence_list
            sentence_list = []

    with open("../../assets/sentence_list_by_file", "wb") as file:
        pickle.dump(sentence_list_by_file, file)
# with open("../../assets/sentence_list_by_file", "rb") as file:
#     sentence_list_by_file = pickle.load(file)


class MyCorpus:
    def __init__(self, sentence_list_by_file):
        self.sentence_list_by_file = sentence_list_by_file

    def __iter__(self):
        for filename in self.sentence_list_by_file:
            for sentence_index, sentence in enumerate(sentence_list_by_file[filename]):
                yield sentence_list_by_file[filename][sentence_index]


# task 6, 7
def w2vec_vectorize(text: str):
    model = gensim.models.Word2Vec.load('../../assets/w2v_model')
    sentence_list = text_by_sentence_tokenize(text)
    sent_vectors = []
    for sentence in sentence_list:
        vectors = []
        for token in sentence:
            if token not in stops:
                try:
                    vectors.append(model.wv[token])
                except Exception as e:
                    print(e)

        sent_vector = np.zeros(model.vector_size)
        if (len(vectors) > 0):
            sent_vector = (np.array([sum(x) for x in zip(*vectors)])) / sent_vector.size
        sent_vectors.append(sent_vector)

    vector = np.zeros(model.vector_size)
    if (len(sent_vectors) > 0):
        vector = (np.array([sum(x) for x in zip(*sent_vectors)])) / vector.size

    return vector


# model fitting
#make_sentence_list_by_file()
with open("../../assets/sentence_list_by_file", "rb") as file:
     sentence_list_by_file = pickle.load(file)
sentences = MyCorpus(sentence_list_by_file)
model = gensim.models.Word2Vec(sentences=sentences, window=10, vector_size=100, epochs=5)
print('Model trained!')
model.save('../../assets/w2v_model')
model = gensim.models.Word2Vec.load('../../assets/w2v_model')

#print(model.wv['hello'])
# for index, word in enumerate(model.wv.index_to_key):
#     print(f"word #{index}/{len(model.wv.index_to_key)} is {word}")
