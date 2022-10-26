from gensim import corpora
from gensim.utils import simple_preprocess
import os

data_path = '../../assets/annotated-corpus/'

dictionary = corpora.Dictionary([])

for split in os.listdir(data_path):
    if split in ['test']:#, 'train']:
        for category in os.listdir(data_path + split):
            for filename in os.listdir(data_path + split + '/' + category):
                file_path = '../../assets/annotated-corpus/' + split + '/' + category + '/' + filename

                with open(file_path) as file:
                    #dictionary.merge_with(corpora.Dictionary(simple_preprocess(line[:-1]) for line in file))
                    a = ([line[:-1]] for line in file)
                    print(a.next(),),
                    dictionary.merge_with(corpora.Dictionary([line[:-1]] for line in file))

print("The dictionary has: " + str(len(dictionary)) + " tokens")
dictionary.save_as_text('../../assets/dictionary.txt')