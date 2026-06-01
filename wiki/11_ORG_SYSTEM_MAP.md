# HawkinsOperations Organization System Map

Status: REVIEWER_ROUTING
Trust class: SOURCE_EXISTS
Control type: reviewer routing / soft enforcement
Scope: Explains organization structure, repo ownership, truth surfaces, promotion flow, and control boundaries.
Can prove: This map exists and summarizes current reviewer routing.
Cannot prove: Runtime state, signal observation, evidence approval, production readiness, fleet coverage, Cribl routing, Wazuh routing, or public-safe proof.

## Purpose

This page is the visual operating map for HawkinsOperations.

It is a docs-as-code map, not a native GitHub Wiki page, so it remains reviewable through normal repository governance.

This map is explanation and reviewer routing only. It does not create proof, promote artifacts, approve evidence, or make runtime claims public-safe.

## One-Sentence Model

HawkinsOperations separates source, validation, runtime, signal, evidence, public proof, and legacy reference surfaces so no claim is promoted beyond what its evidence supports.

## Diagram: Organization Repo Map

```mermaid
flowchart LR
    org[".github<br/>org framing<br/>sanitized governance summaries<br/>reviewer routing"]
    det["hawkinsoperations-detections<br/>detection source only"]
    val["hawkinsoperations-validation<br/>tests / schemas / validation checks only"]
    plat["hawkinsoperations-platform<br/>platform architecture<br/>stack truth tracking<br/>runtime boundary docs"]
    proof["hawkinsoperations-proof<br/>proof records<br/>claim maps<br/>evidence indexes<br/>approved external claim records"]
    web["hawkinsoperations-website<br/>public rendering only"]
    project["Private org control board<br/>operating cockpit<br/>work coordination only"]

    org --> det
    org --> val
    org --> plat
    org --> proof
    org --> web
    org --> project

    det --> val
    val --> proof
    plat --> proof
    proof --> web

    web -. "Warning: website does not prove runtime" .-> proof
    project -. "Warning: board state is not proof or approval" .-> proof
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

    legacy -. "must be reclassified before HawkinsOperations use" .-> idea
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
    current["HO-DET-001 current public repo proof level:<br/>CONTROLLED_TEST_VALIDATED"]
    current -. "inside recorded controlled-test validation scope" .-> l4
    blocked["Public runtime-active, public signal-observed,<br/>public evidence-linked, and public-safe claims remain blocked"]
    l4 -. "private/internal runtime material exists as boundary context,<br/>but public promotion requires review" .-> blocked
```

HO-DET-001 current public repo proof level: CONTROLLED_TEST_VALIDATED.

HO-DET-001 validation enforcement exists through `HawkinsOperations/hawkinsoperations-validation#10`, merge commit `8b48500d2ebbaacd93ac88e77a31dccf1d3b4e25`, only for the exact checked controlled-test validation scope.

Proof-loop CI is a real control only for that exact checked controlled-test validation scope. It does not prove runtime-active, signal-observed, evidence-linked public proof, public-safe, production-ready, fleet-wide, Cribl-routed, Wazuh-routed, AWS-live, private runtime host activity, autonomous SOC, or AI-approved disposition.

HO-DET-001 platform runtime contract enforcement exists through `HawkinsOperations/hawkinsoperations-platform#5`, merge commit `b3d0ffbd66c1bd5f60f7e9ff99712cdc3e0595bd`. It is a non-promotional guardrail that preserves `CONTROLLED_TEST_VALIDATED`, `NOT_PUBLIC_SAFE`, and `BLOCKED`; it does not prove runtime-active status, signal-observed public proof, public-safe runtime proof, live Splunk fired, Splunk-proven Runtime Signal 001, Cribl-routed status, Wazuh-routed public proof, production-ready status, fleet-wide coverage, AWS-live status, autonomous SOC operation, AI-approved disposition, or analyst-approved disposition.

Private/internal runtime material exists only as non-public boundary context; public runtime-active, public signal-observed, public evidence-linked, and public-safe claims remain blocked pending reviewed wording, privacy review, stale review, evidence linkage review, and Raylee approval.

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
    safe["Approved external wording"]

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
    project["Private org control board operating cockpit"]
    ledger["Lifetime Case Ledger public summary"]
    website["Website rendering"]
    boundaries["Claim boundaries"]
    warning["Warning: website is last-mile rendering, not proof"]

    profile --> start --> map --> authority --> source --> validation --> proof --> ledger --> website --> boundaries
    start --> project
    project -. "coordination only" .-> boundaries
    website -.-> warning
