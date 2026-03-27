Hunt for XSS on: $ARGUMENTS

Map all input reflection points: search, forms, URL params, headers.
Test types: reflected, stored, DOM-based.
Use wordlists/xss/payloads.txt for payload list.
Test context: HTML body, attribute, JavaScript, URL.
Try bypasses: encoding, case variation, tag alternatives, event handlers (wordlists/xss/event-handlers.txt).
Check if CSP blocks execution.
Test impact: cookie theft, session hijack, keylogging.
Tools: dalfox > manual.
Output: engagements/<target>/findings/xss-*.md

## Safety
Verify authorization and scope before proceeding. Document all actions.
