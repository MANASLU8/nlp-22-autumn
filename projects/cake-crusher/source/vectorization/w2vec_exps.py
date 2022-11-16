import pickle
import gensim.models
from w2vec import MyCorpus
from w2vec_demo import infer

with open("../../assets/sentence_list_by_file", "rb") as file:
    sentence_list_by_file = pickle.load(file)

# провести серию экспериментов
for i in range(3, 15):
    sentences = MyCorpus(sentence_list_by_file)
    model = gensim.models.Word2Vec(sentences=sentences, window=i)
    print(f'window {i}:')
    infer(model, show=False)
# best window = 10

for i in range(50, 200, 25):
    sentences = MyCorpus(sentence_list_by_file)
    model = gensim.models.Word2Vec(sentences=sentences, window=10, vector_size=i)
    print(f'vector_size {i}:')
    infer(model, show=False)
# best vector_size = 100

for i in range(5, 11):
    sentences = MyCorpus(sentence_list_by_file)
    model = gensim.models.Word2Vec(sentences=sentences, window=10, vector_size=100, epochs=i)
    print(f'epochs {i}:')
    infer(model, show=False)
# best epochs = 5
