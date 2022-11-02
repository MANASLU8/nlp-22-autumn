import os

path = '../../assets/annotated-corpus/test/'
corrupted_path = '../../assets/annotated-corpus/corrupted_test/'
corrected_path = '../../assets/annotated-corpus/corrected_test/'

files_counter = 0
tokens_counter = 0
corrupted_tokens_counter = 0
corrected_tokens_counter = 0
corrupted_good_tokens_counter = 0

for category in os.listdir(corrected_path):
    broken_files = []
    for filename in os.listdir(corrected_path + category):
        files_counter += 1
        test_file_path = path + category + '/' + filename
        corrupted_file_path = corrupted_path + category + '/' + filename
        corrected_file_path = corrected_path + category + '/' + filename
        with open(test_file_path) as f1, open(corrupted_file_path) as f2:
            if len(f1.readlines()) != len(f2.readlines()):
                broken_files.append(filename)
                #print(filename)

    for filename in os.listdir(corrected_path + category):
        if filename not in broken_files:
            test_file_path = path + category + '/' + filename
            corrupted_file_path = corrupted_path + category + '/' + filename
            corrected_file_path = corrected_path + category + '/' + filename
            with open(test_file_path) as f1, open(corrupted_file_path) as f2, open(corrected_file_path) as f3:
                line_number = 0
                for line1, line2, line3 in zip(f1, f2, f3):
                    tokens_counter += 1
                    if line1 == line2 and line1 != line3:
                        corrupted_good_tokens_counter += 1
                    if line1 != '\n' and line1 != line2:
                        corrupted_tokens_counter += 1
                        if line1 == line3:
                            #print(line1[:-1] + ' ' + line2[:-1] + ' ' + line3[:-1])
                            corrected_tokens_counter += 1
                        #print(line1[:-1] + ' ' + line2[:-1] + ' ' + line3[:-1])

print('Corrected files count is '+ str(files_counter))
print('Test tokens count is '+ str(tokens_counter))
print('Corrupted tokens count is ' + str(corrupted_tokens_counter))
print('Corrupted tokens in corrupted set: ' + str(corrupted_tokens_counter * 100 / tokens_counter))
print('Corrected tokens count is ' + str(corrected_tokens_counter))
print('Corrupted tokens in corrected set: ' + str((corrupted_tokens_counter + corrupted_good_tokens_counter - corrected_tokens_counter) * 100 / tokens_counter))
print('Difference is ' + str(corrupted_tokens_counter * 100 / tokens_counter - (corrupted_tokens_counter + corrupted_good_tokens_counter - corrected_tokens_counter) * 100 / tokens_counter))
print('Процент исправленных ошибок: ' + str((corrupted_tokens_counter * 100 / tokens_counter - (corrupted_tokens_counter + corrupted_good_tokens_counter - corrected_tokens_counter) * 100 / tokens_counter) * 100 / (corrupted_tokens_counter * 100 / tokens_counter)))
#print('Добавлено ошибок: ' + str(corrupted_good_tokens_counter))