import re
import spacy
from spacy.matcher import Matcher
from collections import defaultdict
from reader import read_tweet_data
from tweet import Tweet

def identify_awards(tweets):
    with open('regexes/award_regexes.txt', 'r') as file:
        print("reading...")
        regexes = file.readlines()
    nlp = spacy.load("en_core_web_sm")
    final_awards = defaultdict(int)

    matcher = Matcher(nlp.vocab)

    award_pattern1 = [
        {"LOWER": "best"},                     # "best" (case insensitive)
        {"IS_ALPHA": True, "IS_TITLE": True, "OP": "+"},  # One or more title-case words (suggesting formality)
        {"TEXT": {"REGEX": "[-–—]"}},                # Punctuation, like "--" or "-"
        {"IS_ALPHA": True, "IS_TITLE": True, "OP": "+"},   # More formal terms, like role/category/year
        {"POS": "PROPN", "OP": "!"}  # Exclude proper nouns (like names) that follow
    ]
    award_pattern2 = [
        {"LOWER": "best"},    # adjective (e.g., "Best", "Outstanding")
        {"POS": "NOUN", "OP": "+"},    # noun (e.g., "Actress", "Picture")
        {"POS": "PROPN", "OP": "!"}  # Exclude proper nouns (like names) that follow
    ]
    award_pattern3 = [
        {"LOWER": "best"},    # adjective (e.g., "Best", "Outstanding")
        {"POS": "NOUN", "OP": "+"},    # noun (e.g., "Actress", "Picture")
        {"LOWER": "in a"},
        {"POS": "PROPN", "OP": "!"}  # Exclude proper nouns (like names) that follow
    ]

    # TODO: keep in /

    matcher.add("AWARD_NAME1", [award_pattern1])
    matcher.add("AWARD_NAME2", [award_pattern2])
    matcher.add("AWARD_NAME3", [award_pattern3])

    for r in regexes:
        regex = r[0:-1]
        g = regex[:regex.find("[AWARD NAME]")].count("(.+)")
        regex = regex.replace("[AWARD NAME]", "(.+)")
        print(regex, g+1)
        for tweet in tweets.values():
            match = re.search(regex, tweet.clean_text, re.IGNORECASE)
            if match:
                potential_award = match.group(g + 1)
                # print(potential_award)
                doc = nlp(tweet.clean_text)
                # award_entities = [ent.text for ent in doc.ents if ent.label_ in {'PROPN'}]
                matches = matcher(doc)
                # TODO: keep longest
                for match_id, start, end in matches:
                    span = doc[start:end]
                    # award_names.append(span.text)
                    print(span.text)
                    final_awards[span.text] += scoring("", tweet)
                # for award in award_entities:
                #         if award in potential_award:
                #             print(award)
                #             matches[award] += scoring(potential_award, tweet)
    print(dict(sorted(final_awards.items(), key=lambda item: item[1], reverse=True)))
    return(matches)


def scoring(name, tweet):
    if "RT @" in tweet.clean_text:
        return 5
    return 1

tweets = read_tweet_data("gg2013.json")[0]
identify_awards(tweets)