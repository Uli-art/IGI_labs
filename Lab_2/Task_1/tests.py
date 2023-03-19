import unittest
from functions import countOfSentences, nonDeclarativeSentences, averageLengthOfSentence, averageLengthOfWord, \
    topKRepeatedWordNGrams, topKRepeatedSymbolNGrams


class TestStatisticsMethods(unittest.TestCase):
    def testCountOfSentences(self):
        self.assertEqual(countOfSentences(""), 0)
        self.assertEqual(countOfSentences("Have a nice holiday! W. F. Smith jr. asked, \"What time is it?\" "
                         "\"It's 6 p.m. right now.\" - answered Dr. Klanton. \"We waited and waited ... and waited."
                         " Green vegetables such as lettuce, spinach, kale, etc..."), 5)
        self.assertEqual(countOfSentences("Charlie scarfed up every Cheeto that fell out of the bag. "
                         "(I wasn’t fast enough to stop him.) At least we won’t have to sweep the floor."), 3)

    def testNonDeclarativeSentences(self):
        self.assertEqual(nonDeclarativeSentences(""), 0)
        self.assertEqual(nonDeclarativeSentences("Have a nice holiday! W. F. Smith jr. asked, \"What time is it?\" "
                         "\"It's 6 p.m. right now.\" - answered Dr. Klanton. \"We waited and waited ... and waited."
                         " Green vegetables such as lettuce, spinach, kale, etc..."), 2)
        self.assertEqual(nonDeclarativeSentences("Charlie scarfed up every Cheeto that fell out of the bag?!!!! "
                         "(I wasn’t fast enough to stop him.) At least we won’t have to sweep the floor."), 1)

    def testAverageLengthOfSentence(self):
        self.assertAlmostEqual(averageLengthOfSentence(""), 0.0, delta=0.00001)
        self.assertAlmostEqual(averageLengthOfSentence("Have a nice holiday! W. F. Smith jr. asked, "
                                                       "\"What time is it?\" \"It's 6 p.m. right now.\" - answered Dr. Klanton. "
                                                       "\"We waited 543 and waited ... and 75fjg7d.\""), 24.75, delta=0.00001)
        self.assertAlmostEqual(averageLengthOfSentence("Charlie scarfed 647 up every Ch2eet4o that fell 6.24 out of the bag?!!!!"
                                                       " \"(I wasn’t fast enough to stop him 88.134.)"), 36.5, delta=0.00001)

    def testAverageLengthOfWord(self):
        self.assertAlmostEqual(averageLengthOfWord(""), 0.0, delta=0.00001)
        self.assertAlmostEqual(averageLengthOfWord("Have a nice holiday! W. F. Smith jr. asked, "
                                                       "\"What time is it?\" \"It's 6 p.m. right now.\" - answered Dr. Klanton. "
                                                       "\"We waited 543 and waited ... and 75fjg7d.\""), 3.5357142, delta=0.00001)
        self.assertAlmostEqual(averageLengthOfWord("Charlie scarfed 647 up every Ch2eet4o that fell 6.24 out of the bag?!!!!"
                                                       " \"(I wasn’t fast enough to stop him 88.134.)"), 3.8421052, delta=0.00001)

    def testTopKRepeatedWordNGrams(self):
        self.assertEqual(topKRepeatedWordNGrams(""), [])
        self.assertEqual(topKRepeatedWordNGrams("Have a nice holiday! W. F. Smith jr. asked, \"What time is it?\" "
                                                "\"It's 6 p.m. right now.\" - answered Dr. Klanton. Have a nice holiday W. F. Smith!"),
                         [('Have a nice holiday', 2), ('a nice holiday W', 2), ('nice holiday W F', 2), ('holiday W F Smith', 2),
                          ('W F Smith jr', 1), ('F Smith jr asked', 1), ('Smith jr asked What', 1), ('jr asked What time', 1),
                          ('asked What time is', 1), ('What time is it', 1)])

    def testTopKRepeatedSymbolNGrams(self):
        self.assertEqual(topKRepeatedSymbolNGrams(""), [])
        self.assertEqual(topKRepeatedSymbolNGrams("Charlie scarfed up sometime, that fell out of the meantime bag lifetime."
                                                  " I wasn't some fast enough to stop him overtime!"),
                         [('time', 4), ('some', 2), ('etim', 2), ('Char', 1),
                          ('harl', 1), ('arli', 1), ('rlie', 1), ('scar', 1),
                          ('carf', 1), ('arfe', 1)])


if __name__ == '__main__':
    unittest.main()
