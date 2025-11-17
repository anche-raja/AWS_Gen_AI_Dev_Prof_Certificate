data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda"
  output_path = "${path.module}/build/lambda.zip"
}

resource "aws_lambda_function" "invoke_bedrock" {
  function_name = var.lambda_function_name
  description   = "Invokes an Amazon Bedrock foundation model"
  role          = aws_iam_role.lambda_role.arn
  handler       = "handler.lambda_handler"
  runtime       = "python3.12"
  timeout       = var.lambda_timeout_seconds
  filename      = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      MODEL_ID     = var.model_id
      VIDEO_BUCKET = var.video_bucket_name
    }
  }

  tags = {
    Project   = var.project_name
    Terraform = "true"
  }
}


