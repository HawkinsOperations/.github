# Opening Decision Record

- Status: LEGACY_DECISION_RECORD
- Public-safe status: PUBLIC_SAFE_CANDIDATE
- Current authority: No
- Current front door: profile/README.md
- Governance summary: ../governance/GOVERNANCE_SUMMARY.md
- Repo authority map: ../architecture/REPO_AUTHORITY_MAP.md

## Date

2026-04-23

## Purpose

This document records the decision to establish HawkinsOperations as the successor organization for governed AI-assisted detection engineering.

This record explains the architectural intent. It is not operational proof and does not promote any runtime, signal, evidence, or public-proof claim.

## What Changed

A single integrated system is being separated into purpose-specific repositories.

Detection source, validation, platform and runtime tracking, proof records, and website rendering are separate truth surfaces.

Each repository owns one truth surface and must not claim another.

## Governance Posture

AI is controlled labor, not authority.

Repo source is not runtime truth.

Runtime state is not public proof.

Evidence-linked is not automatically public-safe.

Public claims require evidence, review, and approval.

Real controls require checks, hooks, CI, or workflows that block, fail, or force correction.

Until blocking controls exist, governance language is soft enforcement.

## What This Document Does Not Claim

This document does not claim:

- production-ready status
- fully rebuilt status
- runtime-active detections
- Current-system ownership of legacy metrics
- local LLMs governing triage
- GitHub or website presentation as proof
- CI-enforced governance unless a blocking control exists

## Where To Start

- Current organization front door: profile/README.md
- Governance summary: ../governance/GOVERNANCE_SUMMARY.md
- Repository boundaries: ../architecture/REPO_AUTHORITY_MAP.md
