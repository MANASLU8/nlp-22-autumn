import os

from levenshtein import *
from gensim import corpora

dictionary = corpora.Dictionary().load_from_text('../../assets/clean_dictionary.txt')
print("The dictionary has: " + str(len(dictionary)) + " tokens")

# S2 = ['peave', 'karl', 'petro'] #, 'intention', 'subscibe']
test_path = '../../assets/annotated-corpus/test/'
data_path = '../../assets/annotated-corpus/corrupted_test/'
corrected_path = '../../assets/annotated-corpus/corrected_test/'

excluded_categories = []#'alt.atheism', 'comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware', 'comp.sys.mac.hardware']

unaligned_files = []
with open('../../assets/unaligned_files.txt', 'r') as file:
    for line in file:
        currentPlace = line[:-1]
        unaligned_files.append(currentPlace)
print('Number of unaligned files: ' + str(len(unaligned_files)))

for category in os.listdir(data_path):
    if category in excluded_categories:
        continue
    if not os.path.exists('../../assets/annotated-corpus/corrected_test/' + category):
        os.makedirs('../../assets/annotated-corpus/corrected_test/' + category)
    fixed_count = 0
    for tsv_file in os.listdir(data_path + category):
        fixed_count += 1
        corrected_list = []
        if tsv_file not in unaligned_files and fixed_count <= 20 and tsv_file not in os.listdir(corrected_path + category):
            with open(test_path + category + '/' + tsv_file) as f1, open(data_path + category + '/' + tsv_file) as f2:
                for line1, line2 in zip(f1, f2):
                    if line1 == line2:
                        # correct token
                        corrected_list.append(line2[:-1])
                        continue
                    else:
                        # corrupt token
                        token = line2[:-1] if line2 != '\n' else line2
                        print(token, end=' -> ')
                    if token == '\n':
                        most_likely = '\n'
                    elif (len(token) >= 23 and ' ' not in token): #or len(token) == 1 :
                        most_likely = token
                    else:
                        min_cost = {'cost': 1000, 'id': []}
                        for key in dictionary:
                            # print(dictionary[key])
                            cost = levenshtein(dictionary[key], token, min_cost['cost'])
                            if min_cost['cost'] > cost:
                                min_cost['cost'] = cost
                                min_cost['id'] = []
                                min_cost['id'].append(key)
                            elif min_cost['cost'] == cost:
                                min_cost['id'].append(key)
                            if cost == 0:
                                break

                        if len(min_cost['id']) > 1:
                            max_number = 0
                            most_likely = ''
                            for id in min_cost['id']:
                                if dictionary.dfs[id] > max_number:
                                    max_number = dictionary.dfs[id]
                                    most_likely = dictionary[id]
                        else:
                            most_likely = dictionary[min_cost['id'][0]]
                        if min_cost['cost'] > len(token):
                            most_likely = token

                    if most_likely == '\n':
                        print(most_likely, end='')
                    else:
                        if most_likely == line1[:-1]:
                            print(most_likely)
                        else:
                            print(most_likely + '\t' + 'INCORRECT! Source token = ' + line1[:-1])

                    corrected_list.append(most_likely)

            print(corrected_list)
            with open('../../assets/annotated-corpus/corrected_test/' + category + '/' + tsv_file, 'w') as file:
                for token in corrected_list:
                    if token == '\n':
                        file.write(token)
                    else:
                        file.write(token + '\n')
