import math
import matrix
import tokenizer

from gensim.test.utils import common_texts
from gensim.models import Word2Vec

from sklearn.decomposition import PCA

import pickle

from numpy import array
import os
import csv

class VectorizationTFIDF():
    _doc = []

    def __init__(self):
        self.terms = matrix.TermList("projects/mansurov-project/assets/vectorize/terms.tsv")
        self.tdm = matrix.TermDocumentMatrix()
        self.tdm.load("projects/mansurov-project/assets/vectorize/tdm.tsv")
    
    def set_doc(self, text):
        tokens = [token.lower() for token in tokenizer.flat(tokenizer.tokenize(text))]
        self._doc = [self.terms.by_term(token) for token in tokens if self.terms.by_term(token) != None]
    
    def set_doc_sent(self, sent):
        tokens = [token.lower() for token in sent]
        self._doc = [self.terms.by_term(token) for token in tokens if self.terms.by_term(token) != None]
    
    def tf(self, term, doc):
        if doc == -1:
            td = sum([1 for t in self._doc if t==term])
            Td = len(self._doc)
        else:
            td = self.tdm.by_doc_term(doc, term)[1]
            Td = self.tdm.terms_in_doc(doc)
        return td/Td
    
    def idf(self, term, doc):
        nd = self.tdm.count_docs()
        ndt = self.tdm.docs_with_term(term)
        if doc == -1:
            nd += 1
            ndt += 1 if term in self._doc else 0
        return math.log((nd+1)/(ndt+1))

    def tfidf(self, term, doc):
        if doc == -1:
            if term in self._doc:
                return self.tf(term, doc)*self.idf(term, doc)
            else:
                return 0
            
        _ = self.tdm.by_doc_term(doc, term)[1]
        if _ == 0:
            return 0
        else:
            return self.tf(term, doc)*self.idf(term, doc)
    
    def doc_score(self, doc):
        vec = [self.tfidf(term, doc) for term in self.terms.terms]
        return vec
    
    def get_scores(self):
        all_vec = []
        for i in range(100):
            print(i)
            vec = self.doc_score(i)
            all_vec.append(vec)
        return all_vec
    
    def save_pca_scores(self):
        print('get_data')
        all_vec = []
        for i in range(4000):
            print(i)
            vec = self.doc_score(i)
            all_vec.append(vec)
        print('calc_pca')
        pca = PCA(n_components=100)
        pca.fit(all_vec)
        pickle.dump(pca, open("projects/mansurov-project/assets/vectorize/pca.pkl", "wb"))
            
        # with open("projects/mansurov-project/assets/vectorize/tfidf_scores.tsv", "wb") as output:
        #     pass
    
    def get_text_vector(self, text):
        self.set_doc(text)
        vec = [0]*len(self.terms.terms)
        for term in self._doc:
            _ = self.tfidf(term, -1)
            vec[term[0]] = _
        # vec = [self.tfidf(term, -1) if term in self._doc else 0 for term in self.terms.terms]
        return vec
    
class VectorizationNeuro():
    
    def __init__(self, from_file, sentences):
        if from_file is False:
            self.model = Word2Vec(vector_size=100, window=10, workers=4)
            self.model.build_vocab(sentences)
            self.model.train(sentences, total_examples=len(sentences), epochs=5, report_delay=1)
            self.model.save("projects/mansurov-project/assets/vectorize/w2v.model")
        else:
            self.model = Word2Vec.load("projects/mansurov-project/assets/vectorize/w2v.model")
        
    def get_vector(self, word):
        try:
            return self.model.wv[word]
        except:
            return None
    
    def get_text_vector(self, text):
        vectors = [self.get_vector(token.lower()) for sent in tokenizer.tokenize(text) for token in sent]
        vectors = [e for e in vectors if e is not None]
        avg_vec = sum(vectors)/len(vectors)
        return avg_vec
    
    # def get_sent_vector(self, sent):
    #     vectors = [self.get_vector(token.lower()) for token in sent]
    #     vectors = [e for e in vectors if e is not None]
    #     avg_vec = sum(vectors)/len(vectors)
    #     return avg_vec
        
    def cosin(self, word1, word2):
        return self.model.wv.cosine_similarities(self.model.wv[word1], [self.model.wv[word2]])[0]
    
    def cosins(self, word1, words):
        return self.model.wv.cosine_similarities(self.model.wv[word1], [self.model.wv[word] for word in words])

