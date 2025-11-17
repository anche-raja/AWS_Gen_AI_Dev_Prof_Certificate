# Terraform Remote State (S3 + DynamoDB) 🔐

Bootstrap a secure, versioned S3 bucket for Terraform state and a DynamoDB table for state locking for the project: `AWS_Gen_AI_Dev_Prof_Certificate`.

## What it creates
- 🪣 Encrypted S3 bucket (Versioning ON, Public Access Blocked, BucketOwnerEnforced)
- 🔏 DynamoDB lock table (`PAY_PER_REQUEST`)

> 💡 Tip: Keep state isolated in a bootstrap stack; downstream stacks reference it via `backend.hcl`.

## Prerequisites
- 🧩 Terraform >= 1.5
- 🔐 AWS credentials configured (profile, env vars, or SSO)

## Deploy
Initialize and apply (use a globally unique bucket name or the default):

```bash
cd exercises/terraform_state
terraform init
terraform apply \
  -var 's3_bucket_name=tf-state-genai-dev-prof-certificate' \
  -var 'aws_region=us-east-1'
```

✅ Outputs will display the bucket, table, and region.

## Use as backend in other stacks
Add an S3 backend to your other Terraform projects:

```hcl
terraform {
  backend "s3" {
    bucket         = "<state_bucket_output>"
    key            = "global/terraform.tfstate"
    region         = "<region_output>"
    dynamodb_table = "<lock_table_output>"
    encrypt        = true
  }
}
```

Recommended: store values in `backend.hcl` and init with:

```bash
terraform init -backend-config=backend.hcl
```

Example `backend.hcl`:

```hcl
bucket         = "<state_bucket_output>"
key            = "global/terraform.tfstate"
region         = "<region_output>"
dynamodb_table = "<lock_table_output>"
encrypt        = true
```

## Inputs
- `s3_bucket_name` – default `tf-state-genai-dev-prof-certificate`
- `aws_region` – default `us-east-1`
- `dynamodb_table_name` – default `terraform-locks-genai-dev-prof-certificate`
- `project_name` – default `AWS_Gen_AI_Dev_Prof_Certificate`
- `force_destroy` – default `false`
- `sse_kms_key_arn` – default `""` (set to use KMS SSE)

## Notes
- 🚫 The bootstrap uses local state by design; don’t add an S3 backend here.
- 🌍 Bucket names must be globally unique and DNS-compliant.


