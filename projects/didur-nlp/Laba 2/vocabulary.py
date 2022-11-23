import os
import re
from gensim import corpora
vocabulary = corpora.Dictionary([]) #создаем словарь
listdir = os.listdir("C:/Users/Admin/Desktop/pythonProject2/assets/annotated-corpus/test/")
for dirname in listdir:
    filelist = os.listdir("C:/Users/Admin/Desktop/pythonProject2/assets/annotated-corpus/test/" + dirname)
    for filename in filelist:
        with open("C:/Users/Admin/Desktop/pythonProject2/assets/annotated-corpus/test/" + dirname + '/' + filename, 'r') as f:
                vocabulary.merge_with(corpora.Dictionary(([re.split(r'\t', line)[0]] for line in f))) #достать первый токен из строки
vocabulary.filter_extremes(no_below=5) #удаляем редко встречаемые слова
vocabulary.filter_tokens(bad_ids=[40])
vocabulary.save_as_text('file.txt')