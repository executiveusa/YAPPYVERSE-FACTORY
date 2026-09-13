# Business Credit Workflow — Multiplayer ICM

**Purpose:** build a lawful, evidence-backed business-credit readiness system that can be reused across internal companies and client businesses.

This workflow is for research, readiness, documentation, monitoring, and human-approved applications. It is not an autonomous credit-application bot.

## INPUT

Required:
- legal business name
- entity type
- state/country of registration
- EIN/tax ID reference location
- business address
- business phone/email/domain
- bank-account status
- time in business
- authorized owner/operator
- existing business credit accounts if any
- explicit goal: vendor terms, card, line of credit, equipment, working capital, etc.

Never place tax IDs, SSNs, banking credentials, passwords, or full sensitive application data in git.

## PROCESS

### Stage 1 — Identity integrity
Verify the business identity is consistent across authorized/public records and internal documentation.

Check:
- entity status
- business name consistency
- address/phone/domain consistency
- required licenses where applicable
- banking relationship readiness
- accounting/bookkeeping evidence availability

### Stage 2 — Readiness baseline
Create a baseline, not a promise.

Track where legally/technically accessible:
- business credit bureau presence
- payment history
- utilization if relevant
- existing vendor accounts
- derogatory or disputed items
- age of business
- banking history
- revenue documentation readiness

Unavailable values remain `UNKNOWN`.

### Stage 3 — Opportunity research
Research legitimate products and vendors matched to the business profile.

For each candidate record:
- provider
- product type
- published eligibility
- fees/APR/terms if available
- personal guarantee requirement
- bureau reporting claims and source
- geography
- application method
- hard/soft inquiry if disclosed
- evidence date
- confidence

Do not treat affiliate/blog claims as verified lender policy without corroboration.

### Stage 4 — Sequence design
Build a conservative application/order sequence based on real eligibility and business need.

Optimize for:
- useful credit, not vanity accounts
- minimum unnecessary inquiries
- manageable fees
- payment ability
- low fraud/identity risk
- traceable terms

Do not shotgun applications.

### Stage 5 — Human approval gate
Before any application submission, present:

```text
PROVIDER
PRODUCT
PURPOSE
PUBLISHED TERMS
KNOWN FEES
PERSONAL GUARANTEE
INQUIRY TYPE
WHY THIS FITS
RISKS
ALTERNATIVES
DATA TO BE SUBMITTED
```

Gate: PASS / BLOCK by authorized human.

### Stage 6 — Assisted application
A browser/subagent may assist with navigation and form preparation only after approval.

It may:
- open official provider pages
- collect published terms
- prepare a checklist
- populate non-sensitive fields if explicitly authorized
- pause for the owner at identity/consent/signature/financial-commitment steps

It must not:
- impersonate the owner
- fabricate facts
- bypass identity checks
- invent revenue or employees
- create fake invoices or tradelines
- accept terms autonomously
- submit a personal guarantee without the guarantor
- move funds

### Stage 7 — Receipt and monitoring
Record:
- provider
- application date
- human approver
- result
- credit limit/terms if approved
- inquiry evidence
- reporting evidence when later observed
- payment due dates
- next review date

Never commit raw sensitive application data.

## OUTPUT

Per business:

```text
credit/<business-id>/
  profile.md
  readiness.json
  opportunities.json
  sequence.md
  approvals/
  receipts/
  monitoring.json
```

Sensitive documents remain in approved secure storage and are referenced, not copied into git.

## GATE

Only:
- PASS
- BLOCK

No application is considered PASS merely because it was submitted. PASS means the intended stage was completed with evidence and authority.

## RECEIPT

Every action records:
- agent/person
- source
- timestamp
- action
- authority
- result
- next action

## Subagent roles

### Credit Recon Agent
Researches official bureaus, lender/vendor policies, and readiness requirements.

### Identity Consistency Agent
Finds mismatches across authorized/public business identity records.

### Product Fit Agent
Ranks legitimate financing/vendor options by fit and cost, without applying.

### Credit Monitor
Tracks known accounts, deadlines, changes, and evidence on an approved schedule.

### Application Assistant
Human-in-the-loop browser helper. Cannot cross signature, consent, identity, guarantee, or financial-commitment gates autonomously.

### Independent Credit Verifier
Checks whether claims are sourced, terms are current, fees/PG/inquiry implications are visible, and the proposed sequence is not based on myths or vanity tradelines.

## Proven / Better / New

### PROVEN
- accurate business identity
- consistent records
- on-time payment history
- useful trade relationships
- organized financial documentation
- conservative application sequencing
- explicit human consent

### BETTER
- one shared readiness dashboard
- evidence dates on every lender/vendor claim
- automated reminders and monitoring
- application packet templates
- separate research and approval agents

### NEW / EXPERIMENTAL
- browser-assisted multi-provider comparison
- agent-generated readiness scoring
- opportunity routing across team companies

Experimental automation must never replace lender terms, underwriting, owner consent, or legal requirements.

## First internal target

Use the registered Seattle social-purpose business named by the owner as the first credit-readiness test only after its exact legal entity name and authoritative registration details are verified. Do not infer the legal entity from a brand nickname or conversation wording.