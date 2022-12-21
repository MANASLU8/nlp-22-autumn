import pickle
import nltk
import numpy as np
import gensim.models
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
from lab1.tokenizer import to_tokens
from scipy import spatial

stop_words = set(stopwords.words("english"))

with open("../assets/dictionary", "rb") as file:
    dictionary = pickle.load(file)


def cosinus(a, b):
    return 1 - spatial.distance.cosine(a, b)


def word2vec_vectorize(text):
    model = gensim.models.Word2Vec.load('../assets/word2vec_model')
    sentence_list = to_tokens(text)
    s_vectors = []
    for sentence in sentence_list:
        vectors = []
        for token in sentence:
            try:
                vectors.append(model.wv[token.lower()])
            except:
                pass

        sent_v = np.zeros(model.vector_size)
        if len(vectors) > 0:
            sent_v = (np.array([sum(x) for x in zip(*vectors)])) / sent_v.size
        s_vectors.append(sent_v)

    v = np.zeros(model.vector_size)
    if len(s_vectors) > 0:
        v = (np.array([sum(x) for x in zip(*s_vectors)])) / v.size

    return v


class Train:
    def __init__(self, all_sentences):
        self.all_sentences = all_sentences

    def __iter__(self):
        for sentence in self.all_sentences:
            yield sentence


def main():
    with open("../assets/all_sentences", "rb") as file:
        all_sentences = pickle.load(file)
    sentence_iterator = Train(all_sentences)
    model = gensim.models.Word2Vec(sentences=sentence_iterator)
    print('word2vec trained')
    model.save('../assets/word2vec_model')

    # check word2vec
    cat = {'word': 'cat', '1': ['tiger', 'rabbit'], '2': ['animal', 'home'], '3': ['god', 'money']}
    computer = {'word': 'computer', '1': ['laptop', 'pc'], '2': ['mouse', 'display'], '3': ['gun', 'hair']}
    os = {'word': 'os', '1': ['unix', 'mac'], '2': ['memory', 'program'], '3': ['baseball', 'car']}
    themes = [cat, computer, os]

    for index, word_dict in enumerate(themes):
        vector = []
        vect_main_word = model.wv[word_dict['word']].tolist()
        vector.append(vect_main_word)
        base_word = word_dict['word']
        result = []
        length = 2
        for i in range(length):

            similar_word = word_dict['1'][i]
            field_word = word_dict['2'][i]
            different_word = word_dict['3'][i]

            vect_similar_word = model.wv[similar_word].tolist()
            vect_field_word = model.wv[field_word].tolist()
            vect_different_word = model.wv[different_word].tolist()
            vector.extend([vect_similar_word, vect_field_word, vect_different_word])

            value = cosinus(vect_main_word, vect_similar_word)
            result.append((similar_word, value))
            value = cosinus(vect_main_word, vect_field_word)
            result.append((field_word, value))
            value = cosinus(vect_main_word, vect_different_word)
            result.append((different_word, value))

        print(base_word, sorted(result, key=lambda a: a[1], reverse=True))

if __name__ == "__main__":
    main()
