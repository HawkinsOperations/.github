# Organization CI/CD Authority Contract

Status: PHASE_1_DOCUMENTED_CONTRACT_ONLY
Control type: org-level CI/CD authority routing
Trust class: SOURCE_EXISTS after merge

## Purpose

This contract documents how the HawkinsOperations organization treats `.github` as the CI/CD control-plane contract and reviewer entry point. Phase 1 is documentation only.

This file does not create reusable workflows, change branch protection, change rulesets, prove runtime state, publish evidence, promote proof, or make anything public-safe.

## Operating Doctrine

Agents generate work.
Repositories own truth.
CI checks enforce gates.
Proof records authorize claim ceilings.
Website renders only approved public state.
Human review remains promotion authority.

Green CI is not authority. Codex is AI labor, not human governance. Required checks matter only when they actually appear, run, and pass in the relevant pull request or protected branch context.

Docs and diagrams are routing material until backed by checks, required review, branch protection, rulesets, or another fail-closed control. Report-only scanners are not fail-closed controls. Website rendering is not proof.

## Repository Governance Ladder

The organization-level governance ladder is:

```text
.github -> platform -> detections -> validation -> proof -> website
```

This ladder describes authority routing:

| Layer | Owner repo | Owns | Does not prove |
| --- | --- | --- | --- |
| Organization control plane | `.github` | Reviewer routing, CI/CD contract docs, required-check matrix, promotion ladder language. | Detection correctness, validation results, runtime state, signal observation, evidence linkage, public-safe status. |
| Runtime and agent boundary plane | `hawkinsoperations-platform` | Platform contracts, runtime/agent boundary schemas, status/plan visibility, private-review support lanes. | Detection source truth, validation pass/fail truth, public proof, production deployment, public-safe runtime evidence. |
| Detection source plane | `hawkinsoperations-detections` | Detection source files, detection metadata, source status, blocked-claim source ceilings. | Controlled-test validation, runtime activity, signal observation, proof status, public-safe status. |
| Validation behavior plane | `hawkinsoperations-validation` | Deterministic validators, fixtures, validation reports, claim-boundary scanners, report-only parity checks. | Runtime activity, signal observation, public proof, public-safe status, production coverage. |
| Proof ceiling plane | `hawkinsoperations-proof` | Proof records, proof indexes, claim ceilings, public-proof linkage after review. | Raw private evidence publication, runtime operation, website presentation. |
| Public rendering plane | `hawkinsoperations-website` | Approved public rendering and reviewer routes to source, validation, and proof records. | Proof by itself, runtime truth, signal truth, evidence truth, claim approval. |

## Detection Evidence Chain

The detection evidence chain is:

```text
.github policy -> detections source -> validation behavior -> platform visibility/runtime contracts -> proof ceiling -> website rendering
```

The chain separates two appearances of platform:

- Platform appears early for runtime and agent boundary contracts. This is where private runtime receipt shape, status metadata, and agent support boundaries are constrained before any claim can move outward.
- Platform appears after validation for detection status visibility. This is where a validated source can be surfaced as status or plan visibility without becoming proof or public-safe by itself.

`.github` is governance and control-plane routing. It can say what the organization requires, where reviewers should look, and which checks should become authoritative. It is not proof truth.

Detection source can support `SOURCE_EXISTS`. Validation behavior can support controlled-test validation only when the validator, fixtures, and report exist and pass. Platform visibility can describe status and next gates without widening proof. Proof records authorize public claim ceilings. Website rendering only presents approved public state.

## Current-State Notes

These notes are recorded for Phase 1 routing. They do not promote any repository or detection beyond the proof records and checks that actually exist.

