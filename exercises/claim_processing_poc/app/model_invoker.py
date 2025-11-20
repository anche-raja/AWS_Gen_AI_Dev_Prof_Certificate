import os
import json
import boto3
from typing import Any, Dict, List


def get_bedrock_runtime():
    region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("bedrock-runtime", region_name=region)


def invoke_messages_model(messages: List[Dict[str, Any]],
                          max_tokens: int = 600,
                          temperature: float = 0.3,
                          top_k: int = 20,
                          model_id: str | None = None) -> Dict[str, Any]:
    """
    Call a Bedrock messages-style model and return parsed JSON response if possible.
    """
    runtime = get_bedrock_runtime()
    model = model_id or os.environ.get("TEXT_MODEL_ID", "amazon.nova-micro-v1:0")

    body = {
        "schemaVersion": "messages-v1",
        "messages": messages,
        "inferenceConfig": {
            "maxTokens": max_tokens,
            "temperature": temperature,
            "topK": top_k,
        },
    }

    resp = runtime.invoke_model(
        modelId=model,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json",
    )
    payload = resp["body"].read()
    try:
        return json.loads(payload)
    except Exception:
        return {"raw": payload.decode("utf-8", errors="ignore")}


