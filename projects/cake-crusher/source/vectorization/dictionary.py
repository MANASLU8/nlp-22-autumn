import pickle
import os
import re
import copy
import pandas as pd
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords', quiet=True)

stops = set(stopwords.words("english"))

# creating dictionary
data_path = '../../assets/annotated-corpus/'
dictionary = dict()
count = 0
set_name = 'train'
for category in os.listdir(data_path + set_name):
    for filename in os.listdir(data_path + set_name + '/' + category):
        count += 1
        with open(data_path + set_name + '/' + category + '/' + filename) as file:
            for line in file:
                if line != '\n':
                    token = re.split(r'\t', line)[0]
                    # punctuation and stop words cleaner
                    if re.fullmatch(r'[\'!()\\\-\[\]{};@?<>:\",./^&*_|+`%#=~]+', token) or token in stops:
                        continue
                    dictionary[token] = dictionary.get(token, 0) + 1
    print(count)

with open("../../assets/dictionary", "wb") as file:
    pickle.dump(dictionary, file)

print(dictionary)

# filtering low frequency tokens
cropped_dictionary = copy.copy(dictionary)
for token in dictionary:
    if dictionary[token] <= 5:
        del cropped_dictionary[token]
del dictionary

with open("../../assets/cropped_dictionary", "wb") as file:
    pickle.dump(cropped_dictionary, file)

with open("../../assets/token_list_by_file", "rb") as file:
    token_list_by_file = pickle.load(file)

for dict_token in cropped_dictionary:
    df = 0
    for filename in token_list_by_file:
        for token in token_list_by_file[filename]:
            if token == dict_token:
                df += 1
                break
    # print(df)
    cropped_dictionary[dict_token] = (cropped_dictionary[dict_token], df)

# adding df to the dictionary
for token in cropped_dictionary:
    cropped_dictionary[token] = [cropped_dictionary[token], 0]
td_df = pd.read_csv('../../assets/td_matrix')
for index, row in td_df.iterrows():
    for token in cropped_dictionary:
        if row[token] > 0:
            cropped_dictionary[token][1] += 1
            print(token)

with open("../../assets/df_cropped_dictionary", "wb") as file:
    pickle.dump(cropped_dictionary, file)
with open("../../assets/df_cropped_dictionary", "rb") as file:
    df_cropped_dictionary = pickle.load(file)
print(df_cropped_dictionary)
