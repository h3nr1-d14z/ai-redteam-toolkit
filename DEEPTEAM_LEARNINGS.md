# DeepTeam Framework — Research & Learnings

Research from [confident-ai/deepteam](https://github.com/confident-ai/deepteam) — LLM red teaming framework.

---

## Key Patterns We Adopt

### 1. Modular Vulnerability/Attack Architecture

DeepTeam separates **vulnerabilities** (what to test) from **attacks** (how to test). This decoupling is powerful — any vulnerability can be tested with any attack method.

**Applied**: Our `/ai-redteam` command should specify both vulnerability category AND attack method.

### 2. Six Vulnerability Categories (50+ vulnerabilities)

| Category | Key Vulnerabilities | Our Command |
|----------|-------------------|-------------|
| **Data Privacy** | PII leakage, prompt leakage, credential extraction | `/ai-redteam --category privacy` |
| **Responsible AI** | Bias, toxicity, child protection, fairness | `/ai-guardrail-test --category bias` |
| **Security** | BFLA, BOLA, RBAC bypass, injection, tool poisoning | `/ai-redteam --category security` |
| **Safety** | Illegal activity, graphic content, code execution | `/ai-guardrail-test --category safety` |
| **Business** | Misinformation, IP violations, competitor endorsement | `/ai-guardrail-test --category business` |
| **Agentic** | Goal theft, recursive hijacking, tool abuse, agent drift | `/ai-redteam --category agentic` |

### 3. Attack Methods (27 total)

**Single-Turn (22)**: Encoding (Leetspeak, ROT13, Base64), injection (prompt injection, context poisoning), social (roleplay, authority escalation, emotional manipulation), logic (math problem, adversarial poetry), bypass (system override, permission escalation, goal redirection)

**Multi-Turn (5)**: Linear jailbreaking, tree jailbreaking, crescendo jailbreaking, sequential jailbreak, bad Likert judge

**Applied**: Our wordlists and methodology cover these patterns.

### 4. LLM-as-a-Judge Scoring

DeepTeam uses the LLM itself to evaluate attack success — binary pass/fail with reasoning. Smarter than regex.

**Applied**: Our `/ai-guardrail-test` uses Claude to evaluate responses, not pattern matching.

### 5. Framework Alignment

Maps to: OWASP LLM Top 10, OWASP Agentic Top 10, NIST AI RMF, MITRE ATLAS.

**Applied**: Our AI methodology references these. Findings should tag framework mappings.

### 6. model_callback Abstraction

`async def model_callback(input: str) -> str:` — test ANY LLM without knowing internals.

**Applied**: Our tools accept target as URL/endpoint, not hardcoded APIs.

### 7. Seven Guardrail Categories

Toxicity, Prompt Injection, Privacy, Illegal, Hallucination, Topical, Cybersecurity.

**Applied**: Our `/ai-guardrail-test` tests all 7 systematically.

---

## What We Don't Copy

- DeepTeam is a Python library — we're a slash-command framework. Different UX.
- We don't need their scoring infra — Claude Code IS the judge.
- Their agentic attacks are cutting-edge but our primary focus is traditional security + AI as supplement.

---

## Implementation Learnings (from repo hardening)

1. Keep command names file-backed — canonical source is `commands/*.md`
2. One structural truth for commands — flat layout, no subdirectory claims
3. Engagement path standardization — `engagements/<target>/...` consistently
4. Setup script parity per domain — installer for every advertised domain
5. Platform support clarity — Windows routes through WSL2
6. Portable MCP config — relative paths in `.mcp.json`
