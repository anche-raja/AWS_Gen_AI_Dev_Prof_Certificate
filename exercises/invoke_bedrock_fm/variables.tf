variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project tag value to apply to resources"
  type        = string
  default     = "AWS_Gen_AI_Dev_Prof_Certificate"
}

variable "lambda_function_name" {
  description = "Name of the Lambda function that invokes Bedrock"
  type        = string
  default     = "invoke-bedrock-fm"
}

variable "model_id" {
  description = "Bedrock model ID to invoke"
  type        = string
  default     = "amazon.nova-reel-v1:0"
}

variable "lambda_timeout_seconds" {
  description = "Lambda timeout in seconds"
  type        = number
  default     = 30
}

variable "video_bucket_name" {
  description = "S3 bucket to store generated videos"
  type        = string
  default     = "gen-ai-exercise-dp01"
}


