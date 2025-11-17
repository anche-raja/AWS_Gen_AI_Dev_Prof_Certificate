# Invoke Bedrock FM (Terraform + Lambda) 🎥🧠

Provision a Lambda and IAM role to invoke Amazon Bedrock (async video), using a shared S3/DynamoDB backend state. Also supports text generation (sync) and streaming.

## Backend
Configured via `backend.hcl`:
- 🪣 bucket: `tf-state-genai-dev-prof-certificate`
- 📇 table: `terraform-locks-genai-dev-prof-certificate`
- 🌎 region: `us-east-1`

## Deploy
```bash
cd exercises/invoke_bedrock_fm
terraform init -backend-config=backend.hcl
terraform apply -auto-approve
```

## Variables
- `aws_region` (default `us-east-1`)
- `model_id` (default `amazon.nova-reel-v1:0`) – video
- `text_model_id` (default `amazon.nova-micro-v1:0`) – text
- `lambda_function_name` (default `invoke-bedrock-fm`)
- `lambda_timeout_seconds` (default `30`)
- `video_bucket_name` (default `gen-ai-exercise-dp01`)

## Invoke examples
- Video (default action):
```bash
aws lambda invoke \
  --function-name invoke-bedrock-fm \
  --payload '{"prompt":"A person dancing on a mountain."}' \
  --cli-binary-format raw-in-base64-out \
  /dev/stdout | jq
```

- Text (sync):
```bash
aws lambda invoke \
  --function-name invoke-bedrock-fm \
  --payload '{"action":"text_generate","prompt":"Rewrite this sentence for a formal tone: You are very good at your job."}' \
  --cli-binary-format raw-in-base64-out \
  /dev/stdout | jq
```

- Text (streaming):
```bash
aws lambda invoke \
  --function-name invoke-bedrock-fm \
  --payload '{"action":"text_stream","prompt":"Tell me what types of dances people do."}' \
  --cli-binary-format raw-in-base64-out \
  /dev/stdout | jq
```

> 🔒 Note: Ensure your account has access to the models in `us-east-1`. The S3 bucket policy grants `bucket-owner-full-control` for Bedrock writes.

If you need a different model, update `-var "model_id=..."`/`-var "text_model_id=..."` during apply or adjust Lambda env vars.


