import unittest
from source.typos_fixer.levenshtein import *
from gensim import corpora

class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.dictionary = corpora.Dictionary().load_from_text('../../assets/clean_dictionary.txt')
        print("The dictionary has: " + str(len(self.dictionary)) + " tokens")

    def test_on_ok_case(self):
        most_likely_word = fix_word(self.dictionary, 'dictionary', 1)
        self.assertEqual('dictionary', most_likely_word)

    def test_on_delete(self):
        most_likely_word = fix_word(self.dictionary, 'dictionaryk', 1)
        self.assertEqual('dictionary', most_likely_word)

    def test_on_insert(self):
        most_likely_word = fix_word(self.dictionary, 'dictnary', 1)
        self.assertEqual('dictionary', most_likely_word)

    def test_on_subst(self):
        most_likely_word = fix_word(self.dictionary, 'ditianart', 1)
        self.assertEqual('dictionary', most_likely_word)

    def test_on_complex(self):
        most_likely_word = fix_word(self.dictionary, 'apictipnry', 1)
        self.assertEqual('dictionary', most_likely_word)

    def test_on_are_subst_qwerty(self):
        most_likely_word = fix_word(self.dictionary, 'arw', 1)
        self.assertEqual('are', most_likely_word)

    def test_on_are_no_subst_qwerty(self):
        most_likely_word = fix_word(self.dictionary, 'aru', 1)
        self.assertEqual('ar', most_likely_word)

    def test_on_an_to_and_no_insert(self):
        most_likely_word = fix_word(self.dictionary, 'an', 1)
        self.assertEqual('an', most_likely_word)

    def test_on_peace_subst_qwerty(self):
        most_likely_word = fix_word(self.dictionary, 'peave', 1)
        self.assertEqual('peace', most_likely_word)

    def test_on_insert_equals_for_cler(self):
        most_likely_list = fix_word(self.dictionary, 'cler', 2)
        self.assertEqual(['clear', 'clerk'], most_likely_list)

    def test_on_alternatives_with_qwerty_subst_and_delete(self):  # rats rays
        most_likely_list = fix_word(self.dictionary, 'raus', 2)
        self.assertEqual(['rays'], most_likely_list)

    def test_on_rays_like_most_frequent_and_raus_to_rays_qwerty(self):
        most_likely_list = fix_word(self.dictionary, 'raus', 1)
        self.assertEqual('rays', most_likely_list)

    def test_on_rafs_to_rats_qwerty_and_most_freq(self):
        most_likely_list = fix_word(self.dictionary, 'rars', 2)
        self.assertEqual(['ears', 'rats'], most_likely_list)

    def test_on_Lined_to_Lines(self):
        most_likely_list = fix_word(self.dictionary, 'Lined', 1)
        self.assertEqual('Lines', most_likely_list)

    def test_on_Linel_to_Line(self):
        most_likely_list = fix_word(self.dictionary, 'Linel', 1)
        self.assertEqual('Line', most_likely_list)

if __name__ == '__main__':
    unittest.main()
