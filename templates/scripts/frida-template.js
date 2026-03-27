/**
 * Frida Hook Template
 *
 * Target:     [Application Name]
 * Platform:   [Android / iOS]
 * Package:    [com.example.app]
 * Author:     [Your Name]
 * Date:       [YYYY-MM-DD]
 *
 * Description:
 *   [Brief description of what this script hooks and why.]
 *
 * Usage:
 *   frida -U -f com.example.app -l frida-template.js --no-pause
 *   frida -U -n "App Name" -l frida-template.js
 *   frida -H 192.168.1.100 -f com.example.app -l frida-template.js
 */

"use strict";

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

var CONFIG = {
    verbose: true,
    logToFile: false,
    logFile: "/data/local/tmp/frida-hook.log",
    bypassSSLPinning: true,
    bypassRootDetection: true,
};

// ---------------------------------------------------------------------------
// Utility Functions
// ---------------------------------------------------------------------------

function log(msg) {
    var timestamp = new Date().toISOString().substr(11, 12);
    var formatted = "[" + timestamp + "] " + msg;
    console.log(formatted);

    if (CONFIG.logToFile) {
        var f = new File(CONFIG.logFile, "a");
        f.write(formatted + "\n");
        f.flush();
        f.close();
    }
}

function logVerbose(msg) {
    if (CONFIG.verbose) {
        log("[VERBOSE] " + msg);
    }
}

function hexdump(buf, length) {
    if (buf.isNull()) {
        return "<null>";
    }
    length = length || 64;
    return "\n" + Memory.readByteArray(buf, Math.min(length, 256));
}

function getStackTrace() {
    return Thread.backtrace(this.context, Backtracer.ACCURATE)
        .map(DebugSymbol.fromAddress)
        .join("\n    ");
}

function colorize(text, color) {
    var colors = {
        red: "\x1b[31m",
        green: "\x1b[32m",
        yellow: "\x1b[33m",
        blue: "\x1b[34m",
        magenta: "\x1b[35m",
        cyan: "\x1b[36m",
        reset: "\x1b[0m",
    };
    return (colors[color] || "") + text + colors.reset;
}

// ---------------------------------------------------------------------------
// Android: Java Hook Patterns
// ---------------------------------------------------------------------------

function hookJavaMethod() {
    /**
     * Hook a specific Java method.
     * Replace class name and method name with your target.
     */
    Java.perform(function () {
        var targetClass = Java.use("com.example.app.TargetClass");

        // Hook a method with known argument types
        targetClass.targetMethod.overload("java.lang.String", "int").implementation = function (arg1, arg2) {
            log(colorize("[+] targetMethod called", "green"));
            log("    arg1 (String): " + arg1);
            log("    arg2 (int): " + arg2);

            // Call the original method
            var result = this.targetMethod(arg1, arg2);
            log("    return: " + result);

            // Optionally modify the return value
            // return "modified_value";

            return result;
        };

        log("[*] Hooked com.example.app.TargetClass.targetMethod");
    });
}

function hookAllOverloads() {
    /**
     * Hook all overloads of a method when you don't know
     * the exact parameter types.
     */
    Java.perform(function () {
        var targetClass = Java.use("com.example.app.TargetClass");
        var overloads = targetClass.targetMethod.overloads;

        for (var i = 0; i < overloads.length; i++) {
            overloads[i].implementation = function () {
                log(colorize("[+] targetMethod overload called", "green"));
                for (var j = 0; j < arguments.length; j++) {
                    log("    arg" + j + ": " + arguments[j]);
                }
                var result = this.targetMethod.apply(this, arguments);
                log("    return: " + result);
                return result;
            };
        }

        log("[*] Hooked all overloads of targetMethod (" + overloads.length + " overloads)");
    });
}

function hookConstructor() {
    /**
     * Hook a class constructor to inspect object creation.
     */
    Java.perform(function () {
        var targetClass = Java.use("com.example.app.TargetClass");

        targetClass.$init.overload("java.lang.String").implementation = function (arg1) {
            log(colorize("[+] TargetClass constructor called", "cyan"));
            log("    arg1: " + arg1);
            this.$init(arg1);
        };

        log("[*] Hooked TargetClass constructor");
    });
}

