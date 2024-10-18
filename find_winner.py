import re
import spacy
from collections import defaultdict
from reader import read_tweet_data
from tweet import Tweet

# TODO: we'll need to run this on many versions of an award name and aggregate
def identify_winner(award_name, nominees):
    with open('winner_regexes.txt', 'r') as file:
        # read regex line and get rid of \n at the end
        print("reading...")
        regexes = file.readlines()
    nlp = spacy.load("en_core_web_sm")
    matches = defaultdict(int)
    json = "gg2013.json"
    tweets, _ = read_tweet_data(json)
    for regex in regexes:
        regex = regex.replace("[AWARD NAME]", award_name)
        for tweet in tweets.values():
            match = re.search(regex, tweet.clean_text, re.IGNORECASE)
            if match:
                # print("match")
                potential_name = match.group(1)
                doc = nlp(tweet.clean_text)
                people = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']
                for person in people:
                    if person in potential_name:
                        matches[person] += scoring(potential_name, tweet)
    # SEE WHICH OF THEM MATCH THE NOMINEE LIST
    print(dict(sorted(matches.items(), key=lambda item: item[1], reverse=True)))
    return(matches)
    # return a dictionary with counts of each of them

# need a function to aggregate dictionary of counts of potential names into a likely actual winner name
# consider connecting these to the actual tweets so we can determine reliability and weighting
# fuzzywuzzy can help aggregate

def scoring(name, tweet):
    if "RT @" in tweet.clean_text:
        return 5
    return 1

# def aggregate_names(names):
identify_winner("best actress", [])