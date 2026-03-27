# Frida Cheatsheet

## Setup and Connection
```bash
# Install Frida
pip install frida-tools

# Check Frida version
frida --version

# Download frida-server for device
# https://github.com/frida/frida/releases (match version + architecture)

# Push to Android device
adb push frida-server-16.x.x-android-arm64 /data/local/tmp/frida-server
adb shell "chmod 755 /data/local/tmp/frida-server"
adb shell "/data/local/tmp/frida-server &"

# iOS (jailbroken): install via Cydia/Sileo
# Package: re.frida.server

# List processes on USB device
frida-ps -U

# List processes on remote device
frida-ps -H 192.168.1.100

# List running apps (only apps, not all processes)
frida-ps -Ua

# List installed apps
frida-ps -Uai
```

## Connecting to Apps
```bash
# Attach to running app by name
frida -U -n "AppName" -l script.js

# Attach to running app by PID
frida -U -p 1234 -l script.js

# Spawn app (start fresh with hooks)
frida -U -f com.target.app -l script.js --no-pause

# Connect to remote device
frida -H 192.168.1.100:27042 -f com.target.app -l script.js --no-pause

# Interactive REPL (no script)
frida -U -n "AppName"

# Run without pausing on spawn
frida -U -f com.target.app --no-pause

# Load multiple scripts
frida -U -f com.target.app -l script1.js -l script2.js --no-pause
```

## Frida CLI Commands (REPL)
```javascript
// List loaded modules
Process.enumerateModules()

// Find module by name
Process.findModuleByName("libc.so")

// Find export in module
Module.findExportByName("libc.so", "open")

// Read memory
Memory.readUtf8String(ptr("0x12345678"))
Memory.readByteArray(ptr("0x12345678"), 64)

// Write memory
Memory.writeUtf8String(ptr("0x12345678"), "new value")

// Allocate memory
Memory.alloc(1024)

// Scan memory for pattern
Memory.scan(baseAddr, size, "41 42 43 ?? 45", {
    onMatch: function(address, size) { console.log("Found at: " + address); },
    onComplete: function() { console.log("Scan done"); }
});
```

## Java Hooks (Android)
```javascript
// Basic method hook
Java.perform(function() {
    var cls = Java.use("com.example.app.ClassName");
    cls.methodName.implementation = function(arg1, arg2) {
        console.log("Called with: " + arg1 + ", " + arg2);
        var result = this.methodName(arg1, arg2);
        console.log("Returned: " + result);
        return result;
    };
});

// Hook overloaded method
Java.perform(function() {
    var cls = Java.use("com.example.app.ClassName");
    cls.method.overload("java.lang.String", "int").implementation = function(s, i) {
        return this.method(s, i);
    };
});

// Hook constructor
Java.perform(function() {
    var cls = Java.use("com.example.app.ClassName");
    cls.$init.overload("java.lang.String").implementation = function(arg) {
        console.log("Constructor: " + arg);
        this.$init(arg);
    };
});

// Modify return value
Java.perform(function() {
    var cls = Java.use("com.example.app.Security");
    cls.isRooted.implementation = function() {
        console.log("isRooted() called, returning false");
        return false;
    };
});

// Access and modify fields
Java.perform(function() {
    var cls = Java.use("com.example.app.Config");
    // Static field
    console.log("API_URL: " + cls.API_URL.value);
    cls.API_URL.value = "http://attacker.com";

    // Instance field (need an instance)
    Java.choose("com.example.app.Config", {
        onMatch: function(instance) {
            console.log("token: " + instance.token.value);
        },
        onComplete: function() {}
    });
});

// Enumerate loaded classes
Java.perform(function() {
    Java.enumerateLoadedClasses({
        onMatch: function(name) {
            if (name.includes("com.target")) console.log(name);
        },
        onComplete: function() {}
    });
});

// Call a static method
Java.perform(function() {
    var cls = Java.use("com.example.app.Utils");
    var result = cls.staticMethod("arg1");
    console.log("Result: " + result);
});

// Create new Java object
Java.perform(function() {
    var String = Java.use("java.lang.String");
    var newStr = String.$new("hello from frida");
    console.log(newStr.toString());
});
```

## ObjC Hooks (iOS)
```javascript
// Hook Objective-C method
if (ObjC.available) {
    var cls = ObjC.classes.TargetClass;
    var method = cls["- instanceMethod:"];
    Interceptor.attach(method.implementation, {
        onEnter: function(args) {
            // args[0]=self, args[1]=selector, args[2]=first arg
            console.log("arg: " + ObjC.Object(args[2]).toString());
        },
        onLeave: function(retval) {
            console.log("ret: " + ObjC.Object(retval).toString());
        }
    });
}

// Hook class method
var method = ObjC.classes.TargetClass["+ classMethod:"];

// Replace method implementation
var cls = ObjC.classes.JailbreakDetector;
cls["- isJailbroken"].implementation = ObjC.implement(
    cls["- isJailbroken"], function(handle, selector) {
        return 0;  // false
    }
);

// List all methods of a class
var methods = ObjC.classes.TargetClass.$ownMethods;
methods.forEach(function(m) { console.log(m); });

// Find instances of a class
ObjC.choose(ObjC.classes.TargetClass, {
    onMatch: function(instance) {
        console.log("Found: " + instance.toString());
    },
    onComplete: function() {}
});
```

