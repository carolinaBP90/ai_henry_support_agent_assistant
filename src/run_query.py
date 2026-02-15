import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Validate API key presence
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("Missing OPENAI_API_KEY. Set it in .env or environment variables.")

# Define OpenAI client (lee OPENAI_API_KEY del entorno)
client = OpenAI()

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
    print(f"Answer: {answer}")