function enumerateLoadedClasses(filter) {
    /**
     * List all loaded classes matching a filter string.
     */
    Java.perform(function () {
        Java.enumerateLoadedClasses({
            onMatch: function (className) {
                if (className.indexOf(filter) !== -1) {
                    log("[CLASS] " + className);
                }
            },
            onComplete: function () {
                log("[*] Class enumeration complete");
            }
        });
    });
}

function hookCryptoOperations() {
    /**
     * Hook javax.crypto.Cipher to log encryption/decryption operations.
     * Useful for understanding data protection mechanisms.
     */
    Java.perform(function () {
        var Cipher = Java.use("javax.crypto.Cipher");

        Cipher.getInstance.overload("java.lang.String").implementation = function (algorithm) {
            log(colorize("[CRYPTO] Cipher.getInstance: " + algorithm, "yellow"));
            return this.getInstance(algorithm);
        };

        Cipher.doFinal.overload("[B").implementation = function (input) {
            log(colorize("[CRYPTO] Cipher.doFinal called", "yellow"));
            log("    mode: " + (this.getOpmode() === 1 ? "ENCRYPT" : "DECRYPT"));
            log("    algorithm: " + this.getAlgorithm());
            log("    input length: " + input.length);

            var result = this.doFinal(input);

            log("    output length: " + result.length);
            return result;
        };

        log("[*] Hooked javax.crypto.Cipher operations");
    });
}

function hookSharedPreferences() {
    /**
     * Hook SharedPreferences to monitor local storage reads/writes.
     */
    Java.perform(function () {
        var SharedPrefsEditor = Java.use("android.app.SharedPreferencesImpl$EditorImpl");

        SharedPrefsEditor.putString.implementation = function (key, value) {
            log(colorize("[PREFS] putString: " + key + " = " + value, "magenta"));
            return this.putString(key, value);
        };

        SharedPrefsEditor.putInt.implementation = function (key, value) {
            log(colorize("[PREFS] putInt: " + key + " = " + value, "magenta"));
            return this.putInt(key, value);
        };

        SharedPrefsEditor.putBoolean.implementation = function (key, value) {
            log(colorize("[PREFS] putBoolean: " + key + " = " + value, "magenta"));
            return this.putBoolean(key, value);
        };

        log("[*] Hooked SharedPreferences write operations");
    });
}

function hookNetworkRequests() {
    /**
     * Hook OkHttp3 to log network requests and responses.
     */
    Java.perform(function () {
        try {
            var OkHttpClient = Java.use("okhttp3.OkHttpClient");
            var Request = Java.use("okhttp3.Request");
            var Call = Java.use("okhttp3.internal.connection.RealCall");

            Call.execute.implementation = function () {
                var request = this.request();
                log(colorize("[HTTP] " + request.method() + " " + request.url().toString(), "blue"));

                var headers = request.headers();
                for (var i = 0; i < headers.size(); i++) {
                    logVerbose("    " + headers.name(i) + ": " + headers.value(i));
                }

                var response = this.execute();
                log("    Response: " + response.code());
                return response;
            };

            log("[*] Hooked OkHttp3 requests");
        } catch (e) {
            log("[-] OkHttp3 not found in this application");
        }
    });
}

// ---------------------------------------------------------------------------
// SSL Pinning Bypass
// ---------------------------------------------------------------------------

