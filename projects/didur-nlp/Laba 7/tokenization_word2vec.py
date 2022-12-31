import pickle
import gensim.models
import re
import nltk
import os
import numpy as np
from nltk.tokenize import word_tokenize
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
import rulemma
import rupostagger

tagger = rupostagger.RuPosTagger()
tagger.load()

stops = set(stopwords.words('russian'))
lemmatizer = rulemma.Lemmatizer()
lemmatizer.load()


# предложения документов без стоп-слов и пунктуации для word2vec
def make_sentence_list_by_file():
    sentence_list_by_file = dict()
    data_path = '../../assets/preprocessed_articles/'
    print('Collecting sentences...')
    for category in os.listdir(data_path):
        for filename in os.listdir(data_path + '/' + category):
            with open(data_path + '/' + category + '/' + filename, encoding="utf-8") as file:
                text = file.read()
                sent_text = nltk.sent_tokenize(text, language="russian")
                tokenized_text = [word_tokenize(sentence) for sentence in sent_text]
                cleaned_tokenized_text = []
                for sentence in tokenized_text:
                    sent = []
                    for token in sentence:
                        if len(token) == 1 or \
                            token in stops or \
                            re.fullmatch(r'[\'!()\\\[\]{};@?<>:\",./…^&*_|+`%#=~]+|.*[!?.{}%$#*()@<>:;^~\[\]].*', token)\
                                or re.fullmatch(r'.*[a-z].*', token):
                            continue
                        else:
                            sent.append(token)
                    if len(sent) >= 4:
                        tags = tagger.tag(sent)
                        lemmas = lemmatizer.lemmatize(tags)
                        lemms = []
                        for lemma in lemmas:
                            lemms.append(lemma[2])
                        del lemmas
                        cleaned_tokenized_text.append(sent)
            sentence_list_by_file[category + '/' + filename] = cleaned_tokenized_text
    print(sentence_list_by_file)
    with open("../../assets/sentence_list_by_file_speech", "wb") as file:
        pickle.dump(sentence_list_by_file, file)


class MyCorpus:
    def __init__(self, sentence_list_by_file):
        self.sentence_list_by_file = sentence_list_by_file

    def __iter__(self):
        for filename in self.sentence_list_by_file:
            for sentence_index, sentence in enumerate(sentence_list_by_file[filename]):
                yield sentence_list_by_file[filename][sentence_index]


def sentences_to_vector(lst: [[str]], mdl):
    sentence_list = lst
    sent_vectors = []
    for sentence in sentence_list:
        word_vectors = []
        for token in sentence:
            if token not in stops:
                try:
                    word_vectors.append(mdl.wv[token.lower()])
                except Exception as e:
                    # print(e)
                    pass

        sent_vector = np.zeros(mdl.vector_size)
        if (len(word_vectors) > 0):
            sent_vector = (np.array([sum(x) for x in zip(*word_vectors)])) / sent_vector.size
        sent_vectors.append(sent_vector)

    vector = np.zeros(mdl.vector_size)
    if (len(sent_vectors) > 0):
        vector = (np.array([sum(x) for x in zip(*sent_vectors)])) / vector.size

    return vector

if __name__ == "__main__":
    #model fitting
    make_sentence_list_by_file()
    with open("../../assets/sentence_list_by_file_speech", "rb") as file:
        sentence_list_by_file = pickle.load(file)
    sentences = MyCorpus(sentence_list_by_file)
    model = gensim.models.Word2Vec(sentences=sentences, window=10, vector_size=50, epochs=10, min_count=1)
    print('Model trained!')
    model.save('../../assets/w2v_model')