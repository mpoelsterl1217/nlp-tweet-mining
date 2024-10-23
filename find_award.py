import spacy
from spacy.matcher import Matcher

from reader import read_tweet_data

def remove_substrings(input_list):
    result = []
    
    for i in range(len(input_list)):
        is_substring = False
        for j in range(len(input_list)):
            if i != j and input_list[i] in input_list[j]:
                is_substring = True
                break
        if not is_substring:
            result.append(input_list[i])
    
    return result

# Load English language model
nlp = spacy.load("en_core_web_sm")

# Initialize the Matcher
matcher = Matcher(nlp.vocab)

# Define the pattern for matching awards like "Best .... - ...."
award_pattern = [
    {"LOWER": "best"},                     # "best" (case insensitive)
    {"IS_ALPHA": True, "IS_TITLE": True, "OP": "+"},  # One or more title-case words (suggesting formality)
    {"TEXT": {"REGEX": "[-–—]"}},                # Punctuation, like "--" or "-"
    {"IS_ALPHA": True, "IS_TITLE": True, "OP": "+"}   # More formal terms, like role/category/year
]

# Add the pattern to the matcher
matcher.add("AWARD_PATTERN", [award_pattern])

# Example document containing award names
json = "gg2013.json"
tweets, _ = read_tweet_data(json)
result=[]
for tweet in tweets.values():
    doc = nlp(tweet.clean_text)
    # Apply the matcher to the document
    matches = matcher(doc)
    # Print matched spans
    for match_id, start, end in matches:
        span = doc[start:end]  # The matched span
    
        # Check the token after the punctuation
            # Find the part after the hyphen
        after_hyphen = None
        for token in doc[start:end]:
            if token.text in ['-','--']:  # Find the hyphen or dash
                after_hyphen = doc[token.i + 1:end]  # The tokens after the hyphen
                break
    
        # print(after_hyphen)
        # If there's text after the hyphen, check if it contains any PERSON entities
        if after_hyphen:
            after_hyphen_doc = nlp(after_hyphen.text)  # Re-run NER on the after-hyphen span
            # for ent in after_hyphen_doc.ents:
            #     print("Entity found after hyphen:", ent.text)
            #     print("Entity label:", ent.label_)
        
        # Check if any of the entities is a PERSON
        if after_hyphen and any(ent.label_ == "PERSON" for ent in after_hyphen_doc.ents):
            continue  # Skip if a person's name appears after the hyphen

        print("Award Found:", span.text)
        result.append(span.text)

print(remove_substrings(result))


