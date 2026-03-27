# Cloud Security Lab

A simulated AWS cloud environment using LocalStack for practicing cloud security assessment and misconfiguration detection.

> **WARNING**: This lab provisions intentionally misconfigured cloud resources. The secrets and credentials in this lab are all fake/local but represent real-world patterns.

## Prerequisites

- Docker and Docker Compose
- AWS CLI v2 (`brew install awscli` or `pip install awscli`)
- `python3` (for JSON parsing in setup script)
- `curl` (for health checks)

## Quick Start

```bash
# 1. Start LocalStack
docker compose up -d

# 2. Wait ~10 seconds for services to initialize, then provision resources
./setup.sh

# 3. Verify resources exist
aws --endpoint-url=http://localhost:4566 s3 ls
aws --endpoint-url=http://localhost:4566 iam list-users
aws --endpoint-url=http://localhost:4566 lambda list-functions
aws --endpoint-url=http://localhost:4566 sqs list-queues

# 4. When done, tear down
docker compose down -v
```

## Tip: Shell Alias

To avoid typing `--endpoint-url` every time:

```bash
alias awslocal='aws --endpoint-url=http://localhost:4566 --region us-east-1 --no-sign-request'
```

## Misconfigurations to Find

There are **5 intentional misconfigurations** provisioned by `setup.sh`.

| #  | Misconfiguration                        | Difficulty | Service | What to Look For                               |
|----|-----------------------------------------|------------|---------|------------------------------------------------|
| 01 | Public S3 bucket with sensitive files   | Easy       | S3      | .env with prod creds, backup.sql, employee PII |
| 02 | S3 bucket with public read-write ACL    | Easy       | S3      | Anyone can read, write, and delete objects      |
| 03 | IAM user with admin policy              | Medium     | IAM     | An intern account with full admin access        |
| 04 | Lambda with hardcoded secrets           | Medium     | Lambda  | Secrets stored in environment variables         |
| 05 | SQS queue with public access            | Medium     | SQS     | Anyone can send, receive, and delete messages   |

## Exercises

### Exercise 1: S3 Bucket Enumeration (Easy)

Discover and enumerate all S3 buckets. Download their contents and identify sensitive data.

```bash
# List all buckets
awslocal s3 ls

# List contents of a bucket
awslocal s3 ls s3://company-public-assets/

# Download a file
awslocal s3 cp s3://company-public-assets/.env -
```

**Questions:**
- What credentials are stored in the .env file?
- What PII is exposed in employees.json?
- Can you access the backup.sql and extract password hashes?

### Exercise 2: S3 Bucket Policy Analysis (Easy)

Examine bucket policies and ACLs to identify overly permissive configurations.

```bash
# Check bucket ACL
awslocal s3api get-bucket-acl --bucket internal-reports

# Check bucket policy
awslocal s3api get-bucket-policy --bucket internal-reports

# Test if you can write to the bucket (data exfiltration vector)
echo "attacker was here" | awslocal s3 cp - s3://internal-reports/pwned.txt
awslocal s3 cp s3://internal-reports/pwned.txt -
```

**Questions:**
- What actions does the bucket policy allow?
- Who is the Principal — is it restricted to specific accounts?
- Can you delete files from the bucket?

### Exercise 3: IAM Privilege Escalation (Medium)

Analyze IAM users, their policies, and identify over-privileged accounts.

```bash
# List all IAM users
awslocal iam list-users

# List attached policies for a user
awslocal iam list-attached-user-policies --user-name dev-intern

# List inline policies
awslocal iam list-user-policies --user-name dev-intern

# Get inline policy details
awslocal iam get-user-policy --user-name dev-intern --policy-name FullAccess

# List access keys
awslocal iam list-access-keys --user-name dev-intern
```

**Questions:**
- What managed policies are attached to `dev-intern`?
- What does the inline policy allow?
- Is there any MFA configured?
- What could an attacker do with these access keys?

### Exercise 4: Lambda Secret Extraction (Medium)

Inspect Lambda functions and their configurations to find hardcoded secrets.

```bash
# List all Lambda functions
awslocal lambda list-functions

# Get function configuration (includes environment variables)
awslocal lambda get-function-configuration --function-name payment-processor

# Invoke the function
awslocal lambda invoke --function-name payment-processor /dev/stdout
```

**Questions:**
- What secrets are stored in the Lambda environment variables?
- What databases and services could an attacker access with these credentials?
- Does the Lambda function leak environment variables in its response?

### Exercise 5: SQS Message Interception (Medium)

Discover SQS queues and determine if messages can be read by unauthorized parties.

```bash
# List all queues
awslocal sqs list-queues

# Get queue attributes (including policy)
awslocal sqs get-queue-attributes \
    --queue-url http://localhost:4566/000000000000/order-processing \
    --attribute-names All

# Receive messages from the queue
awslocal sqs receive-message \
    --queue-url http://localhost:4566/000000000000/order-processing \
    --max-number-of-messages 10

# Send a rogue message (message injection)
awslocal sqs send-message \
    --queue-url http://localhost:4566/000000000000/order-processing \
    --message-body '{"order_id":"FAKE-001","customer":"attacker@evil.com","amount":0.01}'
```

**Questions:**
- What sensitive data is in the queue messages?
- Can you inject messages into the queue?
- What would the impact be if an attacker could delete messages?

## Advanced Challenges

1. **Automated Scanner**: Write a Python script that enumerates all resources and flags misconfigurations automatically.
2. **Privilege Chain**: Starting from the `dev-intern` access keys, demonstrate how an attacker could access every other misconfigured resource.
3. **Remediation Report**: For each misconfiguration, write the specific AWS CLI commands or Terraform/CloudFormation changes needed to fix it.
4. **Detection Rules**: Write CloudWatch/CloudTrail alert rules that would detect exploitation of each misconfiguration.
5. **Policy Generator**: Create least-privilege IAM policies for each resource to replace the overly permissive ones.

## Tools

Recommended tools for cloud security testing:

- **AWS CLI** -- direct API interaction
- **ScoutSuite** -- multi-cloud security auditing
- **Prowler** -- AWS security best practices assessment
- **Pacu** -- AWS exploitation framework
- **CloudMapper** -- AWS environment visualization
- **Steampipe** -- SQL-based cloud resource querying
- **trufflehog** -- secret scanning

## Cleanup

```bash
docker compose down -v
```

This removes the LocalStack container and all provisioned resources.
