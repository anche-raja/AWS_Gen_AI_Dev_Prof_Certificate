import boto3
import json
import os
import random

bedrock_runtime = boto3.client("bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1"))
bedrock = boto3.client(service_name="bedrock", region_name=os.environ.get("AWS_REGION", "us-east-1"))
s3 = boto3.client("s3")


def lambda_handler(event, context):
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
        "invocationArn": invocation_arn,
    }


