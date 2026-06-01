# HawkinsOperations .github

This repository is the HawkinsOperations GitHub organization command center. It owns the organization profile, reviewer routes, governance summaries, and visual maps that explain how the six-repo system works.

The public organization overview is controlled by [profile/README.md](profile/README.md). This repo is a front door, not a proof source: GitHub rendering is not proof.

## Fast Reviewer Path

| Time | Start | What to confirm |
|---:|---|---|
| 30 sec | [profile/START_HERE.md](profile/START_HERE.md) | What HawkinsOperations is, which repo owns truth, and what remains blocked. |
| 3 min | [profile/README.md](profile/README.md) -> [Control Status Matrix](governance/CONTROL_STATUS_MATRIX.md) | Command-center route, proof ceiling, ledger count boundary, and standing controls. |
| 10 min | [Reproducible Reviewer Path](architecture/REPRODUCIBLE_REVIEWER_PATH.md) | Clone-runnable source/validation/proof inspection without private runtime access. |

## Command Center Routes

| Need | Route | Boundary |
|---|---|---|
| First reviewer path | [profile/START_HERE.md](profile/START_HERE.md) | Click path for review/demo; does not promote claims. |
| Org front door | [profile/README.md](profile/README.md) | Reviewer routing only; does not create proof. |
| Six-repo architecture | [architecture/REPO_AUTHORITY_MAP.md](architecture/REPO_AUTHORITY_MAP.md) | Repo ownership map; source does not prove runtime. |
| Proof chain | [architecture/REPRODUCIBLE_REVIEWER_PATH.md](architecture/REPRODUCIBLE_REVIEWER_PATH.md) | Clone-runnable inspection path; no private runtime access. |
| Truth/control status | [governance/CONTROL_STATUS_MATRIX.md](governance/CONTROL_STATUS_MATRIX.md) | Current wording and blockers; soft unless enforced. |
| Standing control registers | [governance/ISSUE_FACTORY_CONTROL_RECEIPTS.md](governance/ISSUE_FACTORY_CONTROL_RECEIPTS.md) | #8 and #10 remain open standing controls unless Raylee approves a replacement standing-control role; governance classification only. |
| Command-center invariants | [governance/COMMAND_CENTER_INVARIANTS.json](governance/COMMAND_CENTER_INVARIANTS.json) and [scripts/verify-command-center-invariants.py](scripts/verify-command-center-invariants.py) | Verifier control for route and claim-boundary invariants; does not promote proof. |
| Visual system map | [wiki/11_ORG_SYSTEM_MAP.md](wiki/11_ORG_SYSTEM_MAP.md) | Docs-as-code map; routing is not proof. |
| Project cockpit | [private org Control Board route](https://github.com/orgs/HawkinsOperations/projects/2) | Coordination-only operating cockpit; project metadata is report-only, not proof, approval, runtime, signal, public-safe status, or merge authority. Project #1 is not an active reviewer route. |
| Proof records | [hawkinsoperations-proof](https://github.com/HawkinsOperations/hawkinsoperations-proof) | Proof records own claim ceilings. |

## Current Boundary

Current proof records live in [hawkinsoperations-proof](https://github.com/HawkinsOperations/hawkinsoperations-proof), and the current HO-DET-001 public ceiling remains `CONTROLLED_TEST_VALIDATED`.

.github is routing/governance only. It does not own proof authority, runtime truth, signal truth, public-safe status, or website rendering truth.

The front-door/status proof ceiling for the command-center and ledger-status route remains `SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY`.

The proof-owned Lifetime Case Ledger public summary currently records a bounded count route only: 4 ledger events, 4 total cases, 0 public-safe cases, and 0 closed cases. Its ledger status remains `NOT_PUBLIC_SAFE`, and its proof ceiling remains `SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY`.

The canonical private HawkinsOperations Control Board is the private org Project #2 route. Project #1 is not an active reviewer route and was not resolvable through the live ProjectV2 API during the current cleanup pass. Project metadata remains coordination-only and does not create proof, approval, runtime truth, signal truth, public-safe status, or merge authority.
