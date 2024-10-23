import json
import spacy
from fuzzywuzzy import fuzz

# Load the SpaCy language model
nlp = spacy.load('en_core_web_sm')

# Function to extract person names from text
def extract_person_names(text):
    doc = nlp(text)
    persons = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']
    return persons

def extract_verb_names(text):
    doc = nlp(text)
    verbs = [token.text for token in doc if token.pos_ == 'VERB']
    return verbs


# Load the JSON file
with open('gg2013.json', 'r') as file:
    data = json.load(file)

result=[]
for idx, entry in enumerate(data):
    if idx>=10000:
        break
    text = entry['text']
    person_names = extract_person_names(text)
    if person_names :
        for i in person_names:
            if i not in result:
                result.append(i)

print(result)
print(len(result))

# one way to find different person
def find_different_people(names):
    result = []
    
    # Compare each pair in the list
    for i in range(len(names)):
        count=0
        for j in range(len(names)):
            similarity = fuzz.ratio(names[i], names[j])
            
            if similarity < 90:  # If similarity < 90%, consider them different people
                count+=1
                if count==len(names)-1:
                    result.append(names[i])
            if similarity >= 90 and i!=j:
                print(names[i]+" is same "+ names[j])
            
    return result

result=find_different_people(result)
print(result)
print(len(result))

# for entry in data:
#     text = entry['text']
#     verbs = extract_verb_names(text)
#     if verbs:
#         print(verbs)
