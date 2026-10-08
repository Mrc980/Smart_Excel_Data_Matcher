# Smart Excel Data Matcher

A Python application that automates data cleaning, comparing, and matching records across Excel datasets.

The program handles common inconsistencies such as abbreviations, formatting differences, missing values, and small spelling variations. It compares multiple fields, calculates weighted similarity scores, selects the best match for each record, and exports the results to Excel.

The application also supports optional AI-assisted review using the OpenAI API to evaluate uncertain matches and provide additional explanations.

## Features

- Reads Excel datasets using Pandas
- Cleans and normalizes names, addresses, cities, postal codes, phone numbers, and emails
- Includes functions for detecting missing values and duplicate records
- Uses RapidFuzz for fuzzy text matching
- Calculates weighted similarity scores across multiple fields
- Finds the best match for each record
- Classifies matches by confidence level
- Flags differences between matched records
- Optionally uses the OpenAI API to review low-confidence matches
- Exports matching results, similarity scores, and AI assessments to a formatted Excel file

## Technologies Used

- Python
- Pandas
- RapidFuzz
- OpenPyXL
- OpenAI API (GPT-5 mini)
- python-dotenv

## Matching Logic

Each record in Dataset A is compared against records in Dataset B.

The application calculates similarity scores across multiple fields, with each field contributing a different amount to the final score.

| Field               | Weight |
| ------------------- | ------ |
| Name                | 35%    |
| Address             | 40%    |
| City                | 10%    |
| Postal Code         | 10%    |
| Contact Information | 5%     |

The record with the highest overall similarity score is selected as the best match.

Results are classified using the final score:

| Overall Score | Match Status    |
| ------------- | --------------- |
| 95 or higher  | Match           |
| 85 to 94.9    | Potential Match |
| 70 to 84.9    | Review Needed   |
| Below 70      | Low Confidence  |

These classifications are determined by the matching algorithm, independently of AI.

## Optional AI Review

The application integrates the OpenAI API to provide an additional assessment of uncertain record matches.

AI review is automatically triggered for records classified as:

- **Review Needed:** Scores from 70 to 84.9
- **Low Confidence:** Scores below 70

For these records, the application sends the two records being compared, their individual field similarity scores, and their overall score to OpenAI's GPT-5 mini model.

The AI returns one of three assessments:

- **Likely Match**
- **Uncertain**
- **Likely Different**

It also provides a short explanation supporting its assessment.

The AI review is advisory and does not change the original similarity score, selected candidate, or match classification.

### How to Enable AI Review

AI review requires an OpenAI API key.

1. Create a file named `.env` in the project's root directory.
2. Add the following line:

`OPENAI_API_KEY=your_api_key_here`

Replace `your_api_key_here` with your actual OpenAI API key.

When a valid API key is configured, AI review runs automatically for matches scoring below 85.

### Running Without an API Key

An OpenAI API key is not required to use the main matching functionality.

If no key is configured:

- Data cleaning and fuzzy matching work normally.
- Similarity scores and confidence classifications are calculated.
- Difference flags are generated.
- AI review is skipped.
- The Excel report is still exported.

For records that qualify for AI review, the report displays:

- **AI_Review:** Skipped
- **AI_Reason:** OpenAI API key not configured

Matches scoring 85 or higher display `Not Needed` because they do not trigger AI review.

To disable AI review, remove the API key from your `.env` file or leave its value empty. The key must also be absent from the system environment.


## Project Structure

**cleaning.py**
Contains functions used to clean and normalize records before matching.

**matcher.py**
Contains the main matching and scoring logic. It handles best-match selection, confidence labels, difference flags, and optional AI review integration. It also contains helper functions for checking missing values and duplicates.

**ai_review\.py**
Handles the OpenAI API integration. It reviews uncertain matches and returns an AI assessment and explanation. If no API key is configured, the review is skipped.

**report.py**
Exports the final matching results to a formatted Excel file.

**sample_data/**
Contains sample Excel datasets used for testing.

**.env**
Stores the local OpenAI API key. This file is not included in the GitHub repository.

## Example Output

The generated Excel file includes:

- ID from Dataset A
- Name from Dataset A
- Best matching ID from Dataset B
- Best matching name from Dataset B
- Name score
- Address score
- City score
- Postal code score
- Contact information score
- Overall score
- Match status
- AI review decision
- AI review explanation
- Difference flags

The exported report includes adjusted column widths, wrapped text for longer fields, and a frozen header row.

## Running the Project

### 1. Clone the Repository

`git clone https://github.com/Mrc980/Smart_Excel_Data_Matcher.git`

Navigate into the project directory:

`cd Smart_Excel_Data_Matcher`

### 2. Install Dependencies

Install the required packages:

`python -m pip install pandas openpyxl rapidfuzz openai python-dotenv`

### 3. Configure OpenAI API (Optional)

To use AI review, create a `.env` file in the project directory containing:

`OPENAI_API_KEY=your_api_key_here`

If you do not want to use AI review, skip this step.

### 4. Run the Program

`python matcher.py`

The program reads the sample datasets from the `sample_data` directory, performs record matching, and optionally reviews uncertain matches using OpenAI.

The program creates:

`matching_results.xlsx`

The report contains the matching results and any available AI assessments.



