import unittest

from source.tokenizer.tokenizer import tokenize_sentence

class TestTokenization(unittest.TestCase):
    def test_on_empty_string(self):
        self.assertEqual(len(tokenize_sentence("")), 0)

    def test_on_spaces(self):
        self.assertEqual(tokenize_sentence("foo bar"), ("foo", "bar"))

    def test_on_empty_string_with_spaces(self):
        self.assertEqual(len(tokenize_sentence("    ")), 0)

    def test_on_tabs_and_newlines(self):
        self.assertEqual(tokenize_sentence("foo\tbar\nbaz    qux\t\t\t\nquux"), ("foo", "bar", "baz", "qux", "quux"))

if __name__ == "__main__":
    unittest.main()