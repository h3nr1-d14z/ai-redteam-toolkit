# Android Application Penetration Testing Methodology

## Phase 1: Setup and Preparation

### Environment Setup
- Android emulator (Genymotion, Android Studio AVD) or rooted physical device
- ADB installed and connected: `adb devices`
- Burp Suite / mitmproxy configured as proxy on the device
- Frida server running on device: `adb push frida-server /data/local/tmp/ && adb shell chmod 755 /data/local/tmp/frida-server`
- Objection installed: `pip install objection`
- Install target APK: `adb install target.apk`

### Obtain the APK
- From device: `adb shell pm path com.target.app` then `adb pull /path/to/base.apk`
- From Play Store: use `apkeep`, `apkpure.com`, or `evozi.com/apk-downloader`
- From client (if provided directly)
- Multiple APKs (split APKs): `adb shell pm path com.target.app` to list all, pull each

### Initial Triage
- `file target.apk` -- confirm it is a ZIP/JAR
- `aapt dump badging target.apk` -- package name, version, permissions, min SDK
- `apkanalyzer manifest print target.apk` -- full manifest review
- Note: target API level, permissions requested, exported components

---

## Phase 2: Static Analysis

### Decompilation
- jadx (recommended): `jadx -d output/ target.apk` or open in jadx-gui
- apktool (for smali): `apktool d target.apk -o output/`
- dex2jar + JD-GUI: `d2j-dex2jar target.apk` then open JAR in JD-GUI
- For native libraries: extract `lib/` directory, analyze with Ghidra or IDA

### AndroidManifest.xml Analysis
- **Exported components:** activities, services, broadcast receivers, content providers with `exported="true"`
- **Permissions:** custom permissions, dangerous permissions, protection levels
- **Backup flag:** `android:allowBackup="true"` (data extraction risk)
- **Debuggable flag:** `android:debuggable="true"` (debug access)
- **Network security config:** `android:networkSecurityConfig` -- cleartext traffic, custom trust anchors
- **Deep links and intent filters:** URL schemes, web links, app links
- **Min/target SDK:** lower SDK = fewer security features enforced

### Source Code Review
- **Hardcoded secrets:** search for API keys, tokens, passwords, encryption keys
  - `grep -rn "api_key\|apikey\|secret\|password\|token\|Bearer" --include="*.java" output/`
- **URL endpoints:** all server URLs, API base URLs, debug/staging URLs
  - `grep -rn "http://\|https://" --include="*.java" output/`
- **Cryptographic implementation:** weak algorithms (DES, MD5, ECB mode), hardcoded keys/IVs
- **SQL queries:** raw SQL with string concatenation (SQLi in local DB)
- **Logging:** sensitive data in `Log.d()`, `Log.i()`, `Log.e()` calls
- **WebView:** `setJavaScriptEnabled(true)`, `addJavascriptInterface()`, `setAllowFileAccess(true)`
- **File operations:** world-readable/writable files, external storage usage
- **Intent handling:** how intents are received and parsed (intent injection)
- **Certificate pinning:** identify pinning implementation (OkHttp, TrustManager, network_security_config.xml)

### Native Library Analysis
- List native libraries: `find output/lib/ -name "*.so"`
- Check for `JNI_OnLoad`, exported functions
- Analyze with Ghidra: look for cryptographic operations, hardcoded values, anti-tampering
- `strings libname.so | grep -i "key\|secret\|http\|url"` for quick wins

---

## Phase 3: Dynamic Analysis

### Runtime Instrumentation with Frida
- Start Frida server: `adb shell /data/local/tmp/frida-server &`
- List running processes: `frida-ps -U`
- Attach to app: `frida -U -n "App Name" -l script.js`
- Spawn app with script: `frida -U -f com.target.app -l script.js --no-pause`

### Common Frida Tasks
- **SSL pinning bypass:** use objection (`objection -g com.target.app explore` then `android sslpinning disable`)
- **Root detection bypass:** `android root disable` in objection, or custom Frida script
- **Method tracing:** `android hooking watch class com.target.app.ClassName`
- **Return value modification:** hook method and replace return value
- **Argument inspection:** log parameters to sensitive functions (login, encrypt, API calls)
- **Bypass integrity checks:** hook signature verification, checksum validation

### Objection Commands
```
# Connect
objection -g com.target.app explore

# SSL pinning bypass
android sslpinning disable

# Root detection bypass
android root disable

# List activities
android hooking list activities

# List services
android hooking list services

# Search classes
android hooking search classes <keyword>

# Hook a method
android hooking watch class_method com.target.app.Login.checkCredentials --dump-args --dump-return

# List files in app directory
env

# Dump keystore
android keystore list

# SQLite databases
sqlite connect /data/data/com.target.app/databases/app.db
```

### Debugger Attachment
- If `android:debuggable="true"`: attach with Android Studio or jdb
- If not debuggable: use Frida to achieve similar debugging capabilities
- Set breakpoints on interesting methods: login, encryption, token generation

---

## Phase 4: Traffic Analysis

### Proxy Setup
- Configure device proxy to Burp Suite: WiFi settings > proxy > manual > your IP:8080
- Install Burp CA certificate on device:
  - Android 7+: requires root or `network_security_config.xml` modification
  - Or: `apktool d app.apk`, add CA to `res/xml/network_security_config.xml`, rebuild
- For VPN-based proxy: use apps like ProxyDroid or Postern on rooted devices

