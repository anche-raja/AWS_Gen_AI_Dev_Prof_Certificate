# Invoke Bedrock FM (Terraform + Lambda)

This stack creates a Lambda function and IAM role to invoke an Amazon Bedrock foundation model, using the shared S3/DynamoDB backend state.

## Backend
Already configured via `backend.hcl` to use:
- bucket: `tf-state-genai-dev-prof-certificate`
- table: `terraform-locks-genai-dev-prof-certificate`
- region: `us-east-1`

## Deploy
```bash
cd exercises/invoke_bedrock_fm
terraform init -backend-config=backend.hcl
terraform apply -auto-approve
```

## Variables
- `aws_region` (default `us-east-1`)
- `model_id` (default `anthropic.claude-3-haiku-20240307-v1:0`)
- `lambda_function_name` (default `invoke-bedrock-fm`)
- `lambda_timeout_seconds` (default `30`)

## Test
Invoke the Lambda with a prompt:

```bash
aws lambda invoke \
  --function-name invoke-bedrock-fm \
  --payload '{\"prompt\":\"Write a haiku about Terraform and Bedrock.\"}' \
  --cli-binary-format raw-in-base64-out \
  /dev/stdout | jq
```

If you need a different model, update `-var "model_id=..."` during apply or set the environment variable in Terraform.


