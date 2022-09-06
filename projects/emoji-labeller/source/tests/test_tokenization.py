import unittest

from classifier.tokenizer import tokenize

class TestTokenization(unittest.TestCase):
    def test_on_empty_string(self):
        self.assertEqual(len(tokenize("")), 0)

    def test_on_spaces(self):
        self.assertEqual(tokenize("foo bar"), ("foo", "bar"))

    def test_on_empty_string_with_spaces(self):
        self.assertEqual(len(tokenize("    ")), 0)

    def test_on_tabs_and_newlines(self):
        self.assertEqual(tokenize("foo\tbar\nbaz    qux\t\t\t\nquux"), ("foo", "bar", "baz", "qux", "quux"))

if __name__ == "__main__":
    unittest.main()
