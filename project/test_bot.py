import bot
import unittest


class TestNextWord(unittest.TestCase):
    def test_contruct_next_word_graph(self):
        text = 'a a b a d b a e e f f g h i j'
        words = bot.generate_next_word_graph(text)
        print(words)

if __name__ == '__main__':
    unittest.main()
