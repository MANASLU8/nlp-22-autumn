import re
from source.tokenization.tokenizer import tokenize

def text_by_sentence_tokenize(text: str):
    token_list = tokenize(text)
    token_list.append('🍰')
    token_list = [token for token in token_list if not re.fullmatch(r'[\'!()\\\-\[\]{};@?<>:\",./^&*_|+`%#=~]+', token)]
    print(token_list)
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