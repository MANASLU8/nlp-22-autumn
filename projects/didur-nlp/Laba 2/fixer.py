import os
import re
import vagner_fisher as vf
from gensim import corpora
vocabulary = corpora.Dictionary([])
vocabulary = vocabulary.load_from_text("file.txt")
listdir = os.listdir("C:/Users/Admin/Desktop/pythonProject2/newsgroups-test-corrupted/")
for dirname in listdir:
    filelist = os.listdir("C:/Users/Admin/Desktop/pythonProject2/newsgroups-test-corrupted/" + dirname)
    for filename in filelist:
        fixed_list = []
        with open("C:/Users/Admin/Desktop/pythonProject2/newsgroups-test-corrupted/" + dirname + '/' + filename, 'r') as f:
            for line in f:
                if line == "\n":
                    fixed_list.append("\n")
                    continue
                token = re.split(r'\t', line)[0]
                minimum = 1000000
                correct_word = ""
                for ident in vocabulary:
                    distance = vf.distance(token, vocabulary[ident])
                    if distance < minimum:
                        minimum = distance
                        correct_word = vocabulary[ident]
                fixed_list.append(correct_word)
                print(token,correct_word)
        if not os.path.exists("C:/Users/Admin/Desktop/pythonProject2/newsgroups-test-fixed/" + dirname):
            os.makedirs('C:/Users/Admin/Desktop/pythonProject2/newsgroups-test-fixed/' + dirname)
        with open("C:/Users/Admin/Desktop/pythonProject2/newsgroups-test-fixed/" + dirname + '/' + filename, 'w') as fi:
            for i in range(len(fixed_list)):
                if fixed_list[i] == "\n":
                    fi.write ('\n')
                else:
                    fi.write(fixed_list[i] + '\n')
