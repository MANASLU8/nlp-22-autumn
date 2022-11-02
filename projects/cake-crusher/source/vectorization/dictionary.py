import pickle
import os
import re
import nltk
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
import copy
import pandas as pd

stops = set(stopwords.words("english"))

# сreating dictionary
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
                        # print('Skipped punctuation symbol or stop word', token)
                        continue
                    dictionary[token] = dictionary.get(token, 0) + 1
                # else:
                #     token = line
    print(count)

with open("../../assets/dictionary", "wb") as file:
    pickle.dump(dictionary, file)
with open("../../assets/dictionary", "rb") as file:
    dictionary = pickle.load(file)

print(dictionary)

# sorting
# freqs_dict = dict(sorted(freqs_dict.items(), key=lambda item: item[1]))

# filtering low frequency tokens
cropped_dictionary = copy.copy(dictionary)
for token in dictionary:
    if dictionary[token] <= 5:
        del cropped_dictionary[token]
del dictionary

with open("../../assets/cropped_dictionary", "wb") as file:
    pickle.dump(cropped_dictionary, file)
with open("../../assets/cropped_dictionary", "rb") as file:
    cropped_dictionary = pickle.load(file)
#
# print(cropped_dictionary)
# print(len(cropped_dictionary))



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
# for token in cropped_dictionary:
#     cropped_dictionary[token] = [cropped_dictionary[token], 0]
# td_df = pd.read_csv('../../assets/td_matrix')
# for index, row in td_df.iterrows():
#     for token in cropped_dictionary:
#         if row[token] > 0:
#             cropped_dictionary[token][1] += 1
#             print(token)

with open("../../assets/df_cropped_dictionary", "wb") as file:
    pickle.dump(cropped_dictionary, file)
with open("../../assets/df_cropped_dictionary", "rb") as file:
    df_cropped_dictionary = pickle.load(file)
print(df_cropped_dictionary)

# словарь, содержащий ключ=имя файла, значение=список токенов в файле
# test_dict = dict()
# data_path = '../../assets/annotated-corpus/'
# set_name = 'test'
# for category in os.listdir(data_path + set_name):
#     for filename in os.listdir(data_path + set_name + '/' + category):
#         print(filename)
#         token_list = []
#         with open(data_path + set_name + '/' + category + '/' + filename) as file:
#             for line in file:
#                 if line != '\n':
#                     token = re.split(r'\t', line)[0]
#                     # punctuation cleaner
#                     if re.fullmatch(r'[\'!()\\\-\[\]{};@?<>:\",./^&*_|+`%#=~]+', token) or token in stops:
#                         continue
#                     token_list.append(token)
#         test_dict[category + '/' + filename] = token_list
#                 # else:
#                 #     token = line
# with open("../../assets/test_dict", "wb") as file:
#     pickle.dump(test_dict, file)
# with open("../../assets/test_dict", "rb") as file:
#     test_dict = pickle.load(file)
# print(test_dict)

# terms in documents
# for dict_token in dictionary:
#     # dictionary[dict_token] = (dictionary[dict_token], 0)
#     dfs = 0
#     print(dict_token)
#     for filename in test_dict:
#         for token in test_dict[filename]:
#             if token == dict_token:
#                 dfs += 1
#                 break
#     dictionary[dict_token] = (dictionary[dict_token], dfs)
#
# print(dictionary)

# with open("../../assets/test_cfs_dfs_dictionary", "wb") as file:
#     pickle.dump(test_cfs_dfs_dictionary, file)
# with open("../../assets/test_cfs_dfs_dictionary", "rb") as file:
#     test_cfs_dfs_dictionary = pickle.load(file)
