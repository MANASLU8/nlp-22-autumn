import unittest

from classifier.reader import read_emoji_to_label_mapping

class TestClassification(unittest.TestCase):
    def setUp(self):
        self.classifier = read_emoji_to_label_mapping("assets/emoji-to-label.yml")
    
    def test_no_labels(self):
        self.assertEqual(len(self.classifier.classify("foo bar")), 0)

    def test_one_label(self):
        self.assertEqual(self.classifier.classify("foo bar 🐦"), ("birds", ))

    def test_two_labels(self):
        self.assertEqual(self.classifier.classify("foo 😊 bar 🐦"), ("positive-attitude", "birds"))

if __name__ == "__main__":
    unittest.main()
