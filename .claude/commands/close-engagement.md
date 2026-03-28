Close and finalize the engagement for: $ARGUMENTS

1. **Verify completeness**: Check all findings have writeups, CVSS scores, and remediation advice
2. **Final report**: Generate `engagements/<target>/reports/final-report-<date>.md` with executive summary, methodology, findings table, risk matrix, remediation priorities
3. **Cleanup**: Remove any temp files, tokens, test accounts created during engagement
4. **Evidence archive**: Verify all screenshots, logs, PoC scripts are saved in the engagement directory
5. **Debrief notes**: Document lessons learned, new techniques discovered, tool improvements needed
6. **Status update**: Mark engagement as CLOSED in `engagements/<target>/README.md`

Output: engagements/<target>/reports/final-report-<date>.md