- A historical mission audit reported its then-scoped repository set as clean, synced, and carrying zero open PRs. Treat that as historical audit context, not proof of current or future state; the current HawkinsOperations authority model contains exactly seven repositories.
- Detections PR #27 carried ID-DET-002, ID-DET-003, and ID-DET-004 source.
- Validation PR #46 carried ID-DET-002, ID-DET-003, and ID-DET-004 controlled-test validation.
- Platform PR #29 carried ID-DET-002, ID-DET-003, and ID-DET-004 status/plan visibility.
- Proof records, proof cards, and proof-index entries now exist for ID-DET-002, ID-DET-003, and ID-DET-004, each bounded to its recorded controlled-test ceiling.
- Website public routes for ID-DET-002, ID-DET-003, and ID-DET-004 are pending.
- HO-DET-012 has source, controlled validation, platform controls, a proof record, a proof card, and bounded website summary; runtime, signal, and public-safe promotion remain separately gated.
- Cross-repo parity is report-only unless later promoted to fail-closed under separate approval.

## Phase 2A Validation Enforcement

Phase 2A landed in `hawkinsoperations-validation` through PR #47 and merge commit `e3f9087c0c63c88ef29d0709e335175b167ce624`.

What it proves:

- `baseline-hero-validation-contract` now appears on every validation pull request and main push because the baseline workflow no longer depends on fragile PR path filters.
- The validation repository has `validation/VALIDATION_REGISTRY.yml` as a source-controlled registry for validation packages.
- `scripts/verify_validation_registry.py` fails closed for malformed registry entries, missing required files, duplicate detection IDs, unknown proof ceilings, public-safe promotion, runtime/signal promotion, and count drift where applicable.
- `scripts/verify_all_validation_packages.py` runs registered validators, parity checks, and claim-boundary checks for the registry scope.
- Source-backed packages keep local/full-org source dependency checks required by default, while isolated CI may skip only the source-contract portion when the registry explicitly opts the package into `ci_source_dependency_mode=skip_if_missing`.

What it does not prove:

- It does not prove runtime-active public proof.
- It does not prove signal-observed public proof.
- It does not prove public-safe proof.
- It does not prove live IdP, SIEM, Splunk, Wazuh, Cribl, or Security Onion operation.
- It does not prove production-ready, fleet-wide, autonomous SOC, AI-approved disposition, or analyst-approved disposition status.

This is `VALIDATION_REGISTRY_ENFORCED` and `CHECK_ENFORCED_FOR_VALIDATION_REGISTRY_SCOPE` only. It can support `CONTROLLED_TEST_VALIDATED` where the validation records already support that ceiling, but it does not promote proof, runtime, signal, or public-safe state.

The next gate is the proof status index because proof records, not validation checks, authorize public claim ceilings. The control plane should next record which validation-backed detections have proof-index support and which remain `NOT_PUBLIC_SAFE`.

## Phase 1 Boundary

Phase 1 may document:

- which repo owns each truth surface
- which observed checks exist today
- which checks are report-only versus fail-closed
- which blocked claims must stay blocked
- which future verifier should make the chain reproducible

Phase 1 may not:

- create reusable workflows
- edit `.github/workflows`
- change GitHub settings, branch protection, or rulesets
- dispatch workflows
- publish evidence
- promote proof or public-safe status
- change website content
- claim runtime-active, signal-observed, production-ready, or fleet-wide status

## Blocked Claims

The organization-level control plane must not claim:

- runtime-active public proof
- signal-observed public proof
- public-safe proof
- production-ready status
- fleet-wide coverage
- complete identity coverage
- live IdP proof
- live SIEM proof
- live Splunk, Wazuh, Cribl, or Security Onion proof
- autonomous SOC
- AI-approved disposition
- analyst-approved disposition
- customer-ready product
- SOCaaS availability
- public evidence linkage unless the proof index supports it

## Promotion Rule

No public or proof-facing claim may inherit truth just because an upstream repo has text, source, a passing check, or a rendered page.

Promotion requires the owning truth surface, deterministic checks where applicable, proof-record linkage where applicable, blocked-claim review, private-term review, and human review. Raylee remains the promotion authority.

