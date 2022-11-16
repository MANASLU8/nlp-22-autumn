import re
from source.tokenization.tokenizer import tokenize
from numpy import dot
from numpy.linalg import norm
from numpy import round


def cos_sim(a, b):
    cos_sim = dot(a, b) / (norm(a) * norm(b))
    return round(cos_sim, 2)


def text_by_sentence_tokenize(text: str):
    token_list = tokenize(text)
    token_list.append('🍰')
    token_list = [token for token in token_list if not re.fullmatch(r'[\'!()\\\-\[\]{};@?<>:\",./^&*_|+`%#=~]+', token)]
    sentence_list = []
    sentence = []
    for token in token_list:
        # 🍰 is a new sentence identificator
        if token == '🍰':
            sentence_list.append(sentence)
            sentence = []
        else:
            sentence.append(token)
    return sentence_list
