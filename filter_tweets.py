import re
from tweet import Tweet

def filter_tweets(data):
    tweets = []
    with open('regexes/all_regexes.txt', 'r') as file:
        # regexes = file.readlines()
        regexes = [re.compile(r.replace("[AWARD NAME]", "(.+)").strip(), re.IGNORECASE) for r in file]
    for tweet in data:
        # regex = r.replace("[AWARD NAME]", "(.+)")
        # remove \n
        # regex = regex[0:-1]
        # for tweet in data:
        #     match = re.search(regex, tweet.clean_text, re.IGNORECASE)
        #     if match:
        #         tweets.append(tweet)
        if any(regex.search(tweet.clean_text) for regex in regexes):
            tweets.append(tweet)
    return tweets