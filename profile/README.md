<p align="center">
  <img src="./assets/hawkinsoperations-org-banner.png" alt="HawkinsOperations — AI Security Operations banner" width="100%" />
</p>

<div align="center">

# HawkinsOperations

**HawkinsOperations is a governed AI Security Operations and detection engineering system. AI accelerates drafting, triage reasoning, case-packet support, documentation, and automation planning; deterministic validation, proof records, and human review decide what becomes operational truth.**

`CONTROLLED_TEST_VALIDATED` · `HO-DET-001` · `NOT_PUBLIC_SAFE` · `RENDERING_NOT_PROOF` · `HUMAN_REVIEW_REQUIRED`

[Start Here](START_HERE.md) · [Public Control Board](https://github.com/orgs/HawkinsOperations/projects/3) · [proof repo](https://github.com/HawkinsOperations/hawkinsoperations-proof) · [validation repo](https://github.com/HawkinsOperations/hawkinsoperations-validation) · [detections repo](https://github.com/HawkinsOperations/hawkinsoperations-detections) · [website](https://hawkinsoperations.com/) · [HO-DET-001 proof route](https://hawkinsoperations.com/proof/ho-det-001/)

</div>

---

## What this is

HawkinsOperations is a governed AI Security Operations and detection engineering system that turns detection work into source-controlled rules, deterministic validation, platform contracts, proof records, reviewer releases, runtime candidate lanes, and human-governed promotion gates.

AI accelerates drafting, triage reasoning, case-packet support, documentation, and automation planning. Validation, platform guardrails, proof records, and human review decide what becomes operational truth.

## Product 001: Claim Firewall

Claim Firewall blocks unsupported security claims before they ship.

- Product page: https://hawkinsoperations.com/claim-firewall/
- Repo: https://github.com/HawkinsOperations/claim-firewall
- Release: v0.1.0
- Announcement: https://github.com/orgs/HawkinsOperations/discussions/51
- Proof ceiling: TOOL_FUNCTION_ONLY

Claim Firewall checks configured wording policy only. It does not prove detection behavior, runtime telemetry, signal observation, production deployment, public release approval, service availability, customer rollout, AI approval, analyst approval, or final human authorization.

## Current status sources

Current pipeline and ledger values live in their owning repositories and records. This org README links to those sources instead of copying changing counts into a public rendering surface.

| Status area | Authoritative source | Boundary |
|---|---|---|
| Platform ledger state | [Platform ledger state manifest](https://github.com/HawkinsOperations/hawkinsoperations-platform/blob/main/contracts/lifetime-case-ledger-v1-state-manifest.json) | Platform owns ledger mechanics and state manifests; this profile does not create ledger truth. |
| Reviewer metrics pipeline | [Reviewer metrics summary](https://github.com/HawkinsOperations/hawkinsoperations-proof/blob/main/proof/records/reviewer-metrics-pipeline-v1-summary.json) | Reviewer-scale activity does not become governed case truth, runtime truth, signal truth, or public-safe proof by being rendered here. |
| Proof records and claim ceilings | [hawkinsoperations-proof](https://github.com/HawkinsOperations/hawkinsoperations-proof) | Proof records authorize only their stated scope; this profile routes reviewers and preserves boundaries. |
| Control status wording | [Control Status Matrix](../governance/CONTROL_STATUS_MATRIX.md) | Status wording is a routing aid, not proof authority or public-safe approval. |

## Standout receipts

| Receipt | What exists | Why it matters |
|---|---|---|
| [HO-DET-001 proof path](https://github.com/HawkinsOperations/hawkinsoperations-proof/blob/main/proof/records/HO-DET-001.md) | PowerShell EncodedCommand detection route mapped to ATT&CK T1059.001, with detection source, Splunk source, controlled validation, proof record, and public route. | Shows the full source -> validation -> platform contract -> proof -> rendering chain for one concrete detection. |
| [Proof Pack 001](https://github.com/HawkinsOperations/hawkinsoperations-proof/releases/tag/hawkinsoperations-proof-pack-001) | Bounded reviewer release ZIP with SHA256 and verifier route for HO-DET-001. | Gives a reviewer one package to verify without private lab access. |
| [Runtime Route Proof v1](https://github.com/HawkinsOperations/hawkinsoperations-proof/blob/main/proof/maps/RUNTIME-ROUTE-PROOF-V1-REVIEWER-MAP.md) | Private-candidate Wazuh -> Cribl -> Splunk route summary and prerelease. | Preserves a runtime-route proof candidate without publishing raw private evidence or raising public proof status. |
| [Reviewer metrics summary](https://github.com/HawkinsOperations/hawkinsoperations-proof/blob/main/proof/records/reviewer-metrics-pipeline-v1-summary.json) | Reviewer Metrics Pipeline v1 closeout snapshot and source record. | Reports reviewer-scale activity without turning validation activity into governed case truth. |
| [Six-repo authority model](../architecture/REPO_AUTHORITY_MAP.md) | Detections own source, validation owns behavior, platform owns mechanics, proof owns claim ceilings, website renders, and `.github` routes. | Makes the system reviewable without allowing one repo or page to claim another truth surface. |

## Authority engines

| Engine | What it owns | Why it matters |
|---|---|---|
| Detections | Source truth | Detection logic and metadata stay source-controlled and reviewable. |
| Validation | Behavior truth | Controlled cases, parity checks, case packets, AI-boundary checks, and runner trust split prove behavior inside scope. |
| Platform | Control mechanics | Contracts, schemas, factory commands, ledgers, append gates, runtime candidate lanes, and verifier guardrails make the operating model executable. |
| Proof | Claim authority | Proof records, claim ceilings, proof packs, reviewer maps, blocked claims, and releases decide what can be claimed. |
| Website | Rendering | Public cockpit and reviewer routes; rendering does not create proof authority. |
| `.github` | Command center | Org front door, reviewer routing, command-center boundaries, and authority explanation. |

**Platform is the mechanical control layer.** It turns detection work into governed, machine-checkable workflow through contracts, factory commands, ledger mechanics, case-packet schemas, runtime candidate gates, reviewer metrics state, and verifier scripts. Platform does not own proof promotion or public-safe runtime truth.

**Validation is the behavior engine.** It turns detection claims into reproducible checks through controlled cases, local case pipeline, registry checks, activity ledger, parity checks, blocked-claim scans, AI authority boundaries, and runner trust separation. Validation does not prove live runtime, signal-observed public proof, or production deployment.

**Proof is the public trust anchor.** It owns proof records, claim ceilings, Proof Pack 001, Runtime Route Proof v1, reviewer maps, release routes, and proof-boundary case studies. Proof records authorize only their stated scope.

## What this does not claim

Runtime-active public proof, signal-observed public proof, public-safe runtime proof, production SOC, production SOCaaS, customer deployment, live enterprise deployment, autonomous SOC, AI-decided disposition, AI-approved disposition, analyst-approved disposition, case closure, FortiSIEM integration proven, fleet-wide coverage, public-safe Runtime Route Proof v1, Wazuh/Cribl/Splunk public proof, broad ingestion proof, website/GitHub rendering as proof, GitHub Project metadata as proof, and green CI as approval are not claimed here.

## HawkinsOperations Control Panel

`.github` is the org command center for reviewer routing, truth boundaries, and claim controls. It does not create proof authority. Proof records live in [hawkinsoperations-proof](https://github.com/HawkinsOperations/hawkinsoperations-proof), and the current public ceiling remains `CONTROLLED_TEST_VALIDATED` unless a specific proof record says otherwise. Runtime, signal, public-safe, production, SOCaaS, autonomous SOC, AI-approved disposition, and analyst-approved disposition claims remain blocked unless explicitly proven and approved.

Public Control Board: A public-safe project board showing Built, Proven, Blocked, Deferred, and Review Path states. It is a routing/status snapshot only. It does not mirror the private Control Board and does not create proof, runtime truth, signal truth, public-safe approval, or merge authority.

| Command center view | Current route | Boundary |
|---|---|---|
| Six-repo architecture | [Repository Authority Map](../architecture/REPO_AUTHORITY_MAP.md) | Repos own separate truth surfaces; no repo may claim another repo's authority. |
| Proof chain | Detection source -> validation -> case packet -> proof record -> public rendering | Public rendering routes reviewers; it does not create proof. |
| Truth surfaces | [Six truth surfaces](#six-truth-surfaces) | Source, validation, runtime, signal, evidence, and public rendering stay separate. |
| Front-door/status proof ceiling | `SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY` | Applies to command-center and ledger-status routing; HO-DET-001 proof records keep their own proof ceiling. |
| Current ledger status | [Platform ledger state manifest](https://github.com/HawkinsOperations/hawkinsoperations-platform/blob/main/contracts/lifetime-case-ledger-v1-state-manifest.json) | Platform-owned manifest is authoritative for current ledger state; this profile does not copy ledger counts or create public-safe status. |
| Public Control Board | [HawkinsOperations Public Control Board](https://github.com/orgs/HawkinsOperations/projects/3) | Public-safe Built / Proven / Blocked / Deferred / Review Path snapshot; not private Project, not proof authority, not runtime/signal/public-safe approval. |
| Project operating cockpit | [private org Control Board route](https://github.com/orgs/HawkinsOperations/projects/2) | Canonical private HawkinsOperations Control Board; Project #1 is not an active reviewer route; project metadata is not proof, approval, runtime, signal, public-safe status, or merge authority. |
| Reviewer/demo path | [Start Here 30-second path](START_HERE.md#30-second-reviewer-path) and [Reproducible Reviewer Path](../architecture/REPRODUCIBLE_REVIEWER_PATH.md) | Demo routing does not raise the claim ceiling. |
| Command-center invariant check | [`python scripts/verify-command-center-invariants.py`](../scripts/verify-command-center-invariants.py) | Verifier control for route and claim-boundary invariants; it does not create runtime, signal, public-safe, or proof authority. |

| Reviewer need | Route |
|---|---|
| Start the review | [Start Here](START_HERE.md) |
| See repo authority boundaries | [Repository Authority Map](../architecture/REPO_AUTHORITY_MAP.md) |
| Check control status wording | [Control Status Matrix](../governance/CONTROL_STATUS_MATRIX.md) |
| Inspect standing controls | [Standing control registers](../governance/ISSUE_FACTORY_CONTROL_RECEIPTS.md) |
| Inspect proof records | [hawkinsoperations-proof](https://github.com/HawkinsOperations/hawkinsoperations-proof) |
| Inspect validators and case packets | [hawkinsoperations-validation](https://github.com/HawkinsOperations/hawkinsoperations-validation) |
| Inspect detection source | [hawkinsoperations-detections](https://github.com/HawkinsOperations/hawkinsoperations-detections) |
| Inspect platform contracts | [hawkinsoperations-platform](https://github.com/HawkinsOperations/hawkinsoperations-platform) |
| Inspect public rendering | [hawkinsoperations-website](https://github.com/HawkinsOperations/hawkinsoperations-website) |

The private Control Board supports internal governance and navigation. It is not proof, not public evidence, and not a public-safe approval surface.

The private org Control Board is the private Project #2 operating cockpit for current work visibility. Project #1 is not an active reviewer route and was not resolvable through the live ProjectV2 API during the current cleanup pass. The board is useful for navigation, queue review, and sprint context only; it does not mutate proof state, authorize merge, approve public wording, or promote public-safe status.

---

## Fast reviewer paths

| Time | Route | Boundary |
|---:|---|---|
| 30 sec | Open [Start Here](START_HERE.md), then [Control Status Matrix](../governance/CONTROL_STATUS_MATRIX.md). | Confirms the command center, current ceiling, and blocked claims. |
| 3 min | Follow [Start Here](START_HERE.md) through Project #2, repo authority, standing controls, and the HO-DET-001 proof record. | Project metadata remains coordination-only. Proof stays in `hawkinsoperations-proof`. |
| 10 min | Run the [Reproducible Reviewer Path](../architecture/REPRODUCIBLE_REVIEWER_PATH.md) and the command-center invariant verifier. | Clone-runnable inspection and invariant checks only; no private runtime access or proof promotion. |

---

## The enterprise AI failure mode

AI can accelerate security work. It cannot authorize the truth.

Without a control system, AI-generated output becomes a public claim, an analyst conclusion, an operational action, a security disposition, and an executive truth — before any evidence or human review ever authorized it.

```text
   AI OUTPUT
       │
       ▼
   UNVERIFIED CLAIM
       │
       ▼
   OPERATIONAL ACTION
       │
       ▼
   SECURITY DISPOSITION
       │
       ▼
   EXECUTIVE TRUTH                ✕  BLOCKED  ✕
```

This is the failure mode HawkinsOperations is built to prevent.

---

## The HawkinsOperations control route

AI labor enters the system. Source, validation, deterministic verification, evidence records, proof records, and human review stand between labor and any public claim.

```text
   AI LABOR
       │  scoped: drafts, scaffolds, summaries — never authorization
       ▼
   SOURCE                         hawkinsoperations-detections
       │
       ▼
   CONTROLLED VALIDATION          hawkinsoperations-validation
       │
       ▼
   DETERMINISTIC VERIFIER         fixtures · checks · CI gates
       │
       ▼
   EVIDENCE RECORD                bounded, scoped, reviewable
       │
       ▼
   PROOF RECORD                   hawkinsoperations-proof
       │
       ▼
   HUMAN REVIEW                   required · not delegable to AI
       │
       ▼
   PUBLIC BOUNDARY                hawkinsoperations.com · .github
```

**AI generates work. Evidence and human review authorize claims.**

---

## Proof Pack 001 — released

<table>
<tr>
<td width="55%" valign="top">

**HO-DET-001 reviewer release package**

The official, bounded reviewer route for the HO-DET-001 detection: source, validation, case packet, proof record, and the public boundary — packaged as one bounded reviewer ZIP and one GitHub Release.

- Release: [hawkinsoperations-proof-pack-001](https://github.com/HawkinsOperations/hawkinsoperations-proof/releases/tag/hawkinsoperations-proof-pack-001)
- Discussion: [HawkinsOperations Proof Pack 001 Released](https://github.com/orgs/HawkinsOperations/discussions/32)
- Asset: `HAWKINSOPERATIONS_PROOF_PACK_001.zip`
- ZIP SHA256: `44d8a643aa2b113c9e99be0462e699d39af707a67190823cc05bb381907dc452`

</td>
<td width="45%" valign="top">

**What this release is**

| Field | Value |
|---|---|
| Public proof ceiling | `CONTROLLED_TEST_VALIDATED` |
| Reviewer package status | `BOUNDED_REVIEWER_RELEASE_CANDIDATE` |
| Raw/private runtime evidence | `NOT_PUBLIC_SAFE` |
| Public-safe runtime proof | `BLOCKED` |
| Rendering of this page | `RENDERING_NOT_PROOF` |

</td>
</tr>
</table>

**What this release does not prove.** It is a reviewer route and a bounded ZIP. It does not promote runtime-active public proof, signal-observed public proof, public-safe runtime proof, production readiness, SOCaaS, autonomous SOC, AI-approved disposition, or analyst-approved disposition. Website/GitHub rendering is not proof.

---

## Current ledger status

The platform-owned [Lifetime Case Ledger state manifest](https://github.com/HawkinsOperations/hawkinsoperations-platform/blob/main/contracts/lifetime-case-ledger-v1-state-manifest.json) is the authoritative source for current strict governed ledger state. This org README does not copy ledger event counts, case totals, public-safe counts, or closure counts into a public rendering surface.

| Ledger field | Current source-controlled value |
|---|---|
| Ledger state | See the platform ledger state manifest. |
| Ledger counts | See the platform ledger state manifest. |
| Appended detections | `HO-DET-001`, `HO-DET-011`, `HO-DET-012` |
| Ledger public-safe status | `NOT_PUBLIC_SAFE` |
| Ledger proof ceiling | `SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY` |

Runtime Case Collector v0 has separate private candidate lanes. Their current candidate and append state is governed by platform-owned manifests, records, and verifier gates, not by copied counts in this profile.

This ledger route does not prove runtime activity, signal observation, production deployment, SOCaaS availability, public-safe runtime proof, public proof, autonomous SOC authority, AI-approved final disposition, analyst-approved final disposition, or case closure authority.

---

## Reviewer routes

Pick the route that matches your review job. The route changes how you inspect the system; it does not change the proof state.

| Route | Time | What you inspect | Start here |
|---|---:|---|---|
| Hiring manager | 3 min | What the system is, what is proven, what stays blocked. | [Start Here](START_HERE.md) |
| Detection engineer | 10 min | Detection source, validation scope, HO-DET-001 path. | [detections repo](https://github.com/HawkinsOperations/hawkinsoperations-detections) |
| SOC automation lead | 10 min | Case packet flow, deterministic checks, CI boundaries, runtime-contract separation. | [validation repo](https://github.com/HawkinsOperations/hawkinsoperations-validation) |
| AI governance reviewer | 10 min | Where AI supports labor and where human review authorizes claims. | [proof repo](https://github.com/HawkinsOperations/hawkinsoperations-proof) |
| Demo reviewer | 8 min | Command-center route, project cockpit, Proof Pack 001, and reproducible reviewer path. | [Start Here](START_HERE.md) |
| Cyber Kill Chain reviewer | 10 min | Attack-lifecycle coverage map across source, validation, proof, platform contracts, and blocked claims. | [Cyber Kill Chain coverage map](https://github.com/HawkinsOperations/hawkinsoperations-proof/blob/main/docs/mappings/CYBER_KILL_CHAIN_COVERAGE.md) |
| Public rendering reviewer | 2 min | Public presentation and reviewer navigation only; rendering does not create proof. | [HO-DET-001 proof route](https://hawkinsoperations.com/proof/ho-det-001/) |

---

Org-level reviewer entry point: Cyber Kill Chain coverage lives in `hawkinsoperations-proof` as a public route-safe reviewer map. It is not public-safe approval, runtime proof, or proof authority.

## Six truth surfaces

Each surface supports its own claims, nothing more. Authority does not flow between them by presentation.

| Surface | Supports | Does not assert |
|---|---|---|
| Source truth | A source artifact exists and can be reviewed. | Deployment, runtime behavior, signal observation, or public proof. |
| Validation truth | A deterministic validation process passed inside its stated scope. | Runtime operation, public signal, or external-use authorization. |
| Runtime truth | A control or detection is active in a runtime environment when runtime evidence is reviewed. | Signal observation, evidence linkage, or public-safe proof. |
| Signal truth | A bounded signal was observed in a stated context when signal evidence is reviewed. | Fleet scope, production readiness, or public-safe status. |
| Evidence truth | A preserved artifact supports a specific bounded claim. | Claims outside the evidence boundary. |
| Public rendering | Website and GitHub presentation of reviewed routes and wording. | Proof of any kind. |

```mermaid
flowchart LR
    A[Source] --> B[Validation]
    B --> C[Case packet]
    C --> D[Proof record]
    D --> E[Public boundary]
    F[AI support] -. labor only .-> A
    F -. labor only .-> B
    G[Human review] --> D
    H[Deterministic checks] --> D
    E -. rendering is not proof .-> I[Website / GitHub]
```

---

## Repository authority map

Six repositories. Three planes. Authority flows through scoped records, not presentation.

| Plane | Repository | Authority | Boundary |
|---|---|---|---|
| Governance / routing | `.github` | Organization profile, reviewer routing, control summaries. | Routes reviewers; does not prove source, runtime, signal, evidence, or public proof. |
| Authority chain | [`hawkinsoperations-detections`](https://github.com/HawkinsOperations/hawkinsoperations-detections) | Detection source logic and ownership trail. | Source does not prove validation or runtime. |
| Authority chain | [`hawkinsoperations-validation`](https://github.com/HawkinsOperations/hawkinsoperations-validation) | Fixtures, validators, case packets, deterministic checks. | Validation does not prove public runtime or signal state. |
| Internal / private runtime contract | `hawkinsoperations-platform` | Runtime contracts, interface boundaries, non-promotional guardrails. | Internal/private runtime-contract route; not a public proof route and not public proof. |
| Authority chain | [`hawkinsoperations-proof`](https://github.com/HawkinsOperations/hawkinsoperations-proof) | Proof records, claim ceilings, evidence boundary records, cited case packets. | Proof records do not publish private evidence or raise ceilings by presentation. |
| Rendering | [`hawkinsoperations-website`](https://hawkinsoperations.com/) | Public reviewer navigation and rendered wording. | Rendering is not proof and cannot approve a claim. |

Detections → validation → proof feeds the authority chain. `.github` routes reviewers. `hawkinsoperations-platform` remains an internal/private runtime-contract route. The website renders receipts; it does not author them.

---

## Claim firewall

Public wording passes through boundary review before it ships. Blocked terms stay listed because they describe what this surface does not assert.

Blocked unless separately promoted and approved:

`public-safe` · `production-ready` · `fleet-wide` · `live enterprise deployment` · `autonomous SOC` · `AI-approved disposition` · `analyst-approved disposition` · `runtime-active public proof` · `signal-observed public proof` · `evidence-linked public proof` · `live Splunk public proof` · `Cribl-routed public proof` · `Wazuh-routed public proof` · `AWS-live proof` · `customer-ready product` · `sold product` · `enterprise deployment`

Allowed public boundary for this profile:

| Field | Current value |
|---|---|
| Flagship path | `HO-DET-001` |
| Public proof ceiling | `CONTROLLED_TEST_VALIDATED` |
| Public-safe status | `NOT_PUBLIC_SAFE` |
| Surface mode | `RENDERING_NOT_PROOF` |
| Promotion authority | `HUMAN_REVIEW_REQUIRED` |
| Runtime-active public proof | `BLOCKED` |
| Signal-observed public proof | `BLOCKED` |
| Evidence-linked public proof | `BLOCKED` |
| Production / fleet / autonomous claim | `BLOCKED` |

---

## HO-DET-001 — flagship proof path

HO-DET-001 is the artifact reviewers can trace end to end without accepting a stronger public claim.

| Receipt | Review route | What it supports |
|---|---|---|
| Source | [Detection source repo](https://github.com/HawkinsOperations/hawkinsoperations-detections) | The detection source exists under version control. |
| Validation | [Validation repo](https://github.com/HawkinsOperations/hawkinsoperations-validation) | Controlled positive and negative test scope can be inspected. |
| Case packet | [Validation repo](https://github.com/HawkinsOperations/hawkinsoperations-validation) and [Proof repo](https://github.com/HawkinsOperations/hawkinsoperations-proof) | Case packets are produced/validated in validation and cited/recorded by proof. |
| Proof record | [HO-DET-001 proof record](https://github.com/HawkinsOperations/hawkinsoperations-proof/blob/main/proof/records/HO-DET-001.md) | The current public ceiling and blocked claims are recorded. |
| Public rendering | [HO-DET-001 public route](https://hawkinsoperations.com/proof/ho-det-001/) | Reviewer navigation only; rendering does not create proof. |

Public proof ceiling remains `CONTROLLED_TEST_VALIDATED`. Public-safe status remains `NOT_PUBLIC_SAFE`.

---

## Prior operating context

HawkinsOps V1 / SignalFoundry metrics are prior operating context only. They are not current HawkinsOperations proof and do not raise the current HawkinsOperations ceiling.

| Prior context | Boundary |
|---|---|
| 324,074 cases processed | Historical V1 / HawkinsOps context only. |
| 200+ detections built | Historical V1 / HawkinsOps context only. |
| 208/208 CI assertions | Historical V1 / HawkinsOps context only. |
| 39.7% reduction measured | Historical V1 / HawkinsOps context only. |
| 100% high-severity preservation | Historical V1 / HawkinsOps context only. |

Current HawkinsOperations claims are bounded by source, validation, evidence, and the public-proof surface.

---

## Real controls rule

Repo separation creates review boundaries. Real control comes from required review, deterministic verification, CI checks, proof records, and bounded public wording. The split is necessary; it is not sufficient. Treat the boundary as the artifact, not the architecture diagram.

---

<div align="center">

## AI is labor. Governance is authority.

**AI generates work. Evidence and human review authorize claims.**

**Build loud. Verify hard. Claim tight. Ship receipts.**

[Operator profile](https://github.com/raylee-hawkins) · [Proof ledger](https://hawkinsoperations.com/proof/) · [GitHub organization](https://github.com/HawkinsOperations)

</div>
