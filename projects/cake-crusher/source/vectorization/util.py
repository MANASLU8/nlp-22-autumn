import re
from source.tokenization.tokenizer import tokenize
from numpy import dot
from numpy.linalg import norm
from numpy import round
from nltk.corpus import stopwords

stops = set(stopwords.words("english"))

def cos_sim(a, b):
    cos_sim = dot(a, b) / (norm(a) * norm(b))
    return round(cos_sim, 2)


def text_by_sentence_tokenize(text: str):
    token_list = tokenize(text)
    token_list.append('🍰')
    clean_list = []
    for token in token_list:
        if re.fullmatch(r'[\'!()\\\-\[\]{};@?<>:\",./^&*_|+`%#=~]+', token) or token in stops:
            continue
        else:
            clean_list.append(token)
    token_list = clean_list
    del clean_list
    sentence_list = []
    sentence = []
    for token in token_list:
        # 🍰 is a new sentence identificator
        if token == '🍰':
            if len(sentence) > 2 and sentence[0] not in ['From', 'Subject', 'Lines', 'Organization', 'Expires',
                                                         'Keywords', 'Summary']:
                sentence_list.append(sentence)
            sentence = []
        else:
            sentence.append(token)
    return sentence_list
