from gensim.models import Word2Vec
import csv
import tokenizer
import time

class VectorizationNeuro():
    def __init__(self):
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
    
    def cosin(self, word1, word2):
        return self.model.wv.cosine_similarities(self.model.wv[word1], [self.model.wv[word2]])[0]
    
    def cosins(self, word1, words):
        return self.model.wv.cosine_similarities(self.model.wv[word1], [self.model.wv[word] for word in words])


def vectorize_texts(file_in, file_out, vectorizer, rows = 100):
    with open(file_in) as csv_file:
        with open(file_out, "w") as output:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count%1000==0:
                    print(line_count)
                text = ". ".join(row[1:])
                cl = row[0]
                vec = vectorizer.get_text_vector(text)
                output.write(f"{line_count:06} {cl} {' '.join([f'{_:.5}' for _ in vec])}\n")
                line_count += 1
                if line_count==rows:
                    break

if __name__=="__main__":
    print("")
    
    neuro = VectorizationNeuro()
    
    print("\nTEST\n")
    file_in = 'projects/mansurov-project/assets/test.csv'
    file_out = 'projects/mansurov-project/assets/vector_corpus/test.tsv'
    
    _st = time.time()
    vectorize_texts(file_in, file_out, neuro, rows=-1)
    _et = time.time()
    print(f"\n--- {_et-_st} seconds ---")
    
    print("\nTRAIN\n")
    file_in = 'projects/mansurov-project/assets/train.csv'
    file_out = 'projects/mansurov-project/assets/vector_corpus/train.tsv'
    
    _st = time.time()
    vectorize_texts(file_in, file_out, neuro, rows=-1)
    _et = time.time()
    print(f"\n--- {_et-_st} seconds ---")