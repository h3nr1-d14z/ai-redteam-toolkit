# OMC (oh-my-claudecode) Integration Guide

Supercharge AI-RedTeam-Toolkit with oh-my-claudecode's multi-agent orchestration capabilities.

## Installation

```bash
npm install -g oh-my-claudecode
omc setup
```

Run `omc setup` once in the repo root to initialize project memory and agent state. OMC works on top of Claude Code — you need Claude Code installed first.

## Agents Available

OMC ships specialized agents accessible as `oh-my-claudecode:<name>`:

| Agent | Use Case |
|-------|----------|
| `executor` | Focused implementation — write exploits, tools, scripts |
| `architect` | Strategic planning — engagement planning, attack chains |
| `security-reviewer` | Detect vulnerabilities in generated code |
| `code-reviewer` | Review exploit code quality and correctness |
| `tracer` | Evidence-driven root-cause analysis |
| `debugger` | Fix broken exploits, diagnose tool failures |
| `scientist` | Research and data analysis — vuln research, binary analysis |

## OMC Skills for Security Work

| Skill | Command | What It Does |
|-------|---------|--------------|
| Autonomous loop | `/ralph /pentest target.com` | Repeats until thorough |
| Parallel agents | `/team N:executor "..."` | N agents working in parallel |
| Batch tasks | `/ultrawork` | Run multiple independent tasks at once |
| Evidence tracing | `/trace "hypothesis"` | Causal chain from symptom to root cause |
| Multi-model | `/sciomc` | Claude + Codex + Gemini simultaneously |
| Continuous poll | `/loop Xm /command` | Run command every X minutes |
| QA cycle | `/ultraqa /pentest target` | Test → verify → fix loop |

## Autopilot Pentest

Run a full pentest autonomously until thorough:

```
/ralph /pentest https://target.com
```

Ralph loops: pentest → review findings → test more → until satisfied.

## Parallel Multi-Target Scanning

Scan multiple targets simultaneously:

```
/ultrawork
Task 1: /recon target1.com
Task 2: /recon target2.com
Task 3: /recon target3.com
```

## Team-Based Assessment

Multiple agents working on different attack surfaces:

```
/team 3:executor "Pentest https://target.com — Agent 1: web app testing, Agent 2: API testing, Agent 3: infrastructure scanning"
```

## Deep Binary Analysis

Parallel analysis of complex binary with multiple approaches:

```
/sciomc Analyze this game binary — check memory layout, network protocol, anti-cheat mechanisms, and crypto implementation
```

## Root Cause Analysis

Trace a vulnerability to its root cause:

```
/trace Why does the authentication bypass work on /admin endpoint?
```

## Engagement Planning

Structured requirements gathering before a pentest:

```
/deep-interview Plan a red team engagement for a financial services company
```

## Continuous Monitoring

Poll a target for changes during an engagement:

```
/loop 5m /quick-scan https://target.com
```

## Workflow Combinations

| Goal | Command |
|------|---------|
| Autopilot full assessment | `/ralph /full-assessment target.com` |
| Parallel recon + scan | `/ultrawork` with multiple `/recon` tasks |
| Team pentest | `/team 3:executor "pentest target.com"` |
| Deep RE with Ghidra | `/sciomc` + Ghidra MCP tools |
| Iterative exploit dev | `/ralph /exploit "SQLi on /api/users"` |
| QA verification | `/ultraqa /pentest target.com` — test, verify, fix, repeat |
