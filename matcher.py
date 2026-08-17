import pandas as pd
from cleaning import (
    clean_text,
    clean_address,
    clean_email,
    clean_phone,
    clean_postal_code,
    
)

df_a = pd.read_excel("sample_data/sample_data_A.xlsx")


df_b = pd.read_excel("sample_data/sample_data_B.xlsx")

def clean_dataset(df):
    df = df.copy()

    df["Clean_Name"] = df["Name"].apply(clean_text)
    df["Clean_Address"] = df["Address"].apply(clean_address)
    df["Clean_City"] = df["City"].apply(clean_text)
    df["Clean_Postal_Code"] = df["Postal_Code"].apply(clean_postal_code)
    df["Clean_Phone"] = df["Phone"].apply(clean_phone)
    df["Clean_Email"] = df["Email"].apply(clean_email)

    return df

df_a = clean_dataset(df_a)
df_b = clean_dataset(df_b)

print(df_a[["Name", "Clean_Name", "Address", "Clean_Address"]].head())