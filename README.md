# Smart_Excel_Data_Matcher

A Python application for cleaning, comparing, and matching records across Excel datasets.

The program handles common inconsistencies such as abbreviations, formatting differences, missing values, and small spelling variations. 
It compares multiple fields, calculates similarity scores, selects the best match for each record, and exports the results to Excel.

## Features

- Reads Excel datasets using Pandas
- Cleans and normalizes names, addresses, postal codes, phone numbers, and emails
- Detects missing values and duplicate records
- Uses RapidFuzz for fuzzy text matching
- Calculates weighted similarity scores across multiple fields
- Finds the best match for each record
- Classifies matches by confidence level
- Flags differences between matched records
- Exports the final results to Excel

## Technologies Used

Python  
Pandas  
RapidFuzz  
OpenPyXL  

## Matching Logic

Each field contributes a different amount to the final score.

Name: 35%  
Address: 40%  
City: 10%  
Postal Code: 10%  
Contact Information: 5%

Results are classified using the final score.

Match: 95 or higher  
Potential Match: 85 to 94.9  
Review Needed: 70 to 84.9  
Low Confidence: below 70

## Project Structure

**cleaning.py**  
Contains the functions used to clean and normalize the dataset before matching.

**matcher.py**  
Contains the main matching and scoring logic.  
It also handles best-match selection, confidence labels, and difference flags.

**report.py**  
Exports the final matching results to an Excel file.

**sample_data/**  
Contains the sample Excel datasets used for testing.

## Example Output

The generated Excel file includes:

ID from Dataset A  
Best matching ID from Dataset B  
Name score  
Address score  
City score  
Postal code score  
Contact information score  
Overall score  
Match status  
Difference flags

## Running the Project

Install the required packages:

```
python -m pip install pandas openpyxl rapidfuzz
```

Run the program:

```
python matcher.py
```

The program creates:

```
matching_results.xlsx
```


