# Reproducible Reviewer Path

Status: PHASE_1_DOCUMENTED_CONTRACT_ONLY
Control type: reviewer reproduction path
Trust class: SOURCE_EXISTS after merge

## Purpose

This path gives reviewers a clone-runnable route through the six HawkinsOperations repositories without treating `.github`, CI, proof, platform, or website rendering as stronger truth than they can support.

Website/GitHub rendering is not proof. Public surfaces route to proof records. Required checks matter only when they actually appear, run, and pass. Codex is AI labor, not human governance.

## Clone All Six Repos

From an empty organization workspace:

```powershell
mkdir HawkinsOperations
cd HawkinsOperations
git clone https://github.com/HawkinsOperations/.github.git .github
git clone https://github.com/HawkinsOperations/hawkinsoperations-detections.git
git clone https://github.com/HawkinsOperations/hawkinsoperations-validation.git
git clone https://github.com/HawkinsOperations/hawkinsoperations-platform.git
git clone https://github.com/HawkinsOperations/hawkinsoperations-proof.git
git clone https://github.com/HawkinsOperations/hawkinsoperations-website.git
```

Expected sibling layout:

```text
HawkinsOperations/
  .github/
  hawkinsoperations-detections/
  hawkinsoperations-validation/
  hawkinsoperations-platform/
  hawkinsoperations-proof/
  hawkinsoperations-website/
```

## Reviewer Commands Available Today

These commands use source-controlled files only. They do not require private runtime access, private evidence, workflow dispatch, GitHub settings access, or local operator-only paths.

### Organization Control Plane

```powershell
cd .github
git status -sb
git diff --check
```

Read:

- `profile/START_HERE.md`
- `governance/CONTROL_STATUS_MATRIX.md`
- `governance/PR_REVIEW_AUTHORITY.md`
- `architecture/REPO_AUTHORITY_MAP.md`
- `governance/ORG_CI_CD_AUTHORITY_CONTRACT.md`
- `governance/ORG_REQUIRED_CHECKS_MATRIX.yml`
- `governance/PROMOTION_LADDER_CONTRACT.yml`
- `architecture/REPRODUCIBLE_REVIEWER_PATH.md`

### Detection Source Plane

```powershell
cd ..\hawkinsoperations-detections
git status -sb
python .\scripts\verify_detection_contract.py
```

Review current detection source and boundaries in:

- `detections/DETECTION_FACTORY_INDEX.md`
- `detections/successor/ho-det-012/`
- `detections/identity/id-det-002/`
- `detections/identity/id-det-003/`
- `detections/identity/id-det-004/`

### Validation Behavior Plane

```powershell
cd ..\hawkinsoperations-validation
git status -sb
python -B scripts\verify_validation_registry.py
python -B scripts\verify_all_validation_packages.py
python -B scripts\verify_validation_contract.py
python -B scripts\validate-id-det-002.py
python -B scripts\verify-id-det-002-result-parity.py
python -B scripts\scan-id-det-002-claim-boundaries.py
python -B scripts\validate-id-det-003.py
python -B scripts\verify-id-det-003-result-parity.py
python -B scripts\scan-id-det-003-claim-boundaries.py
python -B scripts\validate-id-det-004.py
python -B scripts\verify-id-det-004-result-parity.py
python -B scripts\scan-id-det-004-claim-boundaries.py
python -B scripts\validate-ho-det-012.py --source-contract skip-if-missing
python -B scripts\verify-ho-det-012-result-parity.py
python -B scripts\scan-ho-det-012-claim-boundaries.py
```

Report-only parity command, if the reviewer has all six sibling repos cloned:

```powershell
python -B scripts\verify_cross_repo_claim_parity.py --repo-root .. --report-only
```

Report-only output is not fail-closed enforcement.

### Platform Boundary and Visibility Plane

