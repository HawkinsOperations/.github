# Start Here

HawkinsOperations is a governed AI Security Operations and detection engineering system for turning AI-assisted security work into bounded, inspectable artifacts. AI produces labor; evidence and human review authorize claims.

## Three doors

| Goal | Route | Role |
|---|---|---|
| Understand or present HawkinsOperations | [Website / Reviewer Guide](https://hawkinsoperations.com/) · [presentation mode](https://hawkinsoperations.com/?present=1&scene=1) | Visual system walkthrough and presentation surface. Rendering is not proof. |
| Explore the product | [Hoxline](https://hawkinsoperations.com/hoxline/) | ProofOps control and Claim Authority for AI-assisted security work. |
| Verify the work | [GitHub organization](https://github.com/HawkinsOperations) | Source, validation, proof records, contracts, governance, and reviewer receipts. |

## 30-second reviewer path

1. Open the [Website Reviewer Guide](https://hawkinsoperations.com/) or [start presentation mode](https://hawkinsoperations.com/?present=1&scene=1) to understand the complete system.
2. Open [Hoxline](https://hawkinsoperations.com/hoxline/) to see the product control surface.
3. Inspect the [HO-DET-001 proof route](https://hawkinsoperations.com/proof/ho-det-001/) for one bounded example.
4. Use the [Repository Authority Map](../architecture/REPO_AUTHORITY_MAP.md) to see which repository owns each truth.

Outcome: you should be able to explain the problem, the control loop, where human authority remains mandatory, and why website rendering does not become proof.

## 3-minute command-center path

Follow one detection across its owners:

1. **View source:** [HO-DET-001 detection package](https://github.com/HawkinsOperations/hawkinsoperations-detections/tree/main/detections/successor/ho-det-001).
2. **View validation:** [controlled validation result](https://github.com/HawkinsOperations/hawkinsoperations-validation/blob/main/reports/ho-det-001/validation-result.md).
3. **View proof:** [HO-DET-001 proof record](https://github.com/HawkinsOperations/hawkinsoperations-proof/blob/main/proof/records/HO-DET-001.md).
4. **View the packaged receipt:** [Proof Pack 001](https://github.com/HawkinsOperations/hawkinsoperations-proof/releases/tag/hawkinsoperations-proof-pack-001).
5. **Inspect claim enforcement:** [Claim Firewall](https://hawkinsoperations.com/claim-firewall/).
6. **Confirm the ceiling:** [Control Status Matrix](../governance/CONTROL_STATUS_MATRIX.md).

Outcome: source, validation, proof, product control, and rendering remain inspectable without being treated as interchangeable authority.

## 10-minute reviewer path

From an empty reviewer workspace, clone the organization route and Hoxline side by side. Then run one fixture-based Hoxline loop and inspect the same authority handoffs used by the bounded HO-DET-001 example:

```powershell
git clone https://github.com/HawkinsOperations/.github.git .github
git clone https://github.com/HawkinsOperations/hoxline.git hoxline
cd hoxline
$env:PYTHONDONTWRITEBYTECODE = "1"
python -B -m hoxline demo quickstart
```

Then compare the generated reviewer artifacts with the [HO-DET-001 source](https://github.com/HawkinsOperations/hawkinsoperations-detections/tree/main/detections/successor/ho-det-001), [controlled validation](https://github.com/HawkinsOperations/hawkinsoperations-validation/blob/main/reports/ho-det-001/validation-result.md), and [proof record](https://github.com/HawkinsOperations/hawkinsoperations-proof/blob/main/proof/records/HO-DET-001.md). The demo is local and fixture-based; it does not establish live runtime, signal, production, public-safe, or disposition truth.

For the full seven-repository sweep, continue with the [extended Reproducible Reviewer Path](../architecture/REPRODUCIBLE_REVIEWER_PATH.md).

Continue from the Hoxline repository by returning to the sibling organization repository for its routing and claim-boundary check:

```powershell
cd ..\.github
$env:PYTHONDONTWRITEBYTECODE = "1"
python -B scripts/verify-command-center-invariants.py
```

Expected result:

```text
COMMAND_CENTER_INVARIANTS=PASS
```

The verifier checks only its declared routing, exposure, and claim-boundary invariants. It does not establish runtime truth, signal truth, public-safe status, proof promotion, merge authority, or human approval.

## Seven-repository authority

| Repository | Owns | Does not own |
|---|---|---|
| [HawkinsOperations/.github](https://github.com/HawkinsOperations/.github) | Organization routing and governance shell | Proof or operational truth |
| [HawkinsOperations/hoxline](https://github.com/HawkinsOperations/hoxline) | Product and ProofOps control | Proof records or final approval |
| [hawkinsoperations-detections](https://github.com/HawkinsOperations/hawkinsoperations-detections) | Detection source truth | Validation, runtime, signal, or proof truth |
| [hawkinsoperations-validation](https://github.com/HawkinsOperations/hawkinsoperations-validation) | Controlled validation truth | Live runtime, signal, production, or disposition truth |
| [hawkinsoperations-platform](https://github.com/HawkinsOperations/hawkinsoperations-platform) | Contracts and control mechanics | Proof promotion or claim authority |
| [hawkinsoperations-proof](https://github.com/HawkinsOperations/hawkinsoperations-proof) | Evidence records and claim ceilings | Claims beyond the recorded ceiling |
| [hawkinsoperations-website](https://github.com/HawkinsOperations/hawkinsoperations-website) | Public rendering and presentation | Source, validation, runtime, signal, or proof authority |

No eighth system repository is implied. See the [Repository Authority Map](../architecture/REPO_AUTHORITY_MAP.md) for the detailed contract.

## What AI does—and who decides

| AI can accelerate | AI cannot authorize |
|---|---|
| Drafting, detection logic assistance, query translation, summaries, enrichment, reviewer notes, documentation, and repetitive implementation | Evidence sufficiency, detection or incident disposition, approval, merge authority, claim promotion, public-safe status, production status, or case closure |

Hoxline carries this boundary through the review loop. Claim Firewall is one Hoxline enforcement capability; it checks configured wording policy and blocks unsupported claims. It is not proof authority, runtime proof, signal proof, or an eighth repository.

## The current bounded example

HO-DET-001 has source artifacts, platform-specific query source, controlled positive and negative fixtures, deterministic validation output, and a proof record. Its current public ceiling is `CONTROLLED_TEST_VALIDATED`.

That ceiling supports only the stated controlled-test scope. Runtime-active public proof, signal-observed public proof, production readiness, customer deployment, fleet-wide coverage, SOCaaS operation, autonomous SOC behavior, AI-approved disposition, analyst-approved disposition, public-safe runtime evidence, and case closure remain unproven here.

`NOT_PUBLIC_SAFE` and `SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY` are separate bounded statuses. They do not combine with `CONTROLLED_TEST_VALIDATED` to create a stronger claim.

Website/GitHub rendering is not proof. Green CI is not merge authority. Human review remains mandatory.

## Source-owned status routes

Changing metrics stay in authority-owned records rather than this front door.

| Surface | Source route | Separation rule |
|---|---|---|
| Reviewer metrics pipeline | [proof-owned reviewer metrics summary](https://github.com/HawkinsOperations/hawkinsoperations-proof/blob/main/proof/records/reviewer-metrics-pipeline-v1-summary.json) | Snapshot only; it does not create current ledger truth. |
| Lifetime Governed Cases | [platform ledger state manifest](https://github.com/HawkinsOperations/hawkinsoperations-platform/blob/main/contracts/lifetime-case-ledger-v1-state-manifest.json) | Governed ledger state remains separate from activity volume. |
| Detection Activity / controlled validation fire count | [validation activity ledger](https://github.com/HawkinsOperations/hawkinsoperations-validation/blob/main/activity/detection-activity-ledger-v1.md) | Controlled validation activity is not runtime signal. |
| Validation Case Count | [validation registry](https://github.com/HawkinsOperations/hawkinsoperations-validation/blob/main/validation/VALIDATION_REGISTRY.yml) | Validation volume is not production coverage. |
| Proof Record Count | [proof status index](https://github.com/HawkinsOperations/hawkinsoperations-proof/blob/main/proof/indexes/DETECTION_PROOF_STATUS_INDEX.yml) | Record count is not proof promotion. |
| Blocked Claim Count | [proof-owned reviewer metrics summary](https://github.com/HawkinsOperations/hawkinsoperations-proof/blob/main/proof/records/reviewer-metrics-pipeline-v1-summary.json) | Blocked-claim volume is not missing functionality. |
| Project Board reconciliation status | [Public Control Board](https://github.com/orgs/HawkinsOperations/projects/3) | Project metadata remains coordination-only. |

## Reviewer links

| Need | Route |
|---|---|
| Visual presentation | [Website Reviewer Guide](https://hawkinsoperations.com/) |
| Product control | [Hoxline repository](https://github.com/HawkinsOperations/hoxline) |
| Proof authority | [hawkinsoperations-proof](https://github.com/HawkinsOperations/hawkinsoperations-proof) |
| Detection source | [hawkinsoperations-detections](https://github.com/HawkinsOperations/hawkinsoperations-detections) |
| Controlled validation | [hawkinsoperations-validation](https://github.com/HawkinsOperations/hawkinsoperations-validation) |
| Platform contracts | [hawkinsoperations-platform](https://github.com/HawkinsOperations/hawkinsoperations-platform) |
| Public rendering source | [hawkinsoperations-website](https://github.com/HawkinsOperations/hawkinsoperations-website) |
| Detailed authority | [Repository Authority Map](../architecture/REPO_AUTHORITY_MAP.md) |
| Clone-runnable checks | [Reproducible Reviewer Path](../architecture/REPRODUCIBLE_REVIEWER_PATH.md) |
| Control wording | [Control Status Matrix](../governance/CONTROL_STATUS_MATRIX.md) |
| Review and merge boundary | [PR Review Authority](../governance/PR_REVIEW_AUTHORITY.md) |

## Coordination boundary

The canonical private HawkinsOperations Control Board is Project #2. Project #1 is not an active reviewer route. Project metadata remains coordination-only. Project metadata is not proof or approval. Only an authorized human can approve a merge; runtime truth, signal truth, public-safe status, and final disposition remain separate.

---

**AI is labor. Governance is authority.**
