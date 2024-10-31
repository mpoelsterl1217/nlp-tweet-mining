import json
from tweet import Tweet
from user import User
import preprocess
from collections import defaultdict
import re
import datetime

def read_tweet_data(json_file: str):
    tweets = []
    tweets_by_user = defaultdict(list)

    with open(json_file) as file:
        tweets_json = json.load(file)

    ## Read in all tweets and do basic preprocessing
    for tweet_dict in tweets_json:
        raw_text = tweet_dict["text"]
        user_name = tweet_dict["user"]["screen_name"]
        tweet_id = tweet_dict["id"]
        timestamp_ms = tweet_dict["timestamp_ms"]

        clean_text = preprocess.clean_text(raw_text)
        timestamp_dt = preprocess.timestamp_to_datetime(timestamp_ms)

        tweet = Tweet(clean_text, user_name, tweet_id, timestamp_dt)
        tweets.append(tweet)
        tweets_by_user[user_name].append(tweet)

    ## Handle retweet matching 
    retweet_pattern = r"RT ?@([A-Za-z0-9_]+):(.*)$"
    for tweet in tweets:
        tweet_text = tweet.clean_text
        match = re.search(retweet_pattern, tweet_text)
        if match != None: ## We are dealing with a retweet
            user_name = match.group(1)
            original_tweet_text = match.group(2).strip()
            possible_original_tweets = list(filter(lambda t: original_tweet_text == t.clean_text, tweets_by_user[user_name]))
            if len(possible_original_tweets) == 0:
                original_tweet = Tweet(original_tweet_text, user_name, None, None)
                tweets.append(original_tweet)
                tweets_by_user[user_name].append(original_tweet)
            elif len(possible_original_tweets) == 1:
                original_tweet = possible_original_tweets[0]
            else: 
                raise Exception("reader.py: Found more than 2 original tweets")

            original_tweet.add_retweet_from(user_name)
            tweets.remove(tweet)
            tweets_by_user[tweet.posted_by].remove(tweet)

    ## strip hashtags and @-mentions
    for tweet in tweets:
        tweet_text = tweet.clean_text
        new_text, hashtags, mentions = preprocess.replace_hashtags_usernames(tweet_text)
        tweet.clean_text = new_text
        tweet.hashtags = hashtags

    tweets = list(filter(lambda tweet: tweet.clean_text != "", tweets))

    ## remove non-english tweets
    # print(len(tweets))
    # for tweet in tweets:
    #     if not preprocess.is_english_text(tweet.clean_text):
    #         tweets.remove(tweet)
    # print(len(tweets))
    
    return tweets


if __name__ == "__main__":
    JSON_FILE = "gg2013.json"

    tweets = read_tweet_data(JSON_FILE)
    