function bypassSSLPinning() {
    /**
     * Bypass common SSL pinning implementations.
     * Covers: TrustManager, OkHttp, Retrofit, custom implementations.
     */
    Java.perform(function () {

        // Bypass default TrustManager
        var TrustManagerFactory = Java.use("javax.net.ssl.TrustManagerFactory");
        var SSLContext = Java.use("javax.net.ssl.SSLContext");
        var X509TrustManager = Java.use("javax.net.ssl.X509TrustManager");

        // Create a TrustManager that accepts all certificates
        var TrustAllManager = Java.registerClass({
            name: "com.frida.TrustAllManager",
            implements: [X509TrustManager],
            methods: {
                checkClientTrusted: function (chain, authType) {},
                checkServerTrusted: function (chain, authType) {},
                getAcceptedIssuers: function () {
                    return [];
                },
            },
        });

        SSLContext.init.overload(
            "[Ljavax.net.ssl.KeyManager;",
            "[Ljavax.net.ssl.TrustManager;",
            "java.security.SecureRandom"
        ).implementation = function (keyManagers, trustManagers, secureRandom) {
            log(colorize("[SSL] Bypassing SSLContext.init TrustManager", "red"));
            var trustAllArray = [TrustAllManager.$new()];
            this.init(keyManagers, trustAllArray, secureRandom);
        };

        // Bypass OkHttp3 CertificatePinner
        try {
            var CertificatePinner = Java.use("okhttp3.CertificatePinner");
            CertificatePinner.check.overload("java.lang.String", "java.util.List").implementation = function (hostname, peerCerts) {
                log(colorize("[SSL] Bypassing OkHttp3 CertificatePinner for: " + hostname, "red"));
            };
            log("[*] Bypassed OkHttp3 CertificatePinner");
        } catch (e) {
            logVerbose("OkHttp3 CertificatePinner not found");
        }

        // Bypass Trustkit
        try {
            var TrustKit = Java.use("com.datatheorem.android.trustkit.pinning.OkHostnameVerifier");
            TrustKit.verify.overload("java.lang.String", "javax.net.ssl.SSLSession").implementation = function (hostname, session) {
                log(colorize("[SSL] Bypassing TrustKit for: " + hostname, "red"));
                return true;
            };
            log("[*] Bypassed TrustKit");
        } catch (e) {
            logVerbose("TrustKit not found");
        }

        log("[*] SSL pinning bypass applied");
    });
}

// ---------------------------------------------------------------------------
// Root Detection Bypass
// ---------------------------------------------------------------------------

function bypassRootDetection() {
    /**
     * Bypass common root detection checks.
     */
    Java.perform(function () {

        // Bypass File.exists() checks for common root indicators
        var File = Java.use("java.io.File");
        var rootIndicators = [
            "su", "Superuser.apk", "busybox", "magisk",
            "/system/xbin/su", "/system/bin/su", "/sbin/su",
            "/data/local/xbin/su", "/data/local/bin/su",
            "/system/app/Superuser.apk",
        ];

        File.exists.implementation = function () {
            var path = this.getAbsolutePath();
            for (var i = 0; i < rootIndicators.length; i++) {
                if (path.indexOf(rootIndicators[i]) !== -1) {
                    log(colorize("[ROOT] Hiding root indicator: " + path, "red"));
                    return false;
                }
            }
            return this.exists();
        };

        // Bypass Runtime.exec() for "su" and "which su"
        var Runtime = Java.use("java.lang.Runtime");
        Runtime.exec.overload("java.lang.String").implementation = function (cmd) {
            if (cmd.indexOf("su") !== -1 || cmd.indexOf("which") !== -1) {
                log(colorize("[ROOT] Blocking exec: " + cmd, "red"));
                throw Java.use("java.io.IOException").$new("Command not found");
            }
            return this.exec(cmd);
        };

        // Bypass Build.TAGS check (test-keys detection)
        var Build = Java.use("android.os.Build");
        var tags = Build.TAGS.value;
        if (tags && tags.indexOf("test-keys") !== -1) {
            Build.TAGS.value = "release-keys";
            log("[*] Changed Build.TAGS from test-keys to release-keys");
        }

        // Bypass SafetyNet / Play Integrity (basic)
        try {
            var SafetyNet = Java.use("com.google.android.gms.safetynet.SafetyNetApi");
            log("[*] SafetyNet detected -- manual bypass may be needed");
        } catch (e) {
            logVerbose("SafetyNet not found");
        }

        log("[*] Root detection bypass applied");
    });
}

// ---------------------------------------------------------------------------
// iOS: Objective-C Hook Patterns
// ---------------------------------------------------------------------------

