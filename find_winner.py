import re
import spacy
from collections import defaultdict
from reader import read_tweet_data
from tweet import Tweet

# TODO: we'll need to run this on many versions of an award name and aggregate
def identify_winner(award_name, nominees, tweets):
    with open('regexes/winner_regexes.txt', 'r') as file:
        # read regex line and get rid of \n at the end
        print("reading...")
        regexes = file.readlines()
    nlp = spacy.load("en_core_web_sm")
    matches = defaultdict(int)
    for r in regexes:
        regex = r.replace("[AWARD NAME]", award_name)[0:-1]
        for tweet in tweets.values():
            match = re.search(regex, tweet.clean_text, re.IGNORECASE)
            if match:
                # print("match")
                potential_winner = match.group(1)
                doc = nlp(tweet.clean_text)
                winner_entities = [ent.text for ent in doc.ents if ent.label_ in {'PERSON', 'ORG', 'WORK_OF_ART'}]
                for winner in winner_entities:
                    if winner in potential_winner:
                        matches[winner] += scoring(potential_winner, tweet)
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


tweets = read_tweet_data("gg2013.json")[0]
identify_winner("best screenplay - motion picture", [], tweets)