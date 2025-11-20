import argparse
import json
import os
import boto3

from .model_invoker import invoke_messages_model
from .prompt_templates import build_extraction_prompt, build_summary_prompt
from .validator import validate_extraction
from .rag import load_policies, retrieve_relevant_policies, format_policy_context


def upload_to_s3(bucket: str, local_path: str, key_prefix: str = "claims/") -> str:
    s3 = boto3.client("s3")
    key = f"{key_prefix}{os.path.basename(local_path)}"
    s3.upload_file(local_path, bucket, key)
    return f"s3://{bucket}/{key}"


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def parse_model_text_output(resp: dict) -> str:
    # Try to robustly extract text from messages API style responses
    if isinstance(resp, dict):
        content = resp.get("outputText") or resp.get("content") or resp.get("raw")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = []
            for c in content:
                if isinstance(c, dict):
                    t = c.get("text") or c.get("raw")
                    if t:
                        parts.append(t)
            if parts:
                return "\n".join(parts)
    return json.dumps(resp, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="Claim Processing PoC")
    parser.add_argument("--bucket", required=True, help="S3 bucket for claim documents")
    parser.add_argument("--file", required=True, help="Local path to claim text file")
    parser.add_argument("--policies", required=True, help="Path to policy snippets JSON")
    args = parser.parse_args()

    s3_uri = upload_to_s3(args.bucket, args.file)
    claim_text = read_text(args.file)

    # Simple RAG
    all_policies = load_policies(args.policies)
    top_policies = retrieve_relevant_policies(claim_text, all_policies, k=3)
    policy_context = format_policy_context(top_policies)

    # Information extraction
    extraction_prompt = [build_extraction_prompt(claim_text)]
    extraction_resp = invoke_messages_model(extraction_prompt, max_tokens=400, temperature=0.2)
    extraction_text = parse_model_text_output(extraction_resp)

    try:
        extracted = json.loads(extraction_text)
    except Exception:
        # attempt to locate JSON in text
        try:
            start = extraction_text.index("{")
            end = extraction_text.rindex("}") + 1
            extracted = json.loads(extraction_text[start:end])
        except Exception:
            extracted = {}

    extracted_valid = validate_extraction(extracted)

    # Summary
    summary_prompt = [build_summary_prompt(claim_text, policy_context)]
    summary_resp = invoke_messages_model(summary_prompt, max_tokens=500, temperature=0.4)
    summary_text = parse_model_text_output(summary_resp)

    output = {
        "s3_uri": s3_uri,
        "extracted": extracted_valid,
        "summary": summary_text,
        "policy_context_used": policy_context,
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()


