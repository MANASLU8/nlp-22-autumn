import re

space_regexp = re.compile("\s+")

def tokenize(text: str):
    return tuple(filter(lambda token: len(token) > 0, space_regexp.split(text)))
