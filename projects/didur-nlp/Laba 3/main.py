import os
import re
import pickle
import string
import json
from vocabulary import get_dictionary
from gensim import corpora
import heapq
from collections import Counter
import nltk
from math import pow, log2
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
from nltk.collocations import *

def mi(threegram, freqs_dict, dictionary, S):
    n = 3
    frequency = freqs_dict[threegram]
    multiplication = 1
    for lemma in threegram:
        multiplication *= dictionary[lemma]
        #print(frequency, dictionary.cfs[lemma_id], dictionary.num_pos)
    return log2((frequency * pow(S, n - 1)) / multiplication)

def main():
    # создание списка лемм
    data_path = '../assets/annotated-corpus/train/'
    lemma_list = []
    for category in os.listdir(data_path):
        for filename in os.listdir(data_path + '/' + category):
            with open(data_path + '/' + category + '/' + filename) as file:
                for line in file:
                    if line != '\n':
                        lemma = re.split(r'\t', line)[2][:-1]
                        printable = set(string.printable)
                        lemma = ''.join(i for i in lemma if i in printable)
                        if not lemma:
                            continue
                        if re.fullmatch(r'[\'!()\\\-\[\]{};@?<>:\",./^&*_|+`%#=~]+|.*[0-9$@!\]\[()=+^%\'`*;&^].*|\\x\d\d.*', lemma): #удаляем пунктуацию
                            continue
                    else:
                        lemma = line
                    lemma_list.append(lemma)
    with open("../assets/lemma_list.txt", "wb") as file:
        pickle.dump(lemma_list, file)
    with open("../assets/lemma_list.txt", "rb") as file:
        lemma_list = pickle.load(file)

    # приведение к строчному виду
    lemma_list = [lemma.lower() for lemma in lemma_list]
    print('Все буквы строчные')
    # удаляем стоп-слова (союзы частицы предлоги)
    stops = set(stopwords.words("english"))
    filtered_lemma_list = [lemma for lemma in lemma_list if lemma not in stops]
    with open("../assets/filtered_lemma_list.txt", "wb") as file:
        pickle.dump(filtered_lemma_list, file)
    with open("../assets/filtered_lemma_list.txt", "rb") as file:
        filtered_lemma_list = pickle.load(file)

    # извлечение триграмм
    threegrams_list = []
    for i in range(len(filtered_lemma_list) - 2):
        if filtered_lemma_list[i] == '\n' or filtered_lemma_list[i+1] == '\n' or filtered_lemma_list[i+2] == '\n':
            continue
        threegrams_list.append((filtered_lemma_list[i], filtered_lemma_list[i+1], filtered_lemma_list[i+2]))
    if ('\x08C', '\x08L', '\x08A') in threegrams_list:
        print('Estb')

    # подсчет частоты триграмм
    freqs_dict = dict()
    for threegram in threegrams_list:
        freqs_dict[threegram] = freqs_dict.get(threegram, 0) + 1
    #print(freqs_dict)
    if ('\x08C', '\x08L', '\x08A') in threegrams_list:
        print('Estb')

    # удаление \n для словаря
    lemma_list = filtered_lemma_list
    with open("../assets/lemma_list.txt", "wb") as file:
        pickle.dump(lemma_list, file)
    #filtered_lemma_list = [lemma for lemma in filtered_lemma_list if lemma != '\n']

    # создаем словарь
    dictionary, S = get_dictionary()
    #print(dictionary)
    if 'PROMETHEUS' in dictionary:
        print('Yes')
    # применение mi
    scored_threegrams = dict()
    for threegram in freqs_dict:
        scored_threegrams[threegram] = mi(threegram, freqs_dict, dictionary, S)
    with open("../assets/result_dict.txt", "wb") as file:
        pickle.dump(scored_threegrams, file)
    with open("../assets/result_dict.txt", "rb") as file:
        scored_threegrams = pickle.load(file)
    scored_threegrams = dict(sorted(scored_threegrams.items()))
    #most_common_threegrams = heapq.nlargest(30, scored_threegrams.items(), key=lambda i: i[1])
    most_common_threegrams = Counter(scored_threegrams).most_common(300)
    result_dict = dict()

    for item in most_common_threegrams:
        threegram = item[0][0] + ' ' + item[0][1] + ' ' + item[0][2]
        result_dict[threegram] = item[1]
    #result_dict = dict(sorted(result_dict.items()))
    print(result_dict)
    json.dump(result_dict, open("file_name.json", 'w'))
    #NLTK
    trigram_measures = nltk.collocations.TrigramAssocMeasures()
    text = nltk.Text(lemma_list)
    finder_thr = TrigramCollocationFinder.from_words(text)
    finder_thr.apply_ngram_filter(lambda *trigram: '\\n' in trigram)
    #print(finder_thr.nbest(trigram_measures.pmi, 30))
    scored_threegrams = dict()
    for i in finder_thr.score_ngrams(trigram_measures.pmi):
        scored_threegrams[i[0]] = i[1]
    most_common_threegrams = Counter(scored_threegrams).most_common(300)
    print(most_common_threegrams)

if __name__ == "__main__":
    main()