```

## Rules of Interaction

- No repo may claim another repo's truth surface.
- Source files do not prove runtime.
- Runtime does not automatically create public proof.
- Evidence-linked does not automatically mean public-safe.
- Legacy reference does not become HawkinsOperations truth by copy-paste.
- AI may draft, inspect, compare, and implement scoped tasks.
- AI may not own truth, approve public claims, promote artifacts, or declare runtime active.
- Real control only means something blocks, fails, or forces correction.
- The canonical private HawkinsOperations Control Board may coordinate current work, but board state does not prove source, validation, runtime, signal, evidence, public proof, or public-safe status. Project number remains pending Project #1 reclaim closeout.

## Current Ledger Status

The proof-owned Lifetime Case Ledger public summary is a bounded count route, not runtime truth, signal truth, or public proof.

| Field | Current source-controlled value |
| --- | --- |
| Summary route | `hawkinsoperations-proof/proof/records/lifetime-case-ledger-v1-public-summary.json` |
| Total ledger events | 4 |
| Total cases | 4 |
| Public-safe count | 0 |
| Closed-case count | 0 |
| Appended detections | `HO-DET-001`, `HO-DET-011`, `HO-DET-012` |
| Public-safe boundary | `NOT_PUBLIC_SAFE` |
| Proof ceiling | `SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY` |

The ledger summary does not prove live runtime activity, signal observation, production deployment, SOCaaS availability, public-safe runtime proof, public proof, autonomous SOC authority, AI-approved final disposition, analyst-approved final disposition, or case closure authority.

## Current Org State Summary

The `Claim blocked` column is blocked wording from `governance/CONTROL_STATUS_MATRIX.md`. These entries are included to preserve public claim boundaries, not to assert those claims.

| Item | Current status | Claim allowed | Claim blocked |
| --- | --- | --- | --- |
| Organization profile | Soft routing only | The profile routes reviewers to truth boundaries. | Blocked wording: the profile proves runtime, validation, or public proof. |
| Governance summary | Soft enforcement | Governance summary describes expected gates. | Blocked wording: governance text alone is a real control. |
| Repo authority map | Soft enforcement | The map defines repository ownership boundaries. | Blocked wording: the map proves a repo complied. |
| Website | Rendering only | Website content is rendering only. | Blocked wording: website presentation proves source, runtime, signal, or evidence truth. |
| Project operating cockpit | COORDINATION_ONLY | The canonical private HawkinsOperations Control Board routes current work visibility and review context; `/projects/2` is only the currently visible project route while project number is pending Project #1 reclaim closeout. | Blocked wording: project board state proves source, runtime, signal, evidence, public proof, public-safe status, merge authority, or approval. |
| Lifetime Case Ledger public summary | BOUNDED_COUNT_ROUTE | The proof-owned summary records 4 ledger events, 4 cases, 0 public-safe cases, and 0 closed cases. | Blocked wording: ledger counts prove runtime, signal, public proof, public-safe status, case closure, or disposition authority. |
| HO-DET-001 source | SATISFIED | HO-DET-001 source exists. | Blocked wording: HO-DET-001 is production-ready, fleet-wide, public-safe, or deployed. |
| HO-DET-001 Splunk source | SATISFIED | HO-DET-001 Splunk source exists. | Blocked wording: Live Splunk fired as public proof. |
| HO-DET-001 controlled-test validation | SATISFIED | HO-DET-001 passed controlled-test validation against controlled positive and negative process-creation fixtures. | Blocked wording: HO-DET-001 is production-ready, fleet-wide, public-safe, or catches attacks in production. |
| HO-DET-001 validation enforcement | SATISFIED | HO-DET-001 validation enforcement exists for the exact checked controlled-test validation scope. | Blocked wording: validation enforcement proves runtime-active, signal-observed, evidence-linked public proof, public-safe, production, fleet, Cribl, Wazuh, AWS-live, private runtime host activity, autonomous SOC, or AI-approved disposition. |
| HO-DET-001 platform runtime contract enforcement | SATISFIED | HO-DET-001 platform runtime contract enforcement exists as a non-promotional guardrail. | Blocked wording: platform contract enforcement proves runtime-active, signal-observed public proof, public-safe runtime proof, live Splunk fired, Splunk-proven Runtime Signal 001, Cribl-routed, Wazuh-routed public proof, AWS-live, production-ready, fleet-wide, autonomous SOC, AI-approved disposition, or analyst-approved disposition. |
| HO-DET-001 private runtime boundary context | PRIVATE_INTERNAL_BOUNDARY_CONTEXT | Private/internal runtime material exists only as non-public boundary context, and public-safe promotion remains blocked pending review. | Blocked wording: Live Splunk fired as public proof; raw command lines; encoded payloads; LAN IPs; local artifact paths; raw CSV names; screenshots as public evidence. |
| HO-DET-001 public runtime-active | BLOCKED | Runtime-active status remains blocked on public surfaces. | Blocked wording: HO-DET-001 is active in production. |
| HO-DET-001 public signal-observed | BLOCKED | Signal-observed status remains blocked on public surfaces unless separately scoped and approved as non-public boundary context. | Blocked wording: HO-DET-001 has public signal proof. |
| HO-DET-001 public evidence linkage | BLOCKED | Evidence-linked public proof remains blocked. | Blocked wording: HO-DET-001 public proof is complete. |
| HO-DET-001 public-safe | BLOCKED | Public-safe status is blocked pending reviewed wording, privacy review, stale review, evidence linkage review, and Raylee approval. | Blocked wording: HO-DET-001 is public-safe. |

## Links

- [Organization profile](../profile/README.md)
- [START_HERE](../profile/START_HERE.md)
- [Governance summary](../governance/GOVERNANCE_SUMMARY.md)
- [Control status matrix](../governance/CONTROL_STATUS_MATRIX.md)
- [Repository authority map](../architecture/REPO_AUTHORITY_MAP.md)
- [Project operating cockpit](https://github.com/orgs/HawkinsOperations/projects/2)
- [Lifetime Case Ledger public summary](https://github.com/HawkinsOperations/hawkinsoperations-proof/blob/main/proof/records/lifetime-case-ledger-v1-public-summary.json)
- [HO-DET-001 proof record](https://github.com/HawkinsOperations/hawkinsoperations-proof/blob/main/proof/records/HO-DET-001.md)
