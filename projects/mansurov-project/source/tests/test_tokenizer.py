import unittest

from source.tokenizer.tokenizer import tokenize

class TestTokenizationSpaces(unittest.TestCase):
    def test_on_empty_string(self):
        self.assertEqual(len(tokenize("")), 0)

    def test_on_spaces(self):
        self.assertEqual(tokenize("foo bar"), [["foo", "bar"]])

    def test_on_empty_string_with_spaces(self):
        self.assertEqual(len(tokenize("    ")), 0)

    def test_on_tabs_and_newlines(self):
        self.assertEqual(tokenize("foo\tbar\nbaz    qux\t\t\t\nquux"), [["foo", "bar", "baz", "qux", "quux"]])

class TestTokenizationSentences(unittest.TestCase):
    def test_one_sentence(self):
        self.assertEqual(len(tokenize("My test sentence")), 1)
        
    def test_final_period(self):
        self.assertEqual(len(tokenize("My test sentence.")), 1)
        
    def test_period(self):
        self.assertEqual(len(tokenize("My test sentence. Second sentence")), 2)
        
    def test_punctuations(self):
        tokens = tokenize("My 'test', sentence! Second sentence? Third sentence; Good: word.")
        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens, [["My", "'test'", ",", "sentence", "!"], ["Second", "sentence", "?"], ["Third", "sentence", ";", "Good", ":", "word", "."]])
        
class TestFixes(unittest.TestCase):
    def test_html_code(self):
        self.assertEqual(tokenize("a low-budget stab at the  #36;10 million."), [["a", "low", "-", "budget", "stab", "at", "the", "$", "10", "million", "."]])
        
    def test_dollars(self):
        self.assertEqual(tokenize("a low-budget stab at the $10 million."), [["a", "low", "-", "budget", "stab", "at", "the", "$", "10", "million", "."]])
        self.assertEqual(tokenize("a low-budget stab at the \$10 million."), [["a", "low", "-", "budget", "stab", "at", "the", "$", "10", "million", "."]])
        
    def test_backslash(self):
        self.assertEqual(tokenize(r"\\I've been any code\over for one central reason."), [["I've", "been", "any", "code", "over", "for", "one", "central", "reason", "."]])
        
class TestFindNumber(unittest.TestCase):
    def test_find_numbers_point_1(self):
        self.assertEqual(tokenize("Increase by 1.012 is better"), [["Increase", "by", "1.012", "is", "better"]])
    
    def test_find_numbers_comma_1(self):
        self.assertEqual(tokenize("Increase by 1,012 is better"), [["Increase", "by", "1,012", "is", "better"]])
        
    def test_find_numbers_point_2(self):
        self.assertEqual(tokenize("12 + 30.02 = 42.02."), [["12", "+", "30.02", "=", "42.02", "."]])
    
    def test_find_numbers_comma_2(self):
        self.assertEqual(tokenize("30,02, 42,02, 36,25"), [["30,02", ",", "42,02", ",", "36,25"]])
        
class TestFindEmail(unittest.TestCase):
    def test_find_email_1(self):
        self.assertEqual(tokenize("Email: some.mail-my.h@mail.ru"), [["Email", ":", "some.mail-my.h@mail.ru"]])
    
    def test_find_email_2(self):
        self.assertEqual(tokenize("Email: some.mail-my.h@mail.ru."), [["Email", ":", "some.mail-my.h@mail.ru", "."]])
        
class TestFindUrl(unittest.TestCase):
    def test_find_url_1(self):
        self.assertEqual(tokenize("Go to https://en.wikipedia.org/wiki/Main_Page to know more"), [["Go", "to", "https://en.wikipedia.org/wiki/Main_Page", "to", "know", "more"]])
        
    def test_find_url_2(self):
        self.assertEqual(tokenize("Go to https://en.wikipedia.org/wiki/Main_Page."), [["Go", "to", "https://en.wikipedia.org/wiki/Main_Page", "."]])

class TestFindPhone(unittest.TestCase):
    def test_find_phone_1(self):
        self.assertEqual(tokenize("Phone: 8 (000) 000-00-00"), [["Phone", ":", "8(000)000-00-00"]])
        
    def test_find_phone_2(self):
        self.assertEqual(tokenize("Phone: 8 000 000-00-00"), [["Phone", ":", "8000000-00-00"]])
        
    def test_find_phone_3(self):
        self.assertEqual(tokenize("Phone: +7 (000) 000-00-00"), [["Phone", ":", "+7(000)000-00-00"]])
        
    def test_find_phone_4(self):
        self.assertEqual(tokenize("Phone: 000-00-00"), [["Phone", ":", "000-00-00"]])
        
class TestFindShort(unittest.TestCase):
    # def test_find_short_1(self):
    #     self.assertEqual(tokenize("Dr.Blackwater studying math"), [["Dr.Blackwater", "studying", "math"]])
    
    def test_find_short_2(self):
        self.assertEqual(tokenize("Dr. blackwater studying math"), [["Dr.", "blackwater", "studying", "math"]])
        
    def test_find_short_3(self):
        self.assertEqual(tokenize("Go to Master Inc. hq."), [["Go", "to", "Master", "Inc.", "hq", "."]])
        
    def test_find_short_4(self):
        self.assertEqual(tokenize("Boeing Inc.'s plane."), [["Boeing", "Inc.'s", "plane", "."]])
        
class TestCombined(unittest.TestCase):
    def test_combined_1(self):
        self.assertEqual(tokenize("mail.g12-23.23@mail.ru"), [["mail.g12-23.23@mail.ru"]])
        

if __name__ == "__main__":
    unittest.main()