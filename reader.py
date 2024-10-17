import json
from tweet import Tweet
from user import User

if __name__ == "__main__":
    JSON_FILE = "gg2013.json"

    users = {}
    tweets = {}

    with open(JSON_FILE) as file:
        tweets_json = json.load(file)
        for tweet_dict in tweets_json:
            ## Tweet is dict with keys "text", "user", "id", "timestamp_ms"

            raw_text = tweet_dict["text"]
            user_name = tweet_dict["user"]["screen_name"]
            user_id = tweet_dict["user"]["id"]
            tweet_id = tweet_dict["id"]
            timestamp_ms = tweet_dict["timestamp_ms"]


            ## Create User if non-existent             
            if users.get(user_id) == None:
                users[user_id] = User(user_name, user_id)
            
            tweet = Tweet(raw_text, users[user_id], tweet_id, timestamp_ms)
            tweets[tweet_id] = tweet

    print(tweets[tweet_dict["id"]].clean_text)
    
