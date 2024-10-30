import json
import spacy
from fuzzywuzzy import fuzz
from find_winner import identify_winner

def update_name_keys(input_dict):
    nlp = spacy.load("en_core_web_sm")
    updated_dict = {}
    for key, value in input_dict.items():
        doc = nlp(key)
        # Extract only the name parts (labeled as "PERSON")
        name_parts = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        if name_parts:
            # Join name parts to create the cleaned key
            cleaned_key = " ".join(name_parts)
            updated_dict[cleaned_key] = value
    return updated_dict

# one way to find different person
def aggregate_people(names):
    # double check
    names=update_name_keys(names)

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
