import re
import spacy
from collections import defaultdict
from reader import read_tweet_data
from tweet import Tweet
from aggregate_similarities import aggregate_by_similarities

def identify_host(tweets):
    with open('regexes/host_regexes.txt', 'r') as file:
        # read regex line and get rid of \n at the end
        # print("reading...")
        regexes = file.readlines()
    nlp = spacy.load("en_core_web_sm")
    matches = defaultdict(int)
    for r in regexes:
        #regex = r.replace("[AWARD NAME]", award_name)[0:-1]
        regex = r[0:-1]
        regex = re.compile(regex, re.IGNORECASE)
        for tweet in tweets:
            match = re.search(regex, tweet.clean_text)
            if match:
                # print("match")
                potential_host = match.group(1)
                doc = nlp(tweet.clean_text)
                host_entities = [ent.text for ent in doc.ents if ent.label_ in {'PERSON'}]
                for host in host_entities:
                    if host in potential_host:
                        matches[host] += scoring(potential_host, tweet)
    print(dict(sorted(matches.items(), key=lambda item: item[1], reverse=True)))
    return(matches)
    # return a dictionary with counts of each of them

# need a function to aggregate dictionary of counts of potential names into a likely actual winner name
# consider connecting these to the actual tweets so we can determine reliability and weighting
# fuzzywuzzy can help aggregate

def scoring(name, tweet): 
    if tweet.retweets == 0:
        return 1
    return 5 * tweet.retweets


def find_host(tweets):
    matches = identify_host(tweets)
    matches = aggregate_by_similarities(matches)

    # only get the largest one
    top_n = 2
    top_n = min(top_n, len(matches))
    largest_keys = [key for key, value in sorted(matches.items(), key=lambda item: item[1], reverse=True)[:top_n]]

    return largest_keys

# tweets = read_tweet_data("gg2013.json")[0]
# identify_host(tweets)