# Governance Summary

Status: PUBLIC_SAFE_CANDIDATE
Trust class: SOURCE_EXISTS after creation
Control type: soft enforcement

## Purpose

HawkinsOperations uses governance to keep detection engineering, validation, evidence, and public claims separated until each claim is reviewed for its proper scope.

The goal is not to make every artifact public proof. The goal is to make the system understandable, traceable, and honest about what each artifact can and cannot prove.

## Authority Model

Governance is authority. AI is labor.

AI-assisted work may draft, review, summarize, and implement scoped tasks, but AI output cannot self-authorize promotion, approve public claims, or convert source files into runtime truth.

Promotion authority remains human-owned. Public-facing claims require reviewed wording, evidence linkage, stale review, and approval.

## Truth Boundaries

HawkinsOperations separates these truth surfaces:

- Source truth: repository files or artifacts exist.
- Runtime truth: systems are currently deployed, enabled, scheduled, or operating under stated conditions.
- Signal truth: telemetry, alert, log, or output was observed in context.
- Evidence truth: supporting material is preserved and linked to a claim.
- Public proof: claim wording is reviewed, scoped, approved, and safe for external use.

Repository source does not prove runtime state. Runtime state does not automatically create public proof. Website or README presentation does not generate truth.

## Trust Classes

Trust classes describe what can be claimed about an artifact:

- UNKNOWN: status is not known.
- DRAFT: useful work in progress, not validated.
- RESEARCH_ONLY: analysis or notes for planning.
- LEGACY_REFERENCE: historical material that is not current truth by copy or restatement.
- SOURCE_EXISTS: a source artifact exists, but runtime and evidence are not proven.
- STATIC_VALIDATED: static review found the item coherent for its stated purpose.
- TEST_DEFINED: validation method or acceptance check exists.
- TEST_VALIDATED: a test ran and produced a recorded result.
- RUNTIME_ACTIVE: runtime status is supported by current evidence.
- SIGNAL_OBSERVED: telemetry, alert, log, or output was observed.
- EVIDENCE_LINKED: a claim is linked to supporting evidence.
- VALIDATED_INTERNAL: internally reviewed for a stated scope.
- PUBLIC_SAFE: approved external wording only.
- RETIRED: no longer active or current.
- BLOCKED: cannot proceed until a blocker is resolved.

SOURCE_EXISTS is not RUNTIME_ACTIVE. EVIDENCE_LINKED is not automatically PUBLIC_SAFE.

## Promotion Gates

Promotion requires the right evidence for the next claim. A source file may move through static review, defined tests, recorded validation, runtime evidence, signal observation, evidence linkage, internal validation, and public claim review.

Public use requires:

- claim text
- evidence linkage
- trust class
- allowed wording
- blocked wording
- stale review date
- approval

Unlogged or unreviewed work cannot become public-safe. Legacy material must be reclassified before it can become current successor-system truth.

## Public Claim Discipline

Public claims must not imply more than the evidence supports. The system blocks or withholds claims that present source files as runtime proof, screenshots as public proof, website language as evidence, or AI summaries as authority.

Public-safe content must avoid private details, sensitive operational data, local machine paths, internal logs, and unreviewed evidence.

## Not Published Here

This public summary intentionally excludes local operator paths, raw session logs, private scanner details, private career material, Codex mechanics, and machine-specific governance details.

## Control Status

This document is soft enforcement. It explains the governance model, but it is not a real control until paired with checks, hooks, workflows, or review gates that block, fail, or force correction.