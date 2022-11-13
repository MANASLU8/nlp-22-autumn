# собираем триграммы
# import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords

import os
import re

data_type = {
    0: "words",
    2: "lexemes"
}
data_type_number = 2 # 0: word  # 2: lexeme

path_corpus = "projects/mansurov-project/assets/annotated-corpus/"
path_ngrams = "projects/mansurov-project/assets/ngrams"

stopwords = set(stopwords.words('english'))

# выбор только словоформ/лексем
def collect_words():
    os.makedirs(path_ngrams, exist_ok=True)
    with open(path_ngrams+"/"+data_type[data_type_number]+".tsv", "wb") as output:
        for set_type in os.listdir(path_corpus):
            for set_class in os.listdir(path_corpus+set_type):
                for file in os.listdir(path_corpus+set_type+'/'+set_class):
                    f = path_corpus+set_type+'/'+set_class+'/'+file
                    with open(f, 'rb') as input:
                        lines = input.readlines()
                        for line in lines:
                            line = line.decode('utf8')
                            if line == "\n":
                                output.write(f'\n'.encode())    
                                continue
                            item = line.split('\t')[data_type_number]
                            if data_type_number==2:
                                item = item[:-1]
                            output.write(f'{item}\n'.encode())

# очистка коллекции от знаков препинания и стоп слов                   
def filter_words_collection():
    with open(path_ngrams+"/"+data_type[data_type_number]+"-filtered.tsv", "wb") as output:
        with open(path_ngrams+"/"+data_type[data_type_number]+".tsv", "rb") as input:
            lines = input.readlines()
            for line in lines:
                line = line.decode('utf8')
                line = line[:-1]
                if line == "":
                    continue    
                if re.fullmatch(r"[\.\,\-\:\;\'\"\!\?\=\+\#\$\%\@\^\&\*\\\|\[\]\{\}\(\)]+", line):
                    continue
                line = line.lower()
                if line in stopwords:
                    continue
                output.write(f'{line}\n'.encode())

# подсчет триграмм
def count_trigrams():
    trigrams = {} # (word1, word2, word3) : amount
    # count trigrams
    with open(path_ngrams+"/"+data_type[data_type_number]+"-filtered.tsv", "rb") as input:
        lines = input.readlines()
        linei = 2
        while linei < len(lines):
            line = lines[linei][:-1].decode('utf8')
            # if line == "":
            #     linei = linei + 4 # w w e / w e e / e e w / e w w
            #     continue
            line1, line2 = lines[linei-1][:-1].decode('utf8'), lines[linei-2][:-1].decode('utf8')
            value = trigrams.get((line2, line1, line), 0)
            value = value+1
            trigrams[(line2, line1, line)] = value
            linei = linei + 1
    
    # save trigrams
    with open(path_ngrams+"/"+data_type[data_type_number]+"-trigrams.tsv", "wb") as output:
        for trigram, count in trigrams.items():
            output.write(f'{trigram[0]} {trigram[1]} {trigram[2]}\t{count}\n'.encode())

# посчет слов
def count_words():
    words = {}
    # count words
    with open(path_ngrams+"/"+data_type[data_type_number]+"-filtered.tsv", "rb") as input:
        lines = input.readlines()
        linei = 0
        while linei < len(lines):
            line = lines[linei][:-1].decode('utf8')
            linei = linei + 1
            # if line == "":
            #     continue
            value = words.get(line, 0)
            value = value+1
            words[line] = value
    
    # save words
    with open(path_ngrams+"/"+data_type[data_type_number]+"-freq.tsv", "wb") as output:
        for word, count in words.items():
            output.write(f'{word}\t{count}\n'.encode())


if __name__ == "__main__":
    print("")
    # collect_words()
    # filter_words_collection()
    # count_words()
    # count_trigrams()
    # i = 0
    # while i < 10:
    #     print(i)
    #     i = i + 2