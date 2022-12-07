import os
import re
from collections import Counter

class TermList():
    terms = []  # (term_id, term, term_freq)
    
    def _parse_line(self, line):
        d = line[1].decode('utf8').split("\t")
        return (line[0], d[0], float(d[1]))
    
    def __init__(self, file):
        with open(file, "rb") as input:
            lines = input.readlines()
            self.terms = list(map(self._parse_line, enumerate(lines)))
        
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
                items = [terms.by_term(word)[0] for word in words]
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


if __name__=="__main__":
    print("")
    
    terms = TermList("projects/mansurov-project/assets/vectorize/terms.tsv")
    
    tdm = TermDocumentMatrix()
    tdm.load("projects/mansurov-project/assets/vectorize/tdm.tsv")
    lines = [
        "word",
        "back",
        "reuters",
        "wall",
        "short"
    ]
    print([tdm.by_doc_term(0, terms.by_term(x)) for x in lines])
    
    
    # terms = TermList("projects/mansurov-project/assets/vectorize/terms.tsv")
    # lines = [
    #     "word",
    #     "orion",
    #     "lobbed",
    #     "outback",
    #     "british",
    #     "ddos",
    #     "zambia",
    #     "load",
    #     "amar"
    # ]
    
    # _lines = []
    # for line in lines:
    #     _lines.append(terms.by_term(line.split('\t')[0].lower())[0])
    # print(_lines)
    
    # document = []
    # for line in lines:
    #     if line == "\n":    
    #         continue
    #     item = terms.by_term(line.split('\t')[0].lower())
    #     if item == None:
    #         continue
    #     item = [item[0], 1]
    #     found, ind = binary_search(document, item, lambda x: x[0])
    #     print(f"{found} {ind}")
    #     if found:
    #         document[ind][1] = document[ind][1] + 1
    #     else:
    #         document.insert(ind, item)
    
    # print(document)
    