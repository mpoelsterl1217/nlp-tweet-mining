from reader import read_tweet_data
import pickle


def pickle_tweets():
    tweets = read_tweet_data("gg2013.json")
    with open("gg2013_preprocessed.pickle", "wb") as file:
        pickle.dump(tweets, file)

def unpickle_tweets():
    with open("gg2013_preprocessed.pickle", "rb") as file:
        return pickle.load(file)


if __name__ == "__main__":
    #pickle_tweets()
    
    #tweets = unpickle_tweets()[0:10]
    #print(tweets)
    pass