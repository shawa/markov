from collections import defaultdict
from itertools import islice
import numpy as np
import utils


def generate_next_word_graph(text):
    '''Build the dictionary of {word: [next word]}
    text: string to train graph on
    '''
    # This essentially models a weighted directed graph, where each vertex v_i
    # is a word, and each edge (v_i, v_j) models v_j appearing in the text
    # after v_i.  Edge weights w_ij denote frequency, that is w_ij > w_ik
    # implies v_j appears more frequently after v_k
    counts = defaultdict(lambda: defaultdict(int))
    words = text.split()
    word_pairs = zip(words, islice(words, 1, None))
    for word, next in word_pairs:
        counts[word][next] += 1
    return counts


def output_stream(word_graph, init_word):
    def seed(): return np.random.choice(list(word_graph.keys()))
    prev = init_word if init_word is not None else seed()
    yield prev
    while True:
        next_words = word_graph[prev]
        prev = np.random.choice(list(next_words.keys()),
                                p=utils.normalize(next_words.values()))
        yield prev


if __name__ == '__main__':
    import sys
    try:
        n = int(sys.argv[1])
        seed = sys.argv[2]
    except:  # lol
        seed = None

    with open('tweets/tweets.txt', 'r') as f:
        words = generate_next_word_graph(''.join(f.readlines()))

    for sentence in islice(output_stream(words, seed), n):
        print(sentence, end=' ')
