# Pull Request Review Authority

Status: REVIEWER_ROUTING
Control type: governance / merge-review routing

This document defines the HawkinsOperations pull request review authority standard for organization-level reviewer routing.

PR review authority is a governance control. It is a real blocking control only when backed by required review, rulesets, branch protection, blocking CI, or another mechanism that blocks, fails, or forces correction.

Green CI/status checks are not merge authority.

Codex review is AI labor, not human review authority.

Visible human GitHub review activity is required before merge when a PR affects governance, proof, validation, detection logic, CI enforcement, website/public wording, inventory, or claim-bearing artifacts.

A submitted GitHub review is review evidence for the merge decision only.

Review evidence does not promote runtime-active, signal-observed, evidence-linked public proof, public-safe, production-ready, fleet-wide, Cribl-routed, Wazuh-routed, AWS-live, autonomous SOC, or AI-approved status.

Solo authority is acceptable when disclosed. Fake independence is not.

A second GitHub account controlled by Raylee must not be used for fake independent approval.

MERGE_APPROVED is required before merge, auto-merge, or final merge recommendation.

Website/GitHub rendering is not proof.

## Merge-Readiness Packet

Before recommending merge, Codex must produce a merge-readiness packet with:

- repo
- PR number/link
- branch
- changed files
- merge state
- check/status summary
- review/comment status
- unresolved Codex feedback
- unresolved conversations
- private-term risk
- claim-boundary impact
- proof-boundary impact
- public surface impact
- whether visible human review activity exists
- paste-ready Raylee review comment
- final state: MERGE_READY, NEEDS_HUMAN_REVIEW, NEEDS_CHANGES, or BLOCKED

## Clean Review Pattern

Use only when the PR facts support it:

```text
Governance review complete.

Scope matches approved paths.
CI/status checks reviewed.
Claim boundary reviewed.
No unsupported promotion introduced.
No private-term/public-safety issue observed.
Approved for merge.
```

If the PR has unresolved claim-boundary, proof-boundary, private-term, public-safety, scope, governance, or CI/status issues, submit Comment or Request changes instead and state the blocker without promoting unsupported status.

## Boundary

This document routes merge governance. It does not prove runtime, signal, evidence, public-safe status, or production readiness.
