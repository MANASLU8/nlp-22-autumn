import pickle
import os
import pandas as pd
import re
from nltk.corpus import stopwords
import nltk
from copy import copy
from tokenizer import tokenizer

nltk.download('stopwords', quiet=True)
stops = set(stopwords.words("english"))


def get_td(dictionary):
    data_path = '../assets/annotated-corpus/'
    td = pd.DataFrame(columns=dictionary.keys())
    set_name = 'train'
    for category in os.listdir(data_path + set_name):
        for filename in os.listdir(data_path + set_name + '/' + category):
            td.loc[category + '/' + filename] = 0
            with open(data_path + set_name + '/' + category + '/' + filename) as file:
                for line in file:
                    if line != '\n':
                        token = re.split(r'\t', line)[0]
                        # очистка пунктуации и стоп слов
                        if re.fullmatch(r'[\'!()\\\-\[\]{};@?<>:\",./^&*_|+`%#=~]+', token) or token in stops:
                            continue
                        try:
                            td.at[category + '/' + filename, token] += 1
                        except:
                            pass
    return td


def get_tf(text, dictionary):
    token_list = tokenizer(text)
    # матрица частот токенов
    matrix_tf = pd.DataFrame(columns=dictionary.keys())
#    token_set = set(token_list)
    for token in token_list:
        matrix_tf.loc[token] = 0
    for token in token_list:
        if token in dictionary.keys():
            try:
                matrix_tf.at[token, token] += 1
            except:
                pass
    return matrix_tf

def get_dictionary(stops):
    data_path = '../assets/annotated-corpus/'
    dictionary = dict()
    count = 0
    set_name = 'train'
    for category in os.listdir(data_path + set_name):
        for filename in os.listdir(data_path + set_name + '/' + category):
            count += 1
            with open(data_path + set_name + '/' + category + '/' + filename) as file:
                for line in file:
                    if line != '\n':
                        token = re.split(r'\t', line)[0]
                        # очистка пунктуации и стоп слов
                        if re.fullmatch(r'[\'!()\\\-\[\]{};@?<>:\",./^&*_|+`%#=~]+', token) or token in stops:
                            continue
                        dictionary[token] = dictionary.get(token, 0) + 1
    cropped_dictionary = copy(dictionary)
    for token in dictionary:
        if dictionary[token] <= 5:
            del cropped_dictionary[token]
    del dictionary
    return cropped_dictionary

def main():
    dictionary = get_dictionary(stops)

    tf = get_tf("Many people travel for different purposes. Whether it is for a business trip or a holiday trip,"
                     " we see people travelling often."
                     " Some people prefer a hilly area for travelling while the others like travelling to places with beaches."
                     " In this travelling essay,"
                     " we will look at the importance of travelling and how it has changed ever since the old times.", dictionary)
    print(tf)

    #td = get_td(dictionary)
    #with open('../assets/td', 'wb') as file:
    #    pickle.dump(td, file)
    #print(td)


if __name__ == "__main__":
    main()

