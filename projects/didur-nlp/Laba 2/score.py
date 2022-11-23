import os
import re

path = '../assets/annotated-corpus/test/'
corrupted_path = '../assets/annotated-corpus/newsgroups-test-corrupted/'
corrected_path = '../assets/annotated-corpus/newsgroups-test-fixed/'

files_score = 0
tokens_score = 0
corrupted_tokens_score = 0
fixed_tokens_score = 0
fixed_good_tokens_score = 0

for category in os.listdir(corrected_path):
    broken_files = []
    for filename in os.listdir(corrected_path + category):
        files_score += 1
        test_file_path = path + category + '/' + filename
        corrupted_file_path = corrupted_path + category + '/' + filename
        corrected_file_path = corrected_path + category + '/' + filename
        with open(test_file_path, 'r') as f1, open(corrupted_file_path, 'r') as f2:
            if len(f1.readlines()) != len(f2.readlines()):
               broken_files.append(filename)
    print(broken_files)

    for filename in os.listdir(corrected_path + category):
        if filename not in broken_files:
            test_file_path = path + category + '/' + filename
            corrupted_file_path = corrupted_path + category + '/' + filename
            corrected_file_path = corrected_path + category + '/' + filename
            with open(test_file_path, 'r') as f1, open(corrupted_file_path, 'r') as f2, open(corrected_file_path, 'r') as f3:
                line_number = 0
                for line1, line2, line3 in zip(f1, f2, f3):
                    tokens_score += 1
                    line1 = re.split(r'\t', line1)[0]
                    line2 = re.split(r'\t', line2)[0]
                    line3 = line3[:-1]
                    #print(line1, line2, line3)
                    if line1 == line2 and line1 != line3:
                        fixed_good_tokens_score += 1
                    if line1 != '\n' and line1 != line2:
                        corrupted_tokens_score += 1
                        if line1 == line3:
                            fixed_tokens_score += 1


print('Corrected files count is '+ str(files_score))
print('Test tokens count is '+ str(tokens_score))
print('Corrupted tokens count is ' + str(corrupted_tokens_score))
print('Corrupted tokens in corrupted set: ' + str(corrupted_tokens_score * 100 / tokens_score))
print('Corrected tokens count is ' + str(fixed_tokens_score))
print('Corrupted tokens in corrected set: ' + str((corrupted_tokens_score + fixed_good_tokens_score - fixed_tokens_score) * 100 / tokens_score))
print('Difference is ' + str(corrupted_tokens_score * 100 / tokens_score - (corrupted_tokens_score + fixed_good_tokens_score - fixed_tokens_score) * 100 / tokens_score))
print('Процент исправленных ошибок: ' + str((corrupted_tokens_score * 100 / tokens_score - (corrupted_tokens_score + fixed_good_tokens_score - fixed_tokens_score) * 100 / tokens_score) * 100 / (corrupted_tokens_score * 100 / tokens_score)))
print('Добавлено ошибок: ' + str(fixed_good_tokens_score))