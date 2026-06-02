# HawkinsOperations .github

The HawkinsOperations organization command center and reviewer-routing surface.

The .github is routing/governance only and not proof authority.

## What This Repo Owns

- Organization profile and reviewer routing.
- Governance summaries, control surfaces, and command-center maps.
- Reviewer-facing wording that explains where authority lives.
- The command-center invariant verifier for route and claim-boundary checks.

## What This Repo Does Not Own

- Proof records or proof ceilings.
- Runtime truth or signal truth.
- Public-safe status or public publication approval.
- Merge authority or final disposition authority.
- Website rendering truth.

Evidence and source flow stay separated:

`detection source -> validation behavior -> platform contracts where applicable -> proof records -> public rendering`

## Fast Reviewer Path

| Time | Start | What to confirm |
|---:|---|---|
| 30 sec | [profile/START_HERE.md](profile/START_HERE.md) | What HawkinsOperations is, which repo owns truth, and what remains blocked. |
| 3 min | [profile/README.md](profile/README.md) -> [Control Status Matrix](governance/CONTROL_STATUS_MATRIX.md) | Command-center route, proof ceiling, and standing controls. |
| 10 min | [Reproducible Reviewer Path](architecture/REPRODUCIBLE_REVIEWER_PATH.md) | Clone-runnable source, validation, proof, and rendering review without private runtime access. |

## README / Repo Makeover Order

This is the README/governance cleanup order, not evidence-generation order.

| Order | Repo | Truth surface | Boundary |
|---:|---|---|---|
| 1 | `.github` | Route / governance truth | Routes reviewers and explains authority boundaries; does not prove claims. |
| 2 | `hawkinsoperations-proof` | Claim / proof truth | Owns proof records, proof ceilings, evidence-boundary records, and blocked-claim status. |
| 3 | `hawkinsoperations-platform` | Contract / guardrail truth | Owns schemas, contracts, ledger guardrails, runtime-route guardrails, and non-promotional platform controls. |
| 4 | `hawkinsoperations-validation` | Behavior truth | Owns controlled validation checks, case packets, replay scope, and recorded validation outputs. |
| 5 | `hawkinsoperations-detections` | Source truth | Owns detection source, metadata, source reviewability, and source-level eligibility routing. |
| 6 | `hawkinsoperations-website` | Render truth | Renders public reviewer navigation and bounded wording; rendering is not proof. |

## Command Center Routes

| Need | Route | Boundary |
|---|---|---|
| First reviewer path | [profile/START_HERE.md](profile/START_HERE.md) | Click path for review and demo; does not promote claims. |
| Org front door | [profile/README.md](profile/README.md) | Reviewer routing only; does not create proof. |
| Repository authority map | [architecture/REPO_AUTHORITY_MAP.md](architecture/REPO_AUTHORITY_MAP.md) | Repository ownership map; source does not prove runtime. |
| Proof chain | [architecture/REPRODUCIBLE_REVIEWER_PATH.md](architecture/REPRODUCIBLE_REVIEWER_PATH.md) | Clone-runnable inspection path; no private runtime access. |
| Truth/control status | [governance/CONTROL_STATUS_MATRIX.md](governance/CONTROL_STATUS_MATRIX.md) | Current wording and blockers; soft unless enforced. |
| Standing control registers | [governance/ISSUE_FACTORY_CONTROL_RECEIPTS.md](governance/ISSUE_FACTORY_CONTROL_RECEIPTS.md) | Standing controls and issue receipts; governance classification only. |
| Command-center invariants | [governance/COMMAND_CENTER_INVARIANTS.json](governance/COMMAND_CENTER_INVARIANTS.json) and [scripts/verify-command-center-invariants.py](scripts/verify-command-center-invariants.py) | Route and claim-boundary verifier control; does not promote proof. |
| Visual system map | [wiki/11_ORG_SYSTEM_MAP.md](wiki/11_ORG_SYSTEM_MAP.md) | Docs-as-code map; routing is not proof. |
| Project cockpit | [private org Control Board route](https://github.com/orgs/HawkinsOperations/projects/2) | Canonical private HawkinsOperations Control Board; Project #1 is not an active reviewer route when already established in current `.github` files. Project metadata is coordination-only. |
| Proof records | [hawkinsoperations-proof](https://github.com/HawkinsOperations/hawkinsoperations-proof) | Proof records own claim ceilings. |

## Current Boundary

The current public ceiling for HO-DET-001 remains `CONTROLLED_TEST_VALIDATED`.

The command-center and ledger-status front door remains `SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY`.

`.github` is route/governance truth only. It does not own proof authority, runtime truth, signal truth, public-safe status, merge authority, or public publication approval.

The canonical private HawkinsOperations Control Board is Project #2. Project metadata is coordination-only and does not create proof, approval, runtime truth, signal truth, public-safe status, merge authority, public publication approval, or proof promotion. Project #1 is not an active reviewer route when already established in the current `.github` files.

Current boundary labels:

- `CONTROLLED_TEST_VALIDATED`
- `NOT_PUBLIC_SAFE`
- `BLOCKED`
- `SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY`
- `RENDERING_NOT_PROOF`
- `HUMAN_REVIEW_REQUIRED`

The flow remains:

`detection source -> validation behavior -> platform contracts where applicable -> proof records -> public rendering`

## Blocked Claims

This surface does not claim runtime-active public proof, signal-observed public proof, public-safe runtime proof, production readiness, SOCaaS deployment, autonomous SOC operation, AI-approved disposition, AI-decided disposition, analyst-approved disposition, fleet-wide coverage, customer deployment, live Splunk public proof, live Wazuh public proof, Cribl-routed public proof, Wazuh-routed public proof, AWS-live proof, cloud-live proof, case closure, or public publication approval.

## Related Repositories

| Repo | Truth surface | Boundary |
|---|---|---|
| [hawkinsoperations-proof](https://github.com/HawkinsOperations/hawkinsoperations-proof) | Claim / proof truth | Owns proof records, claim ceilings, and blocked-claim status. |
| [hawkinsoperations-platform](https://github.com/HawkinsOperations/hawkinsoperations-platform) | Contract / guardrail truth | Owns schemas, contracts, and non-promotional platform controls. |
| [hawkinsoperations-validation](https://github.com/HawkinsOperations/hawkinsoperations-validation) | Behavior truth | Owns controlled validation and recorded validation outputs. |
| [hawkinsoperations-detections](https://github.com/HawkinsOperations/hawkinsoperations-detections) | Source truth | Owns detection source and source-level routing. |
| [hawkinsoperations-website](https://github.com/HawkinsOperations/hawkinsoperations-website) | Render truth | Renders public reviewer navigation and bounded wording. |

## Doctrine

AI is labor. Governance is authority.

Build loud. Verify hard. Claim tight. Ship receipts.

Rendering is not proof.
