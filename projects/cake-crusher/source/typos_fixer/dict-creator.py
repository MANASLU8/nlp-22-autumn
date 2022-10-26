from gensim import corpora
from gensim.utils import simple_preprocess
import os
import json

data_path = '../../assets/annotated-corpus/'

dictionary = corpora.Dictionary([[]])

for split in os.listdir(data_path):
    for category in os.listdir(data_path + split):
        for filename in os.listdir(data_path + split + '/' + category):
            file_path = '../../assets/annotated-corpus/' + split + '/' + category + '/' + filename

            # creating a dictionary from a single text file
            dictionary.merge_with(corpora.Dictionary(simple_preprocess(line, deacc=False) for line in open(file_path)))

            # displaying contents of the dictionary
print("The dictionary has: " + str(len(dictionary)) + " tokens")
#print(dictionary.token2id)
dictionary.save('../../assets/dictionary')