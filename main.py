from reader import read_tweet_data
from find_hosts import find_host
from find_nominees import find_nominees
from find_presenters import find_presenters
from find_winner import find_winner
from alternate_find_award import find_award

if __name__ == "__main__":
    JSON_FILE = "gg2013.json"

    tweets, users = read_tweet_data(JSON_FILE)

    # host = find_host(tweets)
    # print(host)

    award_list = find_award(tweets)
    print(award_list)
    award_final = []
    for i in award_list:
        award_final.append(max(i, key=len))
    print(award_final)

    # nominees = find_nominees(award,tweets)

    # winner = find_winner(award,nominees,tweets)
    
    # presenter = find_presenters(award,winner,tweets)

