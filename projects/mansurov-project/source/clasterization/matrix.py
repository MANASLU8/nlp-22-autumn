import os
import re
from collections import Counter
from itertools import groupby

# import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
stopwords = set(stopwords.words('english'))

class TermList():
    terms = []  # (term_id, term, term_freq)
    
    def _parse_line(self, line):
        d = line[1].decode('utf8').split("\t")
        return (line[0], d[0], int(d[1]))
    
    def __init__(self):
        return
    
    def load(self, file):
        with open(file, "rb") as input:
            lines = input.readlines()
            self.terms = list(map(self._parse_line, enumerate(lines)))
    
    def apply_filter(self, filter):
        self.terms = [term for term in self.terms if filter(term[1])]
        
    def apply_map(self, map):
        self.terms = [(term[0], map(term[1]), term[2]) for term in self.terms]
    
    def collect(self, path_corpus, min_freq=5):
        words = {}
        for set_class in os.listdir(path_corpus):
            for file in os.listdir(path_corpus+'/'+set_class):
                f = path_corpus+'/'+set_class+'/'+file
                with open(f, 'rb') as input:
                    lines = input.readlines()
                    for line in lines:
                        line = line.decode('utf8')
                        if line == "\n":    
                            continue
                        item = line.split('\t')[0]
                        item = item.lower()
                        if item == "":
                            continue
                        if re.fullmatch(r"[\.\,\-\:\;\'\"\!\?\=\+\#\$\%\@\^\&\*\\\|\[\]\{\}\(\)]+", item):
                            continue
                        if item in stopwords:
                            continue
            
                        value = words.get(item, 0)
                        value = value+1
                        words[item] = value
        
        words = words.items()
        words = [word for word in words if word[1]>=min_freq]
        words = sorted(words, key=lambda x: x[0], reverse=False)
        self.terms = [(i, word[0], word[1]) for i, word in enumerate(words)]
    
    def fix(self):
        self.terms.sort(key=lambda x: x[1])
        _ = [] # [term, count]
        last_term = ""
        for term in self.terms:
            if term[1] == last_term:
                _[-1][1] += term[2]
            else:
                _.append([term[1], term[2]])
                last_term = term[1]
                
        self.terms = [(i, term[0], term[1]) for i, term in enumerate(_)]
        
    def save(self, file):
        with open(file, "wb") as output:
            for d in self.terms:
                output.write(f'{d[1]}\t{d[2]}\n'.encode())
    
    # binary search
    def by_term(self, term):
        low = 0  
        high = len(self.terms) - 1  
        mid = 0  
        while low <= high:    
            mid = (high + low) // 2  
            if self.terms[mid][1] < term:  
                low = mid + 1  
            elif self.terms[mid][1] > term:  
                high = mid - 1  
            else:  
                return self.terms[mid]  
        return None     
    
    def by_num(self, num):
        return self.terms[num]
    
    def to_dict(self):
        res = {}
        for term in self.terms:
            res[term[0]] = term[1]
        return res
    
