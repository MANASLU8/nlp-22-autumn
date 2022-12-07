import os
import re

from nltk.corpus import stopwords
from matrix import *

path_corpus = "projects/mansurov-project/assets/annotated-corpus/"
path_vectorize = "projects/mansurov-project/assets/vectorize"

stopwords = set(stopwords.words('english'))

min_freq = 5

# выбор только словоформ/лексем
def collect_words():
    words = {}
    os.makedirs(path_vectorize, exist_ok=True)
    for set_class in os.listdir(path_corpus+"train"):
        for file in os.listdir(path_corpus+"train"+'/'+set_class):
            f = path_corpus+"train"+'/'+set_class+'/'+file
            with open(f, 'rb') as input:
                lines = input.readlines()
                for line in lines:
                    line = line.decode('utf8')
                    if line == "\n":    
                        continue
                    item = line.split('\t')[0]
                    item = item.lower()
                    value = words.get(item, 0)
                    value = value+1
                    words[item] = value
                        
    # save words
    with open(path_vectorize+"/dict.tsv", "wb") as output:
        for word, count in words.items():
            output.write(f'{word}\t{count}\n'.encode())

# очистка коллекции от знаков препинания и стоп слов                   
def filter_words_collection():
    with open(path_vectorize+"/dict-filtered.tsv", "wb") as output:
        with open(path_vectorize+"/dict.tsv", "rb") as input:
            lines = input.readlines()
            for line in lines:
                line = line.decode('utf8')
                line = line[:-1]
                if line == "":
                    continue
                word, value = line.split("\t")
                value = int(value)    
                if re.fullmatch(r"[\.\,\-\:\;\'\"\!\?\=\+\#\$\%\@\^\&\*\\\|\[\]\{\}\(\)]+", word):
                    continue
                if word in stopwords:
                    continue
                if value < min_freq:
                    continue
                output.write(f'{line}\n'.encode())
                
def sort_words_collection():
    with open(path_vectorize+"/terms.tsv", "wb") as output:
        with open(path_vectorize+"/dict-filtered.tsv", "rb") as input:
            lines = input.readlines()
            data = sorted(list(map(lambda x: x.decode('utf8').split("\t"), lines)), key=lambda x: x[0], reverse=False)
            for d in data:
                output.write(f'{d[0]}\t{d[1]}'.encode())
    
# создание "термин-документ" матрицы                
def create_term_document():
    terms = TermList(path_vectorize+"/terms.tsv")
    tdm = TermDocumentMatrix()
    tdm.collect(path_vectorize+"/filtered_sentences.tsv", terms)
    tdm.save(path_vectorize+"/tdm.tsv")

def create_filtered_sentences():
    terms = TermList("projects/mansurov-project/assets/vectorize/terms.tsv")
    
    files = []
    for set_class in os.listdir(path_corpus+"train"):
        for file in os.listdir(path_corpus+"train"+'/'+set_class):
            f = path_corpus+"train"+'/'+set_class+'/'+file
            files.append(f)
            # files.insert(int(file[-10:-4]), f)
    files.sort(key=lambda x: int(x[-10:-4]))
    # for f in files[:2000:11]:
    #     print(f"{f}\t{int(f[-10:-4])}")            
    with open(path_vectorize+"/filtered_sentences.tsv", "wb") as output:   
        for f in files:         
            with open(f, 'rb') as input:
                lines = input.readlines()
                for line in lines:
                    line = line.decode('utf8')
                    if line == "\n":    
                        continue
                    item = line.split('\t')[0]
                    item = item.lower()
                    item = terms.by_term(line.split('\t')[0].lower())
                    if item == None:
                        continue
                    output.write(f'{item[1]}\t'.encode())
            output.write(f'\n'.encode())
    
        
    

if __name__ == "__main__":
    print("")
    # collect_words()
    # filter_words_collection()
    # sort_words_collection()
    # create_filtered_sentences()
    # create_term_document()
    
    print("")
    