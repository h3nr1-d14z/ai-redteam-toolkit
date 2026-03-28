Analyze iOS application: $ARGUMENTS

1. **Extract**: Decrypt IPA if needed (frida-ios-dump), unzip and examine bundle contents
2. **Binary analysis**: Check PIE, ARC, stack canaries, encryption (otool/rabin2), list classes and methods
3. **Plist review**: Analyze Info.plist for URL schemes, ATS exceptions, permissions, exported UTIs
4. **Secrets hunt**: Search for hardcoded keys, certificates, API endpoints in binary strings and resources
5. **Storage**: Check Keychain usage, NSUserDefaults, CoreData/SQLite, cached files, cookies
6. **Network**: Identify API endpoints, check for certificate pinning, ATS configuration
7. **Runtime analysis**: Plan Frida/Objection hooks for auth bypass, jailbreak detection bypass

Tools: otool, class-dump, frida-ios-dump, Objection, MobSF
Save analysis to `mobile/ios/<app>/analysis.md`
