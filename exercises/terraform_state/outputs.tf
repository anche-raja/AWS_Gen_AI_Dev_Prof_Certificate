output "state_bucket" {
  description = "Name of the S3 bucket storing Terraform state"
  value       = aws_s3_bucket.tf_state.bucket
}

output "lock_table" {
  description = "Name of the DynamoDB table used for state locking"
  value       = aws_dynamodb_table.tf_lock_table.name
}

output "region" {
  description = "AWS region for the backend"
  value       = var.aws_region
}


