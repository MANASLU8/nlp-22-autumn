from tokenization_word2vec import sentences_to_vector
import gensim.downloader as download_api
import gensim.models
import pickle


model = gensim.models.Word2Vec.load('../../assets/w2v_model')
#model = download_api.load('word2vec-ruscorpora-300')
#print(model['человек_NOUN'])
file_to_vector = dict()
data_path = '../../assets/preprocessed_articles/'
with open("../../assets/sentence_list_by_file_speech", "rb") as file:
    file_to_sentences = pickle.load(file)
    for file in file_to_sentences:
        vector = sentences_to_vector(file_to_sentences[file], model)
        file_to_vector[file] = vector
print(file_to_vector)

with open('../../assets/file_to_vector', 'wb') as file:
    pickle.dump(file_to_vector, file)
