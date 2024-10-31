import re
from tweet import Tweet

def filter_tweets(data):
    tweets = []
    with open('regexes/all_regexes.txt', 'r') as file:
        regexes = file.readlines()
    for r in regexes:
        regex = r.replace("[AWARD NAME]", "(.+)")
        regex = regex[0:-1]
        for tweet in data:
            match = re.search(regex, tweet.clean_text, re.IGNORECASE)
            if match:
                tweets.append(tweet)
    return tweets