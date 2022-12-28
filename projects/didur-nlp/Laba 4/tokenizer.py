import re
def tokenizer(text):
    prefixes = r"(Mr|St|Mrs|Ms|Dr)(\.)"
    suffixes = r"(Inc|Ltd|Jr|Sr|Co)"
    starters = r"(Mr|Mrs|Ms|Dr|He's|She's|It's|They's|Their's|Our's|We's|But's|However's|That's|This's|Wherever)"
    email = r"([\w.]+@[\w.]+\.[\w]+)|"
    version = r'([A-Z][a-z]+: \d\.\d)|' #Version: 1.0
    price = r'([$]\d\.\d{1,2})|' #$4.95
    phone = r'([A-Z][a-z]+: \(\d{2,3}\) \d{3}-?\d{4})|' # Telephone: (608) 256-8900
    fax = r'([A-Z][a-z]+:\s+\(\d{3}\) \d{3}-?\d{4})|' # Fax:      (456) 211-1234
    time = r'(\d\d ?: ?\d\d ?: ?\d\d ?\w\w\w)|' #11:57:19 GMT
    date = r'(\d?\d [A-Z][a-z]+ \d{2,4})' #Thu, 29 Apr 1993
    end_of_string = r'(?<=[\.\?!])\s+(?=[A-Z])'
    text = re.sub(end_of_string, '\n', text)

    tokenlist = re.split(r'(\n+)|\s+|\t+|(:)|(#)|(,)|(\.(?!\d))|((?<!\d)\))|(")|(-)|(_)|(\\)|(/)|(\?)|(<)|(>)|(\((?!\d))|((?<!\d)\))|'
                         + prefixes + '|' + suffixes + '|' + starters + '|'  + email + fax + version + phone + time + date, text)
    tokenlist = list(filter(None, tokenlist))
    tokenlist = [token.lower() for token in tokenlist]
    return tokenlist