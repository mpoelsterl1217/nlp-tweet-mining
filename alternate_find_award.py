import re
import spacy
from spacy.matcher import Matcher
from collections import defaultdict
from reader import read_tweet_data
from tweet import Tweet
from aggregate_award_names import aggregate_names
from aggregate_by_synonym import aggregate_awards

def identify_awards(tweets):

    with open('regexes/award_regexes.txt', 'r') as file:
        # print("reading...")
        regexes = file.readlines()

    nlp = spacy.load("en_core_web_sm")
    final_awards = defaultdict(int)
    matcher = Matcher(nlp.vocab)
    
    
    award_pattern1 = [
        {"LOWER": "best"},                     # "best" (case insensitive)
        {"IS_ALPHA": True, "IS_TITLE": True, "OP": "+"},  # One or more title-case words (suggesting formality)
        {"TEXT": {"REGEX": "[-–—]"}},                # Punctuation, like "--" or "-"
        {"IS_ALPHA": True, "IS_TITLE": True, "OP": "+"}# ,   # More formal terms, like role/category/year
    ]
    award_pattern2 = [
        {"LOWER": "best"},
        {"POS": "NOUN", "OP": "+"}# ,    # noun (e.g., "Actress", "Picture")
    ]
    award_pattern3 = [
        {"LOWER": "best"},
        {"POS": "NOUN", "OP": "+"},    # noun (e.g., "Actress", "Picture")
        {"LOWER": {"IN": ["by", "in"]}, "OP": "?"},
        {"LOWER": "a", "OP": "?"},
        {"POS": "NOUN", "OP": "?"}
    ]
    award_pattern4 = [
        {"LOWER": "best"},
        {"POS": "NOUN", "OP": "+"},    # noun (e.g., "Actress", "Picture")
        {"LOWER": {"IN": ["by", "in"]}, "OP": "?"},
        {"LOWER": "a", "OP": "?"},
        {"POS": "NOUN", "OP": "+"},
        {"TEXT": {"REGEX": "[-–—]"}},
        {"POS": "NOUN", "OP": "+"},
        {"LOWER": {"IN": ["/", "or"]}, "OP": "?"},
        {"POS": "NOUN", "OP": "?"}
    ]
    award_pattern5 = [
        {"LOWER": "best"},
        {"POS": "NOUN", "OP": "+"},    # noun (e.g., "Actress", "Picture")
        {"LOWER": {"IN": ["by", "in"]}, "OP": "?"},
        {"LOWER": "a", "OP": "?"},
        {"POS": "NOUN", "OP": "?"},
        {"TEXT": {"REGEX": "[-–—]"}},
        {"POS": "NOUN", "OP": "+"}
    ]
    award_pattern6 = [
        {"LOWER": "best"},
        {"POS": "NOUN", "OP": "+"},    # noun (e.g., "Actress", "Picture")
        {"TEXT": {"REGEX": "[-–—]"}},
        {"POS": "NOUN", "OP": "+"},
        {"LOWER": {"IN": ["/", "or"]}, "OP": "?"},
        {"POS": "NOUN", "OP": "?"}
    ]
    award_pattern7 = [
        {"LOWER": "best"},
        {"POS": "NOUN", "OP": "+"},    # noun (e.g., "Actress", "Picture")
        {"TEXT": {"REGEX": "[-–—]"}},
        {"POS": "NOUN", "OP": "+"}
    ]

    patterns = [award_pattern1, award_pattern2, award_pattern3, award_pattern4, award_pattern5, award_pattern6, award_pattern7]

    matcher.add("AWARD_NAME", patterns)
    
    '''award_patterns = [
        [
            {"LOWER": "best"},
            {"IS_ALPHA": True, "IS_TITLE": True, "OP": "+"},
            {"TEXT": {"REGEX": "[-–—]?"}},
            {"IS_ALPHA": True, "IS_TITLE": True, "OP": "*"},
        ],
        [
            {"LOWER": "best"},
            {"POS": "NOUN", "OP": "+"},
            {"TEXT": {"REGEX": "^(in|by) a$"}, "OP": "?"},
            {"POS": "NOUN", "OP": "*"},
            {"TEXT": {"REGEX": "[-–—]?(/|or)?$"}, "OP": "?"},
            {"POS": "NOUN", "OP": "*"}
        ]
    ]

    # Add all patterns under a single matcher ID
    for pattern in award_patterns:
        matcher.add("AWARD_NAME", [pattern])
    '''

    for r in regexes:
        regex = r[0:-1]
        g = regex[:regex.find("[AWARD NAME]")].count("(.+)")
        regex = regex.replace("[AWARD NAME]", "(.+)")
        regex = regex.replace("(.+)(.+)", "(.+)")
        regex = re.compile(regex, re.IGNORECASE)
        # print(regex, g+1)
        for tweet in tweets:
            match = re.search(regex, tweet.clean_text)
        # for tweet in tweets:
        #     match = re.search(regex, tweet[0:-1], re.IGNORECASE)
            if match:
                potential_award = match.group(g + 1)
                # doc = nlp(tweet.clean_text)
                # doc = nlp(tweet)
                # award_entities = [ent.text for ent in doc.ents if ent.label_ in {'PROPN'}]
                potential_award = nlp(potential_award)
                matches = matcher(potential_award)
                longest = None
                for match_id, start, end in matches:
                    # print("match whatever")
                    if longest is None or len(longest) < end - start:
                        # print("TRUE", potential_award[start:end], "THAT")
                        longest = potential_award[start:end]
                    # span = doc[start:end]
                    # award_names.append(span.text)
                    # print(span.text)
                if longest is not None:
                    # print("HEREEEEEEEEEEEEEEE")
                    final_awards[longest.text.lower()] += scoring("", tweet)
                # for award in award_entities:
                #         if award in potential_award:
                #             print(award)
                #             matches[award] += scoring(potential_award, tweet)
    print(dict(sorted(final_awards.items(), key=lambda item: item[1], reverse=True)))
    return(final_awards)


def scoring(name, tweet):
    if tweet.retweets == 0:
        return 1
    return 5 * tweet.retweets

def find_award(tweets):
    matches=identify_awards(tweets)
    # remove values smaller than 2
    threshold = 2
    filtered_matches = {key: value for key, value in matches.items() if value >= threshold}

    # matches_list=[]
    # for key, value in filtered_matches.items():
    #     matches_list.append(key)
    # aggregate_award = aggregate_names(matches_list)
    aggregate_award = aggregate_awards(filtered_matches.keys())

    return aggregate_award


# tweets = read_tweet_data("gg2013.json")[0]
# # with open('experiments/best_director_award_experiment.txt', 'r') as file:
# #         print("reading...")
# #         tweets = file.readlines()
# identify_awards(tweets)