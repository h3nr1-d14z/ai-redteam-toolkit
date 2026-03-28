Analyze Android application: $ARGUMENTS

1. **Decompile**: Extract APK with apktool (resources/smali), decompile with jadx (Java source)
2. **Manifest analysis**: Review permissions, exported components (activities, services, receivers, providers), deep links, backup flag
3. **Secrets hunt**: Search for hardcoded API keys, credentials, URLs, tokens, encryption keys in source and resources
4. **Storage**: Check SharedPreferences, SQLite databases, internal/external storage for sensitive data
5. **Network security**: Analyze network_security_config.xml, certificate pinning implementation, cleartext traffic
6. **Native libraries**: List .so files, check for known vulnerable libraries, analyze JNI calls
7. **Root/tamper detection**: Identify detection mechanisms, plan bypass strategy with Frida

Tools: jadx, apktool, androguard, dex2jar, MobSF
Save analysis to `mobile/android/<app>/analysis.md`
