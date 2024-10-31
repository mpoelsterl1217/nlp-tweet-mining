from reader import read_tweet_data
from find_hosts import find_host
from find_nominees import find_nominees
from find_presenters import find_presenters
from find_winner import find_winner
from alternate_find_award import find_award
from filter_tweets import filter_tweets
from pickle_preprocess import unpickle_tweets

if __name__ == "__main__":
    JSON_FILE = "gg2013.json"

    # tweets = read_tweet_data(JSON_FILE)
    tweets = unpickle_tweets()
    tweets = filter_tweets(tweets)
    print("tweet length:", len(tweets))

    host = find_host(tweets)
    print("hosts:", host)

    award_list = find_award(tweets)
    awards_final = []
    for i in award_list:
        awards_final.append(max(i, key=len))

    for i in range(len(award_list)):
        award = awards_final[i]
        print("\n\n")
        print("AWARD:", award)
        print("alternative names:", award_list[i])
        award_names = "(" + "|".join(award_list[i]) + ")"
        nominees = find_nominees(award_names, tweets)
        print("nominees:", nominees)
        winner = find_winner(award_names, nominees, tweets)[0]
        print("winner:", winner)
        presenter = find_presenters(award_names, winner, tweets)
        print("presenters:", presenter)

