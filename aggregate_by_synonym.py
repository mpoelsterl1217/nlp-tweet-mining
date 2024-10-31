from collections import defaultdict
import re

synonym_map = {
    "motion picture": "movie",
    "picture": "movie",
    "film": "movie",
    "in a": " - ",
    " – ": " - ",
    " — ": " - "
}

# Function to normalize each string by replacing synonyms
def normalize_string(text, synonyms):
    # Sort synonyms by length to replace longer terms first
    sorted_synonyms = sorted(synonyms.keys(), key=len, reverse=True)
    for term in sorted_synonyms:
        # Use regex to replace whole words only, ignoring case
        text = re.sub(rf"\b{term}\b", synonyms[term], text, flags=re.IGNORECASE)
    return text.lower()

def aggregate_awards(awards):
    # Normalize each string and store in a dictionary
    groups = defaultdict(list)
    for s in awards:
        normalized = normalize_string(s, synonym_map)
        groups[normalized].append(s)

    # # Print grouped results
    for key, group in groups.items():
        print(f"{key}: {group}")
    return groups.values()