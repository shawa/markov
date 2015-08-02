#!/bin/sh
# Extract a Twitter archive's contents into a tweet-per-line text file
readonly TWEETS_DIR="$1/data/js/tweets"
for file in $(/bin/ls $TWEETS_DIR); do
	tail -n +2 "$TWEETS_DIR/$file" | jq -r '.[].text'
done

