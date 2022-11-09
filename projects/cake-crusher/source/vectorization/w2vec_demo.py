# task № 4
import gensim.models
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from util import cos_sim

# {'word': '', 'similar': [], 'same_field': [], 'different': []}
research = {'word': 'research', 'similar': ['scientific', 'analysis'], 'same_field': ['study', 'theory'],
            'different': ['fish', 'color']}
car = {'word': 'car', 'similar': ['tire', 'wheel'], 'same_field': ['money', 'speed', 'fuel', 'murder', 'horse'],
       'different': ['theory', 'rabbit']}
software = {'word': 'software', 'similar': ['code', 'hardware'], 'same_field': ['unix', 'windows'],
            'different': ['luck', 'cake']}
list_of_dicts = [research, car, software]


def infer(fitted_model, show: bool):
    if not fitted_model:
        model = gensim.models.Word2Vec.load('../../assets/w2v_model')
    else:
        model = fitted_model
    for word_dict in list_of_dicts:
        result = {'word': word_dict['word'], 'similar': dict(), 'same_field': dict(), 'different': dict()}
        annotations = []
        vector = []
        main_word = word_dict['word']
        annotations.append(main_word)
        vect_main_word = model.wv[main_word].tolist()
        vector.append(vect_main_word)
        for i in range(0, 2):
            similar_word = word_dict['similar'][i]
            field_word = word_dict['same_field'][i]
            different_word = word_dict['different'][i]
            annotations.extend([similar_word, field_word, different_word])

            vect_main_word = model.wv[main_word].tolist()
            vect_similar_word = model.wv[similar_word].tolist()
            vect_field_word = model.wv[field_word].tolist()
            vect_different_word = model.wv[different_word].tolist()
            vector.extend([vect_similar_word, vect_field_word, vect_different_word])

            sim = cos_sim(vect_main_word, vect_similar_word)
            result['similar'][similar_word] = sim
            sim = cos_sim(vect_main_word, vect_field_word)
            result['same_field'][field_word] = sim
            sim = cos_sim(vect_main_word, vect_different_word)
            result['different'][different_word] = sim

        result['similar'] = dict(sorted(result['similar'].items(), key=lambda x: x[1], reverse=True))
        result['same_field'] = dict(sorted(result['same_field'].items(), key=lambda x: x[1], reverse=True))
        result['different'] = dict(sorted(result['different'].items(), key=lambda x: x[1], reverse=True))
        print(result)

        if show:
            pca = PCA(n_components=2)
            composed = pca.fit_transform(vector)
            X = composed[:, 0]
            Y = composed[:, 1]
            plt.scatter(X, Y, color="red")
            for i, label in enumerate(annotations):
                plt.annotate(label, (X[i], Y[i]))
            plt.show()


infer(None, show=True)
