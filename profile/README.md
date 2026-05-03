![HawkinsOperations Detection Engineering SOC](./assets/hawkinsoperations-banner.svg)

# HawkinsOperations Detection Engineering SOC

Governed detection engineering, SOC automation, and AI-assisted security operations with proof-bound claims.

**Current public proof ceiling:** `TEST_VALIDATED_SYNTHETIC_SCOPE`

HawkinsOperations speeds up security production without letting the system lie.

## What This Is

HawkinsOperations separates source, validation, runtime, signal, evidence, and public proof so security work can move faster without letting claims drift.

## Current Flagship Proof Boundary

**HO-DET-001** is the current flagship reviewer path. The public ceiling remains `TEST_VALIDATED_SYNTHETIC_SCOPE`. The proof record now includes verifier-backed private/internal controlled lab runtime match evidence, but public-safe runtime proof remains blocked.

| Boundary Item | Current State |
|---|---|
| HO-DET-001 source | Source exists |
| Splunk source | Source exists |
| Controlled synthetic validation | Passed within recorded synthetic scope |
| Platform runtime contract guardrail | Exists as non-promotional contract enforcement |
| Private/internal runtime status | `CONTROLLED_LAB_RUNTIME_MATCH_VERIFIED` |
| Public-safe status | `NOT_PUBLIC_SAFE` |
| Runtime-active, public signal, and public-safe proof | Blocked unless separately reviewed and approved |

## Reviewer Route

<p>
  <a href="https://hawkinsoperations.com/"><strong>hawkinsoperations.com</strong></a>
  &nbsp;|&nbsp;
  <a href="https://github.com/HawkinsOperations/hawkinsoperations-proof"><strong>proof repo</strong></a>
  &nbsp;|&nbsp;
  <a href="https://github.com/HawkinsOperations/hawkinsoperations-validation"><strong>validation repo</strong></a>
  &nbsp;|&nbsp;
  <a href="https://github.com/HawkinsOperations/hawkinsoperations-detections"><strong>detections repo</strong></a>
</p>

## System Map

![Truth surface flow](./assets/truth-surface-flow.svg)

`Source` → `Validation` → `Runtime Contract` → `Evidence` → `Public Rendering`

| Surface | Owns | Boundary |
|---|---|---|
| `hawkinsoperations-detections` | Detections source truth | Source exists does not prove runtime firing |
| `hawkinsoperations-validation` | Behavior and CI truth | Synthetic pass does not prove live signal |
| `hawkinsoperations-platform` | Runtime contract guardrails | Contract enforcement is not public proof |
| `hawkinsoperations-proof` | Evidence records and proof boundaries | Evidence requires review before public-safe use |
| `hawkinsoperations-website` | Public rendering and reviewer route | Website rendering is not proof |
| `.github` | Reviewer routing and governance front door | GitHub rendering is not proof |

Website/GitHub rendering is not proof. Public surfaces route to proof records.

## Real Controls

Docs, README files, issue cards, architecture maps, and diagrams are not real controls by themselves.

A control becomes real only when it blocks, fails, or forces correction through CI, branch protection, required checks, deterministic verifiers, typed claim gates, or another blocking mechanism.

## Supported Vs Blocked

| Supported | Blocked / Not Claimed |
|---|---|
| Source exists | runtime-active |
| Synthetic validation passed | signal-observed |
| Proof-bound reviewer surface | public-safe |
| CI/check-enforced validation scope | production-ready |
| Support-only AI boundary | fleet-wide |
| Verifier-backed private controlled lab runtime match evidence | public-safe runtime proof |
|  | Cribl-routed |
|  | Wazuh-routed |
|  | AWS-live |
|  | autonomous SOC |
|  | AI-approved disposition |
|  | analyst-approved disposition |
|  | live Splunk fired as public proof |

## Next Gate

Recent gate completed: controlled runtime evidence packet -> deterministic verifier -> proof record update.

Validation PR [#22](https://github.com/HawkinsOperations/hawkinsoperations-validation/pull/22) and proof PR [#14](https://github.com/HawkinsOperations/hawkinsoperations-proof/pull/14) support the private/internal status `CONTROLLED_LAB_RUNTIME_MATCH_VERIFIED`. The public ceiling remains `TEST_VALIDATED_SYNTHETIC_SCOPE`, and public-safe status remains `NOT_PUBLIC_SAFE`.

## Legacy Boundary

HawkinsOps / hawkinsops.com is legacy/reference unless explicitly promoted by current HawkinsOperations proof records.

Current claims live under HawkinsOperations proof boundaries.

## Doctrine

**AI is labor. Governance is authority.**

**Build loud. Verify hard. Claim tight. Ship receipts.**
