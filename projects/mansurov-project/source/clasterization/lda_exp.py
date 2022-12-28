from matrix import TermDocumentMatrix, TermList
from gensim.models import LdaModel
import re
import os

components = [2, 4, 5, 10, 20, 40, 60]
iterations = [10, 20, 40, 80]
# iterations = [40]

def conduct_experiment(terms, tdm):
    print("Experiment:")
    for component in components:
        for iteration in iterations:
            print(f"model_{component}_i{iteration}")
            lda = LdaModel(corpus=tdm, num_topics=component, id2word=terms, iterations=iteration)
            lda.save(f"projects/mansurov-project/assets/clasterization/models/model_{component}_i{iteration}.lda")
        
        
def get_stats():
    print("Stats:")
    tdm_test = TermDocumentMatrix()
    tdm_test.load("projects/mansurov-project/assets/clasterization/tdm_test.tsv")
    tdm_test = tdm_test.to_matrix()
    
    tdm_train = TermDocumentMatrix()
    tdm_train.load("projects/mansurov-project/assets/vectorize/tdm.tsv")
    tdm_train = tdm_train.to_matrix()
    
    for component in components:
        for iteration in iterations:
            print(f"model_{component}_i{iteration}")
            lda = LdaModel.load(f"projects/mansurov-project/assets/clasterization/models/model_{component}_i{iteration}.lda")
            top10 = lda.print_topics(num_topics=-1, num_words=10)
            top10 = [re.findall(r'"(.*?)"', line[1]) for line in top10]
            
            perp = lda.log_perplexity(tdm_test)
            perp = 2**(-perp)
            
            topic_data = [lda.get_document_topics(doc) for doc in tdm_train]
            
            os.makedirs(f"projects/mansurov-project/assets/clasterization/experiment_model/model_{component}_i{iteration}", exist_ok=True)
            with open(f"projects/mansurov-project/assets/clasterization/experiment_model/model_{component}_i{iteration}/top10.txt", "w") as output:
                for i, t in enumerate(top10):
                    output.write(f'{i}\t{", ".join(t)}\n')          
            
            with open(f"projects/mansurov-project/assets/clasterization/experiment_model/model_{component}_i{iteration}/perplexity.txt", "w") as output:
                output.write(f'{perp}')          
                
            with open(f"projects/mansurov-project/assets/clasterization/experiment_model/model_{component}_i{iteration}/doc_topics.tsv", "w") as output:
                for i, doc in enumerate(topic_data):
                    _ = "\t".join([f"{t[0]}, {t[1]}" for t in doc])
                    output.write(f'{i}\t{_}\n')          
        
def get_top_docs():
    for component in components:
        for iteration in iterations:
            with open(f"projects/mansurov-project/assets/clasterization/experiment_model/model_{component}_i{iteration}/doc_topics.tsv", "r") as input:
                lines = input.readlines()
                topic_data = [line[:-1].split('\t')[1:] for line in lines]
                topic_data = [[pair.split(', ') for pair in line] for line in topic_data]
                topic_data = [[(int(pair[0]), float(pair[1])) for pair in line] for line in topic_data]
            
            top_docs_for_topic = [[] for i in range(component)]
            for doc_id in range(len(topic_data)):
                for pair in topic_data[doc_id]:
                    top_docs_for_topic[pair[0]].append((doc_id, pair[1]))
            
            for docs in top_docs_for_topic:
                docs.sort(key=lambda x: x[1], reverse=True)
            
            with open(f"projects/mansurov-project/assets/clasterization/experiment_model/model_{component}_i{iteration}/top_docs.tsv", "w") as output:
                for topic_id, docs in enumerate(top_docs_for_topic):
                    top = docs[:5]
                    top = [f"{pair[0]}, {pair[1]}" for pair in top]
                    top = '\t'.join(top)
                    output.write(f"{topic_id}\t{top}\n")

if __name__=="__main__":
    print("")
    
    ##### Experiment
    terms = TermList()
    terms.load("projects/mansurov-project/assets/vectorize/terms.tsv")
    tdm = TermDocumentMatrix()
    tdm.load("projects/mansurov-project/assets/vectorize/tdm.tsv")
    terms = terms.to_dict()
    tdm = tdm.to_matrix()
    conduct_experiment(terms, tdm)
    
    # print("")
    # print("")
    ##### Create tdm for test
    # terms = TermList()
    # terms.load("projects/mansurov-project/assets/vectorize/terms.tsv")
    # tdm = TermDocumentMatrix()
    # tdm.collect("projects/mansurov-project/assets/clasterization/filtered_sentences_test.tsv", terms)
    # tdm.save("projects/mansurov-project/assets/clasterization/tdm_test.tsv")
    
    
    ##### Analyse results
    get_stats()
    get_top_docs()
    
    print("")