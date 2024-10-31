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

def contains_all(name1, group):
    # if name1 not in 
    newName1=extract_keywords([name1])
    Name1_keyword=[]
    for award, keywords in newName1.items():
        Name1_keyword=keywords
    
    newText=extract_keywords(group)
    for award, keywords in newText.items():
        if not (set(keywords).issubset(set(Name1_keyword)) or set(Name1_keyword).issubset(set(keywords))):
            return False
        
    return True

# # Merge similar names
# def aggregate_names(names):
#     # Clean names and extract keywords
#     newText=extract_keywords(names)

#     aggregated = []  # store aggregated
#     processed = set()  # track used award name

#     for award, keywords in newText.items():
#         print("current award " + award)
#         if award not in processed:
#             group = [award]  
            
#             # find all award name have same key word
#             for other_award, other_keywords in newText.items():
#                 # if other_award == "Best actress - drama":
#                 #     print(other_keywords)
#                 #     print(keywords)

#                 if other_award != award and contains_all(other_keywords, keywords):
#                     group.append(other_award)
#                     processed.add(other_award)
            
#             aggregated.append(group)
#             processed.add(award)

#     return aggregated

# Merge similar names
def aggregate_names(names):
    aggregated = []  # store aggregated
    processed = set()  # track used award name

    for award in names:
        # print("current award " + award + "!!!!!")
        if award not in processed:
            group = [award]
            # find all award name have same key word
            for other_award in names:
                if other_award != award and contains_all(other_award, group):
                    group.append(other_award)
                    processed.add(other_award)
            
            aggregated.append(group)
            processed.add(award)

    return aggregated

# Example usage
# award_names = [
#     "Best Motion Picture, Comedy or Musical", "Best Comedy/Musical", "Best Comedy or Musical", "Best Drama","Best television series - drama","Best actress - drama"
# ]

# # award_names = [
# #     "Best Drama", "Best television series - drama", "Best actress - drama"
# # ]

# result = aggregate_names(award_names)
# print(result)
