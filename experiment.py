from reader import read_tweet_data
from tweet import Tweet

tweets = read_tweet_data("gg2013.json")[0]

relevant = []
for t in tweets.values():
    tweet = t.clean_text
    if "Joaquin Phoenix" in tweet:
        relevant.append(tweet)

with open('experiments/everything_with_Joaquin_Phoenix.txt', 'w') as f:
    for line in relevant:
        f.write(f"{line}\n")