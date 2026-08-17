import pandas as pd
import re
import unicodedata


def clean_text(value):
    "converts value to formatted string and detects empty values"

    if pd.isna(value):
        return ""

    value = str(value)
    value = value.lower().strip().split()
    value = " ".join(value)
    

    return value

def clean_address(value):
    value = clean_text(value)

    if value == "":
        return ""

    value = re.sub(r"[^a-z0-9\s]", "", value)
    value = " ".join(value.split())

    replacements = {
        "street": "st",
        "avenue": "ave",
        "boulevard": "blvd",
        "road": "rd",
        "drive": "dr",
        "north": "n",
        "south": "s",
        "east": "e",
        "west": "w",
        "highway": "hwy",
        "apartment": "apt",

    }

    words = value.split()

    cleaned_words = []

    for word in words:
        if word in replacements:
            cleaned_words.append(replacements[word])
        else:
            cleaned_words.append(word)

    words = cleaned_words

    return " ".join(cleaned_words)

    
    

