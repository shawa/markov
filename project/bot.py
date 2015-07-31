# -*- coding: utf-8 -*-
from collections import defaultdict
from itertools import islice, chain
import numpy as np
import json

# ASCII Start Transmission. It's the best I can come up with
# for a sentinel 'start of sentence' marker (´・ω・`)
STX = '\x02'


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
    counts = defaultdict(lambda: defaultdict(int))
    for line in text:
        words = line.split()
        word_pairs = zip(chain([STX], words), words)
        for word, next in word_pairs:
            counts[word][next] += 1
    return counts


def serialze_next_word_graph(graph):
    print(json.dumps(graph))


def output_stream(word_graph):
    prev = STX
    while True:
        next_words = word_graph[prev]
        if not next_words.keys():
            next_words = word_graph[STX]
        prev = np.random.choice(list(next_words.keys()),
                                p=normalize(next_words.values()))
        yield prev


def main(*, training_file='tweets/tweets.txt', n=10):
    '''Build Markov chain from training file, and generate n words of output
    training_file: source text on which to train the bot
    n: number of words of output to generate
    '''
    with open('tweets/tweets.txt', 'r') as f:
        words = generate_next_word_graph(f)

    for sentence in islice(output_stream(words), n):
        print(sentence, end=' ')

if __name__ == '__main__':
    from clize import run
    run(main)
