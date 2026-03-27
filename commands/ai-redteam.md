Red team AI/ML system: $ARGUMENTS

1. **Model identification**: Determine model type, API interface, input/output format, rate limits
2. **Prompt injection**: Test for direct injection, indirect injection (data poisoning), system prompt extraction
3. **Jailbreaking**: Test bypass techniques — role-playing, encoding, language switching, token smuggling, crescendo attacks
4. **Data extraction**: Attempt to extract training data, system prompts, PII, confidential information from model responses
5. **Adversarial inputs**: Test with adversarial examples — perturbations, edge cases, boundary conditions, unusual encodings
6. **Abuse scenarios**: Test for harmful output generation — misinformation, malicious code, social engineering content
7. **Authorization**: Test API key exposure, rate limit bypass, access control on model endpoints
8. **Report**: Document each finding with reproduction steps, impact assessment, and remediation

Save to `engagements/<target>/findings/ai-redteam-*.md`
