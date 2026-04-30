# HawkinsOperations Organization System Map

Status: PUBLIC_SAFE_CANDIDATE
Trust class: SOURCE_EXISTS
Control type: reviewer routing / soft enforcement
Scope: Explains organization structure, repo ownership, truth surfaces, promotion flow, and control boundaries.
Can prove: This map exists and summarizes current public-safe governance routing.
Cannot prove: Runtime state, signal observation, evidence approval, production readiness, fleet coverage, Cribl routing, Wazuh routing, or public-safe proof.

## Purpose

This page is the visual operating map for HawkinsOperations V2.

It is a docs-as-code map, not a native GitHub Wiki page, so it remains reviewable through normal repository governance.

This map is explanation and reviewer routing only. It does not create proof, promote artifacts, approve evidence, or make runtime claims public-safe.

## One-Sentence Model

HawkinsOperations separates source, validation, runtime, signal, evidence, public proof, and legacy reference surfaces so no claim is promoted beyond what its evidence supports.

## Diagram: Organization Repo Map

```mermaid
flowchart LR
    org[".github<br/>org framing<br/>public-safe governance summaries<br/>reviewer routing"]
    det["hawkinsoperations-detections<br/>detection source only"]
    val["hawkinsoperations-validation<br/>tests / schemas / validation checks only"]
    plat["hawkinsoperations-platform<br/>platform architecture<br/>stack truth tracking<br/>runtime boundary docs"]
    proof["hawkinsoperations-proof<br/>proof records<br/>claim maps<br/>evidence indexes<br/>public-safe records"]
    web["hawkinsoperations-website<br/>public rendering only"]

    org --> det
    org --> val
    org --> plat
    org --> proof
    org --> web

    det --> val
    val --> proof
    plat --> proof
    proof --> web

    web -. "Warning: website does not prove runtime" .-> proof
    det -. "Warning: source does not prove deployment" .-> plat
    val -. "Warning: validation does not prove runtime" .-> plat
    proof -. "Warning: raw private evidence is not published" .-> web
    org -. "Warning: routing is not compliance unless checks block violations" .-> proof
```

## Diagram: Truth Surface Flow

```mermaid
flowchart TD
    idea["Idea / Draft"]
    source["Source Truth"]
    static["Static Validation"]
    testDefined["Test Defined"]
    testValidated["Test Validated"]
    runtime["Runtime Truth"]
    signal["Signal Truth"]
    evidence["Evidence Truth"]
    publicProof["Public Proof"]
    legacy["Legacy Reference<br/>side lane"]

    idea --> source
    source --> static
    static --> testDefined
    testDefined --> testValidated
    testValidated --> runtime
    runtime --> signal
    signal --> evidence
    evidence --> publicProof

    legacy -. "must be reclassified before V2 use" .-> idea
    testValidated --> runtimeGate{"runtime evidence required<br/>before runtime claims"}
    runtimeGate --> runtime
    runtime --> signalGate{"observed telemetry/output required<br/>before signal claims"}
    signalGate --> signal
    signal --> evidenceGate{"preserved linked evidence required<br/>before evidence claims"}
    evidenceGate --> evidence
    evidence --> publicGate{"reviewed wording<br/>privacy review<br/>stale review<br/>approval required"}
    publicGate --> publicProof
```

## Diagram: Detection Proof Ladder

```mermaid
flowchart TD
    l0["0 IDEA"]
    l1["1 SOURCE_EXISTS"]
    l2["2 STATIC_VALIDATED"]
    l3["3 TEST_DEFINED"]
    l4["4 TEST_VALIDATED"]
    l5["5 RUNTIME_ACTIVE"]
    l6["6 SIGNAL_OBSERVED"]
    l7["7 EVIDENCE_LINKED"]
    l8["8 PUBLIC_SAFE"]

    l0 --> l1 --> l2 --> l3 --> l4 --> l5 --> l6 --> l7 --> l8
    current["HO-DET-001 current public repo proof level:<br/>TEST_VALIDATED_SYNTHETIC_SCOPE"]
    current -. "inside recorded synthetic validation scope" .-> l4
    blocked["Public runtime-active, public signal-observed,<br/>public evidence-linked, and public-safe claims remain blocked"]
    l4 -. "private controlled lab runtime match exists locally,<br/>but public promotion requires review" .-> blocked
```

HO-DET-001 current public repo proof level: TEST_VALIDATED_SYNTHETIC_SCOPE.

Private controlled lab runtime match exists locally, but public runtime-active, public signal-observed, public evidence-linked, and public-safe claims remain blocked pending reviewed wording, privacy review, stale review, evidence linkage review, and Raylee approval.

## Diagram: Public Claim Gate

```mermaid
flowchart TD
    claim["Candidate Claim"]
    surface["Identify truth surface"]
    path["Find source path / evidence path"]
    trust["Check trust class"]
    allowed["Check allowed wording"]
    blocked["Check blocked wording"]
    privacy["Privacy review"]
    stale["Stale review"]
    approval["Raylee approval"]
    safe["Public-safe wording"]

    claim --> surface --> path --> trust --> allowed --> blocked --> privacy --> stale --> approval --> safe

    blocked --> stop1["Blocked wording: local paths"]
    blocked --> stop2["Blocked wording: LAN IPs"]
    blocked --> stop3["Blocked wording: raw logs"]
    blocked --> stop4["Blocked wording: raw screenshots"]
    blocked --> stop5["Blocked wording: encoded payloads"]
    blocked --> stop6["Blocked wording: raw CSVs"]
    blocked --> stop7["Blocked wording: private career details"]
    blocked --> stop8["Blocked wording: unreviewed evidence"]
    blocked --> stop9["Blocked wording: production / fleet / public-safe overclaims"]
```

