import re
import nltk

# передача DATADIR через cmd и unit tests.
def tokenize(text):
  # add identificator of new string
  text = re.sub(r'(?<!\w\.\w.)(?<![A-Z][a-z])(?<! [A-Z].)(?<=[.?!])[\s]+|(?<![\w])[\n](?<![\w\s])|'
                r'(?<![.])[\n]+(?=[A-Z=\-[\]])', '🍰', text)

  tokens = re.split(
                    r'(🍰)|[\t\n]+|(\.)\n|(:)|(\()(?!\d)|(?<!\d)(\))|(,)|'
                    r'(\?)|(!)(?!\w)|(\\)|(\/)|(\|)|(")|(>)+|(-)+|[\[\]]|'
                    #   PUNCTUATION and Spec. symbols
                    r'([!\w.-]+@[!\w.-]+\.[!\w-]+)|'
                    #  EMAIL
                    r'([A-Z][\w-]+?\s?[A-Z]?\.?\s[A-Zo][\w-]+( ?[A-Za][\w]+){0,4})|'
                    #  Name A. Surname + COMPANIES
                    r'(\d?\d [A-Z][a-z]+ \d{2,4})|'
                    r'(\d?\d[a-z]{2} [JFMASOND][a-z]{2,8} \d{2,4})|'
                    r'(\d?\d[a-z]{2} [JFMASOND][a-z]{2,8})|'
                    r'([JFMASOND][a-z]{2,8} \d?\d[a-z]{2}? \d{2,4})|'
                    r'([JFMASOND][a-z]{2,8} \d?\d \d{2,4})|'
                    # Various Dates 
                    r'(\d\d ?: ?\d\d ?: ?\d\d)|'
                    # Time
                    # r'((?<!\d)(\+\d{1,2}|\d|\(\d{3}\))[ -](\d|\(?\d\d\d\)?)[ -]?\d{1,3}[ -]\d{1,4}[ -]?\d{0,4}(?!\d))|'
                    r'((?<!\d)\+\d{1,2}[ -]\d\d[ -]\d{7}(?!\d))|'
                    r'((?<!\d)\+\d{1,2}[ -]\d{1}[ -]\d{3}[ -]\d{4}(?!\d))|'
                    r'((?<!\d)\+?\d[ -]\(?\d{3}\)?[ -]\d{3}[ -]\d\d[ -]?\d\d(?!\d))|'
                    r'((?<!\d)\(\d{3}\)[ -]\d{3}[ -]\d\d[ -]?\d\d(?!\d))|'
                    r'((?<!\d)\d{1} ?\d{3} \d{7}(?!\d))|'
                    # # various Phone numbers
                    r'(\.)\s|(?<![\d()]) +|^ +$|(\.)(?![a-z]+)|(\.\.\.)'
                    , text)

  tokens = list(filter((None), tokens))
  #                             r'\w +|\t+'
  tokens = [token for token in tokens if not re.match(r'(?<![\d()]) +|^ +$', token)]
  # print(tokens)

  return tokens
