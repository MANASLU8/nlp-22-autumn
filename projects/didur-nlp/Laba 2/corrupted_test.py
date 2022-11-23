import os
import re
import nltk
import snowballstemmer

nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

stemmer = snowballstemmer.stemmer('english')
lemmatizer = nltk.WordNetLemmatizer()

listdir = os.listdir("C:/Users/Admin/Desktop/newsgroups-test-corrupted") #чтение имен всех папок внутри каталога
#print(listdir)
for dirname in listdir:
    filelist = os.listdir("C:/Users/Admin/Desktop/newsgroups-test-corrupted/" + dirname) #чтение всех имен файлов в директрии
#    print(filelist)
    if not os.path.exists("C:/Users/Admin/Desktop/pythonProject2newsgroups-test-corrupted/" + dirname):
        os.makedirs('C:/Users/Admin/Desktop/pythonProject2/newsgroups-test-corrupted/' + dirname)
    for filename in filelist:
        with open ("C:/Users/Admin/Desktop/newsgroups-test-corrupted/" + dirname + '/' + filename, 'r') as f:
            text = f.read()
            text = text.replace('\n', ' ')
#            print(text)
        #alphabets = r"([A-Za-z])"
        prefixes = r"(Mr|St|Mrs|Ms|Dr)(\.)"
        suffixes = r"(Inc|Ltd|Jr|Sr|Co)"
        starters = r"(Mr|Mrs|Ms|Dr|He's|She's|It's|They's|Their's|Our's|We's|But's|However's|That's|This's|Wherever)"
        #acronyms = r"([A-Z][.][A-Z][.](?:[A-Z][.])?)"
        #websites = r"[.](com|net|org|io|gov|me|edu|ru|ua)"
        #digits = r"([0-9])"
        #word = r"([A-Za-z0-9]+)"
        #number = r"([1-9][0-9])|"
        email = r"([\w.]+@[\w.]+\.[\w]+)|"
        version = r'([A-Z][a-z]+: \d\.\d)|' #Version: 1.0
        price = r'([$]\d\.\d{1,2})|' #$4.95
        phone = r'([A-Z][a-z]+: \(\d{2,3}\) \d{3}-?\d{4})|' # Telephone: (608) 256-8900
        fax = r'([A-Z][a-z]+:\s+\(\d{3}\) \d{3}-?\d{4})|' # Fax:      (456) 211-1234
        #phone = r'(\(\d{3}\) \d{3}-?\d{4})|' #(608) 256-8900
        time = r'(\d\d ?: ?\d\d ?: ?\d\d ?\w\w\w)|' #11:57:19 GMT
        date = r'(\d?\d [A-Z][a-z]+ \d{2,4})' #Thu, 29 Apr 1993
        end_of_string = r'(?<=[\.\?!])\s+(?=[A-Z])'
        text = re.sub(end_of_string, '\n', text)

        tokenlist = re.split(r'(\n+)|\s+|\t+|(:)|(#)|(,)|(\.(?!\d))|((?<!\d)\))|(")|(-)|(_)|(\\)|(/)|(\?)|(<)|(>)|(\((?!\d))|((?<!\d)\))|'
                             + prefixes + '|' + suffixes + '|' + starters + '|'  + email + fax + version + phone + time + date, text)
        tokenlist = list(filter(None, tokenlist))
        stemmlist = stemmer.stemWords(tokenlist)
        lemmlist = list([lemmatizer.lemmatize(token) for token in tokenlist])
#       print(tokenlist)
        with open ("C:/Users/Admin/Desktop/pythonProject2/newsgroups-test-corrupted/" + dirname + '/' + filename + '.tsv', 'w') as f2:
            for i in range(len(tokenlist)):
                if tokenlist[i] == "\n":
                    f2.write ('\n')
                else:
                    f2.write(tokenlist[i] + '\t' + stemmlist[i] + '\t'+ lemmlist[i] + '\n')
                print(f2)