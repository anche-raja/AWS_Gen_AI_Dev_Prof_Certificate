# Terraform Remote State (S3 + DynamoDB)

This stack bootstraps a secure S3 bucket for Terraform state and a DynamoDB table for state locking, for the project: AWS_Gen_AI_Dev_Prof_Certificate.

## What it creates
- Versioned, encrypted S3 bucket (public access blocked, BucketOwnerEnforced)
- DynamoDB lock table (`PAY_PER_REQUEST`)

## Prerequisites
- Terraform >= 1.5
- AWS credentials configured (environment, profile, or SSO)

## Usage
Initialize and apply (choose a globally-unique S3 bucket name):

```bash
cd exercises/terraform_state
terraform init
terraform apply \
  -var 's3_bucket_name=<your-unique-bucket-name>' \
  -var 'aws_region=us-east-1'
```

Outputs will show the bucket, table, and region.

## Backend configuration for other stacks
After this stack is applied, configure your other Terraform projects to use the remote backend:

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

Recommended: store these values in a `backend.hcl` file and initialize with:

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
- `s3_bucket_name` (string, required): Globally unique bucket name for state
- `aws_region` (string, default `us-east-1`)
- `dynamodb_table_name` (string, default `terraform-locks`)
- `project_name` (string, default `AWS_Gen_AI_Dev_Prof_Certificate`)
- `force_destroy` (bool, default `false`)
- `sse_kms_key_arn` (string, default `""`) – if set, bucket uses KMS SSE

## Notes
- This bootstrap stack uses local state by design; do not add an S3 backend here.
- Ensure your chosen bucket name is globally unique and DNS-compliant.


