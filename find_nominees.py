import re
import spacy
from collections import defaultdict
from reader import read_tweet_data
from tweet import Tweet

# TODO: we'll need to run this on many versions of an award name and aggregate
def identify_nominees(award_name, tweets):
    with open('nominee_regexes.txt', 'r') as file:
        # read regex line and get rid of \n at the end
        print("reading...")
        regexes = file.readlines()
    nlp = spacy.load("en_core_web_sm")
    matches = defaultdict(int)
    for regex in regexes:
        regex = regex.replace("[AWARD NAME]", award_name)[0:-1]
        for tweet in tweets.values():
            match = re.search(regex, tweet.clean_text, re.IGNORECASE)
            if match:
                # print(tweet.clean_text)
                potential_nominees = match.group(1)
                doc = nlp(tweet.clean_text)
                nominees_entities = [ent.text for ent in doc.ents if ent.label_ in {'PERSON', 'ORG', 'WORK_OF_ART'}]
                for nominee in nominees_entities:
                    if nominee in potential_nominees:
                        matches[nominee] += scoring(potential_nominees, tweet)
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

tweets = read_tweet_data("gg2013.json")[0]
identify_nominees("best screenplay - motion picture", tweets)