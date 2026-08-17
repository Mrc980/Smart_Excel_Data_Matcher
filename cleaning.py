import pandas as pd
import re


def is_missing(value):
    return pd.isna(value) or str(value).strip() == ""


def clean_text(value):
    "converts value to formatted string and detects empty values"

    if is_missing(value):
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


    return " ".join(cleaned_words)

def clean_postal_code(value):
    value = clean_text(value)
    return re.sub(r"[^a-z0-9]", "", value)

def clean_phone(value):
    if is_missing(value):

        return ""

    digits = re.sub(r"\D", "", str(value))


    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]


    return digits

def clean_email(value):
    return clean_text(value)


    
    

