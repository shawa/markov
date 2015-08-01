# -*- coding: utf-8 -*-
from collections import defaultdict
from itertools import islice, chain
import numpy as np
import json

# ASCII Start Transmission. It's the best I can come up with
# for a sentinel 'start of sentence' marker (´・ω・`)
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
    counts = defaultdict(lambda: defaultdict(int))
    for line in text:
        words = line.split()
        word_pairs = zip(([STX] + words), words + [ETX])
        for word, next in word_pairs:
            counts[word][next] += 1
    return counts


def serialze_next_word_graph(graph):
    print(json.dumps(graph))


def sentence(word_graph):
    choices = word_graph[STX]
    next = None
    while True:
        if not choices.keys():
            choices = word_graph[STX]

        next = np.random.choice(list(choices.keys()),
                                p=normalize(choices.values()))
        if next == ETX:
            break

        choices = word_graph[next]
        yield next


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
            print(' '.join(list(sentence(words))))


if __name__ == '__main__':
    from clize import run
    run(main)
