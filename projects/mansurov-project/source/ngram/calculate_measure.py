import math

data_type = {
    0: "words",
    2: "lexemes"
}
data_type_number = 2 # 0: word  # 2: lexeme

path_ngrams = "projects/mansurov-project/assets/ngrams"

word = {}
trigram = {}
all_words = 0

def load_freqs():
    global all_words
    with open(path_ngrams+"/"+data_type[data_type_number]+"-freq.tsv", "rb") as input:
        lines = input.readlines()
        for line in lines:
            w, f = line.decode('utf8').split("\t")
            _ = int(f)
            word[w] = _
            all_words = all_words + _
    
    with open(path_ngrams+"/"+data_type[data_type_number]+"-trigrams.tsv", "rb") as input:
        lines = input.readlines()
        for line in lines:
            w, f = line.decode('utf8').split("\t")
            w = w.split(" ")
            trigram[(w[0],w[1],w[2])] = int(f)


def T_score(n1, n2, n3):
    v = word[n1]*word[n2]*word[n3] # Пf(u)
    v = v/all_words/all_words # N^(3-1)
    v = trigram[(n1, n2, n3)] - v # f(n,c)
    v = v/math.sqrt(trigram[(n1, n2, n3)])
    return v

def MI_score(n1, n2, n3):
    v = trigram[(n1, n2, n3)] # f(n,c)
    v = v*all_words*all_words # N^(3-1)
    v = v/word[n1]/word[n2]/word[n3] # Пf(u)
    v = math.log2(v)
    return v
        
def get_T_score():
    with open(path_ngrams+"/"+data_type[data_type_number]+"-T.tsv", "wb") as output:
        for tri in trigram.keys():
            v = T_score(tri[0], tri[1], tri[2])
            output.write(f'{tri[0]} {tri[1]} {tri[2]}\t{v}\n'.encode())
            
def get_MI_score():
    with open(path_ngrams+"/"+data_type[data_type_number]+"-MI.tsv", "wb") as output:
        for tri in trigram.keys():
            # print(f'{tri[0]} {tri[1]} {tri[2]}')
            v = MI_score(tri[0], tri[1], tri[2])
            output.write(f'{tri[0]} {tri[1]} {tri[2]}\t{v}\n'.encode())
            
def sort_T_score():
    array = []
    with open(path_ngrams+"/"+data_type[data_type_number]+"-T.tsv", "rb") as input:
        lines = input.readlines()
        for line in lines:
            line = line.decode('utf8').split('\t')
            array.append((line[0], float(line[1][:-1])))
    
    array = sorted(array, key=lambda tup: tup[1], reverse=True)
    
    with open(path_ngrams+"/"+data_type[data_type_number]+"-T-sort.tsv", "wb") as output:
        for a in array:
            output.write(f"{a[0]}\t{a[1]}\n".encode())  
            
    return array  

def sort_MI_score():
    array = []
    with open(path_ngrams+"/"+data_type[data_type_number]+"-MI.tsv", "rb") as input:
        lines = input.readlines()
        for line in lines:
            line = line.decode('utf8').split('\t')
            array.append((line[0], float(line[1][:-1])))
    
    array = sorted(array, key=lambda tup: tup[1], reverse=True)
    
    with open(path_ngrams+"/"+data_type[data_type_number]+"-MI-sort.tsv", "wb") as output:
        for a in array:
            output.write(f"{a[0]}\t{a[1]}\n".encode())  
            
    return array  
            
import nltk      
from nltk.collocations import *      
def get_top_T_score_lib():
    with open(path_ngrams+"/"+data_type[data_type_number]+"-filtered.tsv", "rb") as input:
        lines = input.readlines()
        lines = list(map(lambda i: i[:-1].decode('utf8'), lines))
        text = nltk.Text(lines)
        trigram_measures = nltk.collocations.TrigramAssocMeasures()
        finder_thr = TrigramCollocationFinder.from_words(text)
        scores = finder_thr.score_ngrams(trigram_measures.student_t)
        return scores

def get_top_MI_score_lib():
    with open(path_ngrams+"/"+data_type[data_type_number]+"-filtered.tsv", "rb") as input:
        lines = input.readlines()
        lines = list(map(lambda i: i[:-1].decode('utf8'), lines))
        text = nltk.Text(lines)
        trigram_measures = nltk.collocations.TrigramAssocMeasures()
        finder_thr = TrigramCollocationFinder.from_words(text)
        scores = finder_thr.score_ngrams(trigram_measures.pmi)
        return scores


def print_compare(lib, my, postfix):
    with open(path_ngrams+"/"+data_type[data_type_number]+postfix+".tsv", "wb") as output:
        output.write(f"num\tlib_trigram\tlib_score\tmy_trigram\tmy_score\tdiff\n".encode())
        for i in range(len(lib)):
            output.write(f"{i+1}\t{' '.join(lib[i][0])}\t{lib[i][1]}\t{my[i][0]}\t{my[i][1]}\t{lib[i][1]-my[i][1]}\n".encode())
        

if __name__=="__main__":
    print()
    load_freqs()    
    get_MI_score()
    get_T_score()
    
    my = sort_T_score()
    lib = get_top_T_score_lib()
    print_compare(lib[:30], my[:30], "-T-compare")
    
    my = sort_MI_score()
    lib = get_top_MI_score_lib()
    print_compare(lib[:30], my[:30], "-MI-compare")
    
    
    
        