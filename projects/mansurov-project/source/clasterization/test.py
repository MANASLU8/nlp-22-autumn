from sklearn.feature_extraction.text import CountVectorizer

# import nltk
# nltk.download('wordnet')
# nltk.download('omw-1.4')

from nltk import WordNetLemmatizer
from gensim import corpora

from numpy import array

corpus = [
    'This is the first document.',
    'This document is the second document.',
    'And this is the third one.',
    'Is this the first document?',
]

# with open("projects\\mansurov-project\\assets\\clasterization\\corpus.tsv", "wb") as output:
#     _c = [[w.lower() for w in sent.split(' ')] for sent in corpus]
#     _c = ['\t'.join(w) for w in _c]
#     for d in _c:
#         output.write(f"{d}\n".encode())

# _o = [
#     'document\t1',
#     'first\t2',
#     'is\t2',
#     'the\t1',
#     'this\t1',
#     'second\t2',
#     'and\t1',
#     'one\t2',
#     'third\t1'
# ]
# with open("projects\\mansurov-project\\assets\\clasterization\\terms.tsv", "wb") as output:
#     for d in _o:
#         output.write(f'{d}\n'.encode())

# vectorizer = CountVectorizer()

# X = vectorizer.fit_transform(corpus)

# print(vectorizer.get_feature_names_out())

# print(X.toarray())

# # [0 1 1 1 0 0 1 0 1]
# # [0 2 0 1 0 1 1 0 1]
# # [1 0 0 1 1 0 1 1 1]
# # [0 1 1 1 0 0 1 0 1]

# print("\n\n------------------\n\n")

# from nltk.corpus import stopwords
# stops = stopwords.words('english')
# lem = WordNetLemmatizer()

# c2 = [[lem.lemmatize(''.join(x for x in word.lower() if x.isalpha())) for word in sent.split(' ')] for sent in corpus]

# print(c2)

# dictionary = corpora.Dictionary(c2)

# bow = [dictionary.doc2bow(text) for text in c2]

# print(dict(dictionary))
# print(bow)

# [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)]
# [(0, 2), (2, 1), (3, 1), (4, 1), (5, 1)]
# [(2, 1), (3, 1), (4, 1), (6, 1), (7, 1), (8, 1)]
# [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)]

print ("\n\n----------\n\n")
from gensim.models import LdaModel

# lda = LdaModel(corpus=bow, num_topics=2, id2word=dictionary, random_state=42)


# print ("\n\n----------\n\n")
# from sklearn.decomposition import LatentDirichletAllocation as LDA

# bow2 = array([array(a) for a in bow])

# lda = LDA(n_components=2)
# lda.fit(bow2)

from matrix import TermList, TermDocumentMatrix

tl = TermList("projects\\mansurov-project\\assets\\clasterization\\terms.tsv")
print(tl.terms)
tdm = TermDocumentMatrix()
tdm.collect("projects\\mansurov-project\\assets\\clasterization\\corpus.tsv", tl)
print(tdm.tdm)
print(tdm.to_matrix())
print("")

# [(1, 1), (2, 1), (3, 1), (6, 1), (8, 1)]
# [(1, 2), (3, 1), (5, 1), (6, 1), (8, 1)]
# [(0, 1), (3, 1), (4, 1), (6, 1), (7, 1), (8, 1)]
# [(1, 1), (2, 1), (3, 1), (6, 1), (8, 1)]