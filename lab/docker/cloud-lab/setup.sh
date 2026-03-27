#!/usr/bin/env bash
# =============================================================================
# Cloud Lab Setup Script — Misconfigured AWS Resources via LocalStack
# =============================================================================
# This script provisions intentionally misconfigured cloud resources for
# practicing cloud security testing. All resources run locally in LocalStack.
#
# Prerequisites:
#   - Docker Compose running (docker compose up -d)
#   - AWS CLI v2 installed
#   - LocalStack endpoint available at http://localhost:4566
#
# Usage:
#   chmod +x setup.sh
#   ./setup.sh
# =============================================================================

set -euo pipefail

ENDPOINT="http://localhost:4566"
REGION="us-east-1"
ACCOUNT_ID="000000000000"

# AWS CLI alias pointing at LocalStack
aws_local() {
    aws --endpoint-url="$ENDPOINT" --region="$REGION" --no-sign-request "$@" 2>&1
}

echo "============================================="
echo " Cloud Security Lab — Resource Provisioning"
echo "============================================="
echo ""

# Wait for LocalStack to be ready
echo "[*] Waiting for LocalStack to be ready..."
for i in $(seq 1 30); do
    if curl -s "$ENDPOINT/_localstack/health" | grep -q '"s3": "available"'; then
        echo "[+] LocalStack is ready."
        break
    fi
    if [ "$i" -eq 30 ]; then
        echo "[-] ERROR: LocalStack did not become ready in time."
        exit 1
    fi
    sleep 2
done

echo ""
echo "==========================================="
echo " [MISCONFIG-01] Public S3 Bucket with Sensitive Files"
echo "==========================================="

# Create a bucket with public-read ACL
aws_local s3api create-bucket \
    --bucket company-public-assets \
    --acl public-read

# Upload sensitive files that should never be public
echo 'DB_HOST=prod-db.internal.company.com
DB_USER=root
DB_PASSWORD=Sup3rS3cretPr0d!
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
STRIPE_SECRET_KEY=sk_test_FAKE_KEY_FOR_LAB_ENVIRONMENT_ONLY
JWT_SECRET=production-jwt-secret-do-not-share' | \
    aws_local s3 cp - s3://company-public-assets/.env

echo '-- MySQL dump: company_prod database
-- Server version: 8.0.32

CREATE DATABASE IF NOT EXISTS company_prod;
USE company_prod;

CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  email VARCHAR(255),
  password_hash VARCHAR(255),
  api_key VARCHAR(100)
);

INSERT INTO users VALUES
(1, "admin@company.com", "$2b$12$LJ3m4ys3Lg...", "ak_prod_abc123"),
(2, "cto@company.com",   "$2b$12$Xk9d8s...",    "ak_prod_def456");' | \
    aws_local s3 cp - s3://company-public-assets/backup.sql

echo '{"employees":[
  {"name":"John Admin","email":"john@company.com","ssn":"123-45-6789","salary":150000},
  {"name":"Jane CTO","email":"jane@company.com","ssn":"987-65-4321","salary":200000}
]}' | \
    aws_local s3 cp - s3://company-public-assets/employees.json

echo "[+] Created public bucket 'company-public-assets' with .env, backup.sql, employees.json"

echo ""
echo "==========================================="
echo " [MISCONFIG-02] S3 Bucket with Overly Permissive ACL"
echo "==========================================="

aws_local s3api create-bucket \
    --bucket internal-reports \
    --acl public-read-write

echo 'Q3 Revenue: $4.2M | Projected Q4: $5.1M | Confidential' | \
    aws_local s3 cp - s3://internal-reports/financial-q3-2025.txt

echo 'Pending acquisition: TargetCorp — $50M valuation — DO NOT DISTRIBUTE' | \
    aws_local s3 cp - s3://internal-reports/ma-strategy.txt

# Apply a bucket policy that grants public access
aws_local s3api put-bucket-policy \
    --bucket internal-reports \
    --policy '{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadWrite",
                "Effect": "Allow",
                "Principal": "*",
                "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
                "Resource": "arn:aws:s3:::internal-reports/*"
            }
        ]
    }'

echo "[+] Created bucket 'internal-reports' with public read-write ACL and permissive policy"

echo ""
echo "==========================================="
echo " [MISCONFIG-03] IAM User with Admin Policy"
echo "==========================================="

# Create an IAM user with full administrator access
aws_local iam create-user --user-name dev-intern 2>/dev/null || true

# Attach the AdministratorAccess managed policy
aws_local iam attach-user-policy \
    --user-name dev-intern \
    --policy-arn "arn:aws:iam::aws:policy/AdministratorAccess"

# Create access keys for the overprivileged user
KEYS=$(aws_local iam create-access-key --user-name dev-intern 2>/dev/null || echo "already exists")
echo "[+] Created IAM user 'dev-intern' with AdministratorAccess policy"
echo "    Access keys: $KEYS"

# Also create an inline policy that is excessively broad
aws_local iam put-user-policy \
    --user-name dev-intern \
    --policy-name FullAccess \
    --policy-document '{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "*",
                "Resource": "*"
            }
        ]
    }'

echo "[+] Attached inline policy 'FullAccess' (Action: *, Resource: *) to dev-intern"

echo ""
echo "==========================================="
echo " [MISCONFIG-04] Lambda Function with Hardcoded Secrets"
echo "==========================================="