## Diagram: Control Reality Map

```mermaid
flowchart LR
    report["REPORT_ONLY<br/>describes or summarizes"]
    soft["SOFT_ENFORCEMENT<br/>guidance or routing exists"]
    real["REAL_CONTROL<br/>blocks, fails, or forces correction"]

    gov["Governance summary<br/>soft unless backed by checks"]
    auth["Repo authority map<br/>soft unless backed by checks"]
    website["Website<br/>rendering only"]
    workflow["GitHub Action that fails unsafe wording<br/>real only in checked scope"]
    review["Required review / CODEOWNERS<br/>real only if enforced"]
    branch["Branch protection<br/>real only if it blocks bypass"]

    report --> website
    soft --> gov
    soft --> auth
    real --> workflow
    real --> review
    real --> branch
```

## Diagram: Reviewer Navigation Path

```mermaid
flowchart TD
    profile["Reviewer lands on org profile"]
    start["START_HERE"]
    map["Org System Map"]
    authority["Repo Authority Map"]
    source["Detection source"]
    validation["Validation artifacts"]
    proof["Proof record"]
    website["Website rendering"]
    boundaries["Claim boundaries"]
    warning["Warning: website is last-mile rendering, not proof"]

    profile --> start --> map --> authority --> source --> validation --> proof --> website --> boundaries
    website -.-> warning
```

## Rules of Interaction

- No repo may claim another repo's truth surface.
- Source files do not prove runtime.
- Runtime does not automatically create public proof.
- Evidence-linked does not automatically mean public-safe.
- Legacy reference does not become V2 truth by copy-paste.
- AI may draft, inspect, compare, and implement scoped tasks.
- AI may not own truth, approve public claims, promote artifacts, or declare runtime active.
- Real control only means something blocks, fails, or forces correction.

## Current Org State Summary

The `Claim blocked` column is blocked wording from `governance/CONTROL_STATUS_MATRIX.md`. These entries are included to preserve public claim boundaries, not to assert those claims.

| Item | Current status | Claim allowed | Claim blocked |
| --- | --- | --- | --- |
| Organization profile | Soft routing only | The profile routes reviewers to truth boundaries. | Blocked wording: the profile proves runtime, validation, or public proof. |
| Governance summary | Soft enforcement | Governance summary describes expected gates. | Blocked wording: governance text alone is a real control. |
| Repo authority map | Soft enforcement | The map defines repository ownership boundaries. | Blocked wording: the map proves a repo complied. |
| Website | Rendering only | Website content is rendering only. | Blocked wording: website presentation proves source, runtime, signal, or evidence truth. |
| HO-DET-001 source | SATISFIED | HO-DET-001 source exists. | Blocked wording: HO-DET-001 is production-ready, fleet-wide, public-safe, or deployed. |
| HO-DET-001 Splunk source | SATISFIED | HO-DET-001 Splunk source exists. | Blocked wording: Live Splunk fired as public proof. |
| HO-DET-001 synthetic validation | SATISFIED | HO-DET-001 passed synthetic validation against controlled positive and negative process-creation fixtures. | Blocked wording: HO-DET-001 is production-ready, fleet-wide, public-safe, or catches attacks in production. |
| HO-DET-001 private controlled lab runtime match | SATISFIED_PRIVATE_LAB_SCOPE | A private controlled lab runtime match has been captured locally, but public-safe promotion remains blocked pending review. | Blocked wording: Live Splunk fired as public proof; raw command lines; encoded payloads; LAN IPs; local artifact paths; raw CSV names; screenshots as public evidence. |
| HO-DET-001 public runtime-active | BLOCKED | Runtime-active status remains blocked on public surfaces. | Blocked wording: HO-DET-001 is active in production. |
| HO-DET-001 public signal-observed | BLOCKED | Signal-observed status remains blocked on public surfaces unless scoped as private controlled lab signal observed. | Blocked wording: HO-DET-001 has public signal proof. |
| HO-DET-001 public evidence linkage | BLOCKED | Evidence-linked public proof remains blocked. | Blocked wording: HO-DET-001 public proof is complete. |
| HO-DET-001 public-safe | BLOCKED | Public-safe status is blocked pending reviewed wording, privacy review, stale review, evidence linkage review, and Raylee approval. | Blocked wording: HO-DET-001 is public-safe. |

## Links

- [Organization profile](../profile/README.md)
- [START_HERE](../profile/START_HERE.md)
- [Governance summary](../governance/GOVERNANCE_SUMMARY.md)
- [Control status matrix](../governance/CONTROL_STATUS_MATRIX.md)
- [Repository authority map](../architecture/REPO_AUTHORITY_MAP.md)
- [HO-DET-001 proof record](https://github.com/HawkinsOperations/hawkinsoperations-proof/blob/main/proof/records/HO-DET-001.md)
