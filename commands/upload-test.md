Test file upload vulnerabilities on: $ARGUMENTS

1. **Baseline**: Upload allowed file types, note accepted extensions, size limits, storage location
2. **Extension bypass**: Double extensions (.php.jpg), null byte (.php%00.jpg), case variation (.pHP), alternate extensions (.phtml, .php5, .shtml)
3. **Content-Type bypass**: Modify MIME type header while keeping malicious content
4. **Magic bytes**: Prepend valid file signatures (GIF89a, PNG header) to webshells
5. **SVG/XML**: Upload SVG with embedded JavaScript (XSS) or XXE payloads
6. **Path traversal**: Manipulate filename to write outside upload directory (../../etc/cron.d/shell)
7. **Race condition**: Upload and access file before server-side validation/deletion
8. **Webshell**: If upload succeeds, verify code execution and document full chain

Tools: Burp Suite, exiftool (metadata injection), custom upload scripts
Save findings to `engagements/<target>/findings/upload-*.md`
