Perform SSRF exploitation via: $ARGUMENTS

1. **Verify SSRF**: test with httpbin.org, check scheme support (http, file, gopher, dict, s3)
2. **Cloud metadata**: AWS (169.254.169.254), GCP, Azure
3. **Internal scan**: Docker ranges (172.17.0.x, 10.0.0.x, 192.168.x.x), common ports (80, 443, 3000, 5432, 6379, 8000, 8001, 8080, 8200, 9000, 9200)
4. **Service identification**: /health, /metrics, /debug/pprof, /.env, /proc/self/environ
5. **Exfiltrate**: Prometheus metrics, storage buckets, environment variables, cloud credentials
6. **Document**: save to `engagements/<target>/findings/ssrf-exploitation.md`
