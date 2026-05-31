# Repository Authority Map

Public-safe status: NOT_PUBLIC_SAFE
Trust class: SOURCE_EXISTS after creation
Control type: soft enforcement

## Purpose

This map defines what each HawkinsOperations organization repository may own. It prevents source, validation, platform, proof, and website material from claiming another truth surface.

No repository may claim another repository's authority. Repository source is not runtime truth. Website presentation is not proof.

Reviewer entry point: [START_HERE.md](../profile/START_HERE.md). Current control summary: [CONTROL_STATUS_MATRIX.md](../governance/CONTROL_STATUS_MATRIX.md).

HOD-001 baseline validation/proof does not promote HO-DET-001.

## Authority Summary

| Repository | Authority plane | Owns | Boundary |
| --- | --- | --- | --- |
| `.github` | Reviewer routing / governance shell | Organization profile, reviewer routes, governance summaries, and control-panel navigation. | Not proof; does not prove source, runtime, signal, evidence, public-safe status, or production readiness. |
| `hawkinsoperations-detections` | Source truth | Detection source logic and source ownership trail. | Source does not prove validation, runtime, signal, or public proof. |
| `hawkinsoperations-validation` | Validation truth | Fixtures, validators, case packets, deterministic checks, and workflow source. | Validation does not prove runtime deployment, public signal, or public-safe status. |
| `hawkinsoperations-platform` | Contracts / orchestration / control logic | Runtime contracts, interface boundaries, and non-promotional guardrails. | Contracts do not prove public proof, production readiness, or current runtime state. |
| `hawkinsoperations-proof` | Proof records / evidence truth | Proof records, claim ceilings, evidence boundary records, and cited case packets. | Proof records do not publish raw private evidence or raise ceilings by presentation. |
| `hawkinsoperations-website` | Public rendering only | Public reviewer navigation and rendered wording. | Rendering is not proof and cannot approve a claim. |

## Public Readiness Summary

| Repository | Owns | Must Not Own | Public Readiness Status | Blocked Claims |
| --- | --- | --- | --- | --- |
| `.github` | Public organization framing and sanitized governance summaries. | Runtime status, detection validation, evidence approval, private operations detail. | NOT_PUBLIC_SAFE until reviewed and approved. | Organization profile proves runtime, proof, or production readiness. |
| `hawkinsoperations-detections` | Detection source files and detection-authoring structure. | Runtime-active status, signal observation, public proof, platform state. | Source-oriented until validated and linked. | A detection file exists, therefore it is deployed or active. |
| `hawkinsoperations-validation` | Tests, schemas, validation checks, and validation workflow source. | Production status, runtime deployment, signal truth, evidence approval. | Validation-oriented until recorded results are linked. | A validator exists, therefore detections are proven in runtime. |
| `hawkinsoperations-platform` | Platform architecture, stack truth tracking, and environment boundary documentation. | Detection proof, public proof, sensitive runtime exports, private host details. | Architecture-oriented until runtime evidence is reviewed. | Platform docs prove current deployment state. |
| `hawkinsoperations-proof` | Proof contracts, evidence indexes, public-safe records, and claim linkage structure. | Raw private evidence publication, runtime operation, source ownership for other repos. | Proof-oriented only for reviewed and scoped records. | Evidence-linked material is automatically public-safe. |
| `hawkinsoperations-website` | Public rendering of approved content. | Source truth, runtime truth, evidence truth, claim approval. | Rendering-oriented after public claim review. | Website presentation proves a claim by itself. |

## Cross-Repository Rules

- Detection source requires validation before test claims.
- Test results require recorded output before validation claims.
- Runtime claims require runtime evidence.
- Signal claims require observed telemetry, alert, log, or output context.
- Evidence claims require preserved and linked support.
- Public claims require public claim review and approval.

## Blocked Organization-Level Claims

Do not claim:

- production-ready status
- fully rebuilt status
- autonomous AI security operations
- runtime-active detections without runtime evidence
- successor-system ownership of legacy metrics
- public proof from website or README presentation alone
- public safety from evidence linkage alone

## Control Status

This document is soft enforcement. It becomes real control only when repository checks, hooks, CI, or required reviews block or fail violations.