class TermDocumentMatrix():
    tdm = [] # (doc_id, [[term_id, term_freq]])
    
    def __init__(self):
        return
    
    def by_doc(self, doc):
        return self.tdm[doc]
    
    def by_doc_term(self, doc, term):
        i = binary_search(self.tdm[doc][1], term, lambda x: x[0])
        return self.tdm[doc][1][i[1]] if i[0] else (term[0], 0)
    
    def terms_in_doc(self, doc):
        terms = self.tdm[doc][1]
        return sum([x[1] for x in terms])
    
    def count_docs(self):
        return len(self.tdm)
    
    def docs_with_term(self, term):
        summ = 0
        for doc in self.tdm:
            found, ind = binary_search(doc[1], term, lambda x: x[0])
            if found:
                summ += 1
        return summ
                
    def collect(self, file, terms):
        self.tdm = []
        with open(file, 'rb') as input:
            lines = input.readlines()
            doc_num = 0
            for line in lines:
                words = line.decode('utf8').split("\t")[:-1]
                items = [terms.by_term(word) for word in words]
                items = [word[0] for word in items if word != None]
                c = Counter(items)
                c = list(c.items())
                c.sort(key=lambda x: x[0])
                self.tdm.append((doc_num, c))
                doc_num += 1
                
        self.tdm.sort(key=lambda x: x[0])
                
    def save(self, file):
        with open(file, "wb") as output:
            for document in self.tdm:
                output.write(f'{document[0]}'.encode())
                for term in document[1]:
                    output.write(f'\t{term[0]} {term[1]}'.encode())
                output.write(f'\n'.encode())
    
    def load(self, file):
        self.tdm = []
        with open(file, 'rb') as input:
            lines = input.readlines()
            for line in lines:
                line = line.decode('utf8')
                line = line[:-1]
                terms = line.split('\t')
                doc_id = int(terms[0])
                terms = terms[1:]
                terms = list(map(self._parse_term, terms))
                self.tdm.append((doc_id, terms))
    
    def _parse_term(self, term):
        x = term.split(' ')
        return (int(x[0]), int(x[1]))
    
    def to_matrix(self):
        matrix = []
        for sent in self.tdm:
            matrix.append([(term[0], term[1]) for term in sent[1]])
        return matrix
    
    def get_matrix_for_corpus(self, file, terms):
        new_tdm = [] # [(term_id, term_freq)]
        with open(file, 'rb') as input:
            lines = input.readlines()
            doc_num = 0
            for line in lines:
                words = line.decode('utf8').split("\t")[:-1]
                items = [terms.by_term(word) for word in words]
                items = [word[0] for word in items if word != None]
                c = Counter(items)
                c = list(c.items())
                c.sort(key=lambda x: x[0])
                new_tdm.append([(term[0], term[1]) for term in c])
                doc_num += 1
                
        return new_tdm
    
def binary_search(ls, item, key = lambda x: x):
    low, mid, high = 0, 0, len(ls) - 1  
    while low <= high:  
        mid = (high + low) // 2  
        if key(ls[mid]) < key(item):  
            low = mid + 1  
        elif key(ls[mid]) > key(item):  
            high = mid - 1  
        else:  
            return True, mid  
    return False, low     


# def correct_term(x):
#     res = re.search(r'\w+', x)
#     if res == None:
#         return ""
#     x = res.group()
#     return x
    
# def filter_term(x):
#     stops = set(stopwords.words('english'))
#     if len(x)<2:
#         return False
#     if x.isdigit():
#         return False
#     if x in stops:
#         return False
#     return True

def create_filtered_sentences():
    terms = TermList("projects/mansurov-project/assets/vectorize/terms.tsv")
    
    files = []
    for set_class in os.listdir("projects/mansurov-project/assets/annotated-corpus/test"):
        for file in os.listdir("projects/mansurov-project/assets/annotated-corpus/test/"+set_class):
            f = "projects/mansurov-project/assets/annotated-corpus/test/"+set_class+'/'+file
            files.append(f)
    files.sort(key=lambda x: int(x[-10:-4]))        
    with open("projects/mansurov-project/assets/clasterization/filtered_sentences_test.tsv", "wb") as output:   
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

if __name__=="__main__":
    print("")
    
    # terms = TermList()
    # terms.collect("projects/mansurov-project/assets/annotated-corpus/test")
    # terms.save("projects/mansurov-project/assets/clasterization/terms.tsv")
    
    # tdm = TermDocumentMatrix()
    # tdm.collect("projects/mansurov-project/assets/clasterization/filtered_sentences_test.tsv", terms)
    # tdm.save("projects/mansurov-project/assets/clasterization/tdm.tsv")
    
    # terms = TermList("projects/mansurov-project/assets/vectorize/terms.tsv")
    # tdm = TermDocumentMatrix()
    # tdm.load("projects/mansurov-project/assets/vectorize/tdm.tsv")
    
    # create_filtered_sentences()
    
    # terms = TermList("projects/mansurov-project/assets/vectorize/terms.tsv")
    # tdm = TermDocumentMatrix()
    # tdm.load("projects/mansurov-project/assets/vectorize/tdm.tsv")
    # a = tdm.get_matrix_for_corpus("projects/mansurov-project/assets/clasterization/filtered_sentences_test.tsv", terms)
    # print(a[:10])
    
    # print(correct_term("grwe.gwe"))
    # print(correct_term("'hufies'"))
    # print(correct_term("'fewf2<ew'fewf"))
    
    print("")