function hookObjCMethod() {
    /**
     * Hook an Objective-C method on iOS.
     * Use 'ObjC.classes' to find classes and methods.
     */
    if (!ObjC.available) {
        log("[-] Objective-C runtime not available");
        return;
    }

    var className = "TargetClassName";
    var methodName = "- targetMethod:withArg:";

    var hook = ObjC.classes[className][methodName];
    if (!hook) {
        log("[-] Method not found: " + className + " " + methodName);
        return;
    }

    Interceptor.attach(hook.implementation, {
        onEnter: function (args) {
            // args[0] = self, args[1] = selector, args[2]+ = method arguments
            log(colorize("[+] " + className + " " + methodName + " called", "green"));
            log("    arg0: " + ObjC.Object(args[2]).toString());
            log("    arg1: " + ObjC.Object(args[3]).toString());
        },
        onLeave: function (retval) {
            log("    return: " + ObjC.Object(retval).toString());
            // Optionally replace return value
            // retval.replace(ObjC.classes.NSNumber.numberWithBool_(0));
        },
    });

    log("[*] Hooked " + className + " " + methodName);
}

function bypassiOSSSLPinning() {
    /**
     * Bypass SSL pinning on iOS (covers NSURLSession, AFNetworking, Alamofire).
     */
    if (!ObjC.available) {
        log("[-] Objective-C runtime not available");
        return;
    }

    // Bypass NSURLSession delegate
    var resolver = new ApiResolver("objc");
    var matches = resolver.enumerateMatches(
        "-[* URLSession:didReceiveChallenge:completionHandler:]"
    );

    matches.forEach(function (match) {
        Interceptor.attach(match.address, {
            onEnter: function (args) {
                // Get the completion handler
                var completionHandler = new ObjC.Block(args[4]);
                // Call it with "use credential" disposition and server trust
                var challenge = ObjC.Object(args[3]);
                var serverTrust = challenge.protectionSpace().serverTrust();
                var credential = ObjC.classes.NSURLCredential.credentialForTrust_(serverTrust);

                completionHandler.implementation(0, credential);
                log(colorize("[SSL-iOS] Bypassed SSL challenge for delegate", "red"));
            },
        });
    });

    // Bypass AFNetworking
    try {
        var AFSecurityPolicy = ObjC.classes.AFSecurityPolicy;
        if (AFSecurityPolicy) {
            Interceptor.attach(
                AFSecurityPolicy["- setSSLPinningMode:"].implementation,
                {
                    onEnter: function (args) {
                        // Set mode to AFSSLPinningModeNone (0)
                        args[2] = ptr(0);
                        log(colorize("[SSL-iOS] AFNetworking pinning mode set to None", "red"));
                    },
                }
            );
        }
    } catch (e) {
        logVerbose("AFNetworking not found");
    }

    log("[*] iOS SSL pinning bypass applied");
}

function bypassiOSJailbreakDetection() {
    /**
     * Bypass common iOS jailbreak detection checks.
     */
    if (!ObjC.available) {
        log("[-] Objective-C runtime not available");
        return;
    }

    // Bypass NSFileManager fileExistsAtPath: for jailbreak paths
    var NSFileManager = ObjC.classes.NSFileManager;
    var fileExistsAtPath = NSFileManager["- fileExistsAtPath:"];
    var jailbreakPaths = [
        "/Applications/Cydia.app",
        "/Library/MobileSubstrate/MobileSubstrate.dylib",
        "/bin/bash",
        "/usr/sbin/sshd",
        "/etc/apt",
        "/private/var/lib/apt/",
        "/usr/bin/ssh",
        "/private/var/stash",
        "/usr/libexec/sftp-server",
        "/Applications/Sileo.app",
    ];

    Interceptor.attach(fileExistsAtPath.implementation, {
        onEnter: function (args) {
            this.path = ObjC.Object(args[2]).toString();
        },
        onLeave: function (retval) {
            for (var i = 0; i < jailbreakPaths.length; i++) {
                if (this.path.indexOf(jailbreakPaths[i]) !== -1) {
                    log(colorize("[JB] Hiding: " + this.path, "red"));
                    retval.replace(0);
                    break;
                }
            }
        },
    });

    // Bypass canOpenURL: for Cydia
    var UIApplication = ObjC.classes.UIApplication;
    Interceptor.attach(UIApplication["- canOpenURL:"].implementation, {
        onEnter: function (args) {
            this.url = ObjC.Object(args[2]).toString();
        },
        onLeave: function (retval) {
            if (this.url.indexOf("cydia") !== -1 || this.url.indexOf("sileo") !== -1) {
                log(colorize("[JB] Blocking canOpenURL: " + this.url, "red"));
                retval.replace(0);
            }
        },
    });

    log("[*] iOS jailbreak detection bypass applied");
}

