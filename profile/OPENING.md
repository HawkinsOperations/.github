# Opening commit

**Date:** 2026-04-23
**Location:** github.com/HawkinsOperations

---

## What this organization is

The HawkinsOperations organization is the successor home of the HawkinsOps system. It begins on 2026-04-23. It replaces the single-repository V1 at [`raylee-hawkins/HawkinsOperations`](https://github.com/raylee-hawkins/HawkinsOperations) with a five-repository architecture scoped to single audiences and single change velocities, with CI-enforced governance in place of markdown-as-contract.

## Why now

Two independent audits on 2026-04-19 and 2026-04-20 surfaced the same structural conclusion: the V1 tree had carried five trust classes, three proof surfaces, and four metrics endpoints under one git history, and operator vigilance had become the load-bearing safety mechanism. The March 2026 ledger silent-reseed and the April 18 AutoSOC redaction nested-output bug were the canonical evidence that convention-based governance would not scale further. The full diagnosis is documented in the V1 retirement notice at [`raylee-hawkins/HawkinsOperations/docs/V1_RETIREMENT.md`](https://github.com/raylee-hawkins/HawkinsOperations/blob/main/docs/V1_RETIREMENT.md).

## Thesis

The dominant industry frames for AI in security operations are either hand-waving about reliability or treating large language models as opaque copilots attached to a human analyst. Both frames fail at scale. Hand-waving produces pipelines that silently drift. Copilot framing underuses the model while still inheriting its unreliability.

HawkinsOperations starts from a different premise. Large language models are unreliable labor. Unreliable labor, treated as labor, is a problem the manufacturing world solved decades ago through management systems — intake controls, standard work, verification gates, escalation paths, evidence capture, regression harnesses, and post-incident review. The IATF 16949 and ISO 9001 frameworks that govern Tier 1 automotive production floors are, at their core, systems for extracting reliable output from unreliable inputs. Applied to an AI triage workforce running against a live SOC pipeline, the same discipline produces a system that auto-closes what should be closed, escalates what should not, and leaves an audit trail for every decision. The domain changed. The discipline did not.

The operator-hours argument is the spine. The discipline is enforced by the work of building and running this system, under real shifts and real constraints. The thesis is not opinion; it is the structural commitment this organization is built around.

## Five-repo architecture

| Repository | Responsibility | Primary audience | Change velocity |
|---|---|---|---|
| `hawkinsoperations-detections` | Sigma, Wazuh XML, Splunk SPL rule sources | Engineers | High |
| `hawkinsoperations-validation` | Regression harnesses, rule-firing tests, FP/TP tracking | Automation | High |
| `hawkinsoperations-platform` | Pipeline control, AutoSOC orchestration, MCP servers | Engineers | Medium |
| `hawkinsoperations-proof` | Verified counts, case studies, evidence bundles | Reviewers | Low |
| `hawkinsoperations-website` | Source for the successor public site | Visitors | Medium |

Detections change weekly. Proof changes quarterly. Mixing them in one repository produced the commit-history contamination and the truth-surface ambiguity documented in the V1 retirement notice. The split makes each surface legible on its own terms and enforces at the boundary what V1 treated as convention.

## What is live today

The organization profile is live. The five repositories exist as scoped shells with governance documentation and the structural commitments spelled out. The V1 repository remains the canonical public surface for operational evidence during the migration, and [hawkinsops.com](https://hawkinsops.com) remains the canonical home for live metrics.

## What is not yet live

Detection content migration is staged, not complete. The validation replay harness is under construction. The publish-bundle build from the proof repo to the website repo is specified but not yet wired end-to-end. Until the full chain is in place, the V1 repo and hawkinsops.com are the surfaces that carry evidence.

## What this organization does not claim yet

This organization is architecture-in-progress, not a finished system. Canonical operational numbers live at [hawkinsops.com](https://hawkinsops.com) and in the V1 repo's PROOF_PACK. Any number in this organization that disagrees with the site is stale; the site wins. This opening commit dates the architectural decision. It does not claim the architecture is proven.

## Contact

- Current system: [hawkinsops.com](https://hawkinsops.com)
- V1 repository: [raylee-hawkins/HawkinsOperations](https://github.com/raylee-hawkins/HawkinsOperations)
- Public review layer: [rayleeops.com](https://rayleeops.com) — The Ledger
- Methodology paper: [`rayleeops/methodology.md`](https://github.com/raylee-hawkins/rayleeops/blob/main/methodology.md)
- Email: raylee@hawkinsops.com
- LinkedIn: [linkedin.com/in/raylee-hawkins](https://linkedin.com/in/raylee-hawkins)

---

*This document dates and signs the architectural decision. The organization profile README carries the ongoing thesis and the detailed structural commitments. Both documents are read together.*
