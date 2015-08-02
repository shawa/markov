# -*- coding: utf-8 -*-
from collections import Counter
from itertools import chain
from networkx import DiGraph
from numpy.random import choice

# ASCII Start/End text control characters. It's the best I can come up with
# for a sentinel 'start of sentence' marker that probably won't show up in
# training texts # ¯\_(ツ)_/¯
START = '\x02'
END = '\x03'


class Markov(object):
    def __init__(self, text):
        '''Build a graph representing a Markov chain from a training corpus
        text: Training text, must be an iterable of 'statements', where a
              sentence is a meaningful grouping of words, e.g. a sentence,
              tweet, source code line etc.  '''
        # This is weighted directed graph, where each vertex v_i
        # is a word, and each edge (v_i, v_j) models v_j appearing in the text
        # after v_i.  Edge weights w_ij denote frequency, that is w_ij > w_ik
        # implies v_j appears more frequently after v_k
        def word_pairs():
            '''Generate pairs of words, eventually edges.
            The first and last words of the sentence are paired with START and
            END sentinel strings respectively.'''
            for line in text:
                words = line.split()
                yield (zip(([START] + words), words + [END]))

        counted_pairs = Counter(chain(*word_pairs())).items()
        weighted_edges = ((u, v, w) for ((u, v), w) in counted_pairs)
        self.graph = DiGraph()
        self.graph.add_weighted_edges_from(weighted_edges)

    def sentence(self):
        '''Generate a 'sentence' from the training data'''
        # We simply walk the graph from the START vertex, picking a random
        # edge to follow, biased by weight (i.e. frequency in training text)
        # until we reach an END edge.
        def normalize(xs):
            '''Fit list of values to into a probability distribution'''
            s = sum(xs)
            return [i/s for i in xs]

        current = START
        while True:
            neighbours = self.graph[current]
            words = list(neighbours.keys())
            weights = [attr['weight'] for attr in neighbours.values()]
            current = choice(words, p=normalize(weights))
            if current == END:
                break
            else:
                yield current


if __name__ == '__main__':
    from clize import run

    def main(training_file='texts/tweets.txt', n=10):
        '''Build Markov chain from training file, and generate n words of output
        training_file: source text on which to train the bot
        n: number of lines of output to generate
        '''
        with open(training_file, 'r') as f:
            bot = Markov(f)

        for _ in range(n):
            print(' '.join(list(bot.sentence())))

    run(main)
