from nltk.corpus import stopwords
from nltk.collocations import *
from collections import Counter
from math import log2
import re
import os
import nltk

nltk.download('stopwords', quiet=True)


def mi(trigram, trigrams_dict, freq, n):
    fnc = trigrams_dict[trigram]
    denum = freq[trigram[0]] * freq[trigram[1]] * freq[trigram[2]]
    return log2(fnc * n ** 2 / denum)


def main():
    stop_words = set(stopwords.words("english"))
    data_path = '../assets/annotated-corpus/'
    tokens = []
    for label in os.listdir(data_path):
        for file in os.listdir(data_path + label):
            with open(data_path + label + '/' + file) as tsv:
                for row in tsv:
                    if row == '\n':
                        token = '\n'
                    else:
                        split = re.split(r'\t', row)
                        token = split[0]
                        if re.fullmatch(r'.*[0-9!?#$%^&*\]\[()|~{}\\+=<>\-\",_@`].*|'
                                        r'[_|+`%#=~;@?<>&*:\",./^\'!()\\\-\[\]{}]+', token):
                            continue
                    if token not in stop_words:
                        tokens.append(token.lower())

    # finding trigrams
    trigrams = []
    for i in range(len(tokens) - 2):
        if tokens[i] != '\n' and tokens[i + 1] != '\n' and tokens[i + 2] != '\n':
            trigrams.append((tokens[i], tokens[i + 1], tokens[i + 2]))

    # counting trigrams in frequency dict
    trigrams_dict = dict()
    for trigram in trigrams:
        trigrams_dict[trigram] = trigrams_dict.get(trigram, 0) + 1

    # creating dictionary
    raw_tokens = [token for token in tokens if token != '\n']
    frequency_dict = dict()
    for token in raw_tokens:
        frequency_dict[token] = frequency_dict.get(token, 0) + 1

    # mi scoring
    scored_trigrams = dict()
    for trigram in trigrams_dict:
        scored_trigrams[trigram] = mi(trigram, trigrams_dict, frequency_dict, len(tokens))
    best_trigrams = Counter(scored_trigrams).most_common(300)
    best_trigrams_dict = dict()
    for trigram in best_trigrams:
        best_trigrams_dict[trigram[0]] = round(trigram[1], 2)
    print(dict(sorted(best_trigrams_dict.items())))

    # nltk version
    trigram_measures = nltk.collocations.TrigramAssocMeasures()
    text = nltk.Text(tokens)
    finder_thr = TrigramCollocationFinder.from_words(text)
    # lambda w1, w2, w3: target_word not in (w1, w2, w3)
    finder_thr.apply_ngram_filter(lambda *words: '\\n' in words)
    best_trigrams = [(f"{p}: {round(s, 2)}")
                     for p, s in finder_thr.score_ngrams(trigram_measures.pmi)[:300]]
    # print(finder_thr.nbest(trigram_measures.pmi, 300))
    print(best_trigrams)


if __name__ == "__main__":
    main()
