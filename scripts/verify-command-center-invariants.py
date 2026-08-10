#!/usr/bin/env python3
"""Fail-closed checks for the HawkinsOperations .github command center."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "governance" / "COMMAND_CENTER_INVARIANTS.json"
TEXT_SCOPES = ["README.md", "profile", "architecture", "governance", "wiki", ".github"]
SYSTEM_REPOSITORIES = (
    ".github",
    "hoxline",
    "hawkinsoperations-detections",
    "hawkinsoperations-validation",
    "hawkinsoperations-platform",
    "hawkinsoperations-proof",
    "hawkinsoperations-website",
)
EXPECTED_INVARIANTS = {
    "github_repo_role": ".github is reviewer routing and governance shell only",
    "presentation_route": "hawkinsoperations.com is the Website Reviewer Guide and presentation surface",
    "seven_repository_authority": "HawkinsOperations has exactly seven system repositories with separate authority roles",
    "hoxline_role": "Hoxline is the product and ProofOps control surface, not proof authority",
    "project_2_role": "Project #2 is the canonical private HawkinsOperations Control Board operating cockpit",
    "project_1_boundary": "Project #1 is not an active reviewer route",
    "project_metadata_boundary": "Project metadata is coordination only, not proof, approval, merge authority, runtime truth, signal truth, or public-safe status",
    "rendering_boundary": "Website and GitHub rendering are not proof",
    "proof_authority_repo": "hawkinsoperations-proof owns proof records and claim ceilings",
    "command_center_proof_ceiling": "SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY",
    "ledger_public_safe_status": "NOT_PUBLIC_SAFE",
    "reviewer_metrics_pipeline": "Reviewer metrics pipeline keeps Lifetime Governed Cases separate from detection activity, validation cases, proof records, blocked claims, and Project Board reconciliation status",
    "reviewer_metrics_counts": "Reviewer metrics values are authority-owned snapshots in proof/platform records; front-door text must route to those records instead of copying changing counts",
    "ho_det_001_public_ceiling": "CONTROLLED_TEST_VALIDATED",
    "runtime_signal_public_promotions": "runtime-active, signal-observed, evidence-linked public proof, public-safe, production-ready, fleet-wide, AWS-live, Cribl-routed, Wazuh-routed, autonomous SOC, AI-approved, AI-decided, analyst-approved, and live Splunk claims remain blocked unless separately proven and approved",
    "standing_controls": ".github#8 and .github#10 remain standing controls",
    "standing_control_replacement": "Closing or replacing .github#8 or .github#10 requires explicit Raylee approval that names the replacement standing-control role",
}
EXPECTED_HOXLINE_PROMOTION_LAYER = {
    "layer_name": "hoxline_proofops_control",
    "ladder_position": 2,
    "owner_repo": "hoxline",
    "allowed_inherited_truth": [
        "Bounded source, validation, and proof context routed for reviewer inspection.",
        "Claim Authority decisions within configured evidence ceilings.",
        "Claim Firewall enforcement receipts.",
    ],
    "blocked_inherited_truth": [
        "Product control creates proof records or final approval.",
        "Hoxline establishes runtime-active or signal-observed truth.",
        "Claim routing grants merge, disposition, public-safe, or case-closure authority.",
    ],
    "required_promotion_gates": [
        "Owning source, validation, platform, and proof records remain separate.",
        "Claim decisions preserve the configured proof ceiling.",
        "Human review remains required for approval, merge, or promotion.",
    ],
    "status_values": [
        "SOURCE_EXISTS",
        "CONTROLLED_TEST_VALIDATED",
        "BLOCKED",
        "HUMAN_REVIEW_REQUIRED",
    ],
    "human_review_requirement": True,
}

REQUIRED_TEXT = {
    "README.md": [
        ".github is routing/governance only",
        "Website Reviewer Guide",
        "Seven-Repository Authority",
        "hoxline",
        "Project #1 is not an active reviewer route",
        "SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY",
        "NOT_PUBLIC_SAFE",
        "CONTROLLED_TEST_VALIDATED",
    ],
    "profile/README.md": [
        "Website / Reviewer Guide",
        "Seven repositories, seven authority roles",
        "AI produces labor. Evidence and human review authorize claims.",
        "Project #1 is not an active reviewer route",
        "project metadata is not proof",
        "SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY",
        "NOT_PUBLIC_SAFE",
        "CONTROLLED_TEST_VALIDATED",
    ],
    "profile/START_HERE.md": [
        "Three doors",
        "Website / Reviewer Guide",
        "Seven-repository authority",
        "30-second reviewer path",
        "3-minute command-center path",
        "10-minute reviewer path",
        "Reviewer metrics pipeline",
        "Lifetime Governed Cases",
        "Detection Activity / controlled validation fire count",
        "Validation Case Count",
        "Proof Record Count",
        "Blocked Claim Count",
        "HawkinsOperations/hoxline",
        "Project Board reconciliation status",
        "Project #1 is not an active reviewer route",
        "SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY",
        "NOT_PUBLIC_SAFE",
        "CONTROLLED_TEST_VALIDATED",
    ],
    "governance/PROMOTION_LADDER_CONTRACT.yml": [
        "hoxline_proofops_control",
        "Proof records, proof cards, and proof-index entries exist at the recorded CONTROLLED_TEST_VALIDATED ceiling.",
        "proof_record_card_and_index_present: true",
    ],
    "governance/ORG_REQUIRED_CHECKS_MATRIX.yml": [
        "Proof records, proof cards, and proof-index entries exist at CONTROLLED_TEST_VALIDATED.",
        "Proof record, proof card, proof-index entry, and bounded website summary exist",
    ],
    "wiki/11_ORG_SYSTEM_MAP.md": [
        "hoxline<br/>product / ProofOps control",
        "platform state manifest",
        "This routing map deliberately does not copy changing counts.",
    ],
    "governance/ISSUE_FACTORY_CONTROL_RECEIPTS.md": [
        "#10",
        "#8",
        "Reviewer Metrics Pipeline Reconciliation Receipt",
        "Detection Activity / controlled validation fire count",
        "KEEP_OPEN_STANDING_CONTROL",
        "Do not close unless Raylee explicitly approves replacing the standing-control role",
    ],
}

BLOCKED_CLAIMS = [
    "runtime-active",
    "signal-observed",
    "evidence-linked public proof",
    "public-safe",
    "production-ready",
    "fleet-wide",
    "AWS-live",
    "Cribl-routed",
    "Wazuh-routed",
    "autonomous SOC",
    "AI-approved",
    "AI-decided",
    "analyst-approved",
    "live Splunk",
]

BOUNDARY_WORDS = (
    "blocked",
    "blocked_claim",
    "blocked public",
    "blocked_inherited_truth",
    "not ",
    "does not",
    "does_not",
    "do not",
    "must not",
    "must not claim",
    "does not promote",
    "does not prove",
    "unless",
    "boundary",
    "guardrail",
    "forbidden",
    "restricted",
    "cannot",
    "false",
    "claim firewall",
    "remains",
    "no ",
    "without",
    "non-public",
    "not_public_safe",
    "coordination-only",
    "report-only",
    "separate",
    "pending",
)


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def read_text(path: Path, errors: list[str]) -> str:
    if not path.exists():
        fail(f"missing file: {path.relative_to(ROOT).as_posix()}", errors)
        return ""
    return path.read_text(encoding="utf-8")


def read_yaml_mapping(path: Path, errors: list[str]) -> dict:
    text = read_text(path, errors)
    if not text:
        return {}
    try:
        document = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        fail(f"{path.relative_to(ROOT).as_posix()} YAML parse failed: {exc}", errors)
        return {}
    if not isinstance(document, dict):
        fail(f"{path.relative_to(ROOT).as_posix()} must contain a YAML mapping", errors)
        return {}
    return document


def extract_contiguous_table_lines(section_text: str, expected_header: str) -> tuple[str, ...]:
    """Return every contiguous pipe-delimited row beginning at an exact header."""
    section_lines = [line.strip() for line in section_text.splitlines()]
    try:
        header_index = section_lines.index(expected_header)
    except ValueError:
        return ()
    table_lines: list[str] = []
    for line in section_lines[header_index:]:
        if not line or "|" not in line:
            break
        table_lines.append(line)
    return tuple(table_lines)


def iter_text_files() -> list[Path]:
    files: list[Path] = []
    for scope in TEXT_SCOPES:
        path = ROOT / scope
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(
                p
                for p in path.rglob("*")
                if p.is_file() and p.suffix.lower() in {".md", ".json", ".yml", ".yaml"}
            )
    return sorted(set(files))


def load_manifest(errors: list[str]) -> dict:
    text = read_text(MANIFEST_PATH, errors)
    if not text:
        return {}
    try:
        manifest = json.loads(text)
    except json.JSONDecodeError as exc:
        fail(f"manifest JSON parse failed: {exc}", errors)
        return {}
    if manifest.get("schema") != "hawkinsoperations-command-center-invariants-v1":
        fail("manifest schema mismatch", errors)
    if manifest.get("invariants") != EXPECTED_INVARIANTS:
        fail("manifest invariants must match the exact reviewed authority contract", errors)
    return manifest


def check_required_files(manifest: dict, errors: list[str]) -> None:
    required = manifest.get("required_route_files", [])
    if not isinstance(required, list) or not required:
        fail("manifest required_route_files must be a non-empty list", errors)
        return
    for item in required:
        rel = Path(str(item))
        if rel.is_absolute() or ".." in rel.parts:
            fail(f"invalid required route path: {item}", errors)
            continue
        if not (ROOT / rel).is_file():
            fail(f"missing required route file: {item}", errors)


def check_required_text(errors: list[str]) -> None:
    for rel, needles in REQUIRED_TEXT.items():
        text = read_text(ROOT / rel, errors)
        lowered = text.lower()
        for needle in needles:
            if needle.lower() not in lowered:
                fail(f"{rel} missing required wording: {needle}", errors)


def check_front_door_authority_model(manifest: dict, errors: list[str]) -> None:
    manifest_repositories = tuple(manifest.get("system_repositories", []))
    if manifest_repositories != SYSTEM_REPOSITORIES:
        fail("manifest system_repositories must list the exact seven repositories in authority order", errors)

    for rel in ("README.md", "profile/README.md", "profile/START_HERE.md", "architecture/REPO_AUTHORITY_MAP.md"):
        text = read_text(ROOT / rel, errors).lower()
        for repository in SYSTEM_REPOSITORIES:
            if repository.lower() not in text:
                fail(f"{rel} missing system repository role: {repository}", errors)

    profile_text = read_text(ROOT / "profile" / "README.md", errors)
    profile = profile_text.lower()
    door_section = re.search(
        r"## Choose the right door\s+(.*?)(?=\n## |\Z)",
        profile_text,
        re.DOTALL,
    )
    expected_door_lines = (
        "| If you want to... | Start here | What that surface does |",
        "|---|---|---|",
        "| Understand or present the complete system | **[Website / Reviewer Guide](https://hawkinsoperations.com/)** · [enter presentation mode](https://hawkinsoperations.com/?present=1&scene=1) | Visual walkthrough for a podcast, brown bag, show-and-tell, technical review, or self-guided inspection. Website rendering is not proof. |",
        "| Explore the product | **[Hoxline](https://hawkinsoperations.com/hoxline/)** | ProofOps control for the AI security era: how AI-assisted work becomes tested, reviewed, blocked, or safe to claim. |",
        "| Verify source and receipts | **[GitHub reviewer route](START_HERE.md)** | Source, deterministic validation, proof records, contracts, governance, and reproducible checks across seven authority repositories. GitHub rendering is not proof. |",
    )
    actual_door_lines = () if not door_section else extract_contiguous_table_lines(
        door_section.group(1),
        expected_door_lines[0],
    )
    if actual_door_lines != expected_door_lines:
        fail("profile/README.md must preserve the exact three-door routing table", errors)
    if "no eighth" not in profile:
        fail("profile/README.md missing no-eighth-repository boundary", errors)

    authority_tables = (
        (
            "README.md",
            "Seven-Repository Authority",
            "| Order | Repo | Truth surface | Boundary |",
            (
                ("1", "`.github`", "Route / governance truth", "Routes reviewers and explains authority boundaries; does not prove claims."),
                ("2", "`hoxline`", "Product / ProofOps control", "Governs the review path and Claim Authority experience; does not own proof records or final approval."),
                ("3", "`hawkinsoperations-detections`", "Source truth", "Owns detection source, metadata, source reviewability, and source-level eligibility routing."),
                ("4", "`hawkinsoperations-validation`", "Behavior truth", "Owns controlled validation checks, case packets, replay scope, and recorded validation outputs."),
                ("5", "`hawkinsoperations-platform`", "Contract / guardrail truth", "Owns schemas, contracts, ledger guardrails, runtime-route guardrails, and non-promotional platform controls."),
                ("6", "`hawkinsoperations-proof`", "Claim / proof truth", "Owns proof records, proof ceilings, evidence-boundary records, and blocked-claim status."),
                ("7", "`hawkinsoperations-website`", "Render truth", "Renders the public Reviewer Guide and bounded reviewer navigation; rendering is not proof."),
            ),
        ),
        (
            "profile/README.md",
            "Seven repositories, seven authority roles",
            "| Repository | Authority role | Does not own |",
            (
                ("[`.github`](https://github.com/HawkinsOperations/.github)", "Organization routing and governance shell", "Proof, runtime, signal, or merge authority"),
                ("[`hoxline`](https://github.com/HawkinsOperations/hoxline)", "Product and ProofOps control surface", "Proof records, runtime proof, or final approval"),
                ("[`hawkinsoperations-detections`](https://github.com/HawkinsOperations/hawkinsoperations-detections)", "Detection source truth", "Validation, runtime, signal, or proof truth"),
                ("[`hawkinsoperations-validation`](https://github.com/HawkinsOperations/hawkinsoperations-validation)", "Controlled validation truth", "Live runtime, signal, production, or disposition truth"),
                ("[`hawkinsoperations-platform`](https://github.com/HawkinsOperations/hawkinsoperations-platform)", "Contracts and control mechanics", "Proof promotion or final human authority"),
                ("[`hawkinsoperations-proof`](https://github.com/HawkinsOperations/hawkinsoperations-proof)", "Evidence records and claim ceilings", "Broader claims than its records support"),
                ("[`hawkinsoperations-website`](https://github.com/HawkinsOperations/hawkinsoperations-website)", "Public rendering and presentation", "Source, validation, runtime, signal, or proof authority"),
            ),
        ),
        (
            "profile/START_HERE.md",
            "Seven-repository authority",
            "| Repository | Owns | Does not own |",
            (
                ("[HawkinsOperations/.github](https://github.com/HawkinsOperations/.github)", "Organization routing and governance shell", "Proof or operational truth"),
                ("[HawkinsOperations/hoxline](https://github.com/HawkinsOperations/hoxline)", "Product and ProofOps control", "Proof records or final approval"),
                ("[hawkinsoperations-detections](https://github.com/HawkinsOperations/hawkinsoperations-detections)", "Detection source truth", "Validation, runtime, signal, or proof truth"),
                ("[hawkinsoperations-validation](https://github.com/HawkinsOperations/hawkinsoperations-validation)", "Controlled validation truth", "Live runtime, signal, production, or disposition truth"),
                ("[hawkinsoperations-platform](https://github.com/HawkinsOperations/hawkinsoperations-platform)", "Contracts and control mechanics", "Proof promotion or claim authority"),
                ("[hawkinsoperations-proof](https://github.com/HawkinsOperations/hawkinsoperations-proof)", "Evidence records and claim ceilings", "Claims beyond the recorded ceiling"),
                ("[hawkinsoperations-website](https://github.com/HawkinsOperations/hawkinsoperations-website)", "Public rendering and presentation", "Source, validation, runtime, signal, or proof authority"),
            ),
        ),
        (
            "architecture/REPO_AUTHORITY_MAP.md",
            "Authority Summary",
            "| Repository | Authority plane | Owns | Boundary |",
            (
                ("`.github`", "Reviewer routing / governance shell", "Organization profile, reviewer routes, governance summaries, and control-panel navigation.", "Not proof; does not prove source, runtime, signal, evidence, public-safe status, or production readiness."),
                ("`hawkinsoperations-detections`", "Source truth", "Detection source logic and source ownership trail.", "Source does not prove validation, runtime, signal, or public proof."),
                ("`hawkinsoperations-validation`", "Validation truth", "Fixtures, validators, case packets, deterministic checks, and workflow source.", "Validation does not prove runtime deployment, public signal, or public-safe status."),
                ("`hawkinsoperations-platform`", "Contracts / orchestration / control logic", "Runtime contracts, interface boundaries, and non-promotional guardrails.", "Contracts do not prove public proof, production readiness, or current runtime state."),
                ("`hawkinsoperations-proof`", "Proof records / evidence truth", "Proof records, claim ceilings, evidence boundary records, and cited case packets.", "Proof records do not publish raw private evidence or raise ceilings by presentation."),
                ("`hawkinsoperations-website`", "Public rendering only", "Public reviewer navigation and rendered wording.", "Rendering is not proof and cannot approve a claim."),
                ("`hoxline`", "Product / ProofOps control", "Hoxline product surface and Claim Authority capabilities, starting with Claim Firewall.", "Product framing does not prove runtime, signal, evidence, public-safe status, production readiness, or approval."),
            ),
        ),
        (
            "governance/ORG_CI_CD_AUTHORITY_CONTRACT.md",
            "Repository Governance Ladder",
            "| Layer | Owner repo | Owns | Does not prove |",
            (
                ("Organization control plane", "`.github`", "Reviewer routing, CI/CD contract docs, required-check matrix, promotion ladder language.", "Detection correctness, validation results, runtime state, signal observation, evidence linkage, public-safe status."),
                ("Product / ProofOps control plane", "`hoxline`", "Product control experience, bounded review routing, and Claim Authority capabilities such as Claim Firewall.", "Proof records, runtime truth, signal truth, public-safe status, final approval, or merge authority."),
                ("Runtime and agent boundary plane", "`hawkinsoperations-platform`", "Platform contracts, runtime/agent boundary schemas, status/plan visibility, private-review support lanes.", "Detection source truth, validation pass/fail truth, public proof, production deployment, public-safe runtime evidence."),
                ("Detection source plane", "`hawkinsoperations-detections`", "Detection source files, detection metadata, source status, blocked-claim source ceilings.", "Controlled-test validation, runtime activity, signal observation, proof status, public-safe status."),
                ("Validation behavior plane", "`hawkinsoperations-validation`", "Deterministic validators, fixtures, validation reports, claim-boundary scanners, report-only parity checks.", "Runtime activity, signal observation, public proof, public-safe status, production coverage."),
                ("Proof ceiling plane", "`hawkinsoperations-proof`", "Proof records, proof indexes, claim ceilings, public-proof linkage after review.", "Raw private evidence publication, runtime operation, website presentation."),
                ("Public rendering plane", "`hawkinsoperations-website`", "Approved public rendering and reviewer routes to source, validation, and proof records.", "Proof by itself, runtime truth, signal truth, evidence truth, claim approval."),
            ),
        ),
        (
            "governance/CROSS_REPO_PROMOTION_MAP.md",
            "3. Truth Surface Map",
            "| Repository | Owns | Does not own |",
            (
                ("`.github`", "Reviewer routing and claim-control expectations", "Runtime truth, signal truth, proof approval, production status"),
                ("`hoxline`", "Product / ProofOps control experience and Claim Authority capabilities", "Proof records, runtime truth, signal truth, final approval, merge authority"),
                ("`hawkinsoperations-detections`", "Detection source truth", "Validation result, runtime status, evidence approval, public-safe wording"),
                ("`hawkinsoperations-validation`", "Test, fixture, verifier, and behavior truth", "Production runtime, signal observation, public proof"),
                ("`hawkinsoperations-platform`", "Runtime contracts and integration guardrails", "Public-safe runtime proof, detection proof approval"),
                ("`hawkinsoperations-proof`", "Evidence records and claim ceilings", "Source ownership for other repos, raw private evidence publication"),
                ("`hawkinsoperations-website`", "Public rendering only after proof allows wording", "Source truth, runtime truth, signal truth, evidence truth"),
            ),
        ),
    )
    for rel, heading, expected_header, expected_rows in authority_tables:
        table_text = read_text(ROOT / rel, errors)
        section_match = re.search(
            rf"## {re.escape(heading)}\s+(.*?)(?=\n## |\Z)",
            table_text,
            re.DOTALL,
        )
        if not section_match:
            fail(f"{rel} missing parseable authority table: {heading}", errors)
            continue
        table_lines = extract_contiguous_table_lines(section_match.group(1), expected_header)
        if not table_lines or table_lines[0] != expected_header:
            fail(f"{rel} authority table must preserve its exact ownership-boundary headers", errors)
            continue
        if len(table_lines) < 2:
            fail(f"{rel} authority table missing separator and data rows", errors)
            continue
        header_cells = tuple(cell.strip() for cell in table_lines[0].strip("|").split("|"))
        separator_cells = tuple(cell.strip() for cell in table_lines[1].strip("|").split("|"))
        if len(separator_cells) != len(header_cells) or any(
            not re.fullmatch(r":?-{3,}:?", cell) for cell in separator_cells
        ):
            fail(f"{rel} authority table has an invalid Markdown separator row", errors)
            continue
        actual_rows = tuple(
            tuple(cell.strip() for cell in line.strip("|").split("|"))
            for line in table_lines[2:]
        )
        if actual_rows != expected_rows:
            fail(f"{rel} authority table must contain only the exact seven repository ownership rows", errors)

    promotion_document = read_yaml_mapping(ROOT / "governance" / "PROMOTION_LADDER_CONTRACT.yml", errors)
    promotion_layers = promotion_document.get("layers", [])
    if not isinstance(promotion_layers, list) or any(not isinstance(layer, dict) for layer in promotion_layers):
        fail("promotion ladder layers must be a YAML list of mappings", errors)
        promotion_layers = []
    promotion_owners = tuple(layer.get("owner_repo") for layer in promotion_layers)
    expected_promotion_owners = (
        ".github",
        "hoxline",
        "hawkinsoperations-platform",
        "hawkinsoperations-detections",
        "hawkinsoperations-validation",
        "hawkinsoperations-proof",
        "hawkinsoperations-website",
    )
    if promotion_owners != expected_promotion_owners:
        fail("promotion ladder must contain the exact seven repository owners in governed order", errors)
    hoxline_layers = [layer for layer in promotion_layers if layer.get("owner_repo") == "hoxline"]
    if len(hoxline_layers) != 1 or hoxline_layers[0] != EXPECTED_HOXLINE_PROMOTION_LAYER:
        fail("Hoxline promotion layer must preserve its exact position, boundaries, gates, statuses, and human-review requirement", errors)

    required_checks_document = read_yaml_mapping(ROOT / "governance" / "ORG_REQUIRED_CHECKS_MATRIX.yml", errors)
    required_checks_repos = required_checks_document.get("repos", [])
    if not isinstance(required_checks_repos, list) or any(not isinstance(repo, dict) for repo in required_checks_repos):
        fail("required-checks repos must be a YAML list of mappings", errors)
        required_checks_repos = []
    required_checks_blocks = {repo.get("repo_name"): repo for repo in required_checks_repos}
    if len(required_checks_repos) != len(SYSTEM_REPOSITORIES) or set(required_checks_blocks) != set(SYSTEM_REPOSITORIES):
        fail("required-checks matrix must contain each of the exact seven repositories once", errors)
    expected_required_check_markers = {
        ".github": (
            "Organization control-plane routing and reviewer entry point.",
            ".github/workflows/command-center-invariants.yml",
            "command-center-invariants",
        ),
        "hoxline": (
            "Product / ProofOps control experience and Claim Authority capabilities.",
            ".github/workflows/ci.yml",
            "hoxline-trust-boundaries",
        ),
        "hawkinsoperations-detections": (
            "Detection source truth.",
            ".github/workflows/baseline-detection-contract.yml",
            "baseline-hero-artifact-contract",
        ),
        "hawkinsoperations-validation": (
            "Validation behavior, fixtures, reports, and claim-boundary scan truth.",
            ".github/workflows/baseline-validation-contract.yml",
            "baseline-hero-validation-contract",
        ),
        "hawkinsoperations-platform": (
            "Platform runtime/agent boundary contracts and status/plan visibility.",
            ".github/workflows/local-gpu-triage-gate.yml",
            "local-gpu-triage-status",
        ),
        "hawkinsoperations-proof": (
            "Proof records, proof indexes, claim ceilings, and public-proof linkage.",
            ".github/workflows/baseline-proof-integrity.yml",
            "baseline-hod001-proof-integrity",
        ),
        "hawkinsoperations-website": (
            "Public rendering of approved public state.",
            ".github/workflows/governance-gate.yml",
            "build",
        ),
    }
    for repository, (truth_surface, workflow_file, job_id) in expected_required_check_markers.items():
        block = required_checks_blocks.get(repository, {})
        workflow_files = block.get("workflow_file", []) if isinstance(block, dict) else []
        job_contexts = block.get("job_check_context", []) if isinstance(block, dict) else []
        observed_job_ids = {
            context.get("job_id") for context in job_contexts if isinstance(context, dict)
        } if isinstance(job_contexts, list) else set()
        if (
            block.get("truth_surface") != truth_surface
            or not isinstance(workflow_files, list)
            or workflow_file not in workflow_files
            or job_id not in observed_job_ids
        ):
            fail(f"required-checks matrix metadata is not bound to {repository}", errors)

    template_text = read_text(ROOT / ".github" / "pull_request_template.md", errors)
    downstream_section = re.search(
        r"- Downstream repos affected:\s+(.*?)(?=\n- Downstream action:)",
        template_text,
        re.DOTALL,
    )
    expected_downstream_repos = (
        ".github",
        "hoxline",
        "hawkinsoperations-detections",
        "hawkinsoperations-validation",
        "hawkinsoperations-platform",
        "hawkinsoperations-proof",
        "hawkinsoperations-website",
        "None",
    )
    actual_downstream_repos = () if not downstream_section else tuple(
        re.findall(r"^[ \t]*- \[ \] (.+)$", downstream_section.group(1), re.MULTILINE)
    )
    if actual_downstream_repos != expected_downstream_repos:
        fail("pull request template must enumerate exactly seven downstream repositories plus None", errors)

    system_map_text = read_text(ROOT / "wiki" / "11_ORG_SYSTEM_MAP.md", errors)
    required_hoxline_routes = (
        'hox["hoxline<br/>product / ProofOps control',
        "org --> hox",
        "val --> hox",
        "hox --> plat",
        "plat --> proof",
        "validation --> hoxline --> proof",
    )
    for route in required_hoxline_routes:
        if route not in system_map_text:
            fail(f"wiki/11_ORG_SYSTEM_MAP.md missing Hoxline routing: {route}", errors)
    if "plat --> hox" in system_map_text:
        fail("wiki/11_ORG_SYSTEM_MAP.md must not route platform backward through Hoxline", errors)
    if re.search(r"^\| (?:Total ledger events|Total cases|Public-safe count|Closed-case count) \|", system_map_text, re.MULTILINE):
        fail("wiki/11_ORG_SYSTEM_MAP.md must route changing ledger values instead of copying counts", errors)


def check_project_boundaries(all_text: str, errors: list[str]) -> None:
    required = [
        "hoxline",
        "Hoxline by HawkinsOperations",
        "ProofOps control for the AI security era",
        "AI is not the authority. Evidence is.",
        "Project #2",
        "canonical private HawkinsOperations Control Board",
        "Project #1 is not an active reviewer route",
        "Project metadata remains coordination-only",
    ]
    lowered = all_text.lower()
    for needle in required:
        if needle.lower() not in lowered:
            fail(f"missing project boundary wording: {needle}", errors)

    forbidden = [
        r"Project #1\s+is\s+an\s+active\s+reviewer\s+route",
        r"Project #1.{0,80}canonical",
        r"Project metadata\s+is\s+proof",
        r"Project metadata.{0,40}merge authority",
        r"Project metadata.{0,40}runtime truth",
        r"Project metadata.{0,40}signal truth",
        r"Project metadata.{0,40}public-safe status",
    ]
    for pattern in forbidden:
        if re.search(pattern, all_text, re.IGNORECASE | re.DOTALL):
            fail(f"forbidden project-boundary wording matched: {pattern}", errors)


def check_ceiling_boundaries(all_text: str, errors: list[str]) -> None:
    required = [
        "SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY",
        "NOT_PUBLIC_SAFE",
        "CONTROLLED_TEST_VALIDATED",
        "Website/GitHub rendering is not proof",
        "GitHub rendering is not proof",
    ]
    lowered = all_text.lower()
    for needle in required:
        if needle.lower() not in lowered:
            fail(f"missing proof-boundary wording: {needle}", errors)

    forbidden_patterns = [
        r"\brendering\s+is\s+proof\b",
        r"\bGitHub rendering\s+is\s+proof\b",
        r"\bwebsite rendering\s+is\s+proof\b",
        r"PUBLIC_SAFE_APPROVED",
        r"PUBLIC_SAFE_STATUS\s*=\s*PUBLIC_SAFE",
    ]
    for pattern in forbidden_patterns:
        if re.search(pattern, all_text, re.IGNORECASE | re.DOTALL):
            fail(f"forbidden promotion wording matched: {pattern}", errors)


def check_standing_controls(all_text: str, errors: list[str]) -> None:
    for issue in ("#8", "#10"):
        if issue not in all_text:
            fail(f"missing standing control issue reference: {issue}", errors)
    if "Do not close unless Raylee explicitly approves replacing the standing-control role" not in all_text:
        fail("missing explicit replacement-approval boundary for .github#8/#10", errors)


def check_exposure(text_files: list[Path], errors: list[str]) -> None:
    token_prefixes = ["AK" + "IA", "ghp" + "_", "github" + "_pat" + "_"]
    private_ip = re.compile(r"\b(10\.\d{1,3}\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3})\b")
    drive_path = re.compile(r"\b[A-Za-z]:\\")
    private_key = re.compile(r"BEGIN (?:RSA |OPENSSH )?PRIVATE KEY")
    for path in text_files:
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line_no, line in enumerate(text.splitlines(), start=1):
            if drive_path.search(line):
                fail(f"{rel}:{line_no} exposes a local Windows path", errors)
            if private_ip.search(line):
                fail(f"{rel}:{line_no} exposes a private IP address", errors)
            if private_key.search(line):
                fail(f"{rel}:{line_no} exposes a private-key marker", errors)
            for prefix in token_prefixes:
                if prefix in line:
                    fail(f"{rel}:{line_no} exposes a token-looking prefix", errors)


def check_identity_and_claim_context(text_files: list[Path], errors: list[str]) -> None:
    for path in text_files:
        rel = path.relative_to(ROOT).as_posix()
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        for line_no, line in enumerate(lines, start=1):
            lowered = line.lower()
            if "hawkinsops" in lowered and not any(marker in lowered for marker in ("legacy", "reference", "v1", "prior", "not current")):
                fail(f"{rel}:{line_no} uses HawkinsOps outside legacy/reference context", errors)
            for phrase in BLOCKED_CLAIMS:
                phrase_pattern = re.compile(rf"(?<![A-Za-z]){re.escape(phrase.lower())}(?![A-Za-z])")
                if not phrase_pattern.search(lowered):
                    continue
                context_start = max(0, line_no - 15)
                context_end = min(len(lines), line_no + 5)
                context = "\n".join(lines[context_start:context_end]).lower()
                if not any(marker in context for marker in BOUNDARY_WORDS):
                    fail(f"{rel}:{line_no} uses blocked claim phrase without boundary context: {phrase}", errors)


def main() -> int:
    errors: list[str] = []
    manifest = load_manifest(errors)
    check_required_files(manifest, errors)
    check_required_text(errors)
    check_front_door_authority_model(manifest, errors)

    text_files = iter_text_files()
    all_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in text_files)
    check_project_boundaries(all_text, errors)
    check_ceiling_boundaries(all_text, errors)
    check_standing_controls(all_text, errors)
    check_exposure(text_files, errors)
    check_identity_and_claim_context(text_files, errors)

    if errors:
        print("COMMAND_CENTER_INVARIANTS=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("COMMAND_CENTER_INVARIANTS=PASS")
    print(f"checked_files={len(text_files)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
