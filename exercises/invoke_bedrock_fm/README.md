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

---

## Asynchronous invocation (start-async-invoke) ⏳
Use when you don’t need a synchronous response (e.g., video generation). This Lambda already uses async for the video path. You can also:
- Submit job via default action (video_generate)
- Check status by invoking with:
  - `{"action":"async_status","invocationArn":"<arn from submit>"}`

CLI example (check status):
```bash
aws lambda invoke \
  --function-name invoke-bedrock-fm \
  --payload '{"action":"async_status","invocationArn":"<PUT_INVOCATION_ARN_HERE>"}' \
  --cli-binary-format raw-in-base64-out \
  /dev/stdout | jq
```

IAM reminders:
- Role needs `bedrock:StartAsyncInvoke` on the foundation-model ARN
- Role needs `bedrock:InvokeModel`/`bedrock:GetAsyncInvoke` on `arn:aws:bedrock:<region>:<account>:async-invoke/<model_id>`
- Bucket policy must allow Bedrock service to `s3:PutObject` with `bucket-owner-full-control`

---

## Batch invocation (create-model-invocation-job) 📦
Processes many records in parallel from S3 (JSONL input) and writes outputs to S3. Use Lambda actions instead of inline code:
- Submit job:
  - `{"action":"batch_submit","roleArn":"<job role>","inputS3Uri":"s3://bucket/path/data.jsonl","outputS3Uri":"s3://bucket/path/","modelId":"<model-id-optional>","jobName":"optional-name"}`
- Check status:
  - `{"action":"batch_status","jobArn":"<returned job arn>"}`

Model input (JSONL) example to upload to your S3 input location (each line is one InvokeModel request body):
```json
{"input":{"messages":[{"role":"user","content":[{"text":"You are a triage assistant. Classify the urgency: 'Login not working for multiple users'"}]}]}}
{"input":{"messages":[{"role":"user","content":[{"text":"You are a triage assistant. Classify the urgency: 'UI alignment issue on settings page'"}]}]}}
{"input":{"messages":[{"role":"user","content":[{"text":"You are a triage assistant. Classify the urgency: 'Payment gateway returns 500 intermittently'"}]}]}}
```

Alternate JSONL format (recordId + modelInput) also supported by Bedrock batch jobs. Each line should be a compact version of an object like this:
```json
{
  "recordId": "CALL0000001",
  "modelInput": {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": [
          { "type": "text", "text": "Summarize the following call transcript: ..." }
        ]
      }
    ]
  }
}
```

CLI examples:
- Submit:
```bash
aws lambda invoke \
  --function-name invoke-bedrock-fm \
  --payload '{"action":"batch_submit","roleArn":"arn:aws:iam::<ACCOUNT_ID>:role/bedrock-batch-role","inputS3Uri":"s3://my-input-bucket/path/data.jsonl","outputS3Uri":"s3://my-output-bucket/path/","modelId":"anthropic.claude-3-haiku-20240307-v1:0","jobName":"support-ticket-batch"}' \
  --cli-binary-format raw-in-base64-out \
  /dev/stdout | jq
```

- Status:
```bash
aws lambda invoke \
  --function-name invoke-bedrock-fm \
  --payload '{"action":"batch_status","jobArn":"<PUT_JOB_ARN_HERE>"}' \
  --cli-binary-format raw-in-base64-out \
  /dev/stdout | jq
```

Batch job IAM (job role):
- Trust: `bedrock.amazonaws.com`
- Access: `s3:GetObject` on input prefix, `s3:PutObject` on output prefix
- Inference: `bedrock:InvokeModel` (and `bedrock:InvokeModelWithResponseStream` if used)


