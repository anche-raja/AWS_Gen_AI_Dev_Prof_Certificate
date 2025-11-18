# AWS_Gen_AI_Dev_Prof_Certificate ✨
Hands-on exercises for learning and preparing for Amazon's GenAI Developer Professional certification, using Terraform to manage infrastructure.

![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-orange?logo=amazon-aws) ![Terraform](https://img.shields.io/badge/IaC-Terraform-7B42BC?logo=terraform) ![Language](https://img.shields.io/badge/Language-Python-3776AB?logo=python)

## Repository layout
- 📦 `exercises/terraform_state/` – Bootstrap stack for Terraform remote state (S3 + DynamoDB)
- 🎥 `exercises/invoke_bedrock_fm/` – Lambda that invokes Amazon Bedrock (async video), plus S3 bucket for outputs
- 📘 Docs:
  - Best practices and exam tips: `docs/README.md`
  - Amazon Q Developer overview: `docs/amazon-q-developer.md`

## What this repo covers
- Terraform remote state bootstrap (S3 + DynamoDB) for consistent IaC workflows
- Bedrock invocations via Lambda:
  - Async video generation (Nova Reel) with S3 output
  - Text generation (sync) and streaming (Nova Micro)
  - Async status checks and Batch invocation submissions
- Study notes:
  - Best practices, IAM least privilege, Bedrock headers/guardrails
  - Amazon Q Developer overview and Detector Library highlights

## Quick links
- Remote state setup and usage: `exercises/terraform_state/README.md`
- Bedrock Lambda usage (all commands and actions): `exercises/invoke_bedrock_fm/README.md`
- Best practices and exam tips: `docs/README.md`
- Amazon Q Developer: `docs/amazon-q-developer.md`

