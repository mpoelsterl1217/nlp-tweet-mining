from reader import read_tweet_data
from find_hosts import find_host
from find_nominees import find_nominees
from find_presenters import find_presenters
from find_winner import find_winner
from alternate_find_award import find_award
from filter_tweets import filter_tweets

if __name__ == "__main__":
    JSON_FILE = "gg2013.json"

    tweets = read_tweet_data(JSON_FILE)
    tweets = filter_tweets(tweets)
    print("tweet length:", len(tweets))

    host = find_host(tweets)
    print(host)

    award_list = find_award(tweets)
    print(award_list)
    awards_final = []
    for i in award_list:
        awards_final.append(max(i, key=len))
    print(awards_final)

    for award in awards_final:
        nominees = find_nominees(award, tweets)
        winner = find_winner(award, nominees, tweets)
        presenter = find_presenters(award, winner, tweets)

