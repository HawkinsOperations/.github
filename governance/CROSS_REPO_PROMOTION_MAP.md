# Cross-Repo Promotion Map

Status: REVIEWER_ROUTING
Trust class: SOURCE_EXISTS
Control type: governance documentation / soft enforcement

## 1. Purpose

This map explains how HawkinsOperations moves bounded truth across organization repositories.

It documents reviewer routing and claim-control expectations. It does not create proof, approve evidence, promote runtime status, or make public claims safe by itself.

## 2. Core Rule

HawkinsOperations uses gate-based propagation, not PR-number alignment.

PR numbers do not need to match across repositories. Cross-repo work is required only when a changed truth surface affects another repository's owned surface.

Website/GitHub rendering is not proof. Public proof ceiling remains `TEST_VALIDATED_SYNTHETIC_SCOPE` for `HO-DET-001` unless proof records say otherwise.

## 3. Truth Surface Map

| Repository | Owns | Does not own |
|---|---|---|
| `.github` | Reviewer routing and claim-control expectations | Runtime truth, signal truth, proof approval, production status |
| `hawkinsoperations-detections` | Detection source truth | Validation result, runtime status, evidence approval, public-safe wording |
| `hawkinsoperations-validation` | Test, fixture, verifier, and behavior truth | Production runtime, signal observation, public proof |
| `hawkinsoperations-platform` | Runtime contracts and integration guardrails | Public-safe runtime proof, detection proof approval |
| `hawkinsoperations-proof` | Evidence records and claim ceilings | Source ownership for other repos, raw private evidence publication |
| `hawkinsoperations-website` | Public rendering only after proof allows wording | Source truth, runtime truth, signal truth, evidence truth |

## 4. Propagation Triggers

Open or update downstream PRs when the changed surface affects another repository's owned truth.

Examples:

- Detection source changes can trigger validation changes when tests, fixtures, schemas, or expected behavior must change.
- Validation outcome changes can trigger proof changes when the claim ceiling, evidence record, or allowed wording changes.
- Platform contract changes can trigger proof changes when runtime guardrails affect claim boundaries.
- Proof record changes can trigger website changes when public wording becomes newly allowed or newly blocked.
- `.github` routing changes can trigger no downstream PR when they only improve navigation and do not alter source, validation, platform, proof, or public wording truth.

## 5. Required Cross-Repo Impact Table

| Changed repo | Check for downstream impact | Downstream PR required when | Valid no-op when |
|---|---|---|---|
| `.github` | Reviewer route, claim-control expectation, public boundary wording | It changes allowed public wording, proof expectations, or repo ownership boundaries | It only improves navigation, layout, or explanation without changing truth |
| `detections` | Source logic, metadata, IDs, expected behavior | Tests, fixtures, proof records, or platform contracts must change to stay accurate | Source-only change does not affect validation, platform, proof, or website claims |
| `validation` | Test result, verifier, fixture, schema, workflow behavior | Proof ceiling or evidence record must reflect a new validated boundary | Validation tooling changes do not alter recorded claim ceilings |
| `platform` | Runtime contract, integration guardrail, deployment boundary | Proof records or website wording would otherwise overclaim runtime or signal status | Contract cleanup does not change public claim boundaries |
| `proof` | Evidence record, claim ceiling, allowed wording, blocked wording | Website or `.github` public routing must reflect a changed public boundary | Proof maintenance preserves the same public ceiling and wording |
| `website` | Public rendering and reviewer-facing wording | Proof must be updated because website wording would otherwise exceed evidence | Website copy stays within already approved proof boundaries |

## 6. Valid No-Op Rule

A documented no-op is valid when a change does not affect another repository's owned truth surface.

The no-op note should state:

- which downstream repository was considered
- why no downstream truth changed
- which claim ceiling remains unchanged
- whether website/GitHub rendering remains non-proof

No-op documentation is preferable to creating empty alignment PRs. Alignment by PR number is not a control.

## 7. Detection Promotion Example using HO-DET-001

`HO-DET-001` is the flagship proof path.

Current public boundary:

| Surface | Current state |
|---|---|
| Detection source | Source exists |
| Splunk source | Source exists |
| Validation | Synthetic validation passed within controlled scope |
| Platform | Runtime contract exists as a non-promotional guardrail |
| Proof | Public ceiling remains `TEST_VALIDATED_SYNTHETIC_SCOPE` |
| Public-safe status | `NOT_PUBLIC_SAFE` |
| Website/GitHub | Rendering and reviewer routing only |

Promotion example:

1. A detection source change lands in `hawkinsoperations-detections`.
2. Validation updates only if expected behavior, fixtures, schemas, or verifier coverage must change.
3. Proof updates only if recorded validation or claim ceilings change.
4. Website updates only if proof allows different public wording.
5. `.github` updates only if reviewer routing or org-level claim-control expectations change.

The public proof ceiling remains `TEST_VALIDATED_SYNTHETIC_SCOPE` unless the proof repo records a reviewed ceiling change.

## 8. Blocked Claim Boundary

This map does not promote or prove:

- runtime-active status
- signal-observed public proof
- public-safe status
- production status
- fleet-wide status
- enterprise-deployed status
- Cribl-routed status
- Wazuh-routed status
- AWS-live status
- autonomous SOC operation
- AI-approved disposition
- AI-decided disposition
- analyst-approved disposition
- production AutoSOC status

These claims remain blocked unless the correct proof record, claim ceiling, privacy review, stale review, and human approval allow them.

## 9. Real Controls Rule

Docs, READMEs, diagrams, issue cards, and websites are not real controls by themselves.

A control becomes real only when it blocks, fails, or forces correction through required review, branch protection, rulesets, blocking CI, deterministic verifiers, typed claim gates, or another enforceable mechanism.

Green CI/status checks are not merge authority. Codex review is AI labor, not human review authority.

## 10. Reviewer Use

Use this map when reviewing a PR that touches source, validation, platform, proof, website, or organization routing.

Reviewer questions:

- Which truth surface changed?
- Which repository owns that truth?
- Does another repository need a downstream PR?
- Is a documented no-op enough?
- Does public wording stay within the current proof ceiling?
- Does the PR preserve that Website/GitHub rendering is not proof?

Final reviewer position should be one of:

- downstream PR required
- documented no-op accepted
- proof boundary unclear
- blocked claim risk present
