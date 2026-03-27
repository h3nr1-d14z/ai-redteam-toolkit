# iOS Application Penetration Testing Methodology

## Phase 1: Setup and Preparation

### Environment Setup
- Jailbroken iOS device (preferred) or non-jailbroken with limited testing scope
- Jailbreak tools: checkra1n (A11 and below), unc0ver, Dopamine, palera1n
- Install Cydia/Sileo package manager on jailbroken device
- Install on device: OpenSSH, Frida (`frida-server`), SSL Kill Switch 2, Filza
- macOS tools: Xcode, `ideviceinstaller`, `ios-deploy`, `libimobiledevice`
- Burp Suite or mitmproxy configured as proxy
- Objection installed: `pip install objection`

### Obtain the IPA
- From client: direct IPA file
- From jailbroken device: `scp root@device_ip:/var/containers/Bundle/Application/<UUID>/AppName.app ./`
- From App Store (encrypted): use `frida-ios-dump` or `CrackerXI+` on jailbroken device to decrypt
- Thin binary for target architecture: `lipo -thin arm64 binary -output binary_arm64`

### Initial Triage
- `file AppName` -- architecture (arm64, armv7)
- Check `Info.plist`: bundle ID, version, minimum iOS version, URL schemes, transport security
- List entitlements: `codesign -d --entitlements :- AppName.app`
- Check if app uses App Transport Security exceptions

---

## Phase 2: Static Analysis

### IPA Structure Review
- Unzip IPA: `unzip app.ipa -d output/`
- Key files: `Info.plist`, binary executable, frameworks, embedded provisioning profile
- `Payload/AppName.app/` contains the app bundle

### Info.plist Analysis
- `NSAppTransportSecurity`: check for `NSAllowsArbitraryLoads`, domain exceptions
- URL schemes: `CFBundleURLSchemes` -- can be invoked by other apps
- Exported UTIs: document types the app handles
- Background modes: location, fetch, remote notifications
- Privacy descriptions: what permissions the app requests and why

### Binary Analysis
- Check protections: `otool -l binary | grep -A2 LC_ENCRYPTION` (encrypted?), PIE, ARC, stack canaries
- Check linked frameworks: `otool -L binary`
- Class dump: `class-dump binary > classes.h` or use `dsdump`
- String extraction: `strings binary | grep -i "http\|key\|secret\|password\|token\|api"`
- Hardcoded URLs: `strings binary | grep -E "https?://"`
- Check for debug symbols: `nm binary | head -50` (stripped = fewer symbols)

### Reverse Engineering with Ghidra/IDA
- Load the Mach-O binary
- Analyze Objective-C method names (preserved even when stripped)
- Look for: authentication logic, encryption implementation, jailbreak detection, certificate pinning
- Search for cross-references to security-sensitive APIs
- Swift apps: method names are mangled but classes are often readable

### Framework and Library Analysis
- List embedded frameworks: `ls Payload/AppName.app/Frameworks/`
- Check for known vulnerable library versions
- Analyze third-party SDKs: analytics, crash reporting, ad networks (data they collect)

---

## Phase 3: Dynamic Analysis

### Frida Setup
- Start Frida on device: `frida-server &` (or via SSH: `ssh root@device_ip "/usr/sbin/frida-server -D &"`)
- List processes: `frida-ps -U`
- Attach: `frida -U -n "AppName" -l script.js`
- Spawn: `frida -U -f com.target.app -l script.js --no-pause`

### Objection for iOS
```
# Connect
objection -g "AppName" explore

# Environment info
env

# Disable SSL pinning
ios sslpinning disable

# Disable jailbreak detection
ios jailbreak disable

# List classes
ios hooking list classes

# Search for classes
ios hooking search classes Auth

# List methods on a class
ios hooking list class_methods TargetViewController

# Hook a method
ios hooking watch method "-[LoginController validateCredentials:password:]" --dump-args --dump-return

# Dump keychain
ios keychain dump

# List cookies
ios cookies get

# Dump pasteboard
ios pasteboard monitor

# List bundles
ios bundles list_frameworks
```

### Runtime Exploration
- Hook authentication methods to understand login flow
- Hook encryption/decryption to capture plaintext data
- Hook network methods to see unencrypted request/response data
- Modify return values of security checks (jailbreak, integrity, biometric)
- Trace method calls to map application flow

### Debugger
- lldb: `debugserver *:1234 --attach=PID` on device, `lldb` then `process connect connect://device_ip:1234`
- Set breakpoints on interesting methods
- Inspect memory at runtime
- Step through security-critical code paths

---

## Phase 4: Traffic Analysis

### Proxy Configuration
- Set device proxy: Settings > Wi-Fi > HTTP Proxy > Manual > your IP:8080
- Install Burp CA: browse to `http://burp` on device, download and install certificate
- iOS 10.3+: also trust the CA in Settings > General > About > Certificate Trust Settings

### SSL Pinning Bypass
- objection: `ios sslpinning disable` (most common implementations)
- SSL Kill Switch 2: Cydia tweak for system-wide pinning bypass
- Frida script: custom hooks for NSURLSession, AFNetworking, Alamofire
- Manual patching: modify the binary to remove pinning checks, re-sign

### Traffic Analysis Checklist
- Map all API endpoints and their authentication requirements
- Check for HTTP (non-HTTPS) connections
- Look for sensitive data in request/response bodies and headers
- Check for certificate validation issues
- Test API endpoints following the API testing methodology
- Check for data leakage in URLs, headers, cookies
- WebSocket connections: capture and analyze message format

---

## Phase 5: Local Data Storage Analysis

