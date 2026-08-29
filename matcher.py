import pandas as pd
from cleaning import (
    clean_text,
    clean_address,
    clean_email,
    clean_phone,
    clean_postal_code,
    is_missing
)
from rapidfuzz import fuzz

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

def find_missing_values(df, dataset_name):
    issues = []

    columns_to_check = ["Name", "Address", "City", "Postal_Code", "Phone", "Email"]

    for index, row in df.iterrows():
        for column in columns_to_check:
            if is_missing(row[column]):
                issue = {
                    "Dataset": dataset_name,
                    "ID": row["ID"],
                    "Column": column,
                    "issue": "Missing value"
                }

                issues.append(issue)

    return pd.DataFrame(issues)

def find_duplicates(df, dataset_name):
    duplicates = []

    columns_to_check = ["ID", "Clean_Email", "Clean_Phone"]

    for column in columns_to_check:
        for index, row in df.iterrows():
            value = row[column]

            if is_missing(value):
                continue

            matches = df[df[column] == value]
            if len(matches) > 1:
                record_ids = []

                for record_id in matches["ID"]:
                    record_ids.append(str(record_id))

                duplicate_info = {
                    "Dataset": dataset_name,
                    "Field": column,
                    "Value": value,
                    "Record_IDs": ", ".join(record_ids)
                }

                if duplicate_info not in duplicates:
                    duplicates.append(duplicate_info)

    return pd.DataFrame(duplicates)


def calculate_field_scores(row_a, row_b):
    name_score = fuzz.token_sort_ratio(
        row_a["Clean_Name"],
        row_b["Clean_Name"]
    )

    address_score = fuzz.token_sort_ratio(
        row_a["Clean_Address"],
        row_b["Clean_Address"]
    )

    city_score = fuzz.ratio(
        row_a["Clean_City"],
        row_b["Clean_City"]
    )

    if row_a["Clean_Postal_Code"] == row_b["Clean_Postal_Code"]:
        postal_code_score = 100
    else:
        postal_code_score = 0

    phone_score = 0
    email_score = 0

    if row_a["Clean_Phone"] != "" and row_b["Clean_Phone"] != "":
        if row_a["Clean_Phone"] == row_b["Clean_Phone"]:
            phone_score = 100

    if row_a["Clean_Email"] != "" and row_b["Clean_Email"] != "":
        email_score = fuzz.ratio(row_a["Clean_Email"], row_b["Clean_Email"])

    contact_info_score = max(phone_score, email_score)

    return {
        "Name_Score": name_score,
        "Address_Score": address_score,
        "City_Score": city_score,
        "Postal_Code_Score": postal_code_score,
        "Contact_Info_Score": contact_info_score
    }

def calculate_overall_score(scores):

    name_weight = 0.35
    address_weight = 0.40
    city_weight = 0.10
    postal_code_weight = 0.10
    contact_info_weight = 0.05

    overall_score = (
        scores["Name_Score"] * name_weight +
        scores["Address_Score"] * address_weight +
        scores["City_Score"] * city_weight +
        scores["Postal_Code_Score"] * postal_code_weight +
        scores["Contact_Info_Score"] * contact_info_weight
    )

    return round(overall_score, 1)

def get_match_status(score):
    if score >= 95:
        return "Match"
    elif score >= 85:
        return "Potential Match"
    elif score >= 70:
        return "Review Needed"
    else:
        return "Low Confidence"

def find_best_match(row_a, df_b):
    best_match = None
    best_score = -1
    best_scores = None

    for index, row_b in df_b.iterrows():
        scores = calculate_field_scores(row_a, row_b)
        overall_score = calculate_overall_score(scores)

        if overall_score > best_score:
            best_score = overall_score
            best_match = row_b
            best_scores = scores

    return best_match, best_scores, best_score

def match_all_records(df_a, df_b):
    results = []

    for index, row_a in df_a.iterrows():
        best_match, scores, overall_score = find_best_match(row_a, df_b)

        result = {
            "ID_A": row_a["ID"],
            "Name_A": row_a["Name"],

            "ID_B": best_match["ID"],
            "Name_B": best_match["Name"],

            "Name_Score": round(scores["Name_Score"], 1),
            "Address_Score": round(scores["Address_Score"], 1),
            "City_Score": round(scores["City_Score"], 1),
            "Postal_Code_Score": scores["Postal_Code_Score"],
            "Contact_Info_Score": round(scores["Contact_Info_Score"], 1),

            "Overall_Score": overall_score,
            "Match_Status": get_match_status(overall_score)
        }

        results.append(result)

    return pd.DataFrame(results)



df_a = clean_dataset(df_a)
df_b = clean_dataset(df_b)

row_a = df_a.iloc[0]
row_b = df_b.iloc[0]

scores = calculate_field_scores(row_a, row_b)

print("Field Scores:")
print(scores)

print("Overall Score:")
print(calculate_overall_score(scores))

matches = match_all_records(df_a, df_b)

print("Matching Results:")
print(matches)