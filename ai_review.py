import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None


def review_match(record_a, record_b, scores, overall_score):
    if client is None:
        return "Skipped", "OpenAI API key not configured"

    prompt = f"""
Compare these two records and decide if they are likely the same person.

Record A:
{json.dumps(record_a, default=str)}

Record B:
{json.dumps(record_b, default=str)}

Field scores:
{json.dumps(scores, default=str)}

Overall score: {overall_score}

Return only JSON in this format:

{{
    "decision": "Likely Match", "Uncertain", or "Likely Different",
    "reason": "short explanation"
}}
"""

    try:
        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        result = json.loads(response.output_text)

        return result["decision"], result["reason"]

    except Exception as error:
        return "Error", str(error)


