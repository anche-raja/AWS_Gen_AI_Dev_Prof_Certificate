variable "aws_region" {
  description = "AWS region to deploy the Terraform state resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project tag value to apply to resources"
  type        = string
  default     = "AWS_Gen_AI_Dev_Prof_Certificate"
}

variable "s3_bucket_name" {
  description = "Globally unique S3 bucket name for Terraform state (must be unique across AWS)"
  type        = string
  default     = "tf-state-genai-dev-prof-certificate"
}

variable "dynamodb_table_name" {
  description = "DynamoDB table name used for Terraform state locking"
  type        = string
  default     = "terraform-locks-genai-dev-prof-certificate"
}

variable "force_destroy" {
  description = "Allow bucket to be destroyed even if not empty (use with caution)"
  type        = bool
  default     = false
}

variable "sse_kms_key_arn" {
  description = "Optional KMS key ARN for S3 bucket encryption (if empty, SSE-S3 is used)"
  type        = string
  default     = ""
}


