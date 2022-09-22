import re
import html

import nltk
# nltk.download('wordnet')
# nltk.download('omw-1.4')
from nltk.stem import LancasterStemmer
stemmer = LancasterStemmer()
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

import csv

import os

sentence_delimiters = [
    ".",
    "!",
    "?"
]

delimiters = r"\.\.\.|[\.\,!\?\-\:\;\\\"]"

def fix_html(text):
    text = re.sub(r"(\#\d+\;)", r"&\1", text)
    text = html.unescape(text)
    return text

def find_numbers(text):
    text = re.sub(r"(\-?\d+[\,\.]\d+)", r" \b \1 \b ", text)
    return text

def find_email(text):
    text = re.sub(r"(([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*]))", r" \b \1 \b ", text)
    return text

def find_phone(text):
    text = re.sub(r"(((\+?\d+ ?)?((\d+[\- ]?)+ ?((\d+[\- ]?){2,})))|((\+?\d+ ?)?(\((\+?\d+[\- ]?)+\) ?((\d+[\- ]?){2,})))|((\d+[\- ]?){2,})|(\+?\d+))", r" \b \1 \b ", text)
    return text

def find_url(text):
    text = re.sub(r"(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))", r" \b \1 \b ", text)
    return text

# tokenize sentence
def tokenize_sentence(sentence):
    sentence = re.sub(r"(\.\.\.|[\.\,!\?\-\:\;\\\*\$\"])", r" \1 ", sentence)
    tokens = re.split(r"\s+", sentence)
    tokens = [token for token in tokens if token != '']
    return tokens

def combine_tokens(words):
    tokens = []
    new_word = ""
    w1 = False
    for word in words:
        if word == "\x08":
            if w1:
                tokens.append(new_word)
                new_word = ""
            w1 = not w1
            continue
        if w1:
            new_word = new_word + word
            continue
        tokens.append(word)
    return tokens

def split_sentences(words):
    sentences = []
    sentence = []
    for word in words:
        sentence.append(word)
        if word in sentence_delimiters:
            sentences.append(sentence)
            sentence = []
    if len(sentence) > 0:
        sentences.append(sentence)
    return sentences

def tokenize(sentence):
    _ = sentence
    _ = fix_html(_)
    _ = find_url(_)
    _ = find_email(_)
    _ = find_phone(_)
    _ = find_numbers(_)
    _ = tokenize_sentence(_)
    _ = combine_tokens(_)
    _ = split_sentences(_)
    return _

def stem_(tokens):
    stemmed = list(map(stemmer.stem, tokens))
    return stemmed

def lemmatize_(tokens):
    lemmatized = list(map(lemmatizer.lemmatize, tokens))
    return lemmatized

def annotate(text, file):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    f = open(file, "wb")
    sentences = tokenize(text)
    for sentence in sentences:
        for token in sentence:
            stem = stemmer.stem(token)
            lemm = lemmatizer.lemmatize(token)
            line = f"{token}\t{stem}\t{lemm}\n"
            line = line.encode("utf8")
            f.write(line)
        f.write("\n".encode("utf8"))

def read_and_annotate(dataset, rows = 100):
    file = f'projects/mansurov-project/assets/{dataset}.csv'
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            f_out = f'projects/mansurov-project/assets/annotated-corpus/{dataset}/{row[0]}/{line_count:06d}.tsv'
            annotate(". ".join(row[1:]), f_out)
            # print(f'type: {row[0]}, content: {". ".join(row[1:])}\n')
            line_count += 1
            if (line_count==rows):
                break
    print(f'\nProcessed {line_count} rows')
    return

def read_file(file, rows = 100):
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            print(f'type: {row[0]}, content: {". ".join(row[1:])}\n')
            line_count += 1
            if (line_count>=rows):
                break
    print(f'\nProcessed {line_count} rows')
    return 
    
if __name__ == "__main__":
    # print(tokenize_sentence(""))
    # print(tokenize_sentence("This is bad. Really bad (yeah), true. Very bad!"))
    # print(split_sentences(tokenize_sentence("This is bad. Really bad (yeah), true. Very bad!")))
    # print("\n\n")
    # t1 = "AP - A team taking a low-budget stab at the  #36;10 million.f Ansari X Prize for private manned spaceflight suffered a setback Sunday, when their rocket malfunctioned and exploded after shooting less than 1,000 feet in the air."
    # print(tokenize(t1))

    # print(tokenize("grjniogge-3y3532wjhoi_fguhew@m324ail.cofm"))
    # print(tokenize("200-6606-48, 7 (900) 456 45 45, +7 (000) 000-00-00"))
    # t1 = "AP - The Southern chorus frog has been found in southeastern Virginia, far outside its previously known range. The animal had never before been reported north of Beaufort County, N.C., about 125 miles to the south."
    # print(split_sentences(tokenize_sentence(fix_html(t1))))
    # t1 = "\\Zawodny  threads off of Scoble  on the IE issue:\\""I have to say, when I first read that I nearly fell off my chair laughing. I was\thinking ""how stupid ARE these IE guys?!?!?!"" But we all know that Microsoft is\full of smart people who care about what they're doing. So something really\doesn't compute here.""\\""Last time I checked, IE wasn't even close to feature parity with Mozilla's\browsers. No popup blocking, no tabbed browsing, etc.""\\""Does the IE team really not know what their product is missing?""\\Perhaps.  It's highly likely that they just don't know.\\The bigger issue here is that Microsoft products can't fail and they can't\succeed.  Microsoft has 40-50 billion in the bank.  There ...\\"
    # print(tokenize_sentence(fix_html(t1)))
    
    # t1 = "Russian Alien Spaceship Claims Raise Eyebrows, Skepticism (SPACE.com). SPACE.com - An expedition of Russian researchers claims to have found evidence that an \  alien spaceship had something to do with a huge explosion over Siberia in 1908. \  Experts in asteroids and comets have long said the massive blast was caused \  by a space rock."
    # print(tokenize(t1))
    
    # read_file('projects/mansurov-project/assets/train.csv')
    
    read_and_annotate('test', rows = -1)
    
    # f_out = f'projects/mansurov-project/assets/annotated-corpus/train/3/test.tsv'
    # annotate("Russian Alien Spaceship Claims Raise Eyebrows, Skepticism (SPACE.com). SPACE.com - An expedition of Russian researchers claims to have found evidence that an \  alien spaceship had something to do with a huge explosion over Siberia in 1908. \  Experts in asteroids and comets have long said the massive blast was caused \  by a space rock.", f_out)