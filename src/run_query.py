import datetime
import os
import json
import time
import openai 
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Validate API key presence
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("Missing OPENAI_API_KEY. Set it in .env or environment variables.")

# Define OpenAI client (lee OPENAI_API_KEY del entorno)
client = openai.OpenAI()

def parse_response_to_json(response_text):
    """Parse the API response string to valid JSON."""
    if response_text is None:
        return {
            "answer": "",
            "confidence": 0.0,
            "actions": [],
            "error": "Empty response from API"
        }
    try:
        json_response = json.loads(response_text)
        return json_response
    except json.JSONDecodeError:
        return {
            "answer": response_text.strip(),
            "confidence": 0.0,
            "actions": []
        }

def query_openai_api(prompt):
    """Query the OpenAI API and return the response"""
    start_time = time.time()
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": "Devuelve SOLO un JSON válido (sin fences ```), con las claves: answer, confidence, actions. No agregues texto extra."},
            {"role": "user", "content": prompt}
        ]
    )
    end_time = time.time()
    latency_ms = (end_time - start_time) * 1000

    return response.output_text, response.usage.total_tokens, response.usage.input_tokens, response.usage.output_tokens, latency_ms

def get_user_input():
    """Prompt the user for input"""
    return input("Please enter your query: ")

def save_response_and_metrics(response_json, metrics):
    """Save the response and metrics to a file."""
    output_dir = os.path.join(os.path.dirname(__file__), '../reports')
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.datetime.now().timestamp()
    output_file = os.path.join(output_dir, f'response_{timestamp}.json')
    
    output_data = {
        "timestamp": datetime.datetime.now().timestamp(),
        "response": response_json,
        "metrics": metrics
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    return output_file

# main
if __name__ == "__main__":
    user_prompt = get_user_input()
    print("Proceeding with query...")
    answer, total_tokens, prompt_tokens, completion_tokens, latency_ms = query_openai_api(user_prompt)

    # Parse response to JSON
    response_json = parse_response_to_json(answer)

    # Prepare metrics
    metrics = {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "latency_ms": latency_ms
    }

    # Save response and metrics
    output_file = save_response_and_metrics(response_json, metrics)

    print(f"Answer: ")
    print(json.dumps(response_json, indent=2, ensure_ascii=False))
    print("Metrics: ")
    print(f"Tokens used: {total_tokens}")
    print(f"Latency: {latency_ms:.2f} ms")
    print(f"\nResponse saved to: {output_file}")
