Bypass SSL certificate pinning on: $ARGUMENTS

1. **Identify pinning**: Determine pinning method — OkHttp CertificatePinner, TrustManager, NSURLSession, AFNetworking, custom implementation
2. **Generic bypass**: Try universal Frida scripts (objection, frida-android-unpinning) first
3. **Platform-specific**:
   - Android: Hook TrustManagerImpl.checkTrustedRecursive, OkHttp CertificatePinner.check, WebViewClient.onReceivedSslError
   - iOS: Hook SecTrustEvaluate, NSURLSessionDelegate, AFSecurityPolicy
4. **Custom bypass**: If generic fails, identify the specific pinning class and write targeted Frida hook
5. **Network config**: For Android, patch network_security_config.xml to trust user certificates
6. **Proxy setup**: Configure Burp/mitmproxy certificate on device, verify interception works
7. **Document**: Save working bypass script to `mobile/frida-scripts/ssl-pinning-bypass-<app>.js`

Tools: Frida, Objection, apktool (for repacking), mitmproxy/Burp Suite
