import spacy
from spacy.matcher import Matcher

def remove_substrings(input_list):
    # 创建一个新的列表，保存那些不是其他元素的子串的字符串
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

# Load English language model with NER
nlp = spacy.load("en_core_web_sm")

# Initialize the Matcher
matcher = Matcher(nlp.vocab)

# Define a pattern for matching awards like "Best .... -- ...." or "Best ....-...."
award_pattern = [
    {"LOWER": "best"},                                   # "best" (case insensitive)
    {"IS_ALPHA": True, "IS_TITLE": True, "OP": "+"},     # One or more title-case words describing the award
    {"TEXT": {"REGEX": "[-–—]"}},                        # Hyphen, en-dash, or em-dash (with or without spaces)
    {"IS_ALPHA": True, "IS_TITLE": True, "OP": "+"},     # Title-case words after hyphen (e.g., category, drama, etc.)
]

# Add the pattern to the matcher
matcher.add("AWARD_PATTERN", [award_pattern])

# Example text with both valid awards and invalid matches with names
doc = nlp("Best Actor - Leading Role, Best Director - 2020, Best Actor - Tom Hanks, Best Actress -- Meryl Streep, Best Actress-drama, Best Actor-leading, Best Actor -- Leading, Best Actress-Drama")

# Apply the matcher to the document
matches = matcher(doc)

result=[]
# # Iterate over matches and filter out cases where the text after '-' is a person's name
for match_id, start, end in matches:
    span = doc[start:end]  # The matched span
    string_id = nlp.vocab.strings[match_id]

    # Find the part after the hyphen
    after_hyphen = None
    for token in doc[start:end]:
        if token.text in ['-','--']:  # Find the hyphen or dash
            after_hyphen = doc[token.i + 1:end]  # The tokens after the hyphen
            break
    
    print(after_hyphen)
    # If there's text after the hyphen, check if it contains any PERSON entities
    if after_hyphen:
        after_hyphen_doc = nlp(after_hyphen.text)  # Re-run NER on the after-hyphen span
        for ent in after_hyphen_doc.ents:
            print("Entity found after hyphen:", ent.text)
            print("Entity label:", ent.label_)
        
        # Check if any of the entities is a PERSON
        if any(ent.label_ == "PERSON" for ent in after_hyphen_doc.ents):
            continue  # Skip if a person's name appears after the hyphen

    print("Award Found:", span.text)
    result.append(span.text)

print(remove_substrings(result))



