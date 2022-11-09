import pickle
import pandas as pd
import os
import re
import nltk
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords

stops = set(stopwords.words("english"))

with open("../../assets/cropped_dictionary", "rb") as file:
    dictionary = pickle.load(file)
print('Длина словаря:', len(dictionary))

# создать словарь, содержащий ключ=имя_файла, значение=список_токенов_в_файле
token_list_by_file = dict()
data_path = '../../assets/annotated-corpus/'
set_name = 'train'
for category in os.listdir(data_path + set_name):
    for filename in os.listdir(data_path + set_name + '/' + category):
        print(filename)
        token_list = []
        with open(data_path + set_name + '/' + category + '/' + filename) as file:
            for line in file:
                if line != '\n':
                    token = re.split(r'\t', line)[0]
                    # punctuation cleaner
                    if re.fullmatch(r'[\'!()\\\-\[\]{};@?<>:\",./^&*_|+`%#=~]+', token) or token in stops:
                        continue
                    token_list.append(token)
        token_list_by_file[category + '/' + filename] = token_list

with open("../../assets/token_list_by_file", "wb") as file:
    pickle.dump(token_list_by_file, file)
# with open("../../assets/token_list_by_file", "rb") as file:
#     token_list_by_file = pickle.load(file)
print(token_list_by_file)

for filename in token_list_by_file:
    token_list_by_file[filename] = [token for token in token_list_by_file[filename] if token in dictionary]
print('Filtered!')

# creating term-document matrix
data_path = '../../assets/annotated-corpus/'
set_name = 'train'
df = pd.DataFrame(columns=dictionary.keys())
for category in os.listdir(data_path + set_name):
    for filename in os.listdir(data_path + set_name + '/' + category):
        df.loc[category + '/' + filename] = 0
        for token in token_list_by_file[category + '/' + filename]:
            try:
                df.at[category + '/' + filename, token] += 1
            except Exception as e:
                print(e)
                pass
    print(category, 'Done')

df.to_csv('../../assets/td_matrix')
df = pd.read_csv('../../assets/td_matrix')
print(df)
