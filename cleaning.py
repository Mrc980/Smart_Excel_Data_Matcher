import pandas as pd

def clean_text(value):
    "converts value to formatted string and detects empty values"

    if pd.isna(value):
        return ""

    value = str(value)
    value = value.lower().strip().split()
    value = " ".join(value)
    

    return value

print(clean_text("  Ottawa         Public Library  "))
print(clean_text(" "))
print(clean_text(None))
    
    

