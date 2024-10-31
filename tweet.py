import user
import datetime
import preprocess
from typing import List

class Tweet:
    clean_text: str
    posted_by: str
    tweet_id: int
    timestamp: datetime.datetime
    retweeted_by: List[str]
    hashtags: List[str]

    def __init__(self, clean_text, poster_name, id, timestamp):
        self.clean_text = clean_text
        self.posted_by = poster_name
        self.tweet_id = id
        self.timestamp = timestamp
        self.retweeted_by = []
        self.retweets = 0
        self.hashtags = []

    def add_retweet_from(self, screen_name: str):
        self.retweeted_by.append(screen_name)
        self.retweets += 1




