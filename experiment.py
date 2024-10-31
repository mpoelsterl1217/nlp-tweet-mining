from reader import read_tweet_data
from tweet import Tweet

tweets = read_tweet_data("gg2013.json")[0]

relevant = []
i = 0
for t in tweets.values():
    tweet = t.clean_text
    if "Best Director" in tweet:
        relevant.append(tweet)
        i += 1
    if i == 1000:
        break

with open('experiments/best_director_award_experiment.txt', 'w') as f:
    for line in relevant:
        f.write(f"{line}\n")