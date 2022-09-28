import unittest

from tokenization.tokenizer import tokenize

class TestTokenization(unittest.TestCase):
    def test_on_empty_string(self):
        self.assertEqual(0, len(tokenize("")))

    def test_on_spaces(self):
        self.assertEqual(["foo", "bar"], tokenize("foo bar"))

    def test_on_empty_string_with_spaces(self):
        self.assertEqual(0, len(tokenize("      ")))

    def test_on_tabs_and_newlines(self):
        self.assertEqual(["foo", "bar", "baz", "qux", "quux"],
                         tokenize("foo\tbar\nbaz    qux\t\t\t\nquux"))

    def test_on_email_hosts(self):
        self.assertEqual(["wes!ton@uc!ssun1.sdsu.edu", "obelix.gaul.csd.u!wo.ca",
                          "1pr9qnI.NNiag@tahko.lpr.carel.fi"],
                         tokenize("wes!ton@uc!ssun1.sdsu.edu "
                                  "obelix.gaul.csd.u!wo.ca "
                                  "1pr9qnI.NNiag@tahko.lpr.carel.fi "))

    def test_on_names(self):
        self.assertEqual(["Aaron Johnson", "Henry A. Neill", "Obi-Wan Kenobi", "Michael B Jordan-Bordan"],
                        tokenize("Aaron Johnson    Henry A. Neill      Obi-Wan Kenobi     Michael B Jordan-Bordan"))

    def test_on_companies(self):
        self.assertEqual(["Ford Motor Company", "School of EECS", "University of Illinois at Urbana"],
                         tokenize("Ford Motor Company   School of EECS  University of Illinois at Urbana"))

    def test_on_phone_numbers(self):
        self.assertEqual(["+34 1 336-7448", "+7 (921) 662-07 74", "8 921 548 72 72", "(503) 629-7605",
                          "8 921 6620774", "8 921 662 0774", "+41-21-6934290"],
                         tokenize("+34 1 336-7448 "
                                  "+7 (921) 662-07 74 "
                                  " 8 921 548 72 72"
                                  " (503) 629-7605 "
                                  "8 921 6620774 "
                                  "8 921 662 0774 "
                                  "+41-21-6934290"))

    def test_on_date(self):
        self.assertEqual(["25th June 1993", "30th Sep", "Dec 9th 2003", "Nov 25 1999", "25 Nov 99"],
                         tokenize("25th June 1993 30th Sep Dec 9th 2003 Nov 25 1999 25 Nov 99"))

if __name__ == "__main__":
        unittest.main()
