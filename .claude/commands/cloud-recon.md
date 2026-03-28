Perform cloud infrastructure reconnaissance on: $ARGUMENTS

1. **Identify providers**: Detect AWS, GCP, Azure, DigitalOcean from DNS, headers, IP ranges
2. **S3/Storage buckets**: Enumerate buckets (naming patterns: <company>-backup, <company>-dev, <company>-assets), test permissions (list, read, write)
3. **Cloud metadata**: Check for exposed metadata endpoints, SSRF vectors to 169.254.169.254
4. **CDN/Edge**: Identify CloudFront, Cloudflare, Akamai — test for origin IP leak, cache poisoning
5. **Serverless**: Detect Lambda/Functions URLs, API Gateway endpoints
6. **IAM enumeration**: Test for misconfigured public APIs, unauthenticated access, overly permissive CORS
7. **Certificate transparency**: Search for internal hostnames in CT logs

Tools: cloud_enum, S3Scanner, awscli, gcloud, az cli
Save results to `engagements/<target>/recon/cloud-recon.md`
