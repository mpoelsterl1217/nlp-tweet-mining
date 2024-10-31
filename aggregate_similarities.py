import json
import spacy
from fuzzywuzzy import fuzz
import re

# def update_name_keys(input_dict):
#     nlp = spacy.load("en_core_web_sm")
#     updated_dict = {}
#     for key, value in input_dict.items():
#         doc = nlp(key)
#         # Extract only the name parts (labeled as "PERSON")
#         name_parts = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
#         if name_parts:
#             # Join name parts to create the cleaned key
#             cleaned_key = " ".join(name_parts)
#             updated_dict[cleaned_key] = value
#     return updated_dict

# # one way to find different person
# def aggregate_people(names,threshold=90):
#     # double check
#     names=update_name_keys(names)

#     result = {}
#     # Process the dictionary
#     for key, value in names.items():
#         found = False
#         for existing_key in result.keys():
#             if fuzz.ratio(key.lower(), existing_key.lower()) >= threshold:
#                 result[existing_key] += value
#                 found = True
#                 break
#         if not found:
#             result[key] = value

#     return result


# one way to aggregate winner/nominees
def aggregate_by_similarities(names,threshold=90):

    names=aggragate_filter(names)

    result = {}
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
    
    # print(result)
    result=combine_subset_key(result)
    return result

def combine_subset_key(data):
    # Create a new dictionary to store combined results
    combined_data = {}

    # Loop through each key in the dictionary
    for key in data:
        # Check if the current key is a substring of any existing key in combined_data
        found_superstring = False
        for combined_key in combined_data:
            if key in combined_key:
                # Add the value to the existing longer key
                combined_data[combined_key] += data[key]
                found_superstring = True
                break
            elif combined_key in key:
                # If an existing key is a substring of the current key, merge and replace
                combined_data[key] = combined_data.pop(combined_key) + data[key]
                found_superstring = True
                break

        # If the key was not a substring of any existing key, add it to combined_data
        if not found_superstring:
            combined_data[key] = data[key]
    
    #Remove entries with "Golden Globes" in the key
    combined_data = {
        key.replace("Golden Globes", "").replace("Golden Globe", "").strip(): value
        for key, value in combined_data.items()
        if key not in ["Golden Globes", "Golden Globe"]
    }

    return combined_data

def aggragate_filter(data):
    # Regex pattern to remove "'s" at the end or any standalone "'"
    pattern = re.compile(r"'s\b|'", re.IGNORECASE)

    # Create a new dictionary with cleaned keys
    cleaned_data = {}
    for key, value in data.items():
        # Remove unwanted patterns
        cleaned_key = pattern.sub("", key)
        # Add the cleaned key and value to the new dictionary
        cleaned_data[cleaned_key.strip()] = value
    return cleaned_data

# test={
#     "Golden Globes Jack": ["Best Actor"],
#     "Golden Globe Jill": ["Best Actress"],
#     "Oscars": ["Best Picture", "Best Director"],
#     "Golden Globes": ["Best TV Series"],
#     "Golden Globe": ["Best Movie"],
#     "lol Golden Globe": ["Best"],
# }

# print(aggregate_by_similarities(test))