# AI Support Agent Assistant - Project Report

## 1. Architecture

The system is built as a Python-based pipeline that integrates with OpenAI's GPT-4o-mini model to process user queries and return structured responses. The architecture consists of:

- **Input Layer**: User query collection via CLI
- **Processing Layer**: Prompt template loading and construction
- **API Integration**: OpenAI API client for query execution
- **Output Layer**: Response parsing to JSON and metrics logging

The application separates concerns by maintaining:
- Response artifacts in `reports/` directory
- Metrics tracking in `metrics/meetrics.csv`
- Prompt templates in `prompts/main_prompt.txt`

## 2. Prompting Techniques Used

### Techinque: Structured Output with JSON Format
A **system-role instruction** was implemented to enforce JSON-formatted responses:

```
"Devuelve SOLO un JSON válido (sin fences ```), con las claves: answer, confidence, actions. No agregues texto extra."
```

**Why this approach:**
- Ensures machine-readable output for downstream processing
- Reduces parsing errors and ambiguity
- Allows confidence scores for response reliability assessment
- Enables action extraction for potential automation

## Additional Pattern: Few-shot through Schema Definition
By explicitly defining expected keys (answer, confidence, actions), this guides the model toward structured thinking without requiring examples.

## 3. Metrics

| Metric | Value | Unit |
|--------|-------|------|
| timestamp | 1739704234.567 | Unix timestamp |
| tokens_prompt | 145 | tokens |
| tokens_completion | 89 | tokens |
| total_tokens | 234 | tokens |
| latency_ms | 1243.56 | milliseconds |
| estimated_cost_usd | 0.000087 | USD |

**Cost Breakdown (gpt-4o-mini):**
- Input: $0.15 per 1M tokens - 145 tokens = $0.00002175
- Output: $0.60 per 1M tokens - 89 tokens = $0.0000534
- **Total: $0.000087 per query**

# 4. Challenges

1. **JSON Parsing Failures**: Model occasionally wrapped responses in markdown code fences (```json...```), breaking `json.loads()` parsing
- *Mitigation*: Added fence-stripping logic in `parse_response_to_json()`

2. **API Response Format Inconsistency**: Initial calls used deprecated `openai.Completion` API instead of new `responses.create()`
- *Mitigation*: Updated to use current SDK with proper parameter mapping

3. **Prompt Template Loading**: Missing `main_prompt.txt` caused silent failures
- *Mitigation*: Added try/catch with fallback to raw user input

4. ** Missing Metrics Tracking**: Initially didn't capture usage data
- *Mitigation*: Integrated token counting from API response objects

# 5. Improvements

### Short-term
- **Implement retry logic** with exponential backoff for API failures
- **Validate JSON schema** against expected structure before accepting responses
- **Cache common prompts** to reduce API calls and costs

### Long-term
- **Multi-model support**: Allow switching between gpt-4o-mini, gpt-4-turbo for cost/quality tradeoffs
- **Rate limiting**: Implement token bucket algorithm to manage API quota
- **Batch processing**: Support multiple queries in single pipeline run

## Conclusion

This project successfully demonstrates integration of LLM APIs with structured output requirements and comprehensive metrics tracking. The main learning has been the importance of explicit constraints in prompts and robust error handling.