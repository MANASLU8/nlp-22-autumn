import os
import re
import pickle
from gensim import corpora
from t_score import *
from collections import Counter
import matplotlib.pyplot as plt
import nltk
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
from nltk.collocations import *


def main():
    # сreating lemmas list
    data_path = '../../assets/annotated-corpus/'
    lemma_list = []
    for set_name in os.listdir(data_path):
        set_type = re.search(r'\w+$', set_name)[0]
        for category in os.listdir(data_path + set_name):
            for filename in os.listdir(data_path + set_name + '/' + category):
                with open(data_path + set_name + '/' + category + '/' + filename) as file:
                    for line in file:
                        if line != '\n':
                            lemma = re.split(r'(\t)', line)[2]
                            # punctuation cleaner
                            if re.fullmatch(r'[\'!()\\\-\[\]{};@?<>:\",./^&*_|+`%#=~]+', lemma):
                                # print('Skipped punctuation symbol ', lemma)
                                continue
                        else:
                            lemma = line
                        lemma_list.append(lemma)
    # print(lemma_list)
    with open("../../assets/lemma_list.txt", "wb") as file:
        pickle.dump(lemma_list, file)
    with open("../../assets/lemma_list.txt", "rb") as file:
        lemma_list = pickle.load(file)

    # to lower case
    [lemma.lower() for lemma in lemma_list]
    print('Lowered')

    # clean stop words
    stops = set(stopwords.words("english"))
    filtered_lemma_list = [lemma for lemma in lemma_list if lemma not in stops]
    with open("../../assets/filtered_lemma_list.txt", "wb") as file:
        pickle.dump(filtered_lemma_list, file)
    with open("../../assets/filtered_lemma_list.txt", "rb") as file:
        filtered_lemma_list = pickle.load(file)

    # extraction of threegrams
    threegrams_list = []
    for i in range(len(filtered_lemma_list) - 2):
        if filtered_lemma_list[i] == '\n' or filtered_lemma_list[i+1] == '\n' or filtered_lemma_list[i+2] == '\n':
            continue
        threegrams_list.append((filtered_lemma_list[i], filtered_lemma_list[i+1], filtered_lemma_list[i+2]))

    # counting frequency of threegrams
    freqs_dict = dict()
    for threegram in threegrams_list:
        freqs_dict[threegram] = freqs_dict.get(threegram, 0) + 1

    # deleting \n
    filtered_lemma_list = [lemma for lemma in filtered_lemma_list if lemma != '\n']

    # creating dictionary
    dictionary = corpora.Dictionary([filtered_lemma_list])
    print("The dictionary has: " + str(len(dictionary)) + " tokens")
    dictionary.save_as_text('../../assets/filtered_lemma_dictionary')
    dictionary.save('../../assets/filtered_lemma_dictionary')
    dictionary = corpora.Dictionary().load('../../assets/filtered_lemma_dictionary')

    # applying t-score
    scored_threegrams = dict()
    for threegram in freqs_dict:
        scored_threegrams[threegram] = t_score(threegram, freqs_dict, dictionary)
    with open("../../assets/result_dict.txt", "wb") as file:
        pickle.dump(scored_threegrams, file)
    with open("../../assets/result_dict.txt", "rb") as file:
        scored_threegrams = pickle.load(file)
    most_common_threegrams = Counter(scored_threegrams).most_common(30)
    result_dict = dict()
    for item in most_common_threegrams:
        threegram = item[0][0] + ' ' + item[0][1] + ' ' + item[0][2]
        result_dict[threegram] = round(item[1], 2)
    print(result_dict)
    fig = plt.figure(figsize=(20, 8))
    plt.bar(range(len(result_dict)), list(result_dict.values()))
    plt.xticks(range(len(result_dict)), list(result_dict.keys()), rotation=45, ha='right', rotation_mode='anchor')
    plt.tight_layout()
    plt.savefig('../../assets/t_score_bar_plot.png')
    plt.show()

    # checking results with nltk alternative
    with open("../../assets/filtered_lemma_list.txt", "rb") as file:
        filtered_lemma_list = pickle.load(file)
    trigram_measures = nltk.collocations.TrigramAssocMeasures()
    text = nltk.Text(filtered_lemma_list)
    finder_thr = TrigramCollocationFinder.from_words(text)
    print(finder_thr.nbest(trigram_measures.student_t, 30))

if __name__ == "__main__":
    main()
