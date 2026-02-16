import datetime
import os
import json
import time
import csv
import openai 
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Validate API key presence
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("Missing OPENAI_API_KEY. Set it in .env or environment variables.")

# Define OpenAI client (lee OPENAI_API_KEY del entorno)
client = openai.OpenAI()

# Pricing for GPT-4o-mini model (per 1 million tokens)
PRICING = {
    "input": 0.15,
    "output": 0.60
}

def calculate_estimated_cost(prompt_tokens, completion_tokens):
    """Calculate estimated cost in USD based on token usage."""
    input_cost = (prompt_tokens / 1_000_000) * PRICING["input"]
    output_cost = (completion_tokens / 1_000_000) * PRICING["output"]
    return round(input_cost + output_cost, 6)


def load_prompt_template():
    """Load the main prompt template from disk."""
    prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/main_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as file:
        return file.read().strip()
    
def build_prompt(template, user_prompt):
    """Combine the template with user input to create the final prompt."""
    return f"{template}\n\n##User Input:\n{user_prompt}\n\n## Output\n"

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
        "response": response_json
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    # Save metrics to CSV
    metrics_dir = os.path.join(os.path.dirname(__file__), '../metrics')
    os.makedirs(metrics_dir, exist_ok=True)
    
    metrics_file = os.path.join(metrics_dir, 'metrics.csv')
    
    # Calculate estimated cost
    estimated_cost = calculate_estimated_cost(metrics["prompt_tokens"], metrics["completion_tokens"])
    
    # Prepare metrics row
    metrics_row = {
        "timestamp": metrics["timestamp"],
        "tokens_prompt": metrics["prompt_tokens"],
        "tokens_completion": metrics["completion_tokens"],
        "total_tokens": metrics["total_tokens"],
        "latency_ms": metrics["latency_ms"],
        "estimated_cost_usd": estimated_cost
    }

    # Write to CSV
    file_exists = os.path.isfile(metrics_file)
    with open(metrics_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=metrics_row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(metrics_row)
    
    return output_file, metrics_file

# main
if __name__ == "__main__":
    user_prompt = get_user_input()
    print("Proceeding with query...")
    try:
        template = load_prompt_template()
        full_prompt = build_prompt(template, user_prompt)
    except FileNotFoundError:
        print("Warning: main_prompt.txt not found. Using raw user input.")
        full_prompt = user_prompt

    answer, total_tokens, prompt_tokens, completion_tokens, latency_ms = query_openai_api(full_prompt)

    # Parse response to JSON
    response_json = parse_response_to_json(answer)

    # Prepare metrics
    metrics = {
        "timestamp": datetime.datetime.now().timestamp(),
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
