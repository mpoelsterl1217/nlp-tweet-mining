import json
import spacy
from fuzzywuzzy import fuzz
from find_winner import identify_winner

# one way to find different person
def find_different_people(names):
    result = {}
    
    threshold=90
    # Process the dictionary
    for key, value in names.items():
        found = False
        for existing_key in result.keys():
            if fuzz.ratio(key.lower(), existing_key.lower()) >= threshold:
                result[existing_key] += value
                found = True
                break
        if not found:
            result[key] = value

    return result


