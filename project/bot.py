# -*- coding: utf-8 -*-
from itertools import islice, chain
from collections import Counter
import numpy as np
import random
import json
import networkx as nx

# ASCII Start/End text. It's the best I can come up with
# for a sentinel 'start of sentence' marker that won't show up
# in training text (´・ω・`)
STX = '\x02'
ETX = '\x03'


def normalize(xs):
    s = sum(xs)
    return [i/s for i in xs]


def generate_next_word_graph(text):
    '''Build the dictionary of {word: [next word]}
    text: Training text, must be an iterable of 'statements', where a sentence
          is a meaningful grouping of words, e.g. a sentence, tweet,
          source code statement etc.
    '''
    # This essentially models a weighted directed graph, where each vertex v_i
    # is a word, and each edge (v_i, v_j) models v_j appearing in the text
    # after v_i.  Edge weights w_ij denote frequency, that is w_ij > w_ik
    # implies v_j appears more frequently after v_k
    def word_pairs():
        for line in text:
            words = line.split()
            yield (zip(([STX] + words), words + [ETX]))
    counted_pairs = Counter(chain(*word_pairs())).items()
    weigthed_edges = ((u, v, w) for ((u, v), w) in counted_pairs)
    counts = nx.DiGraph()
    counts.add_weighted_edges_from(weigthed_edges)
    return counts

# TODO: counter


def serialze_next_word_graph(graph):
    print(json.dumps(graph))


def sentence(word_graph):
    current = STX
    while True:
        neighbours = word_graph[current]
        words = list(neighbours.keys())
        weights = [attr['weight'] for attr in neighbours.values()]
        current = np.random.choice(words, p=normalize(weights))
        if current == ETX:
            break
        else:
            yield current


def main(*, training_file='texts/tweets.txt', n=10, s=False):
    '''Build Markov chain from training file, and generate n words of output
    training_file: source text on which to train the bot
    n: number of words of output to generate
    s: if true, will serialize graph instead of outputting text
    '''
    with open(training_file, 'r') as f:
        words = generate_next_word_graph(f)
    if s:
        serialze_next_word_graph(words)
    else:
        for _ in range(n):
            for word in sentence(words):
                print(word, end=' ')
            print()



if __name__ == '__main__':
    from clize import run
    run(main)
