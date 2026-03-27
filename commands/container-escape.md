Test container escape vectors on: $ARGUMENTS

1. **Container info**: Identify runtime (Docker/containerd/CRI-O), check cgroup version, namespace isolation
2. **Privileged check**: Test if container is privileged (--privileged), has dangerous capabilities (SYS_ADMIN, SYS_PTRACE, DAC_OVERRIDE)
3. **Mount check**: Look for mounted Docker socket (/var/run/docker.sock), host filesystem mounts, sensitive procfs/sysfs
4. **Kernel exploits**: Check kernel version for known container escapes (CVE-2022-0185, CVE-2022-0847 Dirty Pipe)
5. **Network**: Test for access to host network, cloud metadata, other containers, Kubernetes API
6. **K8s specific**: Check service account permissions, mounted tokens, RBAC misconfig, pod security policies
7. **Escape PoC**: If escape vector found, develop controlled PoC demonstrating host access

Tools: amicontained, deepce, kubectl, docker CLI, linpeas
Save to `engagements/<target>/findings/container-escape-*.md`