def get_sentences():
    with open("projects/mansurov-project/assets/vectorize/filtered_sentences.tsv", 'rb') as input:
        lines = input.readlines()
        sentences = [line.decode('utf8').split("\t")[:-1] for line in lines]
    return sentences

def save_lists_data(data, file):
    with open(file, "wb") as output:
        for s in data:
            for i in s:
                output.write(f'{i}\t'.encode())
            output.write(f'\n'.encode())


def vectorize_text(text, neuro, tfidf):
    sentences_tokens = tokenizer.tokenize(text)
    sentences_matrix = [[neuro.get_vector(token.lower()) for token in sent] for sent in sentences_tokens]
    sentence_vectors = []
    for i in range(len(sentences_tokens)):
        sent = sentences_tokens[i]
        matrix = sentences_matrix[i]
        
        tfidf.set_doc_sent(sent)
        weights = [tfidf.tfidf(tfidf.terms.by_term(token.lower()), -1) for token in sent]
        
        sent_vec = [[_*weights[i] for _ in matrix[i]] for i in range(len(weights)) if matrix[i] is not None]
        sent_vec = array(sent_vec)
        sent_vec = sum(sent_vec)
        sentence_vectors.append(sent_vec)
    text_vector = sum(sentence_vectors)
    text_vector = text_vector/len(sentences_tokens)
    return text_vector

def vectorize_test(rows = 100):
    tfidf = VectorizationTFIDF()
    neuro = VectorizationNeuro(from_file=True, sentences=get_sentences())
    with open('projects/mansurov-project/assets/test.csv') as csv_file:
        with open("projects/mansurov-project/assets/annotated-corpus/test-embeddings.tsv", "wb") as output:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                print(line_count)
                text = ". ".join(row[1:])
                vec = vectorize_text(text, neuro, tfidf)
                output.write(f"{line_count:05} {' '.join([f'{_:5.2}' for _ in vec])}\n".encode())
                line_count += 1
                if (line_count==rows):
                    break
    

if __name__=="__main__":
    # vec = VectorizationTFIDF()
    # v = vec.get_text_vector("Some good text. You will be fine.")
    # print([i for i, x in enumerate(v) if x!=0])
    # v = vec.doc_score(3)
    # print([i for i, x in enumerate(v) if x!=0])
    
    # print(get_sentences()[:5])
    # model = VectorizationNeuro(from_file=True, sentences=get_sentences())
    # print(model.get_vector('good'))
    # print(model.get_text_vector('All good that is ends well. At least I think so.'))
    
    # Получаем вектора TFIDF для тренировочного датасета
    # vec = VectorizationTFIDF()
    # vec.save_pca_scores()
    # print('print')
    # print(len(tfidf_vec))
    # print(len(pca_vec))
    # save_lists_data(tfidf_vec, "projects/mansurov-project/assets/vectorize/tfidf_scores.tsv")
    # save_lists_data(pca_vec, "projects/mansurov-project/assets/vectorize/pca_tfidf_scores.tsv")
        
    # text = "AP - The man who claims Gov. James E. McGreevey sexually harassed him was pushing for a cash settlement of up to  #36;50 million before the governor decided to announce that he was gay and had an extramarital affair, sources told The Associated Press."
    # tfidf = VectorizationTFIDF()
    # neuro = VectorizationNeuro(from_file=True, sentences=get_sentences())
    
    # _ = vectorize_text(text, neuro, tfidf)
    # print(_)
    
    vectorize_test(-1)
    
    print("")