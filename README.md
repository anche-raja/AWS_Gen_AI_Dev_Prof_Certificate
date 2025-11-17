# AWS_Gen_AI_Dev_Prof_Certificate
Hands-on exercises for Amazon's GenAI Developer Professional Certificate, using Terraform to manage infrastructure.

## Prerequisites
- Terraform >= 1.5
- AWS CLI configured (profile, env vars, or SSO)
- Permissions to create S3, DynamoDB, IAM, Lambda, and Bedrock invoke

## Repository layout
- `exercises/terraform_state/` – Bootstrap stack for Terraform remote state (S3 + DynamoDB)
- `exercises/invoke_bedrock_fm/` – Lambda that invokes Amazon Bedrock (async video), plus S3 bucket for outputs

## 1) Bootstrap Terraform remote state
Creates a versioned, encrypted S3 bucket and a DynamoDB table for Terraform state locking.

```bash
cd exercises/terraform_state
terraform init
terraform apply \
  -var 's3_bucket_name=<your-unique-bucket-name>' \
  -var 'aws_region=us-east-1'
```

Outputs:
- `state_bucket` – S3 bucket name for remote state
- `lock_table` – DynamoDB lock table
- `region` – Region for backend

In other stacks, configure the backend via a `backend.hcl` file:

```hcl
bucket         = "<state_bucket_output>"
key            = "global/terraform.tfstate"
region         = "<region_output>"
dynamodb_table = "<lock_table_output>"
encrypt        = true
```

Then initialize with:

```bash
terraform init -backend-config=backend.hcl
```

## 2) Invoke Bedrock foundation model (async video)
Provisions:
- IAM role with least-privilege access to submit async jobs to a specific model and write to CloudWatch Logs
- S3 bucket `gen-ai-exercise-dp01` for video outputs
- Lambda `invoke-bedrock-fm` that calls `amazon.nova-reel-v1:0` asynchronously and writes outputs to S3

Deploy:

```bash
cd exercises/invoke_bedrock_fm
terraform init -backend-config=backend.hcl
terraform apply -auto-approve
```

Invoke the Lambda:

```bash
aws lambda invoke \
  --function-name invoke-bedrock-fm \
  --payload '{"prompt":"A person dancing on a mountain."}' \
  --cli-binary-format raw-in-base64-out \
  /dev/stdout | jq
```

Outputs are stored in:
- `s3://gen-ai-exercise-dp01/video/`

### Notes
- Ensure your account has access to the Bedrock model `amazon.nova-reel-v1:0` in `us-east-1`.
- The S3 bucket policy allows the Bedrock service to write objects with `bucket-owner-full-control`.
- Lambda environment:
  - `MODEL_ID` (default `amazon.nova-reel-v1:0`)
  - `VIDEO_BUCKET` (default `gen-ai-exercise-dp01`)
- IAM least-privilege highlights:
  - `bedrock:StartAsyncInvoke` on the specific foundation model ARN
  - `bedrock:InvokeModel` on the account’s async-invoke resource for the model

