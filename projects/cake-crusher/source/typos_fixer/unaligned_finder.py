import os

data_path = '../../assets/annotated-corpus/corrupted_test/'
test_path = '../../assets/annotated-corpus/test/'

with open('../../assets/unaligned_files.txt', 'w') as f:

    unaligned_files = []

    for category in os.listdir(data_path):
        for filename in os.listdir(data_path + category):
            test_file_path = test_path + category + '/' + filename
            corrupted_file_path = data_path + category + '/' + filename
            with open(test_file_path) as f1, open(corrupted_file_path) as f2:
                if len(f1.readlines()) != len(f2.readlines()):
                    unaligned_files.append(filename)
    with open('../../assets/unaligned_files.txt', 'w') as unaligned_files:
        for filename in unaligned_files:
            f.write("%s\n" % filename)
    print(unaligned_files)