// ---------------------------------------------------------------------------
// Native Hook Patterns
// ---------------------------------------------------------------------------

function hookNativeFunction() {
    /**
     * Hook a native (C/C++) function by symbol or address.
     */

    // Hook by export name
    var targetFunc = Module.findExportByName("libnative.so", "target_function");
    if (targetFunc) {
        Interceptor.attach(targetFunc, {
            onEnter: function (args) {
                log(colorize("[NATIVE] target_function called", "green"));
                log("    arg0: " + args[0]);
                log("    arg1: " + args[1].readUtf8String());
            },
            onLeave: function (retval) {
                log("    return: " + retval);
            },
        });
        log("[*] Hooked native target_function");
    }

    // Hook by address offset within a module
    var baseAddr = Module.findBaseAddress("libnative.so");
    if (baseAddr) {
        var funcAddr = baseAddr.add(0x1234);  // Replace with actual offset
        Interceptor.attach(funcAddr, {
            onEnter: function (args) {
                log(colorize("[NATIVE] Function at offset 0x1234 called", "green"));
            },
            onLeave: function (retval) {
                log("    return: " + retval);
            },
        });
        log("[*] Hooked function at " + funcAddr);
    }
}

function hookDlopen() {
    /**
     * Monitor library loading to hook functions in late-loaded libraries.
     */
    var dlopen = Module.findExportByName(null, "dlopen");
    var android_dlopen_ext = Module.findExportByName(null, "android_dlopen_ext");

    var hookDl = function (addr, name) {
        if (!addr) return;
        Interceptor.attach(addr, {
            onEnter: function (args) {
                this.path = args[0].readCString();
                log("[DLOPEN] " + name + ": " + this.path);
            },
            onLeave: function (retval) {
                if (this.path && this.path.indexOf("target_library") !== -1) {
                    log("[DLOPEN] Target library loaded! Applying hooks...");
                    // Apply hooks to the newly loaded library here
                    hookNativeFunction();
                }
            },
        });
    };

    hookDl(dlopen, "dlopen");
    hookDl(android_dlopen_ext, "android_dlopen_ext");
    log("[*] Monitoring library loads via dlopen");
}

// ---------------------------------------------------------------------------
// Main Initialization
// ---------------------------------------------------------------------------

function main() {
    log("=========================================");
    log("  Frida Hook Script Initialized");
    log("  Target: [Application Name]");
    log("=========================================");

    // Wait for Java runtime to be available (Android)
    if (Java.available) {
        log("[*] Java runtime detected (Android)");

        // Apply bypasses
        if (CONFIG.bypassSSLPinning) {
            bypassSSLPinning();
        }
        if (CONFIG.bypassRootDetection) {
            bypassRootDetection();
        }

        // Apply hooks
        // Uncomment the hooks you need:
        // hookJavaMethod();
        // hookAllOverloads();
        // hookConstructor();
        // hookCryptoOperations();
        // hookSharedPreferences();
        // hookNetworkRequests();
        // enumerateLoadedClasses("com.example");
    }

    // iOS hooks
    if (ObjC.available) {
        log("[*] Objective-C runtime detected (iOS)");

        if (CONFIG.bypassSSLPinning) {
            bypassiOSSSLPinning();
        }
        if (CONFIG.bypassRootDetection) {
            bypassiOSJailbreakDetection();
        }

        // Uncomment the hooks you need:
        // hookObjCMethod();
    }

    // Native hooks (both platforms)
    // hookNativeFunction();
    // hookDlopen();

    log("=========================================");
    log("  Hooks applied. Monitoring...");
    log("=========================================");
}

// Run
main();
