![HawkinsOperations Detection Engineering SOC](./assets/hawkinsoperations-banner.svg)

<div align="center">

# HawkinsOperations

### Claim-Control System for AI-Assisted Detection Engineering

**AI generates work. Evidence and human review authorize claims.**

<kbd>CLAIM_CONTROL_SYSTEM</kbd>
<kbd>TEST_VALIDATED_SYNTHETIC_SCOPE</kbd>
<kbd>PUBLIC_SAFE_BLOCKED</kbd>
<kbd>RENDERING_NOT_PROOF</kbd>
<kbd>HUMAN_REVIEW_REQUIRED</kbd>

</div>

## Reviewer Routes

<table>
  <tr>
    <td width="33%" valign="top">
      <strong>Executive route</strong><br>
      Start with the claim boundary, repo map, and public proof ceiling.<br><br>
      <a href="./START_HERE.md">Start Here</a><br>
      <a href="../governance/CONTROL_STATUS_MATRIX.md">Control Status Matrix</a>
    </td>
    <td width="33%" valign="top">
      <strong>Technical route</strong><br>
      Check source, validation scope, platform guardrails, and promotion triggers.<br><br>
      <a href="https://github.com/HawkinsOperations/hawkinsoperations-detections">Detections</a><br>
      <a href="https://github.com/HawkinsOperations/hawkinsoperations-validation">Validation</a><br>
      <a href="https://github.com/HawkinsOperations/hawkinsoperations-platform">Platform</a>
    </td>
    <td width="33%" valign="top">
      <strong>Proof route</strong><br>
      Verify evidence records before trusting public wording or rendered pages.<br><br>
      <a href="https://github.com/HawkinsOperations/hawkinsoperations-proof">Proof repo</a><br>
      <a href="../governance/CROSS_REPO_PROMOTION_MAP.md">Cross-Repo Promotion Map</a>
    </td>
  </tr>
</table>

## Current Boundary

| Boundary | Current state |
|---|---|
| Flagship proof path | `HO-DET-001` |
| Public ceiling | `TEST_VALIDATED_SYNTHETIC_SCOPE` |
| Public-safe status | `NOT_PUBLIC_SAFE` |
| Website/GitHub status | Rendering and reviewer routing only |
| Runtime-active public claim | `BLOCKED` |
| Public signal-observed claim | `BLOCKED` |
| Production, fleet, enterprise-deployed claim | `BLOCKED` |
| Cribl-routed, Wazuh-routed, AWS-live claim | `BLOCKED` |
| Autonomous SOC / AI-approved / AI-decided claim | `BLOCKED` |

Website/GitHub rendering is not proof. Public surfaces route reviewers to proof records, validation artifacts, and claim boundaries.

## Fast Reviewer Path

1. Read [Start Here](./START_HERE.md) for the current proof ceiling and blocked wording.
2. Check [Control Status Matrix](../governance/CONTROL_STATUS_MATRIX.md) for what is routing, soft enforcement, or real control.
3. Use the [Cross-Repo Promotion Map](../governance/CROSS_REPO_PROMOTION_MAP.md) to decide whether downstream PRs are required.
4. Review `HO-DET-001` in the [proof repo](https://github.com/HawkinsOperations/hawkinsoperations-proof/blob/main/proof/records/HO-DET-001.md).
5. Treat [hawkinsoperations.com](https://hawkinsoperations.com/) as public rendering only, not proof.

## Repo Map

<table>
  <tr>
    <td width="50%" valign="top">
      <strong>.github</strong><br>
      Owns org profile, reviewer routing, and claim-control expectations.<br>
      Does not prove runtime, signal, evidence, production, or public-safe status.
    </td>
    <td width="50%" valign="top">
      <strong>hawkinsoperations-detections</strong><br>
      Owns detection source truth.<br>
      Does not prove live firing, deployment, runtime, or public proof.
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <strong>hawkinsoperations-validation</strong><br>
      Owns tests, fixtures, verifiers, and behavior truth.<br>
      Synthetic validation is not live signal.
    </td>
    <td width="50%" valign="top">
      <strong>hawkinsoperations-platform</strong><br>
      Owns runtime contracts and integration guardrails.<br>
      Contract presence is not public runtime proof.
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <strong>hawkinsoperations-proof</strong><br>
      Owns evidence records and claim ceilings.<br>
      Claims cannot exceed the recorded proof boundary.
    </td>
    <td width="50%" valign="top">
      <strong>hawkinsoperations-website</strong><br>
      Owns public rendering after proof permits wording.<br>
      Website presentation does not create proof.
    </td>
  </tr>
</table>

## HO-DET-001 Flagship Path

| Item | Current public boundary |
|---|---|
| Detection ID | `HO-DET-001` |
| Source | Exists |
| Splunk source | Exists |
| Validation | Synthetic validation passed within controlled scope |
| Platform guardrail | Runtime contract exists as a non-promotional guardrail |
| Public ceiling | `TEST_VALIDATED_SYNTHETIC_SCOPE` |
| Public-safe status | `NOT_PUBLIC_SAFE` |
| Public runtime/signal proof | `BLOCKED` |

Private/internal controlled lab runtime match status is tracked separately from public-safe proof. It does not promote public runtime-active, signal-observed, production, fleet-wide, enterprise-deployed, Cribl-routed, Wazuh-routed, AWS-live, autonomous SOC, AI-approved, AI-decided, analyst-approved, or production AutoSOC status.

## Cross-Repo Promotion

HawkinsOperations uses gate-based cross-repo propagation, not PR-number alignment.

A changed truth surface only requires downstream PRs when it affects another repo's owned surface. A documented no-op is valid when no downstream repo is affected.

Use the [Cross-Repo Promotion Map](../governance/CROSS_REPO_PROMOTION_MAP.md) before treating source, validation, platform, proof, or website changes as promoted.

## Real Controls Rule

Docs, READMEs, diagrams, issue cards, and websites are not real controls by themselves.

A control becomes real only when it blocks, fails, or forces correction through required review, branch protection, rulesets, blocking CI, deterministic verifiers, typed claim gates, or another enforceable mechanism.

Green CI/status checks are not merge authority. Codex review is AI labor, not human review authority.

## Doctrine

**AI is labor. Governance is authority.**

**Build loud. Verify hard. Claim tight. Ship receipts.**
