# Insurance Claim Processing PoC 🏥📄

Automate processing of claim documents to reduce manual effort and improve consistency using Amazon Bedrock.

## Step 1. Design the architecture (Skill 1.1.1)

```mermaid
flowchart LR
    A[User] -->|Upload| B[S3: claim-documents-poc-<init>]
    B --> C[Processing Workflow (Python app)]
    C --> D[Amazon Bedrock (Foundation Models)]
    C --> E[(Policy Knowledge - simple RAG)]
    D --> F[Response Generation (Summary + Extracted Fields)]
    E --> C
    F --> G[Store/Return Results]
```

- Document storage: Amazon S3
- Processing workflow: Python application (upload, validate, invoke models, generate responses)
- Foundation model integration: Amazon Bedrock
- Response generation: JSON extraction + human-readable summary

Model selection (examples; tune as needed):
- Document understanding: `amazon.nova-micro-v1:0` (messages API)
- Information extraction: `amazon.nova-micro-v1:0` with structured prompt
- Summary generation: `amazon.nova-micro-v1:0` concise summary prompt

## Step 2. Implement proof-of-concept (Skill 1.1.2)

Set up AWS environment:

```bash
aws s3 mb s3://claim-documents-poc-<your-initials>
```

Run the Python app:

```bash
cd exercises/claim_processing_poc
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

export AWS_REGION=us-east-1
export TEXT_MODEL_ID=amazon.nova-micro-v1:0

# Upload and process a sample claim (summarize + extract)
python -m app.main \
  --bucket claim-documents-poc-<your-initials> \
  --file sample_docs/claim1.txt \
  --policies policies/policy_snippets.json
```

Outputs:
- S3 upload path for the document
- Extracted fields (JSON)
- Summary text (includes simple RAG context)

## Step 3. Create reusable components (Skill 1.1.3)

This PoC includes standardized components:
- Prompt template manager: `app/prompt_templates.py`
- Model invoker: `app/model_invoker.py`
- Basic content validator: `app/validator.py`
- Simple RAG retriever: `app/rag.py`

## Step 4. Test and evaluate

- Test with 2–3 sample documents (`sample_docs/`)
- Compare different models by setting `TEXT_MODEL_ID`
- Document findings in this README (below)

### Notes and recommendations
- For PDFs/scans, add Amazon Textract to extract text before model invocation.
- For stronger RAG, replace keyword overlap with embeddings/vector search.
- Log prompts and responses (redact PII) for reproducibility/tuning.