## Native Hooks
```javascript
// Hook by export name
Interceptor.attach(Module.findExportByName("libc.so", "open"), {
    onEnter: function(args) {
        this.path = args[0].readUtf8String();
        console.log("open(" + this.path + ")");
    },
    onLeave: function(retval) {
        console.log("  returned fd: " + retval);
    }
});

// Hook by address
var base = Module.findBaseAddress("libtarget.so");
Interceptor.attach(base.add(0x1234), {
    onEnter: function(args) {
        console.log("Function called");
        console.log("arg0: " + args[0]);
        console.log("arg1: " + args[1].readUtf8String());
    }
});

// Replace function entirely
Interceptor.replace(Module.findExportByName("libtarget.so", "checkLicense"),
    new NativeCallback(function() {
        console.log("checkLicense() bypassed");
        return 1;  // always return true
    }, 'int', [])
);

// Call a native function
var puts = new NativeFunction(
    Module.findExportByName(null, "puts"), 'int', ['pointer']
);
var str = Memory.allocUtf8String("Hello from Frida");
puts(str);

// Hook dlopen to catch library loads
Interceptor.attach(Module.findExportByName(null, "dlopen"), {
    onEnter: function(args) {
        console.log("dlopen: " + args[0].readCString());
    }
});
```

## Common Bypass Patterns
```javascript
// SSL Pinning Bypass (Android - generic)
Java.perform(function() {
    // TrustManager bypass
    var X509TrustManager = Java.use("javax.net.ssl.X509TrustManager");
    var SSLContext = Java.use("javax.net.ssl.SSLContext");
    var TrustAll = Java.registerClass({
        name: "com.frida.TrustAll",
        implements: [X509TrustManager],
        methods: {
            checkClientTrusted: function(chain, authType) {},
            checkServerTrusted: function(chain, authType) {},
            getAcceptedIssuers: function() { return []; }
        }
    });
    SSLContext.init.overload("[Ljavax.net.ssl.KeyManager;", "[Ljavax.net.ssl.TrustManager;", "java.security.SecureRandom")
        .implementation = function(km, tm, sr) {
        this.init(km, [TrustAll.$new()], sr);
    };

    // OkHttp CertificatePinner
    try {
        var CertPinner = Java.use("okhttp3.CertificatePinner");
        CertPinner.check.overload("java.lang.String", "java.util.List").implementation = function() {};
    } catch(e) {}
});

// Root Detection Bypass (Android)
Java.perform(function() {
    var RootBeer = Java.use("com.scottyab.rootbeer.RootBeer");
    RootBeer.isRooted.implementation = function() { return false; };
    RootBeer.isRootedWithoutBusyBoxCheck.implementation = function() { return false; };
});

// Biometric Bypass (Android)
Java.perform(function() {
    var BiometricPrompt = Java.use("android.hardware.biometrics.BiometricPrompt");
    // Hook onAuthenticationSucceeded callback
});

// Jailbreak Detection Bypass (iOS)
if (ObjC.available) {
    // NSFileManager.fileExistsAtPath
    Interceptor.attach(ObjC.classes.NSFileManager["- fileExistsAtPath:"].implementation, {
        onEnter: function(args) { this.path = ObjC.Object(args[2]).toString(); },
        onLeave: function(retval) {
            var jbPaths = ["/Applications/Cydia.app", "/bin/bash", "/usr/sbin/sshd"];
            if (jbPaths.some(p => this.path.includes(p))) retval.replace(0);
        }
    });
}
```

## Useful One-Liners
```bash
# Trace all method calls on a class
frida-trace -U -n "AppName" -j "com.target.app.ClassName*!*"

# Trace native function calls
frida-trace -U -n "AppName" -i "open" -i "read" -i "write"

# Trace ObjC method
frida-trace -U -n "AppName" -m "-[ClassName methodName:]"

# Dump all classes
frida -U -n "App" -e "Java.perform(function(){Java.enumerateLoadedClasses({onMatch:function(c){if(c.includes('com.target'))console.log(c)},onComplete:function(){}})})"

# Quick SSL pinning bypass via objection
objection -g com.target.app explore -c "android sslpinning disable"
```

## Objection Quick Reference
```bash
# Connect
objection -g com.target.app explore          # Android
objection -g "App Name" explore              # iOS

# Android commands
android sslpinning disable                   # Bypass SSL pinning
android root disable                         # Bypass root detection
android hooking list classes                 # List classes
android hooking search classes Auth          # Search classes
android hooking list class_methods <class>   # List methods
android hooking watch class_method <method> --dump-args --dump-return
android keystore list                        # Dump keystore
android clipboard monitor                    # Monitor clipboard

# iOS commands
ios sslpinning disable                       # Bypass SSL pinning
ios jailbreak disable                        # Bypass jailbreak detection
ios hooking list classes                     # List classes
ios keychain dump                            # Dump keychain
ios cookies get                              # Get cookies
ios pasteboard monitor                       # Monitor clipboard

# Common commands (both platforms)
env                                          # Show app environment
ls / cat / download / upload                 # File operations
sqlite connect <db_path>                     # Connect to SQLite DB
```
