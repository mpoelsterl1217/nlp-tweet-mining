from ftfy import fix_text
from unidecode import unidecode
from nltk.stem import WordNetLemmatizer as wnl
## TODO: confirm nltk data is downloaded as needed
import datetime

def clean_text(text: str) -> str:
    return lemmatize(remove_whitespace(replace_non_ascii(replace_html_chars(text))))

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

## TODO: Exclude non-English text


## TODO: convert hashtags and usernames to natural text


## read timestamps into a DateTime object
def timestamp_to_datetime(timestamp_ms: int):
    return datetime.datetime.fromtimestamp(timestamp_ms/1000.0)


## TODO: subset out dataset
    ## - No RT or QT
    ## - RT, no QT
    ## - QT, no RT
    ## - QT and RT