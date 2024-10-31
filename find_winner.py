import re
import spacy
from collections import defaultdict
from reader import read_tweet_data
from tweet import Tweet
from aggregate_similarities import aggregate_by_similarities

# TODO: we'll need to run this on many versions of an award name and aggregate
def identify_winner(award_name, nominees, tweets):
    with open('regexes/winner_regexes.txt', 'r') as file:
        # read regex line and get rid of \n at the end
        # print("reading...")
        regexes = file.readlines()
    nlp = spacy.load("en_core_web_sm")
    matches = defaultdict(int)
    labels = {'PERSON'}
    if not ("actor" in award_name or "actress" in award_name or "performance" in award_name or "director" in award_name):
        labels.add('ORG')
        labels.add('WORK_OF_ART')
    for r in regexes:
        regex = r.replace("[AWARD NAME]", award_name)[0:-1]
        regex = re.compile(regex, re.IGNORECASE)
        for tweet in tweets:
            match = re.search(regex, tweet.clean_text)
            if match:
                # print("match")
                potential_winner = match.group(1)
                doc = nlp(tweet.clean_text)
                winner_entities = [ent.text for ent in doc.ents if ent.label_ in labels]
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
    if tweet.retweets == 0:
        return 1
    return 5 * tweet.retweets

def find_winner(award_name, nominees, tweets):
    matches = identify_winner(award_name, nominees, tweets)
    # matches = aggregate_by_similarities(matches)

    # # only get the largest one
    # top_n = 1
    # top_n = min(top_n, len(matches))
    # largest_keys = [key for key, value in sorted(matches.items(), key=lambda item: item[1], reverse=True)[:top_n]]

    # return largest_keys
    if len(matches) == 0:
        return []
    else:
        filtered_matches = {k: v for k, v in matches.items() if k != "Golden Globes" or "Golden Globe"}
        winner = max(filtered_matches, key=filtered_matches.get)
        if winner in "Golden Globes" or "Golden Globe":
            winner = winner.replace("Golden Globes", "").strip()
            winner = winner.replace("Golden Globe", "").strip()
        return [winner]

# tweets = read_tweet_data("gg2013.json")[0]
# print(find_winner("best screenplay - motion picture", [], tweets))