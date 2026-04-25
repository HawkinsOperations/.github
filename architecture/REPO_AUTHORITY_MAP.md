# Repository Authority Map

Status: PUBLIC_SAFE_CANDIDATE
Trust class: SOURCE_EXISTS after creation
Control type: soft enforcement

## Purpose

This map defines what each HawkinsOperations organization repository may own. It prevents source, validation, platform, proof, and website material from claiming another truth surface.

No repository may claim another repository's authority. Repository source is not runtime truth. Website presentation is not proof.

## Authority Summary

| Repository | Owns | Must Not Own | Public Readiness Status | Blocked Claims |
| --- | --- | --- | --- | --- |
| `.github` | Public organization framing and sanitized governance summaries. | Runtime status, detection validation, evidence approval, private operations detail. | Public-safe candidate after review. | Organization profile proves runtime, proof, or production readiness. |
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