import bot
import unittest
from itertools import islice
from pprint import pprint


class TestNextWord(unittest.TestCase):
    def test_contruct_next_word_graph(self):
        text = 'a a a b a c'
        words = bot.generate_next_word_graph(text)
        # TODO Assert weights
        pprint(words)

    def test_sentence_stream(self):
        text = 'a a a b a c'
        words = bot.generate_next_word_graph(text)
        for x in islice(bot.output_stream(words, None), 10):
            print(x, sep=None)
        print()


if __name__ == '__main__':
    unittest.main()