# Create a minimal Lambda deployment package
LAMBDA_DIR=$(mktemp -d)
cat > "$LAMBDA_DIR/index.py" << 'PYEOF'
import os
import json

def handler(event, context):
    """
    This Lambda has secrets in environment variables.
    An attacker with Lambda read access can extract them.
    """
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Payment processor running",
            "environment": dict(os.environ)  # Leaks all env vars in response
        })
    }
PYEOF

(cd "$LAMBDA_DIR" && zip -j function.zip index.py) > /dev/null

# Create IAM role for Lambda (required by API)
aws_local iam create-role \
    --role-name lambda-exec-role \
    --assume-role-policy-document '{
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }' 2>/dev/null || true

# Create the Lambda function with hardcoded secrets in environment variables
aws_local lambda create-function \
    --function-name payment-processor \
    --runtime python3.11 \
    --role "arn:aws:iam::${ACCOUNT_ID}:role/lambda-exec-role" \
    --handler index.handler \
    --zip-file "fileb://${LAMBDA_DIR}/function.zip" \
    --environment '{
        "Variables": {
            "STRIPE_SECRET_KEY": "sk_test_FAKE_KEY_FOR_LAB_ENVIRONMENT_ONLY",
            "DB_CONNECTION_STRING": "postgresql://admin:Pr0dP@ssw0rd!@prod-db.company.com:5432/payments",
            "ENCRYPTION_KEY": "aes-256-cbc-key-d3adb33f1337cafe",
            "SLACK_WEBHOOK": "https://hooks.slack.com/services/FAKE/WEBHOOK/FOR-LAB-ONLY",
            "INTERNAL_API_TOKEN": "eyJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiYWRtaW4ifQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        }
    }' 2>/dev/null || \
aws_local lambda update-function-configuration \
    --function-name payment-processor \
    --environment '{
        "Variables": {
            "STRIPE_SECRET_KEY": "sk_test_FAKE_KEY_FOR_LAB_ENVIRONMENT_ONLY",
            "DB_CONNECTION_STRING": "postgresql://admin:Pr0dP@ssw0rd!@prod-db.company.com:5432/payments",
            "ENCRYPTION_KEY": "aes-256-cbc-key-d3adb33f1337cafe",
            "SLACK_WEBHOOK": "https://hooks.slack.com/services/FAKE/WEBHOOK/FOR-LAB-ONLY",
            "INTERNAL_API_TOKEN": "eyJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiYWRtaW4ifQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        }
    }'

rm -rf "$LAMBDA_DIR"
echo "[+] Created Lambda 'payment-processor' with hardcoded secrets in environment variables"

echo ""
echo "==========================================="
echo " [MISCONFIG-05] SQS Queue with Public Access"
echo "==========================================="

# Create an SQS queue
QUEUE_URL=$(aws_local sqs create-queue \
    --queue-name order-processing \
    --attributes '{
        "VisibilityTimeout": "30",
        "MessageRetentionPeriod": "86400"
    }' | python3 -c "import sys,json; print(json.load(sys.stdin)['QueueUrl'])" 2>/dev/null || echo "$ENDPOINT/000000000000/order-processing")

# Set a policy that allows anyone to send/receive/delete messages
aws_local sqs set-queue-attributes \
    --queue-url "$QUEUE_URL" \
    --attributes '{
        "Policy": "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Sid\":\"PublicAccess\",\"Effect\":\"Allow\",\"Principal\":\"*\",\"Action\":[\"sqs:SendMessage\",\"sqs:ReceiveMessage\",\"sqs:DeleteMessage\",\"sqs:GetQueueAttributes\"],\"Resource\":\"*\"}]}"
    }'

# Send some sample messages with sensitive order data
aws_local sqs send-message \
    --queue-url "$QUEUE_URL" \
    --message-body '{"order_id":"ORD-9001","customer":"john@company.com","card_last4":"4242","amount":1599.99,"item":"Enterprise License"}'

aws_local sqs send-message \
    --queue-url "$QUEUE_URL" \
    --message-body '{"order_id":"ORD-9002","customer":"jane@company.com","card_last4":"1234","amount":299.00,"item":"Pro Subscription","promo_code":"INTERNAL50"}'

echo "[+] Created SQS queue 'order-processing' with public access policy"
echo "    Queue URL: $QUEUE_URL"

echo ""
echo "============================================="
echo " Setup Complete!"
echo "============================================="
echo ""
echo "Misconfigured resources:"
echo "  [01] S3 bucket 'company-public-assets' — public read, contains .env & backup.sql"
echo "  [02] S3 bucket 'internal-reports'      — public read-write with permissive policy"
echo "  [03] IAM user  'dev-intern'            — has AdministratorAccess + wildcard inline policy"
echo "  [04] Lambda    'payment-processor'     — hardcoded secrets in environment variables"
echo "  [05] SQS queue 'order-processing'      — public send/receive/delete access"
echo ""
echo "AWS CLI usage (point at LocalStack):"
echo "  export AWS_ENDPOINT_URL=$ENDPOINT"
echo "  aws --endpoint-url=$ENDPOINT s3 ls"
echo "  aws --endpoint-url=$ENDPOINT s3 cp s3://company-public-assets/.env -"
echo ""
echo "Happy hunting!"
