import bot
import unittest
from itertools import islice
from pprint import pprint
import networkx as nx


class TestNextWord(unittest.TestCase):
    def test_contruct_next_word_graph(self):
        text = 'a a a b a c'
        words = bot.generate_next_word_graph([text])
        for n in words:
            print(n)
if __name__ == '__main__':
    unittest.main()
