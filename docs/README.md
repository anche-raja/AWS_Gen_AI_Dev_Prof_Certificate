# Best Practices and Exam Tips (Bedrock + AWS)

Use this as a quick reference for patterns and gotchas you’re likely to see on the exam or in real projects.

## Lambda packaging and environment
- Don’t set reserved Lambda env vars like `AWS_REGION`. The platform injects them; setting them causes `InvalidParameterValueException`.
- Keep model ID and output bucket in env vars (easier to change without code edits).

## Bedrock async invoke IAM (least privilege)
You typically need BOTH of these permissions:
- bedrock:StartAsyncInvoke on the specific foundation model ARN:
  - Resource: `arn:aws:bedrock:<region>::foundation-model/<model_id>`
- bedrock:InvokeModel on the async-invoke resource:
  - Resource (scoped): `arn:aws:bedrock:<region>:<account_id>:async-invoke/<model_id>`
  - If you don’t know the model at deploy time, use `async-invoke/*` (broader).

Common error and fix:
- Error: “is not authorized to perform: bedrock:InvokeModel on resource: arn:aws:bedrock:<region>:<account_id>:async-invoke/*”
  - Fix: add `bedrock:InvokeModel` on the `async-invoke` resource (plus `StartAsyncInvoke` on `foundation-model/<model_id>`).

Optional (depending on API): also include `bedrock:InvokeModelWithResponseStream` when using streaming responses.

## S3 bucket policy for Bedrock outputs
- Allow the Bedrock service principal to write objects with bucket-owner control:
  - Action: `s3:PutObject`
  - Principal: `bedrock.amazonaws.com`
  - Resource: `arn:aws:s3:::<bucket>/*`
  - Condition: `StringEquals` `s3:x-amz-acl = bucket-owner-full-control`
- If the service uses multipart uploads, allow:
  - Action: `s3:AbortMultipartUpload` on `arn:aws:s3:::<bucket>/*`
- Enforce TLS:
  - Deny `s3:*` with `Bool aws:SecureTransport = false` on bucket and objects.
- Avoid “MalformedPolicy: Conditions do not apply…” by:
  - Not attaching object-level conditions to bucket-level actions (e.g., don’t mix `ListBucket` with object ACL conditions in the same statement).
  - Splitting statements by action/resource type.

## Least privilege refinements
- Scope Bedrock permissions to exact models where possible.
- If Bedrock writes to S3 directly (via bucket policy), your Lambda usually does not need S3 write permissions—remove `s3:PutObject` from the Lambda role unless your code writes to S3.

## Troubleshooting quick hits
- Lambda “reserved keys” error: remove `AWS_REGION` (and other reserved keys) from Lambda environment.
- S3 policy “MalformedPolicy” with conditions: split object and bucket actions into separate statements and apply conditions only where valid.
- Bedrock AccessDenied on async jobs: add `bedrock:InvokeModel` on `async-invoke/<model_id>` (and `StartAsyncInvoke` on `foundation-model/<model_id>`).

## Exam-oriented reminders
- Map service-specific ARNs: Bedrock `foundation-model` (no account id) vs `async-invoke` (with account id).
- Principle of least privilege: scope actions to specific resources; avoid `*` unless necessary.
- Decode AccessDenied messages: they usually state the missing action and the exact resource ARN to allow.


