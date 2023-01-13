from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.neural_network import MLPClassifier
from gensim.models import Word2Vec
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from nltk.stem import SnowballStemmer
# from nltk.corpus import stopwords
from copy import copy
import pandas as pd
import pickle
import numpy as np
import re
import nltk
nltk.download('stopwords', quiet=True)
# nltk.download('punkt')
# stops = set(stopwords.words('english'))
stemmer = SnowballStemmer('english')


class Train:
    def __init__(self, all_sentences):
        self.all_sentences = all_sentences

    def __iter__(self):
        for filename in self.all_sentences:
            for sentence_index, sentence in enumerate(self.all_sentences[filename]):
                yield self.all_sentences[filename][sentence_index]


def my_tokenizer(text):
    sent_text = sent_tokenize(text)
    tokenized_text = [word_tokenize(sentence) for sentence in sent_text]
    clean = []
    for sentence in tokenized_text:
        sent = []
        for token in sentence:
            if re.fullmatch(r'[\'!()\\\[\]{};@?<>:\",./…^&*_|+`%#=~]+|.*[!?.{}%$#*()@<>:;^~\[\]].*', token):
                continue
            else:
                sent.append(stemmer.stem(token.lower()))
        if len(sent) >= 2:
            clean.append(sent)
    return clean


def word2vec_vectorize(tokenized_text, model):
    sent_vectors = []
    for sentence in tokenized_text:
        vectors = []
        for token in sentence:
            try:
                vectors.append(model.wv[stemmer.stem(token.lower())])
            except Exception as e:
                pass

        sent_v = np.zeros(model.vector_size)
        if len(vectors) > 0:
            sent_v = (np.array([sum(x) for x in zip(*vectors)])) / sent_v.size
        sent_vectors.append(sent_v)

    v = np.zeros(model.vector_size)
    if len(sent_vectors) > 0:
        v = (np.array([sum(x) for x in zip(*sent_vectors)])) / v.size

    return v


def train_and_evaluate(genre_to_vector, prefix):
    x = []
    y = []
    for genre in genre_to_vector:
        x.append(genre_to_vector[genre])
        label = re.split('_', genre)[0]
        y.append(label)
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.1)
    mlp = MLPClassifier(max_iter=4000)
    mlp.fit(X_train, y_train)
    print(mlp.classes_)
    y_pred = mlp.predict(X_test)
    with open(f'{prefix}_clf', 'wb') as file:
        pickle.dump(mlp, file)
    # оценка классификатора
    accuracy = accuracy_score(y_test, y_pred)
    print(accuracy)
    conf_matrix = confusion_matrix(y_test, y_pred)
    print(conf_matrix)


def main():
    # чтение данных
    df = pd.read_csv('spotify_songs.csv')
    df = df[['lyrics', 'playlist_genre', 'playlist_subgenre', 'language']]
    df = df[df['language'] == 'en']
    df = df[~df.playlist_genre.isin(['edm', 'latin'])]
    df = df.reset_index(drop=True)
    lyrics = df['lyrics']
    # subgenres = df['playlist_subgenre']
    # print(subgenres)

    # подготовка данных к обучению word2vec
    song_dict = dict()
    for i, text in enumerate(lyrics):
        tokens = my_tokenizer(text)
        song_dict[i] = tokens

    # обучение модели
    sentence_iterator = Train(song_dict)
    model = Word2Vec(sentences=sentence_iterator, vector_size=300, min_count=1, epochs=20, window=10)
    print('word2vec trained')
    model.save('word2vec_model')
    model = Word2Vec.load('word2vec_model')

    # # векторизация текстов песен
    song_to_vector = dict()
    for song in song_dict:
        vector = word2vec_vectorize(song_dict[song], model)
        song_to_vector[song] = vector

    with open('song_to_vector', 'wb') as file:
        pickle.dump(song_to_vector, file)

    # связывание с лейблами
    with open('song_to_vector', 'rb') as file:
        song_to_vector = pickle.load(file)
    print(len(song_to_vector))
    genre_to_vector = dict()
    pop_to_vector = dict()
    rock_to_vector = dict()
    rap_to_vector = dict()
    for i, genre in enumerate(df['playlist_genre']):
        if genre == 'pop':
            subgenre = df.at[i, 'playlist_subgenre']
            pop_to_vector[subgenre + f'_{i}'] = copy(song_to_vector[i])
        if genre == 'rock':
            subgenre = df.at[i, 'playlist_subgenre']
            rock_to_vector[subgenre + f'_{i}'] = copy(song_to_vector[i])
        if genre == 'rap':
            subgenre = df.at[i, 'playlist_subgenre']
            rap_to_vector[subgenre + f'_{i}'] = copy(song_to_vector[i])
        genre_to_vector[genre + f'_{i}'] = copy(song_to_vector[i])
    print(len(genre_to_vector))
    print(len(pop_to_vector))
    print(len(rock_to_vector))
    print(len(rap_to_vector))

    # обучение общего классификатора
    train_and_evaluate(genre_to_vector, 'all')

    # глубокий классификатор pop
    train_and_evaluate(pop_to_vector, 'pop')

    # глубокий классификатор rock
    train_and_evaluate(rock_to_vector, 'rock')

    # глубокий классификатор rap
    train_and_evaluate(rap_to_vector, 'rap')


if __name__ == "__main__":
    main()
