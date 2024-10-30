import re
from fuzzywuzzy import fuzz
from collections import defaultdict
import spacy

# Load Spacy model for extracting tokens and lemmatization
nlp = spacy.load("en_core_web_sm")

# Function to compute similarity using Levenshtein distance
def is_similar(name1, name2, threshold=0.8):
    return fuzz.ratio(name1, name2) >= threshold

# Extract keywords using SpaCy, ignoring order/punctuation
def extract_keywords(names):
    keywords = {}
    for name in names:
        doc = nlp(name.lower())
        # 
        tokens = [token.lemma_ for token in doc if not token.is_stop and token.pos_ in {"NOUN", "PROPN", "ADJ"} ]
        keywords[name] = sorted(tokens)
    return keywords

def contains_all(list1, list2):
    return set(list2).issubset(set(list1)) or set(list1).issubset(set(list2))

# Merge similar names
def aggregate_names(names):
    # Clean names and extract keywords
    newText=extract_keywords(names)

    aggregated = []  # store aggregated
    processed = set()  # track used award name

    for award, keywords in newText.items():
        if award not in processed:
            group = [award]  
            
            # find all award name have same key word
            for other_award, other_keywords in newText.items():
                if other_award != award and contains_all(other_keywords, keywords):
                    group.append(other_award)
                    processed.add(other_award)
            
            aggregated.append(group)
            processed.add(award)

    return aggregated

# # Example usage
# award_names = [
#     "Best Motion Picture, Comedy or Musical", "Best Comedy/Musical", "Best Comedy or Musical", "Best Drama"
# ]

# result = aggregate_names(award_names)
# print(result)
