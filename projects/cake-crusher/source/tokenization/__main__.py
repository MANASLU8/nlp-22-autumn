import click
import os
import re
import snowballstemmer
import nltk
import shutil

from tokenizer import tokenize
from writer import write_to_tsv


# @click.group()
def main():
    pass
#
# @main.command()
# @click.argument("data_path", type=str)
def run(data_path):

    nltk.download('wordnet')
    nltk.download('omw-1.4')
    try:
        stemmer = snowballstemmer.stemmer('english')
        lemmatizer = nltk.WordNetLemmatizer()
    except Exception as e:
        print(e)

    if os.path.exists('../../assets/annotated-corpus'):
        shutil.rmtree('../../assets/annotated-corpus')

    for set_name in os.listdir(data_path):
        print(set_name + ' >>>')
        set_type = re.search(r'\w+$', set_name)[0]
        for category in os.listdir(data_path + set_name):
            print('\t' + category)
            if not os.path.exists('../../assets/annotated-corpus/' + set_type + '/' + category):
                os.makedirs('../../assets/annotated-corpus/' + set_type + '/' + category)

            for filename in os.listdir(data_path + set_name + '/' + category):
                # print(filename)
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
# @main.command()
# @click.argument("text", type=str)
# def label(text):
#     labels = read_emoji_to_label_mapping("assets/emoji-to-label.yml").classify(text)
#
#     if len(labels) == 0:
#         print("No labels found for the given text")
#     else:
#         print(f"Provided text mentions {', '.join(labels)}")

if __name__ == "__main__":
    # main()
    run(data_path='D:/Edu Projects/nlp-22-autumn/projects/cake-crusher/dataset/')