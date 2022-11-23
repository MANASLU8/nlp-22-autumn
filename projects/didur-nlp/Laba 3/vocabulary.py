# creating dictionary
import os
import pickle
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords', quiet=True)

def get_dictionary():
    S = 0
    dictionary = dict()
    with open("../assets/lemma_list.txt", "rb") as file:
        lemma_list = pickle.load(file)
    for lemma in lemma_list:
        dictionary[lemma] = dictionary.get(lemma, 0) + 1
        S += 1
    # stops = set(stopwords.words("english"))
    # data_path = '../assets/annotated-corpus/'
    # dictionary = dict()
    # count = 0
    # S = 0
    # set_name = 'train'
    # for category in os.listdir(data_path + set_name):
    #     for filename in os.listdir(data_path + set_name + '/' + category):
    #         count += 1
    #         with open(data_path + set_name + '/' + category + '/' + filename) as file:
    #             for line in file:
    #                 if line != '\n':
    #                     token = re.split(r'\t', line)[2][:-1]
    #                     # punctuation and stop words cleaner
    #                     if re.fullmatch(r'[\'!()\\\-\[\]{};@?<>:\",./^&*_|+`%#=~]+', token) or token in stops:
    #                         # print('Skipped punctuation symbol or stop word', token)
    #                         continue
    #                     S += 1
    #                    dictionary[token] = dictionary.get(token, 0) + 1
                    # else:
                    #     token = line

    with open("../assets/dictionary", "wb") as file:
        pickle.dump(dictionary, file)
    return dictionary, S