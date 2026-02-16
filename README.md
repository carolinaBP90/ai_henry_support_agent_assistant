# AI Henry Support Agent Assistant

A Python-based support agent that leverages OpenAI's GPT-4o-mini model to answer user queries with structured JSON responses and comprehensive metrics tracking.

## Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- OpenAI API key

### Installation

1. **Clone or download the project:**
```bash
cd c:\Users\Carolina\ai_henry_support_agent_assistant
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

Expected packages:
- `openai>=1.0.0`
- `python-dotenv>=0.19.0`

## Environment Variables

Create a `.env` file in the project root with:

```dotenv
OPENAI_API_KEY=your_api_key_here
```

**Important:** 
- Never commit `.env` to version control (it's in `.gitignore`)
- Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
- Keep your key confidential

## Execution Commands

### Run the support agent:
```bash
python src/run_query.py
```

The system will:
1. Prompt for user input
2. Load the prompt template from `prompts/main_prompt.txt`
3. Query OpenAI API
4. Parse response to JSON
5. Save response to `reports/`
6. Log metrics to `metrics/metrics.csv`

### Output structure after execution:
```
reports/
  └── response_1739704234.567.json    # Response artifact
metrics/
  └── metrics.csv                      # Cumulative metrics log
```

## Reproducing Metrics

### Step 1: Ensure environment is set up
```bash
# Verify .env exists and contains OPENAI_API_KEY
cat .env
```

### Step 2: Run queries
```bash
python src/run_query.py
# Enter your query when prompted
# Example: "How do I reset my password?"
```

### Step 3: Check metrics
```bash
# View metrics CSV
type metrics\metrics.csv

# Or open in Excel/spreadsheet software
```

### Step 4: Analyze results
Metrics CSV contains:
- `timestamp`: Unix timestamp of execution
- `tokens_prompt`: Input tokens used
- `tokens_completion`: Output tokens generated
- `total_tokens`: Sum of input + output
- `latency_ms`: API response time in milliseconds
- `estimated_cost_usd`: Calculated cost for this query

**Example metrics output:**
```csv
timestamp,tokens_prompt,tokens_completion,total_tokens,latency_ms,estimated_cost_usd
1739704234.567,145,89,234,1243.56,0.000087
1739704250.123,156,92
