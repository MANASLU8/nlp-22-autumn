import pickle
import gensim.models
import re
import nltk
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords

stops = set(stopwords.words("english"))
with open("../../assets/cropped_dictionary", "rb") as file:
    dictionary = pickle.load(file)
# документы train без стоп-слов и пунктуации
with open("../../assets/token_list_by_file", "rb") as file:
    token_list_by_file = pickle.load(file)

# корректно ли скармливать по документу или нужно по предложению?
class MyCorpus:
    def __init__(self, token_list_by_file):
        # new_dict = dict()
        # for index, sentence in enumerate(token_list_by_file):
        #     new_dict[sentence] = sentence
        #     if index >= 5:
        #         break

        self.token_list_by_file = token_list_by_file

    def __iter__(self):
        for filename in self.token_list_by_file:
            yield token_list_by_file[filename]

sentences = MyCorpus(token_list_by_file)
model = gensim.models.Word2Vec(sentences=sentences)
model.save('../../assets/w2v_model')
model = gensim.models.Word2Vec.load('../../assets/w2v_model')
print(model.wv['hello'])
for index, word in enumerate(model.wv.index_to_key):
    # if index == 10:
    #     break
    print(f"word #{index}/{len(model.wv.index_to_key)} is {word}")

data_path = '../../assets/annotated-corpus/test'
sentence_list = []
with open(data_path + '/comp.graphics/38758.tsv') as file:
    sentence = []
    for line in file:
        if line != '\n':
            token = re.split(r'\t', line)[0]
            # punctuation cleaner
            if re.fullmatch(r'[\'!()\\\-\[\]{};@?<>:\",./^&*_|+`%#=~]+', token) or token not in dictionary:
                continue
            sentence.append(token)
        elif line == '\n':
            if sentence:
                sentence_list.append(sentence)
            sentence = []
print(sentence_list)

for sentence in sentence_list:
    print(model.wv[sentence])
