import nltk
import re
import os
nltk.download('punkt', quiet=True)


def chunk_list(lst, n):
    for x in range(0, len(lst), n):
        e_c = lst[x : n + x]

        if len(e_c) < n:
            e_c = e_c + [None for y in range(n - len(e_c))]
        yield e_c


for cls in os.listdir("../../assets/raw_articles"):
    if not os.path.exists("../../assets/preprocessed_articles/" + cls):
        os.makedirs("../../assets/preprocessed_articles/" + cls)
    for filename in os.listdir("../../assets/raw_articles/" + cls):
        with open("../../assets/raw_articles/" + cls + '/' + filename, encoding="utf-8") as file:
            text = file.read()
            text = text.lower()
            text = re.sub('||\d+|®||||||||||\.{4,100}|…', '', text)
            text = re.sub('-', ' ', text)
            text = re.sub('.*введение', '', text)
            text = re.sub('список литературы.*', '', text)
            sent_text = nltk.sent_tokenize(text, language="russian")
            print(len(sent_text))
            n = len(sent_text) // 100
            print(n)
            #lol = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
            chunks = list(zip(*[iter(sent_text)]*(100)))
            ident = 0
            for chunk in chunks:
                print(chunk)
                sent = ""
                for sentence in chunk:
                    sent += '\n' + sentence
                with open(f"../../assets/preprocessed_articles/{cls}/{filename}_{ident}", 'a+', encoding="utf-8") as f:
                    f.write(sent)
                ident += 1
