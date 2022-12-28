import re
from nltk.tokenize import word_tokenize
from deeppavlov.core.common.file import read_json
from deeppavlov import build_model, configs
import pickle
import os
import nltk


def make_sentence_list_by_file():
    sentence_list_by_file = dict()
    data_path = '../../assets/preprocessed_articles/'
    print('Collecting sentences...')
    for category in os.listdir(data_path):
        for filename in os.listdir(data_path + '/' + category):
            with open(data_path + '/' + category + '/' + filename, encoding="utf-8") as file:
                cleaned_text = []
                text = file.read()
                sent_text = nltk.sent_tokenize(text, language="russian")
                result = []
                for sent in sent_text:
                    sent = re.sub(r'\n|\\n|.*[a-z].*|[\'!()\\\[\]{};@?<>:\",./…^&*_|+`%#=~]+|.*[!?.{}%$#*()@<>:;^~\[\]].*', '', sent)
                    if len(sent) < 10:
                        continue
                    if len(word_tokenize(sent)) > 400:
                        sent = sent[:100]
                    result.append(sent)
                cleaned_text.append(sent)
            sentence_list_by_file[category + '/' + filename] = result
    print(sentence_list_by_file)
    with open("../../assets/bert_sentence_list_by_file", "wb") as file:
        pickle.dump(sentence_list_by_file, file)


make_sentence_list_by_file()

bert_config = read_json(configs.embedder.bert_embedder)
print(bert_config)
bert_config['metadata']['variables']['BERT_PATH'] = '../../assets/rubert'
bert_config['chainer']['pipe'][1]['bert_config_path'] = '{BERT_PATH}/config.json'
print(bert_config['chainer']['pipe'][1]['bert_config_path'])

m = build_model(bert_config)

#texts = ['Hi, i want my embedding.', 'And mine too, please!']
with open("../../assets/bert_sentence_list_by_file", "rb") as file:
    bert_sentence_list_by_file = pickle.load(file)

for key in bert_sentence_list_by_file:
    text = bert_sentence_list_by_file[key]
    tokens, token_embs, subtokens, subtoken_embs, sent_max_embs, sent_mean_embs, bert_pooler_outputs = m(text)
    print(sent_mean_embs)
    print(len(sent_mean_embs))
