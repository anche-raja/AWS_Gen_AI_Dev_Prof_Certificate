resource "aws_s3_bucket" "video_bucket" {
  bucket        = var.video_bucket_name
  force_destroy = false

  tags = {
    Project   = var.project_name
    Terraform = "true"
    Purpose   = "bedrock-video-output"
  }
}

resource "aws_s3_bucket_versioning" "video_bucket" {
  bucket = aws_s3_bucket.video_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "video_bucket" {
  bucket = aws_s3_bucket.video_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "video_bucket" {
  bucket                  = aws_s3_bucket.video_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_ownership_controls" "video_bucket" {
  bucket = aws_s3_bucket.video_bucket.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

data "aws_iam_policy_document" "video_bucket_policy" {
  statement {
    sid     = "AllowBedrockPutObjectWithBOFC"
    effect  = "Allow"
    principals {
      type        = "Service"
      identifiers = ["bedrock.amazonaws.com"]
    }
    actions = [
      "s3:PutObject"
    ]
    resources = [
      "arn:aws:s3:::${var.video_bucket_name}/*"
    ]
    condition {
      test     = "StringEquals"
      variable = "s3:x-amz-acl"
      values   = ["bucket-owner-full-control"]
    }
  }

  statement {
    sid     = "AllowBedrockAbortMultipartUpload"
    effect  = "Allow"
    principals {
      type        = "Service"
      identifiers = ["bedrock.amazonaws.com"]
    }
    actions = [
      "s3:AbortMultipartUpload"
    ]
    resources = [
      "arn:aws:s3:::${var.video_bucket_name}/*"
    ]
  }

  statement {
    sid     = "EnforceTLSRequestsOnly"
    effect  = "Deny"
    principals {
      type        = "*"
      identifiers = ["*"]
    }
    actions   = ["s3:*"]
    resources = [
      "arn:aws:s3:::${var.video_bucket_name}",
      "arn:aws:s3:::${var.video_bucket_name}/*"
    ]
    condition {
      test     = "Bool"
      variable = "aws:SecureTransport"
      values   = ["false"]
    }
  }
}

resource "aws_s3_bucket_policy" "video_bucket" {
  bucket = aws_s3_bucket.video_bucket.id
  policy = data.aws_iam_policy_document.video_bucket_policy.json
}


