import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Validate API key presence
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("Missing OPENAI_API_KEY. Set it in .env or environment variables.")

# Define OpenAI client (lee OPENAI_API_KEY del entorno)
client = OpenAI()

def parse_response_to_json(response_text):
    """Parse the API response string to valid JSON."""
    try:
        # Try to parse the raw response
        json_response = json.loads(response_text)
        return json_response
    except json.JSONDecodeError:
        # If parsing fails, return structured error response
        return {
            "answer": response_text.strip(),
            "confidence": 0.0,
            "actions": []
        }

def query_openai_api(prompt):
    """Query the OpenAI API and return the response"""
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )
    return response.output_text.strip()

def get_user_input():
    """Prompt the user for input"""
    return input("Please enter your query: ")

# main
if __name__ == "__main__":
    user_prompt = get_user_input()
    print("Proceeding with query...")
    answer = query_openai_api(user_prompt)

    # Parse response to JSON
    response_json = parse_response_to_json(answer)

    print(f"Answer: {answer}")
