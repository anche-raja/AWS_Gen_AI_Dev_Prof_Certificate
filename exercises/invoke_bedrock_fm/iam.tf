data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda_role" {
  name               = "${var.lambda_function_name}-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json

  tags = {
    Project   = var.project_name
    Terraform = "true"
  }
}

data "aws_iam_policy_document" "lambda_policy" {
  statement {
    sid     = "AllowCloudWatchLogs"
    effect  = "Allow"
    actions = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["arn:aws:logs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:*"]
  }

  statement {
    sid     = "AllowBedrockStartAsyncInvokeOnModel"
    effect  = "Allow"
    actions = ["bedrock:StartAsyncInvoke"]
    resources = ["arn:aws:bedrock:${var.aws_region}::foundation-model/${var.model_id}"]
  }

  statement {
    sid     = "AllowBedrockInvokeOnAsyncResource"
    effect  = "Allow"
    actions = ["bedrock:InvokeModel"]
    resources = ["arn:aws:bedrock:us-east-1:284244381060:async-invoke/*",
                "arn:aws:bedrock:us-east-1::foundation-model/*"]
  }
  statement {
    sid     = "AllowS3WriteVideoOutputs"
    effect  = "Allow"
    actions = [
      "s3:PutObject",
      "s3:AbortMultipartUpload",
      "s3:ListBucket",
      "s3:GetObject"
    ]
    resources = [
      "arn:aws:s3:::${var.video_bucket_name}",
      "arn:aws:s3:::${var.video_bucket_name}/*"
    ]
  }
}

resource "aws_iam_role_policy" "lambda_inline" {
  name   = "${var.lambda_function_name}-policy"
  role   = aws_iam_role.lambda_role.id
  policy = data.aws_iam_policy_document.lambda_policy.json
}

data "aws_caller_identity" "current" {}