```powershell
cd ..\hawkinsoperations-platform
git status -sb
python -B scripts\ho_factory.py status --detection ID-DET-002 --repo-root .. --format json
python -B scripts\ho_factory.py status --detection ID-DET-003 --repo-root .. --format json
python -B scripts\ho_factory.py status --detection ID-DET-004 --repo-root .. --format json
python -B scripts\ho_factory.py status --detection HO-DET-012 --repo-root .. --format json
python -B scripts\ho_factory.py plan --detection ID-DET-002 --repo-root .. --format json
python -B scripts\ho_factory.py plan --detection ID-DET-003 --repo-root .. --format json
python -B scripts\ho_factory.py plan --detection ID-DET-004 --repo-root .. --format json
python -B scripts\ho_factory.py plan --detection HO-DET-012 --repo-root .. --format json
```

Platform output is status/plan visibility unless the relevant proof record and promotion gates say otherwise.

### Proof Ceiling Plane

```powershell
cd ..\hawkinsoperations-proof
git status -sb
python scripts\verify_proof_integrity.py
```

Expected Phase 1 gap:

- ID-DET-002, ID-DET-003, and ID-DET-004 proof index entries and proof records are pending.
- HO-DET-012 proof parity is pending if public routing is desired.

### Website Rendering Plane

```powershell
cd ..\hawkinsoperations-website
git status -sb
npm install
npm run check:site
npm run build
```

Expected Phase 1 gap:

- ID-DET-002, ID-DET-003, and ID-DET-004 public website routes are pending.
- HO-DET-012 appears in current website source data, but proof and website parity remain required before any public proof or public-safe wording can be claimed.

## Private-Only Commands Excluded

The public clone path excludes:

- runtime system access
- workflow dispatch
- private evidence exports
- local operator-only evidence staging paths
- private hostnames, IPs, usernames, tokens, credentials, or screenshots
- Splunk, Wazuh, Cribl, Security Onion, IdP, or SIEM live queries
- commands that publish evidence or promote proof/public-safe status
- any command that would change GitHub settings, branch protection, rulesets, or repository secrets

Private evidence can inform future review only after privacy review, stale review, evidence linkage review, wording review, and Raylee approval.

## Command-Center Invariant Verifier

The `.github` command-center route has a local invariant verifier for reviewer-route and claim-boundary checks:

```powershell
cd .github
python scripts\verify-command-center-invariants.py
```

Expected output fields:

```text
COMMAND_CENTER_INVARIANTS=PASS
checked_files=<count>
```

This verifier proves only that checked command-center route files and invariant wording passed. It does not prove runtime truth, signal truth, public-safe status, Project-board approval, merge authority, or public proof.

## Current Gap Summary

| Item | Current routed state | Remaining gap |
| --- | --- | --- |
| ID-DET-002 | Source, controlled-test validation, and platform status/plan visibility are documented as carried by PRs #27, #46, and #29. | Proof record/index and website route are pending. |
| ID-DET-003 | Source, controlled-test validation, and platform status/plan visibility are documented as carried by PRs #27, #46, and #29. | Proof record/index and website route are pending. |
| ID-DET-004 | Source, controlled-test validation, and platform status/plan visibility are documented as carried by PRs #27, #46, and #29. | Proof record/index and website route are pending. |
| HO-DET-012 | Source, validation, and platform progress exist. | Proof and website parity are still required if public routing is desired. |
| Cross-repo parity | Report-only scanner exists in validation. | Fail-closed promotion requires separate approval. |

## Claim Boundary

This reviewer path supports reproducible inspection of source-controlled contracts and deterministic checks. It does not prove runtime-active public proof, signal-observed public proof, public-safe proof, production-ready status, fleet-wide coverage, complete identity coverage, live IdP proof, live SIEM proof, live Splunk/Wazuh/Cribl/Security Onion proof, autonomous SOC, AI-approved disposition, analyst-approved disposition, customer-ready product, SOCaaS availability, or public evidence linkage unless the proof index supports it.

