# Control Status Matrix

Status: REVIEWER_ROUTING
Control type: reviewer routing and claim-boundary summary

This matrix states what each control or artifact can safely say today. Governance documents are soft routing unless they block, fail, or force correction through a check, workflow, hook, or required review.

| Control / Artifact | Owner repo | Current status | Trust class | Real control? | Evidence path / link | Allowed wording | Blocked wording | Next gate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Organization profile | `.github` | soft routing only | SOURCE_EXISTS | No, soft routing only | `profile/README.md` | "The profile routes reviewers to truth boundaries." | "The profile proves runtime, validation, or public proof." | Keep links current and reviewed. |
| Governance summary | `.github` | soft enforcement | SOURCE_EXISTS | No, unless backed by blocking checks | `governance/GOVERNANCE_SUMMARY.md` | "Governance summary describes expected gates." | "Governance text alone is a real control." | Add checks or required review that fail violations. |
| Repo authority map | `.github` | soft enforcement | SOURCE_EXISTS | No, unless backed by blocking checks | `architecture/REPO_AUTHORITY_MAP.md` | "The map defines repository ownership boundaries." | "The map proves a repo complied." | Add enforceable checks for boundary violations. |
| Website | `hawkinsoperations-website` | rendering only | SOURCE_EXISTS | No | [hawkinsoperations.com](https://hawkinsoperations.com) | "The website renders reviewed public wording." | "Website presentation proves source, runtime, signal, or evidence truth." | Link claims to reviewed proof records. |
| HO-DET-001 source | `hawkinsoperations-detections` | SOURCE_EXISTS | SOURCE_EXISTS | No | `detections/successor/ho-det-001/rule.yml` | "HO-DET-001 source exists." | "HO-DET-001 is validated, active, or public-safe." | Static review against source and rule contract. |
| HO-DET-001 static review | `hawkinsoperations-validation` / `hawkinsoperations-proof` | NOT_SATISFIED | UNKNOWN | No | No promoted static review linked | "Static review is required." | "HO-DET-001 passed static review." | Create and link static review result. |
| HO-DET-001 validation plan | `hawkinsoperations-validation` | NOT_SATISFIED | UNKNOWN | No | No HO-DET-001 validation plan linked | "Validation planning is pending." | "A validation plan is defined for HO-DET-001." | Define positive and negative validation cases. |
| HO-DET-001 validation result | `hawkinsoperations-validation` / `hawkinsoperations-proof` | NOT_SATISFIED | UNKNOWN | No | No HO-DET-001 validation result linked | "Validation result is not proven." | "HO-DET-001 passed validation." | Run validation and preserve result output. |
| HO-DET-001 runtime | `hawkinsoperations-platform` | NOT_SATISFIED | UNKNOWN | No | No runtime evidence linked | "Runtime status is unknown." | "HO-DET-001 is runtime-active." | Preserve deployment or enablement evidence. |
| HO-DET-001 signal | `hawkinsoperations-proof` | NOT_SATISFIED | UNKNOWN | No | No signal evidence linked | "Signal observation is not proven." | "HO-DET-001 has observed signal." | Preserve telemetry, alert, log, or search evidence. |
| HO-DET-001 evidence linkage | `hawkinsoperations-proof` | NOT_SATISFIED | UNKNOWN | No | [HO-DET-001 proof record](https://github.com/HawkinsOperations/hawkinsoperations-proof/blob/main/proof/records/HO-DET-001.md) | "Evidence linkage is pending." | "HO-DET-001 is evidence-linked." | Link reviewed evidence item IDs to supported claims. |
| HO-DET-001 public-safe | `hawkinsoperations-proof` | BLOCKED | NOT_PUBLIC_SAFE | No | No public-safe approval linked | "Public-safe status is blocked pending review and approval." | "HO-DET-001 is PUBLIC_SAFE." | Complete evidence linkage, stale review, privacy review, wording review, and approval. |
| HOD-001 baseline proof chain | `hawkinsoperations-proof` | separate baseline only | VALIDATED_INTERNAL for its own scoped baseline artifacts only if record says so | Yes only within its recorded baseline scope | Proof ledger and HOD-001 baseline artifacts in `hawkinsoperations-proof` | "HOD-001 baseline artifacts are separate reference material." | "HOD-001 validates or promotes HO-DET-001." | Map any reusable findings through successor review. |
| Governance workflows if present | owning repo where workflow runs | real only for the narrow files/checks they block | CHECK_ENFORCED only in checked scope | Yes, only when they block or fail violations | Repository workflow files and check output | "This workflow blocks the exact checked violation." | "A workflow proves broad governance compliance." | Expand checks and record pass/fail output. |

## Current HO-DET-001 Ceiling

HO-DET-001 remains SOURCE_EXISTS. The next gate is static review and validation planning, not runtime, signal, evidence-linked, or public-safe promotion.
