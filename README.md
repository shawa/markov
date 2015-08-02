# Markov?
A couple of scripts to play around with [Markov chain](http://blog.codinghorror.com/markov-and-you/)-based text generation.

'We' implement a Markov chain based off a training piece of text (corpus), by building a [weighted Digraph](https://en.wikipedia.org/wiki/Directed_graph).
Edges from one word to another are weighted based on how frequently they appear in the training text.
To generate text from the chain, we need only walk a trail from a start to an end token, picking the next edge at each vertex as a weighted random choice.

## Usage
Simply run `bot.py <training corpus>` to start generating (usually humorous) text from the training set.

Originally I was intending to write a twitter bot, trained on my twitter archive.
[Grab your archive](https://support.twitter.com/articles/20170160) from here,
and run `extract_tweets.sh $TWITTER_ARCHIVE_DIRECTORY > tweets.txt` (requires the marvellous [jq](http://stedolan.github.io/jq/).
Now use `tweets.txt` as the training set and see what comes out.

These are always more fun when you [mix training sets](http://kingjamesprogramming.tumblr.com),
shove a load of different sources (roughly of the same length) into one file and see what comes out.
