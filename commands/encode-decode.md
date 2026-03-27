Encode or decode data: $ARGUMENTS

1. **Identify encoding**: Detect encoding type — Base64, URL encoding, HTML entities, hex, Unicode, Base32, Base58
2. **Decode chain**: Apply multiple decoding rounds if data is multi-encoded
3. **Common transformations**:
   - Base64: standard, URL-safe, padding variants
   - URL: single/double/triple encoding
   - HTML: named entities, numeric entities, hex entities
   - Unicode: UTF-8, UTF-16, \uXXXX escapes
   - Hex: \x format, 0x format, raw hex
   - Binary/Octal: for specific contexts
4. **Payload encoding**: Encode payloads to bypass WAF/filters in required format
5. **Hash generation**: If needed, generate MD5/SHA1/SHA256 hashes
6. **CyberChef recipe**: Provide equivalent CyberChef recipe for complex transformations

Tools: CyberChef, Python (base64, urllib, html modules), command-line tools
Output decoded/encoded data with explanation of each transformation step.
