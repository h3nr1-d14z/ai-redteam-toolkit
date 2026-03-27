# [Challenge Name]

| Field | Value |
|---|---|
| **Event** | [CTF Event Name / Year] |
| **Category** | [Web / Pwn / RE / Crypto / Forensics / Misc / OSINT] |
| **Difficulty** | [Easy / Medium / Hard / Insane] |
| **Points** | [Point value] |
| **Solves** | [Number of solves during the event] |
| **Author** | [Challenge author if known] |
| **Solved By** | [Your name] |
| **Date** | [YYYY-MM-DD] |

---

## Challenge Description

> [Paste the exact challenge description here, preserving formatting.]
> [Include any hints that were released.]

**Files Provided:**
- [filename1.ext] -- [description, e.g., "ELF 64-bit binary"]
- [filename2.ext] -- [description, e.g., "packet capture file"]
- [server connection info if applicable: nc challenge.ctf.com 1337]

**File Hashes (SHA256):**
```
[sha256hash]  filename1.ext
[sha256hash]  filename2.ext
```

---

## Reconnaissance

[Describe your initial analysis of the challenge. What did you notice first? What tools did you use for initial triage?]

**Initial observations:**
- [Observation 1: e.g., "Binary is stripped, 64-bit ELF, dynamically linked"]
- [Observation 2: e.g., "Web app uses Flask based on error messages"]
- [Observation 3: e.g., "PCAP contains HTTP traffic with interesting POST requests"]

**Tools used for recon:**
- [Tool 1: purpose]
- [Tool 2: purpose]

---

## Analysis

[Detailed analysis of the challenge. Walk through your thought process step by step.]

### Step 1: [Description]

[Explain what you did and what you found.]

```
[Relevant command output, code snippet, or tool output]
```

[Explain the significance of what you found.]

### Step 2: [Description]

[Continue walking through the analysis.]

```
[Relevant command output or code]
```

### Step 3: [Description]

[Continue as needed. Each step should build on the previous one.]

---

## Vulnerability / Weakness

[Clearly identify the core vulnerability, weakness, or trick that the challenge relies on.]

- **Type:** [e.g., Buffer Overflow, SQL Injection, RSA small exponent, XOR with known plaintext]
- **Root Cause:** [Why does this vulnerability exist in the challenge?]
- **Key Insight:** [What was the "aha" moment that led to the solution?]

---

## Solution

### Approach

[Summarize your solution approach in 2-3 sentences before diving into the details.]

### Exploit / Solution Script

```python
#!/usr/bin/env python3
"""
Solve script for [Challenge Name]
CTF: [Event Name]
Category: [Category]
"""

# [Full working solution script]
# [Make sure it runs and produces the flag]

def solve():
    # Solution implementation
    pass

if __name__ == "__main__":
    solve()
```

### Manual Steps (if applicable)

[If the solution involves manual steps (e.g., using a GUI tool, browser interaction), document them here with screenshots or detailed descriptions.]

1. [Step 1]
2. [Step 2]
3. [Step 3]

---

## Flag

```
flag{example_flag_here}
```

---

## Takeaways

### What I Learned

- [Key concept or technique learned from this challenge]
- [New tool or method discovered]
- [Security principle demonstrated]

### What I Could Improve

- [What took the most time? How could you solve it faster next time?]
- [What wrong paths did you go down?]
- [What would you do differently?]

### Related Resources

- [Link to relevant documentation or technique explanation]
- [Link to similar challenges or writeups]
- [Link to tools used]

### Similar Challenges

- [Other challenges that use similar techniques]
- [Practice resources for this category]

---

## Alternative Solutions

[If you know of other approaches that work, briefly describe them.]

### Approach 2: [Brief description]

[How this alternative approach works and why it's valid.]

### Approach 3: [Brief description]

[How this alternative approach works and why it's valid.]
