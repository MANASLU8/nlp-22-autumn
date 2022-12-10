from main import freq_vectorizer
from word2vector import word2vec_vectorize, cosinus


with open('text1.txt') as file:
    text1 = file.read()
with open('text2.txt') as file:
    text2 = file.read()
with open('text3.txt') as file:
    text3 = file.read()

vec_text1_freq = freq_vectorizer(text1)
vec_text1_w2v = word2vec_vectorize(text1)
vec_text2_freq = freq_vectorizer(text2)
vec_text2_w2v = word2vec_vectorize(text2)
vec_text3_freq = freq_vectorizer(text3)
vec_text3_w2v = word2vec_vectorize(text3)
freq_similarity = cosinus(vec_text1_freq, vec_text2_freq)
word2vec_similarity = cosinus(vec_text1_w2v, vec_text2_w2v)
freq_antisimilarity = cosinus(vec_text1_freq, vec_text3_freq)
word2vec_antisimilarity = cosinus(vec_text1_w2v, vec_text3_w2v)
print(f'Similarity for frequency vectorizer: {freq_similarity}')
print(f'Similarity for word2vec vectorizer: {word2vec_similarity}')
print(f'Antisimilarity for frequency vectorizer: {freq_antisimilarity}')
print(f'Antisimilarity for word2vec vectorizer: {word2vec_antisimilarity}')
