from yaml import safe_load
from .tokenizer import tokenize

class EmojiBasedClassifier:
    def __init__(self, mapping: dict):
        self.mapping = mapping

    def _classify(self, text: str):
        for token in tokenize(text):
            if (label := self.mapping.get(token)) is not None:
                yield label

    def classify(self, text: str):
        return tuple(self._classify(text))

def read_emoji_to_label_mapping(path):
    with open(path) as file:
        return EmojiBasedClassifier(safe_load(file))
