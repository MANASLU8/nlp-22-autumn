import csv

import os


def create_dict():
    dictionary = []
    for i in range(1, 5):
        dir = f'projects/mansurov-project/assets/annotated-corpus/train/{i}'
        for file in os.listdir(dir):
            f = os.path.join(dir, file)
            with open(f, 'rb') as tsv_file:
                lines = tsv_file.readlines()
                for line in lines:
                    line = line.decode('utf8')
                    item = line.split('\t')[0]
                    # if normal word then save lowercase
                    # else save as is
                    if (item.isalpha() and item[1:].islower()):
                        dictionary.append(item.lower())
                    else:
                        dictionary.append(item)
    
    set_ = set(dictionary)
    os.makedirs('projects/mansurov-project/assets/dictionary', exist_ok=True)
    f = open('projects/mansurov-project/assets/dictionary/dict.tsv', "wb")
    for token in set_:
        f.write(f'{token}\n'.encode('utf8'))
    
        
if __name__ == "__main__":
    create_dict()