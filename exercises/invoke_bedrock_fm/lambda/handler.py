import boto3
import json
import os
import random

bedrock_runtime = boto3.client("bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1"))
bedrock = boto3.client(service_name="bedrock", region_name=os.environ.get("AWS_REGION", "us-east-1"))
s3 = boto3.client("s3")


def lambda_handler(event, context):
    action = (event or {}).get("action", "video_generate")
    if action == "text_generate":
        return _handle_text_generate(event)
    if action == "text_stream":
        return _handle_text_stream(event)
    return _handle_video_generate(event)


def _handle_video_generate(event):
    model_id = os.environ.get("MODEL_ID", "amazon.nova-reel-v1:0")
    prompt = (event or {}).get("prompt", "A person dancing on a mountain.")
    seed = random.randint(0, 2147483646)
    model_input = {
        "taskType": "TEXT_VIDEO",
        "textToVideoParams": {"text": prompt},
        "videoGenerationConfig": {
            "fps": 24,
            "durationSeconds": 6,
            "dimension": "1280x720",
            "seed": seed,
        },
    }

    bucket = os.environ.get("VIDEO_BUCKET", "gen-ai-exercise-dp01")
    output_config = {
        "s3OutputDataConfig": {
            "s3Uri": f"s3://{bucket}/video/"
        }
    }

    response = bedrock_runtime.start_async_invoke(
        modelId=model_id,
        modelInput=model_input,
        outputDataConfig=output_config,
    )

    invocation_arn = response["invocationArn"]

    return {
        "statusCode": 200,
        "action": "video_generate",
        "invocationArn": invocation_arn,
    }


def _handle_text_generate(event):
    text_model_id = os.environ.get("TEXT_MODEL_ID", "amazon.nova-micro-v1:0")
    prompt = (event or {}).get("prompt", "Rewrite this sentence in a formal tone: You are very good at your job.")
    body = {
        "schemaVersion": "messages-v1",
        "messages": [
            {"role": "user", "content": [{"text": prompt}]}
        ],
        "inferenceConfig": {"maxTokens": 500, "topK": 20, "temperature": 0.7}
    }
    response = bedrock_runtime.invoke_model(
        modelId=text_model_id,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )
    payload = response["body"].read()
    try:
        data = json.loads(payload)
    except Exception:
        data = {"raw": payload.decode("utf-8")}
    return {
        "statusCode": 200,
        "action": "text_generate",
        "modelId": text_model_id,
        "body": data,
    }


def _handle_text_stream(event):
    text_model_id = os.environ.get("TEXT_MODEL_ID", "amazon.nova-micro-v1:0")
    prompt = (event or {}).get("prompt", "Tell me what type of dances people do.")
    body = {
        "messages": [
            {"role": "user", "content": [{"text": prompt}]}
        ]
    }
    response = bedrock_runtime.invoke_model_with_response_stream(
        modelId=text_model_id,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )
    stream = response["body"]
    full_text = ""
    for event in stream:
        # Each event contains a 'chunk' with bytes
        chunk = event.get("chunk")
        if not chunk:
            continue
        chunk_bytes = chunk.get("bytes")
        if not chunk_bytes:
            continue
        try:
            decoded = chunk_bytes.decode("utf-8")
        except Exception:
            continue
        # Try to parse JSON; if it contains text fields, extract them
        try:
            obj = json.loads(decoded)
            # Attempt a few common fields
            if isinstance(obj, dict):
                # Messages schema may stream 'outputText' or similar fields
                text_part = obj.get("outputText") or obj.get("text") or ""
                if text_part:
                    full_text += text_part
                else:
                    # Fallback to raw append
                    full_text += decoded
            else:
                full_text += decoded
        except Exception:
            full_text += decoded
    return {
        "statusCode": 200,
        "action": "text_stream",
        "modelId": text_model_id,
        "body": full_text,
    }

