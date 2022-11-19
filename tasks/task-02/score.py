import os
import re

path = 'assets/annotated-corpus/test/'
corrupted_path = 'assets/annotated-corpus/newsgroups-test-corrupted/'
corrected_path = 'assets/annotated-corpus/newsgroups-test-fixed/'

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
                    if line1 == line2 and line1 != line3:
                        fixed_good_tokens_score += 1
                    if line1 != '\n' and line1 != line2:
                        corrupted_tokens_score += 1
                        if line1 == line3:
                            fixed_tokens_score += 1


print('Количество исправленных файлов '+ str(files_score))
print('Количество тестовых токенов '+ str(tokens_score))
print('Количество поврежденных токенов ' + str(corrupted_tokens_score))
print('Поврежденные токены в поврежденном наборе в % соотношении: ' + str(corrupted_tokens_score * 100 / tokens_score))
print('Счетчик корректных токенов в исправленном датасете ' + str(fixed_tokens_score))
print('Поврежденные токены в исправленном датасете: ' + str((corrupted_tokens_score - fixed_tokens_score) * 100 / tokens_score))
print('Разница между исходным и исправленным в процентах ' + str(corrupted_tokens_score * 100 / tokens_score - (corrupted_tokens_score - fixed_tokens_score) * 100 / tokens_score))