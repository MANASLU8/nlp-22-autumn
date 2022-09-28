import click
import os
import re
import snowballstemmer
import nltk
import shutil

from tokenizer import tokenize
from writer import write_to_tsv

@click.command()
@click.argument("data_path", type=str)
def main(data_path):

    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)

    try:
        stemmer = snowballstemmer.stemmer('english')
        lemmatizer = nltk.WordNetLemmatizer()
    except Exception as e:
        print(e)
        exit()

    if os.path.exists('../../assets/annotated-corpus'):
        shutil.rmtree('../../assets/annotated-corpus')

    for set_name in os.listdir(data_path):
        print(set_name + ' >>>')
        set_type = re.search(r'\w+$', set_name)[0]
        for category in os.listdir(data_path + set_name):
            count = 0
            length = round(len(os.listdir(data_path + set_name + '/' + category)), -1)
            print('\t' + category + ' >>', end='')
            if not os.path.exists('../../assets/annotated-corpus/' + set_type + '/' + category):
                os.makedirs('../../assets/annotated-corpus/' + set_type + '/' + category)

            for filename in os.listdir(data_path + set_name + '/' + category):
                count += 1
                if (count/length*100) % 10 == 0:
                    print('.', end='')
                with open(data_path + set_name + '/' + category + '/' + filename, 'r') as f:
                    try:
                        text = f.read()
                        tokens = tokenize(text)
                        stemms = stemmer.stemWords(tokens)
                        lemms = list([lemmatizer.lemmatize(token) for token in tokens])
                        write_to_tsv(set_type, category, filename, tokens, stemms, lemms)
                    except Exception as e:
                      # print(e)
                      pass
            print('.<< Done')
            # print('\t' + "".join([' ' for x in range(len(category))]) + '   << Done')
        print('<<< Done')
if __name__ == "__main__":
    main()
    # run(data_path='D:/Edu Projects/nlp-22-autumn/projects/cake-crusher/dataset/')