## JSON Formatting for Amazon Bedrock 📦🤖

Proper JSON formatting is **critical** for successful Amazon Bedrock API calls. This summary focuses on the key structures, model-specific schemas, and validation/debugging practices you need for the cert.

---

## 1. Bedrock request basics 🧱

Every Bedrock API request includes:
- **Model identifier** – which FM to invoke (`modelId`).
- **Request body (JSON)** – prompt/messages + parameters.
- **Headers** – `Content-Type: application/json`, SigV4 auth headers.
- **Authentication** – AWS credentials/roles with Bedrock permissions.

Core idea: **payload shape depends on the model family** (Claude vs Titan vs AI21), but you always send well‑formed JSON in the `body` field.

---

## 2. Universal JSON fields (core parameters) 🌐

Many models support a common set of parameters:

- **prompt / input text**
  ```json
  { "prompt": "Explain the benefits of cloud computing" }
  ```

- **max_tokens / maxTokenCount**
  ```json
  { "max_tokens": 500 }
  ```

- **temperature** – randomness (0.0–1.0).
  ```json
  { "temperature": 0.7 }
  ```

Optional knobs:
- `top_p` / `topP` – nucleus sampling.
- `stop_sequences` / `stopSequences` – strings where generation stops.
- `stream` – enable streaming responses.

Headers (conceptual):
```json
{
  "Content-Type": "application/json",
  "X-Amz-Date": "20240101T120000Z"
}
```

---

## 3. Model-specific JSON formats 🧬

Different model families use different JSON shapes – **memorize the patterns**.

### 3.1 Claude (Anthropic) – messages format
```json
{
  "anthropic_version": "bedrock-2023-05-31",
  "max_tokens": 1000,
  "messages": [
    { "role": "user", "content": "What are the key principles of cloud architecture?" }
  ],
  "temperature": 0.7,
  "top_p": 0.9
}
```

### 3.2 Titan – prompt + textGenerationConfig
```json
{
  "inputText": "Describe the advantages of serverless computing",
  "textGenerationConfig": {
    "maxTokenCount": 500,
    "temperature": 0.8,
    "topP": 0.9,
    "stopSequences": ["User:", "Assistant:"]
  }
}
```

### 3.3 AI21 Jurassic – rich parameter set
```json
{
  "prompt": "What are the key principles of cloud architecture?",
  "numResults": 1,
  "maxTokens": 1000,
  "temperature": 0.7,
  "topP": 0.9,
  "stopSequences": [],
  "countPenalty": { "scale": 0 },
  "presencePenalty": { "scale": 0 },
  "frequencyPenalty": { "scale": 0 }
}
```

> Exam cue: **parameter names and nesting differ by model family** – use the docs/examples for the exact schema.

---

## 4. Advanced JSON configuration ⚙️

Advanced Bedrock features are also JSON-driven:

- **System messages & context** – steer behavior and constraints.
- **Multi‑turn conversations** – send prior messages in the `messages` array.
- **Image/multimodal inputs** – model-specific fields for images + text.
- **Streaming** – `stream: true` (e.g., Claude messages):
  ```json
  {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 1000,
    "messages": [{ "role": "user", "content": "Write a detailed explanation of AWS Lambda" }],
    "stream": true
  }
  ```

---

## 5. Error handling and debugging 🧪

Common JSON/HTTP issues:
- **400 Bad Request** – malformed JSON, missing required fields.
- **413 Payload Too Large** – request exceeds limits.
- **429 Too Many Requests** – rate limiting.
- **500 Internal Server Error** – backend issues (still check your payload).

Validation strategies:
- JSON schema validation before calling Bedrock.
- Parameter/type/range checks for numeric fields.

Debugging techniques:
- Log full request/response (redact secrets).
- Use `curl`/Postman for quick manual tests.
- Implement retries with exponential backoff.
- Inspect CloudWatch logs for detailed error messages.

### JSON schema validation (conceptual)
Use libraries like `jsonschema` to validate request bodies against a schema (e.g., required `anthropic_version`, `max_tokens`, `messages` with `role` + `content`).

---

## 6. API testing & validation workflow ✅

Three layers of testing:

1. **CLI testing (curl)** – quick verification of headers + payload.
2. **Postman collections** – reusable requests per model; env vars for creds; basic assertions.
3. **Automated tests (boto3 + pytest)** – CI/CD checks that:
   - Requests return HTTP 200.
   - Response JSON has expected fields.

Comprehensive testing prevents regressions as you tweak prompts, parameters, or model IDs.

---

## 7. JSON formatting best practices (exam highlights) 📌

- Always validate JSON (schema + types + ranges) **before** sending to Bedrock.
- Externalize model parameters (max tokens, temperature, stop sequences) into config.
- Protect sensitive data in logs; avoid dumping full payloads in production logs.
- Monitor latency, error rates, payload sizes, and token usage to tune cost/perf.
- Treat JSON schema changes like API changes – version them and update tests accordingly.

---

## 8. Structured data preparation for SageMaker endpoints 📦

When you deploy foundation models behind **SageMaker endpoints**, input format and preprocessing are critical for **latency, throughput, and correctness**.

### 8.1 Supported input formats
- **JSON** – flexible key–value payloads; common for real‑time inference.
- **CSV** – structured/tabular batch jobs.
- **Protocol Buffers (Protobuf)** – efficient binary format for high‑throughput, low‑latency scenarios.

> Protobuf is ideal when you have strict performance or memory constraints and a well‑defined schema.

### 8.2 Preprocessing pipelines (text + multimodal) 🧱

Well‑designed pipelines transform raw input into **model‑ready** payloads:

- **Text processing:**
  - Clean/normalize text (strip HTML, normalize Unicode, collapse whitespace).
  - Apply case rules per model (lowercase vs preserve case).
  - Tokenize or chunk if the model expects specific lengths.

  ```python
  import re, unicodedata

  def clean_text(text: str) -> str:
      text = re.sub(r"<[^>]+>", "", text)              # remove HTML
      text = unicodedata.normalize("NFKD", text)       # normalize Unicode
      text = re.sub(r"\s+", " ", text).strip()         # normalize spaces
      return text
  ```

- **Multimodal handling:**
  - Convert images to **base64** so they can be sent in JSON alongside text.
  - Standardize image size/format as required by the model.

### 8.3 Structuring combined payloads

Example multimodal payload for a custom endpoint:

```json
{
  "inputs": {
    "text": "Describe what you see in this image",
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
  },
  "parameters": {
    "max_new_tokens": 150
  }
}
```

Effective preprocessing = **match the model’s expected schema** and **test with real samples** before production.

### 8.4 Performance optimization strategies 🚀

- **Input size management**
  - Trim irrelevant context; avoid oversized prompts/payloads.
- **Payload structure optimization**
  - Avoid deeply nested or redundant fields.
  - Use concise keys where appropriate.
- **Batch processing**
  - Use mini‑batches where the model/endpoint supports it to improve throughput.
- **Memory vs latency trade‑offs**
  - Small batches → lower memory, potentially higher overall latency.
  - Larger batches → higher throughput, more memory; tune using endpoint metrics.

### 8.5 Implementation best practices (SageMaker) ✅

- Always **validate input format against the model’s schema** before hitting production endpoints.
- Test preprocessing with **representative production samples**.
- For multimodal requests, ensure images are correctly **base64‑encoded** in JSON.
- Use CloudWatch metrics (latency, errors, invocations) to tune batch size and payload structure.



