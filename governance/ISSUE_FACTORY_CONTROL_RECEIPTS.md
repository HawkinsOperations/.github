# Issue Factory Control Receipts

Status: REVIEWER_ROUTING
Control type: governance receipt and control-board classification
Review pass: 2026-05-31 issue-factory pass

This file records the receipt-backed governance artifacts produced from the open `.github` issue queue. It is source truth for the existence of these rows only. It does not prove runtime state, signal observation, evidence approval, public-safe status, production readiness, fleet scope, Cribl routing, Wazuh routing, AWS-live status, live Splunk firing, autonomous SOC authority, AI approval, analyst approval, or Project-board approval.

## Issue Queue Summary

Open issues inspected in this pass:

| Issue | Title | Labels observed | Milestone | Issue role | Current action |
| --- | --- | --- | --- | --- | --- |
| [#39](https://github.com/HawkinsOperations/.github/issues/39) | Project #2 - single control board consolidation | `claim:not-public-safe`, `needs:raylee-review`, `lane:control` | None | Artifact task for Project #2 consolidation receipt | Close after this receipt lands on `main`. |
| [#10](https://github.com/HawkinsOperations/.github/issues/10) | Blocked claims register - control board - keep unsupported claims visible | `risk:blocked-claim`, `claim:not-public-safe`, `needs:raylee-review`, `lane:control`, `needs:receipt`, `lane:blocked-claims` | Day 1 - Evidence Lane Decision | Standing control register | Keep open as standing control after this receipt lands. |
| [#8](https://github.com/HawkinsOperations/.github/issues/8) | Enforcement ledger - control board - map checks to control class | `claim:not-public-safe`, `lane:control`, `lane:enforcement`, `needs:receipt`, `control:report-only` | Day 1 - Evidence Lane Decision | Standing enforcement ledger | Keep open as standing control after this receipt lands. |
| [#5](https://github.com/HawkinsOperations/.github/issues/5) | Dirty repo state - repo truth - classify before writes | `track:repo-hygiene`, `control:soft` | Day 1 - Evidence Lane Decision | Artifact task / hygiene control | Close after this receipt lands on `main`. |

## Blocked Claims Register

Purpose: advances issue [#10](https://github.com/HawkinsOperations/.github/issues/10) by keeping unsupported claims visible as blocked rows.

Boundary: this register proves only that blocked claims are tracked. It does not prove the positive claim in any row.

| claim_id | Claim text | Claim family | Current status | Truth surface | Current proof ceiling | Why blocked | Evidence required to unblock | Next gate | Owner approval required | Reviewer-facing allowed wording | Blocked wording | Control class | Enforcement artifact/check | Receipt/evidence link | Last reviewed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BC-001 | runtime-active | Runtime | BLOCKED | Runtime truth | CONTROLLED_TEST_VALIDATED public ceiling | No approved public runtime-state evidence is linked for this claim. | Reviewed runtime receipt, stale review, privacy review, public wording review, and approval. | Runtime evidence review and public-claim gate. | Yes | "Runtime-active status remains blocked on public surfaces." | "This proves runtime-active status." | REPORT_ONLY | Claim-boundary docs; not fail-closed by this file. | [Control Status Matrix](CONTROL_STATUS_MATRIX.md) | 2026-05-31 |
| BC-002 | signal-observed | Signal | BLOCKED | Signal truth | CONTROLLED_TEST_VALIDATED public ceiling | No approved public signal evidence is linked for this claim. | Reviewed signal receipt, stale review, privacy review, public wording review, and approval. | Signal evidence review and public-claim gate. | Yes | "Signal-observed status remains blocked on public surfaces." | "This proves signal-observed status." | REPORT_ONLY | Claim-boundary docs; not fail-closed by this file. | [Control Status Matrix](CONTROL_STATUS_MATRIX.md) | 2026-05-31 |
| BC-003 | evidence-linked public proof | Evidence / public proof | BLOCKED | Evidence truth / public proof | CONTROLLED_TEST_VALIDATED public ceiling | Private or source-controlled material does not become public proof by existence. | Approved public evidence linkage and reviewer-safe proof record. | Evidence linkage review and public-proof approval. | Yes | "Evidence-linked public proof remains blocked." | "This proves evidence-linked public proof." | REPORT_ONLY | Claim-boundary docs; not fail-closed by this file. | [Control Status Matrix](CONTROL_STATUS_MATRIX.md) | 2026-05-31 |
| BC-004 | public-safe | Public status | BLOCKED | Public-safe status | NOT_PUBLIC_SAFE | Public-safe status requires explicit wording, privacy, stale, evidence-link, and surface approval. | Public-safe approval packet with allowed wording and route. | Public-safe release/publication gate. | Yes | "Public-safe status is blocked pending review and approval." | "This proves public-safe status." | REPORT_ONLY | Claim-boundary docs; not fail-closed by this file. | [Control Status Matrix](CONTROL_STATUS_MATRIX.md) | 2026-05-31 |
| BC-005 | public-safe runtime proof | Runtime / public proof | BLOCKED | Runtime truth / public proof | NOT_PUBLIC_SAFE | Runtime material is private by default and not public-safe by repo presence. | Reviewed runtime proof packet approved for public use. | Public-safe runtime-proof gate. | Yes | "Public-safe runtime proof remains blocked." | "This proves public-safe runtime proof." | REPORT_ONLY | Claim-boundary docs; not fail-closed by this file. | [Control Status Matrix](CONTROL_STATUS_MATRIX.md) | 2026-05-31 |
| BC-006 | production-ready | Production | BLOCKED | Runtime / public proof | CONTROLLED_TEST_VALIDATED public ceiling | Validation fixtures and source records do not prove production readiness. | Approved production deployment/service evidence and public wording review. | Production-claim review gate. | Yes | "Production readiness is not claimed." | "This proves production-ready status." | REPORT_ONLY | Claim-boundary docs; not fail-closed by this file. | [Control Status Matrix](CONTROL_STATUS_MATRIX.md) | 2026-05-31 |
| BC-007 | production triage | Production | BLOCKED | Runtime / signal | CONTROLLED_TEST_VALIDATED public ceiling | Support workflows and case packets do not prove production triage operation. | Approved operational triage evidence, scope, and human authority boundary. | Runtime/signal review gate. | Yes | "Production triage is not claimed." | "This proves production triage." | REPORT_ONLY | Claim-boundary docs; not fail-closed by this file. | [Control Status Matrix](CONTROL_STATUS_MATRIX.md) | 2026-05-31 |
| BC-008 | autonomous SOC | AI / operations | BLOCKED | Runtime / AI output | CONTROLLED_TEST_VALIDATED public ceiling | AI output is labor, not authority; no autonomous-operation approval exists. | Approved operational model, human-review gates, and public wording review. | AI authority review gate. | Yes | "AI support remains bounded by human review." | "This proves autonomous SOC operation." | REPORT_ONLY | Claim-boundary docs; not fail-closed by this file. | [Control Status Matrix](CONTROL_STATUS_MATRIX.md) | 2026-05-31 |
| BC-009 | AI-approved disposition | AI / disposition | BLOCKED | AI output | CONTROLLED_TEST_VALIDATED public ceiling | AI cannot authorize final security disposition. | Human-approved disposition process and explicit public wording approval. | Human authority gate. | Yes | "AI does not approve disposition." | "AI-approved disposition." | REPORT_ONLY | PR template guardrail text; not fail-closed by this file. | [.github/pull_request_template.md](../.github/pull_request_template.md) | 2026-05-31 |
| BC-010 | AI-decided disposition | AI / disposition | BLOCKED | AI output | CONTROLLED_TEST_VALIDATED public ceiling | AI cannot make final disposition decisions. | Human-owned decision workflow and approved wording. | Human authority gate. | Yes | "AI does not decide disposition." | "AI-decided disposition." | REPORT_ONLY | PR template guardrail text; not fail-closed by this file. | [.github/pull_request_template.md](../.github/pull_request_template.md) | 2026-05-31 |
| BC-011 | analyst-approved disposition | Human disposition | BLOCKED | Human review | CONTROLLED_TEST_VALIDATED public ceiling | No approved analyst-disposition record is linked here. | Analyst/human approval record and approved public wording. | Human review evidence gate. | Yes | "Analyst-approved disposition is not claimed." | "Analyst-approved disposition." | REPORT_ONLY | Claim-boundary docs; not fail-closed by this file. | [Control Status Matrix](CONTROL_STATUS_MATRIX.md) | 2026-05-31 |
| BC-012 | Cribl-routed | Pipeline | BLOCKED | Runtime / route truth | CONTROLLED_TEST_VALIDATED public ceiling | No approved public Cribl route evidence is linked for this claim. | Reviewed route receipt and approved public wording. | Pipeline evidence review gate. | Yes | "Cribl-routed status remains blocked unless separately proven and approved." | "This proves Cribl-routed status." | REPORT_ONLY | Claim-boundary docs; not fail-closed by this file. | [Control Status Matrix](CONTROL_STATUS_MATRIX.md) | 2026-05-31 |
| BC-013 | Wazuh-routed | Pipeline | BLOCKED | Runtime / route truth | CONTROLLED_TEST_VALIDATED public ceiling | No approved public Wazuh route evidence is linked for this claim. | Reviewed route receipt and approved public wording. | Pipeline evidence review gate. | Yes | "Wazuh-routed status remains blocked unless separately proven and approved." | "This proves Wazuh-routed status." | REPORT_ONLY | Claim-boundary docs; not fail-closed by this file. | [Control Status Matrix](CONTROL_STATUS_MATRIX.md) | 2026-05-31 |
| BC-014 | AWS-live | Cloud/runtime | BLOCKED | Runtime truth | CONTROLLED_TEST_VALIDATED public ceiling | Fixture or source validation does not prove live AWS operation. | Approved cloud runtime evidence and public wording review. | Cloud/runtime evidence gate. | Yes | "AWS-live status is not claimed." | "This proves AWS-live status." | REPORT_ONLY | Claim-boundary docs; not fail-closed by this file. | [Control Status Matrix](CONTROL_STATUS_MATRIX.md) | 2026-05-31 |
| BC-015 | fleet-wide deployment | Deployment | BLOCKED | Runtime truth | CONTROLLED_TEST_VALIDATED public ceiling | No approved fleet-scope deployment evidence is linked here. | Approved deployment inventory, scope, stale review, and public wording review. | Deployment scope gate. | Yes | "Fleet-wide deployment is not claimed." | "This proves fleet-wide deployment." | REPORT_ONLY | Claim-boundary docs; not fail-closed by this file. | [Control Status Matrix](CONTROL_STATUS_MATRIX.md) | 2026-05-31 |
| BC-016 | live Splunk firing | Signal / tool output | BLOCKED | Signal truth | CONTROLLED_TEST_VALIDATED public ceiling | Tool output or private runtime material is not public proof by default. | Reviewed signal evidence and approved public wording. | Signal evidence/public-safe gate. | Yes | "Live Splunk firing is not claimed as public proof." | "This proves live Splunk firing." | REPORT_ONLY | Claim-boundary docs; not fail-closed by this file. | [Control Status Matrix](CONTROL_STATUS_MATRIX.md) | 2026-05-31 |
| BC-017 | HO-GPU-01 runtime-active | Runtime / host | BLOCKED | Runtime truth | CONTROLLED_TEST_VALIDATED public ceiling | No approved public host runtime-state evidence is linked here. | Approved host runtime receipt, privacy review, stale review, and public wording approval. | Host runtime evidence gate. | Yes | "HO-GPU-01 runtime-active status is not claimed." | "This proves HO-GPU-01 runtime-active status." | REPORT_ONLY | Claim-boundary docs; not fail-closed by this file. | [Control Status Matrix](CONTROL_STATUS_MATRIX.md) | 2026-05-31 |

## Enforcement Ledger / Control-Class Map

Purpose: advances issue [#8](https://github.com/HawkinsOperations/.github/issues/8) by mapping visible control surfaces to their actual control class.

Boundary: docs, issues, comments, project fields, and reviewer-routing pages are `REPORT_ONLY` unless they block, fail, or force correction. A check is `REAL_CONTROL` only in the exact scope where it is required and fails closed.

| control_id | Control/check/review surface | Owning repo or surface | Artifact path or URL | Control class | Classification reason | What it can prove | What it cannot prove | Enforcement mechanism | Bypass risk | Next strengthening gate | Receipt link |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EC-001 | Project #2 fields | Private org project | https://github.com/orgs/HawkinsOperations/projects/2 | REPORT_ONLY | Project fields classify work but do not block repo changes or approve claims. | Board fields exist and can classify issue/control state. | Source truth, validation truth, runtime truth, signal truth, evidence truth, public proof, public-safe status, merge approval, or final disposition. | Manual project metadata. | Board state can drift from repo truth if not reconciled. | Add periodic receipt reconciliation and keep proof authority in repo records. | `gh project field-list 2 --owner HawkinsOperations` observed required fields on 2026-05-31. |
| EC-002 | GitHub issues | HawkinsOperations/.github | https://github.com/HawkinsOperations/.github/issues | REPORT_ONLY | Issues track work and decisions but do not block branch mutation. | Issue bodies/comments preserve governance intent and close recommendations. | That work is complete unless linked to merged artifacts or approved receipts. | Manual issue triage. | An issue can be closed without the artifact existing unless governance review catches it. | Require closure comments with artifact/PR links. | This file's issue closeout matrix. |
| EC-003 | Issue labels | HawkinsOperations/.github | Repository issue labels | REPORT_ONLY | Labels are visible classification, not a blocking mechanism. | Lane, risk, and review tags. | Claim truth, proof status, public-safe approval, or done status. | Manual label management. | Labels can be missing, stale, or inconsistent. | Add label audit if Raylee wants stronger hygiene. | Open issue metadata observed by `gh issue list`. |
| EC-004 | PR comments | HawkinsOperations/.github | Pull request conversation | REPORT_ONLY | Comments explain scope and recommendations but do not block unless required conversation resolution applies. | Human-readable review context and receipt routing. | That checks passed, claims are promoted, or merge is approved. | GitHub comments plus conversation resolution when configured. | Non-blocking comments can be ignored unless unresolved conversation resolution applies. | Use review-thread resolution and required review when needed. | Branch protection API shows required conversation resolution enabled. |
| EC-005 | PR reviews | HawkinsOperations/.github | Pull request reviews | SOFT_ENFORCEMENT | Main requires PR flow and conversation resolution, but required approving review count is `0`. | Review activity can add visible governance context. | Independent human approval, proof promotion, or production readiness. | Branch protection requires PR reviews object with zero approving reviews and conversation resolution. | Zero required approvals means review quality depends on Raylee governance, not GitHub hard blocking. | Increase required approving review count only with explicit GitHub-settings approval. | Branch protection API observed 2026-05-31. |
| EC-006 | README / START_HERE / wiki docs | HawkinsOperations/.github | `README.md`, `profile/START_HERE.md`, `wiki/11_ORG_SYSTEM_MAP.md` | REPORT_ONLY | Reviewer routing docs describe boundaries but do not fail violations. | Current routes and stated claim boundaries. | Runtime, signal, evidence, public-proof, or public-safe truth. | Source-controlled documentation. | Docs can become stale until reviewed. | Add deterministic wording scans if needed. | Existing files read in this pass. |
| EC-007 | Main branch protection | HawkinsOperations/.github | `main` branch protection | SOFT_ENFORCEMENT | PR flow and conversation resolution are enabled; status checks are not required for this repo. | Direct pushes are constrained by PR-flow settings and admin enforcement. | Claim correctness, proof promotion, or validation success. | GitHub branch protection. | No required status checks and zero required approvals reduce fail-closed coverage. | Add required checks/reviews only with explicit GitHub-settings approval. | Branch protection API observed 2026-05-31. |
| EC-008 | Repository rulesets | HawkinsOperations/.github | GitHub repository settings | NOT_YET_CONTROL | No ruleset change was made in this pass; ruleset state was not needed beyond branch protection. | Nothing from this pass. | Any required-check or ruleset enforcement claim. | Not established by this pass. | Unknown/stale if settings change later. | Inspect rulesets under explicit settings audit scope. | Not verified by this pass. |
| EC-009 | CI workflows in `.github` repo | HawkinsOperations/.github | `.github/` directory | NOT_YET_CONTROL | No repo-local workflow file was observed; only a pull request template was present. | No workflow control exists in this repo from current files. | Any .github repo CI enforcement claim. | None observed. | No local CI gate protects these docs unless external/org settings add one. | Add a scoped verifier workflow only under separate approval. | `Get-ChildItem .github` observed pull request template only. |
| EC-010 | Referenced validation checks | HawkinsOperations/hawkinsoperations-validation | `governance/ORG_REQUIRED_CHECKS_MATRIX.yml` | REAL_CONTROL only in required checked scope | Matrix records validation workflows and verifier commands; real only where required and failing closed. | Checked validation registry/package scope when required checks run and pass. | Runtime, signal, public-safe, production, fleet, Cribl, Wazuh, AWS-live, autonomous SOC, AI approval, or analyst approval. | GitHub Actions/verifiers in owning repo. | Path filters, non-required checks, or report-only mode can limit control strength. | Keep matrix current with observed required checks. | [ORG_REQUIRED_CHECKS_MATRIX.yml](ORG_REQUIRED_CHECKS_MATRIX.yml) |
| EC-011 | Referenced proof checks | HawkinsOperations/hawkinsoperations-proof | `governance/ORG_REQUIRED_CHECKS_MATRIX.yml` | REAL_CONTROL only in required checked scope | Matrix records proof integrity/release checks; real only where required and failing closed. | Checked proof-record integrity and release-contract scope. | Runtime, signal, public-safe, production, fleet, live Splunk, Cribl, Wazuh, AWS-live, autonomous SOC, AI approval, or analyst approval. | GitHub Actions/verifiers in owning repo. | Proof checks prove only checked proof-contract fields. | Keep proof check receipts current. | [ORG_REQUIRED_CHECKS_MATRIX.yml](ORG_REQUIRED_CHECKS_MATRIX.yml) |
| EC-012 | Referenced platform checks | HawkinsOperations/hawkinsoperations-platform | `governance/ORG_REQUIRED_CHECKS_MATRIX.yml` | SOFT_ENFORCEMENT to REAL_CONTROL by check | Matrix records governance gate and dispatch-only local GPU triage; dispatch-only checks are not PR protection. | Platform contract/check scope where required and failing closed. | Production runtime, signal, public-safe, fleet, or AI/human disposition authority. | GitHub Actions/verifiers in owning repo. | Dispatch-only checks can be skipped in normal PR flow. | Promote only approved checks into required gates. | [ORG_REQUIRED_CHECKS_MATRIX.yml](ORG_REQUIRED_CHECKS_MATRIX.yml) |
| EC-013 | Codex kickoff/closeout logging | Operator logbook | `C:\Raylee\Operations\Logbook` | REPORT_ONLY | Operator logging records session chronology and governance scope; it is not public proof. | A controlled session was logged locally. | Source truth, validation truth, runtime truth, signal truth, public-safe status, or issue closure authority. | Append-only operator bookkeeping. | Local log is not a GitHub hard gate. | Keep logs paired with repo receipts when public/reviewer routing is needed. | Kickoff log appended for this pass. |
| EC-014 | Closed-unmerged PR handling | GitHub PR state | Pull request merge state | REPORT_ONLY | Closed PRs without merge are not receipt-backed completion by default. | A closed-unmerged PR may document attempted work or supersession. | That a change landed on `main`. | Manual inspection of PR merge state and replacement links. | Closed PRs can be mistaken for merged evidence. | Require merged commit or replacement receipt link. | Project #2 receipt below. |
| EC-015 | Merged replacement receipt handling | GitHub PR state + source files | Merged PR and changed artifact path | SOFT_ENFORCEMENT | A merged replacement can satisfy an issue only when linked to the issue and artifact path. | The replacement artifact exists on `main` after merge. | Any broader proof or public-safe claim beyond the artifact wording. | Git history plus issue closeout comment. | Replacement may not cover all original done criteria. | Require issue-by-issue closeout comments. | Issue closeout matrix below. |

## Project #2 Consolidation Receipt

Purpose: advances issue [#39](https://github.com/HawkinsOperations/.github/issues/39).

| Field | Observed / recorded value |
| --- | --- |
| Project title | `HawkinsOperations Control Board` |
| Project number / route | https://github.com/orgs/HawkinsOperations/projects/2 |
| Visibility | Private, verified by `gh project list --owner HawkinsOperations --format json --limit 20` on 2026-05-31. |
| Canonical status | Canonical private operating control board for current HawkinsOperations control-board coordination. |
| Proof ceiling | Project metadata and governance classification only. |
| Public/reviewer status | Not public proof. Not public-safe approval. Reviewer route only where explicitly linked and bounded. |
| Required fields observed | `Control Status`, `Lane`, `Truth Surface`, `Control Level`, `Receipt Status`, `Reviewer Facing`, `Proof Ceiling`, `Evidence Link`, `Next Gate`. |
| Additional relevant fields observed | `Repo / Authority Surface`, `Work Lane`, `Truth Boundary`, `Public-Safe Status`, `Runtime / Signal Status`, `Reviewer Route`, `Blocker`, `Next Action`. |
| `.github#6` status | [#6](https://github.com/HawkinsOperations/.github/issues/6) is closed, so the issue-#39 "if still open" add-to-Project criterion does not apply in this pass. |
| Stale Project #1 handling | Not verified by this pass; existing docs still state project number is pending Project #1 reclaim closeout. |
| SignalFoundry handling | Not verified by this pass; no SignalFoundry claim is created here. |
| Closed-unmerged PR handling | Closed-unmerged PRs are not represented as receipt-backed completion unless a merged replacement receipt exists. |
| Superseded item handling | Superseded items require a replacement artifact or merged PR link before closure recommendation. |
| Public-readiness gate | Privacy review, proof-boundary review, stale review, and Raylee approval are required before any public Project-board exposure. |

### Project #2 Field Semantics

| Field | Semantics | What it proves | What it cannot prove |
| --- | --- | --- | --- |
| Control Status | Work-state classification such as Ready, Blocked, Review Needed, Done With Receipts, Closed Not Planned, or Superseded. | Board-level coordination status. | Artifact truth or proof approval. |
| Lane | Work lane such as Control, Enforcement / Verifiers, Blocked Claims, or Proof / Public Routing. | Routing intent. | The lane's work is complete. |
| Truth Surface | The truth surface a card references: repo truth, validation truth, runtime private, signal private, evidence truth, public proof, public rendering, or governance/routing. | Which surface is under discussion. | That the surface is proven or promoted. |
| Control Level | NOT_YET_CONTROL, REPORT_ONLY, SOFT_ENFORCEMENT, or REAL_CONTROL. | Current control classification when kept in sync with receipts. | That enforcement exists without a blocking mechanism. |
| Receipt Status | Missing, Partial, Verified, or Not Applicable. | Whether a card has a receipt classification. | That all done criteria are complete unless linked to the receipt. |
| Reviewer Facing | Internal Only, Public Candidate, or Public Safe After Review. | Intended review exposure status. | Public-safe approval by itself. |
| Proof Ceiling | Text field for the maximum claim ceiling. | The ceiling recorded on the board. | That the ceiling is correct without source/proof verification. |
| Evidence Link | Link to supporting artifact or receipt. | Route to supporting material. | That linked material is public-safe or sufficient. |
| Next Gate | Next owner/action gate. | What must happen next. | That the gate has been completed. |

### Remaining Project #2 Blockers

- Project #2 remains private and must not be described as public proof.
- Project visibility and metadata are not proof authority.
- Public/reviewer exposure requires privacy review, proof-boundary review, stale review, evidence-link review, and Raylee approval.
- Project #1 reclaim / number-finality remains not verified by this pass.
- Board state must not be treated as merge approval, issue closure authority, runtime truth, signal truth, evidence truth, public proof, or public-safe status.

## Dirty Repo State / Repo Hygiene Receipt

Purpose: advances issue [#5](https://github.com/HawkinsOperations/.github/issues/5).

| Rule / receipt item | Current receipt |
| --- | --- |
| Dirty repo rule | Before scoped modification, run `git status --short --branch` in the target repo and classify dirty/untracked files. |
| Unrelated dirty stop condition | Unrelated dirty files in the target write repo block mutation. Known unrelated dirty in non-target repos is warning-only unless it overlaps the task, publication claim, proof claim, merge target, or file being edited. |
| Allowed append-only log exception | The governed kickoff/closeout log append under `C:\Raylee\Operations\Logbook` is operator bookkeeping, not repo mutation. |
| Validation command | `git status --short --branch` in `C:\Raylee\Repo\HawkinsOperations\.github` before branch creation and mutation. |
| Branch safety | Start from clean `main`, create a scoped branch, and avoid branch switching with unclassified dirty state. |
| Staging rule | Never use `git add .`; stage exact changed files only. |
| Proof boundary | Dirty-state classification proves only workspace hygiene for the scoped task. It does not prove runtime, signal, evidence, public proof, public-safe status, production readiness, or issue completion outside linked artifacts. |
| Current `.github` repo status before branch | Clean `main...origin/main`, observed before branch creation on 2026-05-31. |
| Read-only sibling repo status | `hawkinsoperations-detections`, `hawkinsoperations-validation`, `hawkinsoperations-platform`, `hawkinsoperations-proof`, and `hawkinsoperations-website` all showed clean `main...origin/main` in this pass. |
| Close recommendation for #5 | CLOSE_AFTER_PR_MERGE because this receipt covers the durable repo-hygiene rule and current scoped status is clean. |

## Issue Closeout Matrix

Purpose: operator map for the currently open `.github` issue queue.

| Issue | Title | Action classification | Artifact produced or linked | Close state | Reason | Required next action |
| --- | --- | --- | --- | --- | --- | --- |
| [#39](https://github.com/HawkinsOperations/.github/issues/39) | Project #2 - single control board consolidation | Artifact task | Project #2 Consolidation Receipt in this file | CLOSE_AFTER_PR_MERGE | Project title, private visibility, and required fields were verified; source receipt needs to land on `main`. | Merge the receipt PR after review, then close with receipt link. |
| [#10](https://github.com/HawkinsOperations/.github/issues/10) | Blocked claims register - control board - keep unsupported claims visible | Standing control register | Blocked Claims Register in this file | KEEP_OPEN_STANDING_CONTROL | Issue body/comments define current standing guardrail behavior; the register should remain visible for future blocked claims. | Comment with PR/receipt; leave open for ongoing control-board tracking. |
| [#8](https://github.com/HawkinsOperations/.github/issues/8) | Enforcement ledger - control board - map checks to control class | Standing enforcement ledger | Enforcement Ledger / Control-Class Map in this file | KEEP_OPEN_STANDING_CONTROL | Issue body/comments define standing control classification; this ledger should remain open for future check/ruleset drift. | Comment with PR/receipt; leave open for ongoing enforcement mapping. |
| [#5](https://github.com/HawkinsOperations/.github/issues/5) | Dirty repo state - repo truth - classify before writes | Artifact task / repo hygiene control | Dirty Repo State / Repo Hygiene Receipt in this file | CLOSE_AFTER_PR_MERGE | The previous blocker was dirty-state classification; current scoped and read-only sibling repos are clean and the durable rule is recorded. | Merge the receipt PR after review, then close with receipt link. |

## Closeout Comment Template

Use this bounded structure for affected issue comments after the PR is opened:

```text
Receipt update:
- Artifact path: governance/ISSUE_FACTORY_CONTROL_RECEIPTS.md
- PR: <PR URL>
- Recommendation: <CLOSE_AFTER_PR_MERGE | KEEP_OPEN_STANDING_CONTROL>
- Boundary: this is governance/control-board classification only. It does not promote runtime-active, signal-observed, evidence-linked public proof, public-safe, production-ready, fleet-wide, live Splunk, Cribl-routed, Wazuh-routed, AWS-live, autonomous SOC, AI-approved, AI-decided, or analyst-approved claims.
```
