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

def fix_escaped_dollar(text):
    text = re.sub(r"\\\$", "$", text)
    return text

def fix_backslash(text):
    text = re.sub(r"\\\\", "\n", text)
    text = re.sub(r"\\", " ", text)
    return text

def find_numbers(parts):
    # print(parts)
    parts_ = []
    k = True
    for text in parts:
        k = not k
        if k:
            parts_.append(text)
            continue
        text = re.sub(r"(\-?\d+[\,\.]\d+)", r" \b \1 \b ", text)
        parts_.extend(text.split("\x08"))
    return parts_

def find_email(parts):
    # print(parts)
    parts_ = []
    k = True
    for text in parts:
        k = not k
        if k:
            parts_.append(text)
            continue
        text = re.sub(r"(([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*]))", r" \b \1 \b ", text)
        parts_.extend(text.split("\x08"))
    return parts_

def find_phone(parts):
    # print(parts)
    parts_ = []
    k = True
    for text in parts:
        k = not k
        if k:
            parts_.append(text)
            continue
        text = re.sub(r"(\s|^|\,)((((\+?\d+ ?)?((\d+[\- ]?)+ ?((\d+[\- ]?){2,})))|((\+?\d+ ?)?(\((\+?\d+[\- ]?)+\) ?((\d+[\- ]?){2,})))|((\d+[\- ]?){2,})|(\+?\d+)))(\s|$|\,)", r" \b \2 \b ", text)
        parts_.extend(text.split("\x08"))
    return parts_

def find_url(parts):
    # print(parts)
    parts_ = []
    k = True
    for text in parts:
        k = not k
        if k:
            parts_.append(text)
            continue
        text = re.sub(r"(?i)\b((?:https?:(?:\/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:\w+)\/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:\w+)\b\/?(?!@)))", r" \b \1 \b ", text)
        parts_.extend(text.split("\x08"))
    return parts_

def find_short(parts):
    # print(parts)
    parts_ = []
    k = True
    for text in parts:
        k = not k
        if k:
            parts_.append(text)
            continue
        # print(text)
        text = re.sub(r"(\w+\.\'\w+)|(\w+\.)[\t ]+([^A-Z]+)|(\w+\.)[^\s\n]", r" \b \1 \2 \4 \b \3 ", text)
        # print(text)
        parts_.extend(text.split("\x08"))
    return parts_

# tokenize sentence
def tokenize_sentence(sentence):
    # print(sentence)
    sentence = re.sub(r"(\.\.\.|[\.\,!\?\-\:\;\\\*\$\"\(\)])", r" \1 ", sentence)
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
    text = sentence
    
    text = fix_html(text)
    text = fix_escaped_dollar(text)
    text = fix_backslash(text)
    
    parts = [text]
    
    parts = find_email(parts)
    parts = find_url(parts)
    parts = find_numbers(parts)
    parts = find_phone(parts)
    parts = find_short(parts)
    
    text = "\x08".join(parts)
    
    tokens = tokenize_sentence(text)
    tokens = combine_tokens(tokens)
    sentences = split_sentences(tokens)
    
    return sentences

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
    
    
def fix_all(text):
    text = fix_html(text)
    text = fix_escaped_dollar(text)
    text = fix_backslash(text)
    return text    

if __name__ == "__main__":
    # print(tokenize(""))
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
    
    # print(tokenize("s226.223pace.k@g.com"))
    
    # t1 = "Russian Alien Spaceship Claims Raise Eyebrows, Skepticism (SPACE.com). SPACE.com - An expedition of Russian researchers claims to have found evidence that an \  alien spaceship had something to do with a huge explosion over Siberia in 1908. \  Experts in asteroids and comets have long said the massive blast was caused \  by a space rock."
    # print(tokenize(t1))
    
    # print("\n\n")
    
    # t1 = r"EUROPES biggest defence contractors will have the chance to bid for a \$23 billion (12 billion) air refuelling contract for the US Air Force that has been withdrawn from Boeing."
    # print(tokenize(t1))
    # print("\n\n")
    
    # t1 = r"Reuters - A group of technology companies\including Texas Instruments Inc. (TXN.N), STMicroelectronics\(STM) and Broadcom Corp. (BRCM.O), on Thursday said they\will propose a new wireless networking standard up to 10 times\the speed of the current generation."
    # print(tokenize(t1))
    # print("\n\n")
    
    # print(tokenize("Master (a.k.a. lord)."))
    # print(tokenize("My test sentence. Second sentence"))
    
    # print(tokenize("Email: some.mail-my.h@mail.ru."))
    
    # t1 = r"\\I've been a big fan of Log4J  for a while \ now but haven't migrated any code\over for one central reason.  The following line of code:\\    final static Logger logger = Logger.getLogger( ""some.name"" );\\... is amazingly ugly and difficult to work with.\\Most people use Log4J with a logger based on the classname:\\So we would probably see:\\    static Logger logger = Logger.getLogger( ""org.apache.commons.feedparser.locate.FeedLocator"" );\\Which is amazingly verbose.  A lot of developers shorten this to:\\    static Logger logger = Logger.getLogger( FeedLocator.class );\\But this still leaves us with cut and paste errors.\\What if we could just reduce it to:\\    static Logger logger = Logger.g ...\\"
    # print(tokenize(t1))
    # print("\n\n")
    
    # t1 = r"The \$41 billion merger between Cingular Wireless LLC and AT T Wireless Services Inc. won approval from the Federal Communications Commission Friday, according to federal sources close to the agency. &lt;BR&gt;\&lt;FONT face=""verdana,MS Sans Serif,arial,helvetica"" size=""-2""\ color=""#666666""&gt;&lt;B&gt;-The Washington Post&lt;/B&gt;&lt;/FONT&gt;"
    # print(tokenize(t1))
    # print("\n\n")
    
    # t1 = r"AP - Steve Gleason of the New Orleans Saints was fined  #36;5,000 by the NFL on Wednesday after being thrown out of last week's game with Carolina for punching the Panthers' Kemp Rasmussen at the end of a kickoff return."
    # print(tokenize(t1))
    # print("\n\n")
    
    # print("\\\\$ \\\$ \\$ \$ $")
    # print(fix_escaped_dollar("\\\\$ \\\$ \\$ \$ $"))
    
    # read_file('projects/mansurov-project/assets/train.csv')
    
    read_and_annotate('test', rows = -1)
    read_and_annotate('train', rows = -1)
    
    # f_out = f'projects/mansurov-project/assets/annotated-corpus/train/3/test.tsv'
    # annotate("Russian Alien Spaceship Claims Raise Eyebrows, Skepticism (SPACE.com). SPACE.com - An expedition of Russian researchers claims to have found evidence that an \  alien spaceship had something to do with a huge explosion over Siberia in 1908. \  Experts in asteroids and comets have long said the massive blast was caused \  by a space rock.", f_out)