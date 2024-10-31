from ftfy import fix_text
from unidecode import unidecode
from nltk.stem import WordNetLemmatizer as wnl
## TODO: confirm nltk data is downloaded as needed
import datetime
import re
from typing import List
from langdetect import detect


url_pattern = re.compile(r"\b(https?://)?(www\.)?([a-zA-Z0-9-]+\.[a-zA-Z]{2,})([\w\.\_\-/]*)*/?\b")
hashtag_pattern = re.compile(r"#[A-Za-z0-9_]+")
username_pattern = re.compile(r"@[A-Za-z0-9_]+")
word_split_pattern = re.compile(r"((?<=[a-z])(?=[A-Z]))|((?<=[A-Za-z])(?=[0-9]))|((?<=[0-9])(?=[A-Za-z]))|(?<=[A-Za-z0-9])_+(?=[A-Za-z0-9])")


def clean_text(text: str) -> str:
    return lemmatize(remove_urls(remove_whitespace(replace_non_ascii(replace_html_chars(text)))))

## Clean up HTML special characters
def replace_html_chars(text: str) -> str:
    return fix_text(text)

## Replace non-ascii character with ascii
def replace_non_ascii(text: str) -> str:
    return unidecode(text)

## TODO: What to do with URLs?

## Clean up whitespace
def remove_whitespace(text: str) -> str:
    return " ".join(text.split())

## Lemmatize text
def lemmatize(text: str) -> str:
    return wnl().lemmatize(text)

def remove_urls(text: str) -> str:
    return re.sub(url_pattern, "", text)

def replace_hashtags_usernames(text: str) -> (str, List[str], List[str]):

    hashtags = re.findall(hashtag_pattern, text)
    usernames = re.findall(username_pattern, text)

    for hashtag in hashtags:
        stripped_hashtag = hashtag.strip("#_")
        parts = re.split(word_split_pattern, stripped_hashtag)
        parts = filter(lambda part: part != None and part != "", parts)
        split_hashtag = " ".join(parts)
        text = re.sub(hashtag, split_hashtag, text)
    
    for username in usernames:
        stripped_username = username.strip("@_")
        parts = re.split(word_split_pattern, stripped_username)
        parts = filter(lambda part: part != None and part != "", parts)
        split_username = " ".join(parts)
        text = re.sub(username, split_username, text)

    return [text, hashtags, usernames]

def is_english_text(text: str) -> bool:
    try: 
        lang = detect(text)
    except:
        print(text)
        lang = "<unk>"

    return lang == "en"



## read timestamps into a DateTime object
def timestamp_to_datetime(timestamp_ms: int):
    return datetime.datetime.fromtimestamp(timestamp_ms/1000.0)

