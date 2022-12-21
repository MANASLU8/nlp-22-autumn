import unittest

from source.spellfix.spellcheck import spellcheck, __init__

class TestSpellcheck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        __init__()
    
    def test_cat(self):
        self.assertEqual(spellcheck("cat"), "cat")
        
    def test_dog(self):
        self.assertEqual(spellcheck("dog"), "dog")
        self.assertEqual(spellcheck("doh"), "dog")
        self.assertEqual(spellcheck("Doh"), "Dog")
        
    def test_doc(self):
        self.assertEqual(spellcheck("doc"), "doc")
        
    def test_goods(self):
        self.assertEqual(spellcheck("goads"), "gods")
        
    def test_airplane(self):
        self.assertEqual(spellcheck("airplane"), "airplane")
        
    def test_assault(self):
        self.assertEqual(spellcheck("aasalt"), "assault")
        