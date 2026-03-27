# AWS Cloud Security Assessment Methodology

## Phase 1: Reconnaissance and Enumeration

### External Reconnaissance
- Identify AWS usage: check DNS records for `amazonaws.com`, `cloudfront.net`, `elb.amazonaws.com`
- S3 bucket discovery: `aws s3 ls s3://company-name`, try naming conventions (company-backup, company-dev, company-assets)
- Certificate Transparency: find subdomains pointing to AWS services
- Shodan: `org:"Amazon" hostname:target.com`, search for exposed services
- Check for exposed EC2 metadata via SSRF on web applications

### Account Enumeration
- If credentials provided (grey/white box): `aws sts get-caller-identity`
- List account aliases: `aws iam list-account-aliases`
- Check organization membership: `aws organizations describe-organization`
- Identify regions in use: check CloudTrail, or enumerate services per region

### Service Discovery
- Enumerate what services are in use with provided credentials
- Key services to check: EC2, S3, Lambda, RDS, IAM, ECS, EKS, DynamoDB, SQS, SNS, API Gateway, CloudFront, Secrets Manager, SSM Parameter Store

---

## Phase 2: IAM Assessment

### User and Role Analysis
- List users: `aws iam list-users`
- List roles: `aws iam list-roles`
- List groups: `aws iam list-groups`
- List policies: `aws iam list-policies --scope Local`
- Get policy details: `aws iam get-policy-version --policy-arn <arn> --version-id <v>`

### Permission Analysis
- Enumerate current permissions: use `enumerate-iam` tool or `aws iam simulate-principal-policy`
- Check for `*:*` (admin) policies on non-admin users/roles
- Look for overly permissive policies: `s3:*`, `ec2:*`, `iam:*`
- Check for inline policies vs managed policies
- Check for unused permissions (principle of least privilege violations)

### Privilege Escalation Paths
- IAM users who can create/attach policies: `iam:CreatePolicy`, `iam:AttachUserPolicy`
- Users who can create access keys for others: `iam:CreateAccessKey`
- Users who can assume roles: check `sts:AssumeRole` and role trust policies
- Lambda privilege escalation: `lambda:CreateFunction` + `iam:PassRole` + `lambda:InvokeFunction`
- EC2 instance profile abuse: `ec2:RunInstances` + `iam:PassRole`
- CloudFormation: `cloudformation:CreateStack` + `iam:PassRole`
- Tool: `pmapper` (Principal Mapper) or `cloudsplaining` for automated analysis

### Credential Security
- Check for access keys older than 90 days: `aws iam list-access-keys --user-name <user>`
- Check for MFA enforcement: `aws iam list-mfa-devices --user-name <user>`
- Check password policy: `aws iam get-account-password-policy`
- Identify unused credentials: `aws iam generate-credential-report` then `aws iam get-credential-report`
- Check for root account usage (should have MFA, no access keys)

---

## Phase 3: S3 Bucket Security

### Bucket Discovery and Enumeration
- List all buckets: `aws s3api list-buckets`
- Check each bucket's region: `aws s3api get-bucket-location --bucket <name>`

### Bucket Policy and ACL Review
- Get bucket policy: `aws s3api get-bucket-policy --bucket <name>`
- Get bucket ACL: `aws s3api get-bucket-acl --bucket <name>`
- Check for public access: look for `Principal: "*"` or `AllUsers` grants
- Check Block Public Access settings: `aws s3api get-public-access-block --bucket <name>`

### Data Exposure Testing
- List objects: `aws s3 ls s3://bucket-name --recursive`
- Check for sensitive files: backups, credentials, database dumps, logs, PII
- Test anonymous access: `aws s3 ls s3://bucket-name --no-sign-request`
- Test cross-account access if relevant
- Check for versioning: `aws s3api get-bucket-versioning --bucket <name>` (deleted files may be recoverable)

### Encryption
- Check default encryption: `aws s3api get-bucket-encryption --bucket <name>`
- Verify objects are encrypted: `aws s3api head-object --bucket <name> --key <key>`
- Check encryption type: SSE-S3, SSE-KMS, SSE-C
- Verify KMS key policies are restrictive

### Logging
- Check access logging: `aws s3api get-bucket-logging --bucket <name>`
- Check if CloudTrail data events cover S3

---

## Phase 4: EC2 and Network Security

### EC2 Instance Review
- List instances: `aws ec2 describe-instances --query 'Reservations[].Instances[].{ID:InstanceId,Type:InstanceType,State:State.Name,IP:PublicIpAddress,Profile:IamInstanceProfile.Arn}'`
- Check instance metadata service: IMDSv1 (vulnerable to SSRF) vs IMDSv2 (token required)
  - `aws ec2 describe-instances --query 'Reservations[].Instances[].{ID:InstanceId,IMDS:MetadataOptions.HttpTokens}'`
- Check for public IPs on instances that should be internal
- Review instance profiles (IAM roles attached to EC2)
- Check user data scripts: `aws ec2 describe-instance-attribute --instance-id <id> --attribute userData` (may contain secrets)

### Security Group Review
- List security groups: `aws ec2 describe-security-groups`
- Check for overly permissive inbound rules: `0.0.0.0/0` on sensitive ports (22, 3389, 3306, 5432)
- Check for unrestricted outbound rules (data exfiltration risk)
- Look for unused security groups
- Check for security groups allowing all traffic between instances