### Keychain
- Dump with objection: `ios keychain dump`
- Dump with Frida: custom script to enumerate keychain items
- Check accessibility attributes: `kSecAttrAccessibleWhenUnlocked`, `kSecAttrAccessibleAlways` (insecure), `kSecAttrAccessibleAfterFirstUnlock`
- Check for sensitive data: passwords, tokens, keys, certificates
- Check if data protection class is appropriate for the sensitivity level

### NSUserDefaults (plist files)
- Location: `/var/mobile/Containers/Data/Application/<UUID>/Library/Preferences/`
- `plutil -p com.target.app.plist`
- Check for: credentials, tokens, PII, session data, configuration secrets
- These files are backed up to iCloud/iTunes by default

### SQLite Databases
- Location: `/var/mobile/Containers/Data/Application/<UUID>/Documents/`, `Library/`
- Find: `find /var/mobile/Containers/Data/Application/<UUID>/ -name "*.db" -o -name "*.sqlite"`
- Open with `sqlite3` or pull to macOS and use DB Browser
- Check Core Data stores (`.sqlite` files)
- Check for unencrypted sensitive data

### Cache and Temporary Files
- HTTP cache: `Library/Caches/`
- Snapshot images: `Library/SplashBoard/Snapshots/` (screenshots of app state)
- Check if sensitive screens are captured in snapshots
- Temporary files: `tmp/`
- Cookie storage: `Library/Cookies/`
- WebKit cache: `Library/WebKit/`

### Application Logs
- Check for sensitive data in logs: `idevicesyslog | grep AppName`
- NSLog output on non-jailbroken: connect via Xcode console
- Check `Library/Caches/Logs/` for persistent logs

### Pasteboard/Clipboard
- Monitor: `objection -g AppName explore -c "ios pasteboard monitor"`
- Check if sensitive data (passwords, tokens) is copied to clipboard
- Universal clipboard syncs across Apple devices

---

## Phase 6: Binary Protections

### Jailbreak Detection
- Common checks: file existence (Cydia, substrate), fork() behavior, sandbox integrity
- Check for: `canOpenURL("cydia://")`, stat() on jailbreak paths, dyld checks
- Bypass: objection `ios jailbreak disable`, Frida hooks, Liberty Lite, A-Bypass

### Anti-Tampering
- Code signature validation at runtime
- Integrity checks on binary, frameworks, resources
- Bypass: Frida hooks on verification functions

### Anti-Debugging
- `sysctl` check for `P_TRACED` flag
- `ptrace(PT_DENY_ATTACH)` call
- `isatty()` and `ioctl()` checks
- Bypass: Frida hooks to NOP out or modify return values

### Obfuscation
- Objective-C: method names are always readable (runtime requirement)
- Swift: names partially preserved, some mangling
- Commercial obfuscators: iXGuard, Arxan -- rename strings, encrypt classes
- Check for string encryption, control flow obfuscation

---

## Phase 7: Platform-Specific Testing

### URL Scheme Handling
- Identify schemes from `Info.plist`: `CFBundleURLSchemes`
- Test: `open url-scheme://malicious-input` from Safari or another app
- Check for: injection in URL parameters, unauthorized actions, data leakage
- Universal Links (`applinks:`): verify `apple-app-site-association` configuration

### Inter-Process Communication
- App extensions: check shared data containers, extension entitlements
- Shared Keychain groups: can other apps from same developer access secrets?
- UIPasteboard: named vs general pasteboard, expiration
- Handoff and AirDrop: data exposure during transfers

### WebView Security
- WKWebView vs UIWebView (deprecated, less secure)
- JavaScript enabled: check for JavaScript bridge vulnerabilities
- `evaluateJavaScript`: can attacker-controlled content execute JS?
- File access from WebView: `allowFileAccessFromFileURLs`
- Deep link to WebView: can you load arbitrary URLs in the app's WebView?

### Push Notifications
- Are sensitive data included in push notification payloads?
- Notifications are visible on lock screen by default
- Rich notifications: check for data leakage in attachments

### Biometric Authentication
- Is biometric auth just a local gate, or does it unlock a server-side credential?
- Can biometric auth be bypassed by hooking `LAContext.evaluatePolicy`?
- Check fallback mechanism (passcode, password)
- Frida bypass: hook `evaluatePolicy:localizedReason:reply:` and call reply block with success

---

## Phase 8: Reporting

### Finding Categories (OWASP MASTG)
| Category | Examples |
|---|---|
| Insecure Data Storage | Keychain with kSecAttrAccessibleAlways, plaintext DB |
| Insecure Communication | ATS exceptions, missing pinning, HTTP endpoints |
| Insecure Authentication | Bypassable biometric, weak session management |
| Insecure Authorization | Missing server-side checks, IDOR |
| Client Code Quality | URL scheme injection, WebView vulnerabilities |
| Anti-Tampering | Missing jailbreak detection, no integrity checks |
| Cryptography | Hardcoded keys, weak algorithms, improper key storage |
| Privacy | Excessive data collection, clipboard leakage, logging PII |

### Tools Quick Reference

| Task | Tools |
|---|---|
| Static Analysis | class-dump, dsdump, MobSF, Ghidra, Hopper |
| Dynamic Analysis | Frida, objection, cycript, lldb |
| Proxy | Burp Suite, mitmproxy, Charles |
| Jailbreak Bypass | Liberty Lite, A-Bypass, Shadow, custom Frida scripts |
| SSL Bypass | SSL Kill Switch 2, objection, Frida |
| File System | Filza, iExplorer, ifuse, scp |
| Keychain | keychain-dumper, objection |
| Network | Wireshark, tcpdump (on device), rvictl |
