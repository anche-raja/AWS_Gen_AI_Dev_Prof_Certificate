output "lambda_function_name" {
  description = "Name of the Lambda function that can invoke Bedrock"
  value       = aws_lambda_function.invoke_bedrock.function_name
}

output "video_bucket" {
  description = "S3 bucket used to store generated videos"
  value       = aws_s3_bucket.video_bucket.bucket
}