### VPC Configuration
- List VPCs: `aws ec2 describe-vpcs`
- Check VPC flow logs: `aws ec2 describe-flow-logs`
- Review NACLs: `aws ec2 describe-network-acls`
- Check VPC peering: `aws ec2 describe-vpc-peering-connections`
- Check VPN connections: `aws ec2 describe-vpn-connections`
- Verify no public subnets have instances that should be private

### Key Pairs and SSH
- List key pairs: `aws ec2 describe-key-pairs`
- Check for SSH keys stored in S3 or Parameter Store
- Systems Manager Session Manager as SSH alternative (check configuration)

---

## Phase 5: Lambda and Serverless

### Function Enumeration
- List functions: `aws lambda list-functions`
- Get function configuration: `aws lambda get-function-configuration --function-name <name>`
- Get function code: `aws lambda get-function --function-name <name>` (download the deployment package)

### Security Review
- Check environment variables for secrets: hardcoded API keys, database credentials, tokens
- Review IAM execution role permissions (overly broad roles are common)
- Check for publicly accessible function URLs: `aws lambda get-function-url-config --function-name <name>`
- Check event source mappings: what triggers the function (API Gateway, S3, SQS)?
- Review function policies: who can invoke the function?

### Code Review
- Download and review function code for vulnerabilities
- Check for: injection vulnerabilities, insecure deserialization, hardcoded secrets
- Check dependency vulnerabilities in layers and packages
- Review timeout and memory settings (resource exhaustion)

### API Gateway
- List APIs: `aws apigateway get-rest-apis` or `aws apigatewayv2 get-apis`
- Check authentication: API keys, IAM, Cognito, Lambda authorizers
- Check for APIs without authentication
- Review resource policies and throttling
- Test each endpoint for common API vulnerabilities

---

## Phase 6: Database Security

### RDS
- List instances: `aws rds describe-db-instances`
- Check public accessibility: `PubliclyAccessible` field
- Check encryption at rest: `StorageEncrypted` field
- Check security groups: what IPs/networks can connect?
- Check for automated backups and snapshot exposure
- Check for public snapshots: `aws rds describe-db-snapshots --snapshot-type public`
- Verify SSL enforcement for connections

### DynamoDB
- List tables: `aws dynamodb list-tables`
- Check encryption: `aws dynamodb describe-table --table-name <name>`
- Check for point-in-time recovery: disaster recovery implications
- Check table policies and access controls
- Verify no table is publicly accessible via API Gateway without auth

### ElastiCache / DocumentDB / Others
- Check for instances without encryption
- Check for instances in public subnets
- Review security group rules

---

## Phase 7: Logging and Monitoring

### CloudTrail
- Check if CloudTrail is enabled in all regions: `aws cloudtrail describe-trails`
- Check for multi-region trail
- Check if log file validation is enabled
- Check if logs are encrypted with KMS
- Check S3 bucket where logs are stored (access controls)
- Verify management events and data events are logged

### CloudWatch
- Check for alarms on security-relevant events: root login, IAM changes, security group changes
- Check for log groups containing sensitive data
- Review metric filters for security monitoring

### GuardDuty
- Check if enabled: `aws guardduty list-detectors`
- Review findings: `aws guardduty list-findings --detector-id <id>`
- Check for suppressed findings that should be investigated

### Config
- Check if AWS Config is enabled: `aws configservice describe-configuration-recorders`
- Review compliance rules and non-compliant resources
- Check for config rules covering security baselines

---

## Phase 8: Additional Services

### Secrets Manager and Parameter Store
- List secrets: `aws secretsmanager list-secrets`
- List parameters: `aws ssm describe-parameters`
- Check rotation configuration for secrets
- Verify access policies are least-privilege
- Check for SecureString vs String parameters (encryption)

### ECS/EKS
- Check container definitions for hardcoded secrets in environment variables
- Review task execution roles and task roles
- Check for privileged containers
- EKS: review RBAC configuration, check for public API server endpoint
- Check for container images from untrusted registries

### SNS/SQS
- Check for public access policies on queues and topics
- Check for unencrypted messages containing sensitive data
- Review subscription configurations

### KMS
- List keys: `aws kms list-keys`
- Review key policies: who can use, manage, grant access to keys?
- Check for key rotation
- Verify keys are used where encryption is required

---

## Phase 9: Reporting

### Severity Classification
| Severity | Examples |
|---|---|
| Critical | Public S3 with sensitive data, IAM admin on all users, IMDS v1 with SSRF |
| High | Overly permissive IAM policies, public RDS, missing CloudTrail |
| Medium | Missing encryption at rest, no MFA on IAM users, outdated access keys |
| Low | Missing VPC flow logs, non-standard tagging, unused security groups |
| Info | Best practice deviations, optimization opportunities |

### Tools Quick Reference

| Task | Tools |
|---|---|
| Enumeration | aws-cli, enumerate-iam, weirdAAL |
| IAM Analysis | pmapper, cloudsplaining, Parliament, iamlive |
| S3 Audit | s3scanner, S3Scanner, bucket-finder |
| Scanning | Prowler, ScoutSuite, CloudSploit |
| Exploitation | Pacu (AWS exploitation framework) |
| Visualization | CloudMapper, Cartography |
| Compliance | Prowler (CIS benchmarks), AWS Config rules |
