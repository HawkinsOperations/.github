## Summary

Describe the governance, routing, documentation, or public-surface change.

## Scope

- Repo:
- Branch:
- Exact affected files:
- Out of scope:

## Truth Surface

Classify the truth surface affected by this PR:

- [ ] Repo/source truth
- [ ] Validation truth
- [ ] Runtime contract or runtime-state reference
- [ ] Signal/evidence reference
- [ ] Public proof or public wording
- [ ] Reviewer routing / governance documentation
- [ ] Other:

## Cross-Repo Propagation

Cross-repo work aligns by detection ID, artifact ID, proof gate, evidence reference, and downstream truth impact, not by PR number.

- Phase ID:
- Detection / Artifact ID:
- Truth surface changed:
  - [ ] Source
  - [ ] Validation
  - [ ] Runtime
  - [ ] Signal
  - [ ] Evidence
  - [ ] Public Rendering
  - [ ] Reviewer Routing / Claim Control
- Current proof gate:
- Downstream repos affected:
  - [ ] .github
  - [ ] hawkinsoperations-detections
  - [ ] hawkinsoperations-validation
  - [ ] hawkinsoperations-platform
  - [ ] hawkinsoperations-proof
  - [ ] hawkinsoperations-website
  - [ ] None
- Downstream action:
  - [ ] Required
  - [ ] Blocked
  - [ ] Valid no-op
- Valid no-op statement:
- Claim ceiling after this PR:
- Public wording impact:
- Evidence/proof reference:
- Reviewer note:

This PR template section is soft enforcement only. It does not prove or promote runtime-active, signal-observed, public-safe, production, fleet-wide, enterprise-deployed, Cribl-routed, Wazuh-routed, AWS-live, autonomous SOC, AI-approved, AI-decided, analyst-approved, live Splunk firing, public-safe runtime proof, or production AutoSOC status.

## Claim Boundary

State what this PR can safely claim and what it does not prove.

## Testing / Validation

List checks run, checks not run, and any required status checks.

Green CI/status checks are not merge authority.

For command-center, reviewer-route, governance, or proof-boundary changes, run:

`python scripts/verify-command-center-invariants.py`

## Security / Privacy

State whether private-term, public-safety, secret, hostname, LAN IP, raw-log, screenshot, CSV export, or local evidence-path risk was reviewed.

## Human Review Authority

Codex review is AI labor, not human governance.

Visible human GitHub review activity is required before merge when this PR affects governance, proof, validation, detection logic, CI enforcement, website/public wording, inventory, or claim-bearing artifacts.

Solo authority is acceptable when disclosed. Fake independence is not.

Do not use a second GitHub account controlled by Raylee for fake independent approval.

Before merge recommendation, prepare a merge-readiness packet with repo, PR number/link, branch, changed files, merge state, check/status summary, review/comment status, unresolved Codex feedback, unresolved conversations, private-term risk, claim-boundary impact, proof-boundary impact, public surface impact, whether visible human governance review exists, paste-ready Raylee review comment, and final state: MERGE_READY, NEEDS_HUMAN_REVIEW, NEEDS_CHANGES, or BLOCKED.

MERGE_APPROVED is required before merge, auto-merge, or final merge recommendation.

## HawkinsOperations Guardrails

Website/GitHub rendering is not proof.

This PR must not promote runtime-active, signal-observed, evidence-linked public proof, public-safe, production-ready, fleet-wide, Cribl-routed, Wazuh-routed, AWS-live, autonomous SOC, or AI-approved status unless separately supported by scoped evidence and Raylee approval.

## Checklist

- [ ] Exact affected files listed
- [ ] No unrelated dirty state included
- [ ] Claim boundary included
- [ ] Testing/validation listed
- [ ] Command-center invariant check run or explicitly not applicable
- [ ] Private-term/public-safety review completed or explicitly not run
- [ ] No runtime/signal/public-safe overclaim added
- [ ] Required session log appended if this was meaningful work
- [ ] Visible human governance review completed or explicitly not required
- [ ] Codex/bot review comments addressed, dismissed with reason, or marked non-blocking
- [ ] Merge-readiness packet prepared before merge recommendation
