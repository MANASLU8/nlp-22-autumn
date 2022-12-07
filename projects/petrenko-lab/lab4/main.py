from lab1.tokenizer import to_tokens
import pandas as pd
import pickle
import copy
import os
import re
import numpy as np
import nltk
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
stop_words = set(stopwords.words("english"))


def freq_vectorizer(text):
    tokenized_text = to_tokens(text)
    with open("../assets/dictionary", "rb") as file:
        dictionary = pickle.load(file)
    with open("../assets/pca_model", "rb") as file:
        pca = pickle.load(file)
    freq_matrix = pd.DataFrame(columns=dictionary.keys())
    for sentence in tokenized_text:
        for token in sentence:
            # init 0 0 0...
            freq_matrix.loc[token] = 0
        for token in sentence:
            try:
                freq_matrix.at[token, token] += 1
            except:
                pass
    vector = []
    for token in dictionary:
        vector.append(round(freq_matrix[token].mean(), 3))
    vector = pca.transform(np.array(vector).reshape(1, -1))[0]

    return vector


def main():

    tokens = [] # for freq dictionary
    tokens_in_files = dict() # for termin-document matrix
    all_sentences = [] # for word2vec fitting

    stop_words = set(stopwords.words("english"))
    data = '../assets/annotated-corpus/'
    for label in os.listdir(data):
        for file in os.listdir(data + label):
            token_list = [] # for building tokens_in_files dictionary
            token_list_by_sentence = [] # for building all_sentences list
            with open(data + label + '/' + file) as tsv:
                for row in tsv:
                    if row == '\n':
                        token = '\n'
                        all_sentences.append(token_list_by_sentence)
                        token_list_by_sentence = []
                    else:
                        split = re.split(r'\t', row)
                        token = split[0]
                        if re.fullmatch(r'.*[0-9!?#$%^&*\]\[()|~{}\\+=<>\-\",_@`].*|'
                                        r'[_|+`%#=~;@?<>&*:\",./^\'!()\\\-\[\]{}]+', token):
                            continue
                    if token not in stop_words:
                        tokens.append(token.lower())
                        if token != '\n':
                            token_list.append(token.lower())
                            token_list_by_sentence.append(token.lower())
            tokens_in_files[label + '/' + file] = token_list

    with open('../assets/all_sentences', 'wb') as file:
        pickle.dump(all_sentences, file)

    # need dictionary
    raw_tokens = [token for token in tokens if token != '\n']
    frequency_dict = dict()
    for token in raw_tokens:
        frequency_dict[token] = frequency_dict.get(token, 0) + 1

    # filtering low frequency
    dictionary = copy.copy(frequency_dict)
    for token in frequency_dict:
        if frequency_dict[token] <= 6:
            del dictionary[token]
    del frequency_dict

    # save dictionary
    with open('../assets/dictionary', 'wb') as file:
        pickle.dump(dictionary, file)
    with open('../assets/dictionary', 'rb') as file:
        dictionary = pickle.load(file)

    # make termin-document matrix
    data = '../assets/annotated-corpus/'
    termin_document = pd.DataFrame(columns=dictionary.keys())
    for label in os.listdir(data):
        for file in os.listdir(data + label):
            print(file)
            termin_document.loc[label + '/' + file] = 0
            for token in tokens_in_files[label + '/' + file]:
                try:
                    termin_document.at[label + '/' + file, token] += 1
                except:
                    # токена нет в укороченном словаре
                    pass
    with open('../assets/termin_document', 'wb') as file:
        pickle.dump(termin_document, file)


if __name__ == "__main__":
    main()