### SSL Pinning Bypass
- Objection: `android sslpinning disable` (covers most cases)
- Frida script: custom hooks for OkHttp CertificatePinner, TrustManager, X509TrustManager
- apktool method: decompile, remove pinning code, recompile and sign
- Magisk + TrustMeAlready / AlwaysTrustUserCerts modules (rooted device)

### Traffic Analysis
- Map all API endpoints from traffic
- Check for sensitive data in requests/responses: tokens, PII, credentials
- Check for HTTP traffic (non-HTTPS) for any endpoints
- Test all API endpoints as documented in the API testing methodology
- Look for hardcoded tokens, API keys in request headers
- Check certificate validation: does the app accept invalid/self-signed certs without pinning bypass?

---

## Phase 5: Local Data Storage Analysis

### Shared Preferences
- Location: `/data/data/com.target.app/shared_prefs/`
- `adb shell cat /data/data/com.target.app/shared_prefs/*.xml`
- Check for: credentials, tokens, session data, PII, encryption keys
- Check if values are encrypted (and if the encryption key is hardcoded)

### SQLite Databases
- Location: `/data/data/com.target.app/databases/`
- Pull: `adb pull /data/data/com.target.app/databases/ ./`
- Open with `sqlite3` or DB Browser for SQLite
- Check for: credentials, tokens, PII, unencrypted sensitive data
- Check if SQLCipher is used (encrypted database)

### Internal Storage
- Location: `/data/data/com.target.app/files/`, `/data/data/com.target.app/cache/`
- Check file permissions: are any files world-readable?
- Look for: logs, cached credentials, temporary files, downloaded data

### External Storage
- Location: `/sdcard/Android/data/com.target.app/`
- External storage is world-readable (pre-Android 11)
- Check for sensitive data stored on external storage
- Check for files created in shared external storage locations

### Keystore / KeyChain
- Use objection: `android keystore list`
- Check if keys are hardware-backed (TEE/StrongBox)
- Check key access controls: biometric required, user authentication required

### Clipboard
- Check if the app copies sensitive data to clipboard
- Clipboard is accessible by all apps (pre-Android 10)

---

## Phase 6: Component Testing

### Exported Activities
- List: `adb shell dumpsys package com.target.app | grep -A1 "Activity"`
- Launch directly: `adb shell am start -n com.target.app/.AdminActivity`
- Can you bypass authentication by launching internal activities directly?
- Deep link testing: `adb shell am start -a android.intent.action.VIEW -d "scheme://host/path"`

### Content Providers
- List: check manifest for `<provider>` with `exported="true"` or missing `exported` attribute
- Query: `adb shell content query --uri content://com.target.app.provider/users`
- Test for SQL injection: `content://com.target.app.provider/users/1' OR '1'='1`
- Check for path traversal in content providers
- Check `grantUriPermissions` for temporary access grants

### Broadcast Receivers
- List exported receivers from manifest
- Send broadcast: `adb shell am broadcast -a com.target.app.ACTION -e key value`
- Check if sensitive actions are triggered by broadcasts without proper permission checks
- Sniff broadcasts: register a receiver for broadcasted intents

### Services
- List exported services from manifest
- Bind to service: check if sensitive operations are exposed without authentication

---

## Phase 7: Binary Protections

### Obfuscation Assessment
- ProGuard/R8: check for renamed classes (a.b.c), string encryption
- If not obfuscated: direct source code reading is possible
- DexGuard, Arxan, iXGuard: more advanced protections (commercial)

### Anti-Tampering
- Signature verification: does the app check its own APK signature at runtime?
- Integrity checks: checksum verification of DEX files, native libraries
- Bypass: Frida hooks on verification functions, patch smali code

### Anti-Debugging
- `android.os.Debug.isDebuggerConnected()` checks
- TracerPid checks in `/proc/self/status`
- Timing checks to detect single-stepping
- Bypass: Frida hooks to return false for detection methods

### Anti-Root Detection
- Common checks: su binary, Magisk files, test-keys, root management apps
- Libraries: RootBeer, SafetyNet/Play Integrity
- Bypass: Frida scripts, Magisk Hide/Zygisk DenyList, objection

---

## Phase 8: Reporting

### Finding Categories
| Category | Examples |
|---|---|
| Insecure Data Storage | Plaintext credentials in SharedPreferences, unencrypted DB |
| Insecure Communication | HTTP endpoints, missing certificate pinning |
| Insufficient Cryptography | Hardcoded keys, weak algorithms, ECB mode |
| Insecure Authentication | Bypassable login, weak session management |
| Insecure Authorization | Exported activities bypass auth, IDOR via API |
| Client Code Quality | SQL injection in local DB, WebView vulnerabilities |
| Code Tampering | Missing integrity checks, no obfuscation |
| Reverse Engineering | Hardcoded secrets, readable source code |
| Extraneous Functionality | Debug endpoints, hidden admin features |

### Tools Quick Reference

| Task | Tools |
|---|---|
| Decompilation | jadx, apktool, dex2jar, JD-GUI |
| Static Analysis | MobSF, QARK, androguard |
| Dynamic Analysis | Frida, objection, Xposed |
| Proxy | Burp Suite, mitmproxy |
| Device | Genymotion, Android Studio emulator, rooted physical |
| Binary | Ghidra, IDA Pro, radare2 |
| Storage | sqlite3, DB Browser, adb shell |
| Automation | Drozer (component testing), MobSF (automated scan) |
