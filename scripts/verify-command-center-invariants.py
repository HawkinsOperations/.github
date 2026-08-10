#!/usr/bin/env python3
"""Fail-closed checks for the HawkinsOperations .github command center."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


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
    if not isinstance(manifest.get("invariants"), dict):
        fail("manifest invariants must be an object", errors)
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
    if not door_section or not re.search(
        r"\*\*\[Website / Reviewer Guide\]\(https://hawkinsoperations\.com/\)\*\*",
        door_section.group(1),
    ):
        fail("profile/README.md must bind the Website / Reviewer Guide door to the stable Website route", errors)
    if "no eighth" not in profile:
        fail("profile/README.md missing no-eighth-repository boundary", errors)

    authority_tables = (
        (
            "README.md",
            "Seven-Repository Authority",
            "| Order | Repo | Truth surface | Boundary |",
            r"^\|\s*\d+\s*\|\s*`([^`]+)`\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$",
            (
                (".github", "Route / governance truth", "Routes reviewers and explains authority boundaries; does not prove claims."),
                ("hoxline", "Product / ProofOps control", "Governs the review path and Claim Authority experience; does not own proof records or final approval."),
                ("hawkinsoperations-detections", "Source truth", "Owns detection source, metadata, source reviewability, and source-level eligibility routing."),
                ("hawkinsoperations-validation", "Behavior truth", "Owns controlled validation checks, case packets, replay scope, and recorded validation outputs."),
                ("hawkinsoperations-platform", "Contract / guardrail truth", "Owns schemas, contracts, ledger guardrails, runtime-route guardrails, and non-promotional platform controls."),
                ("hawkinsoperations-proof", "Claim / proof truth", "Owns proof records, proof ceilings, evidence-boundary records, and blocked-claim status."),
                ("hawkinsoperations-website", "Render truth", "Renders the public Reviewer Guide and bounded reviewer navigation; rendering is not proof."),
            ),
        ),
        (
            "profile/README.md",
            "Seven repositories, seven authority roles",
            "| Repository | Authority role | Does not own |",
            r"^\|\s*\[`[^`]+`\]\(https://github\.com/HawkinsOperations/([A-Za-z0-9_.-]+)\)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$",
            (
                (".github", "Organization routing and governance shell", "Proof, runtime, signal, or merge authority"),
                ("hoxline", "Product and ProofOps control surface", "Proof records, runtime proof, or final approval"),
                ("hawkinsoperations-detections", "Detection source truth", "Validation, runtime, signal, or proof truth"),
                ("hawkinsoperations-validation", "Controlled validation truth", "Live runtime, signal, production, or disposition truth"),
                ("hawkinsoperations-platform", "Contracts and control mechanics", "Proof promotion or final human authority"),
                ("hawkinsoperations-proof", "Evidence records and claim ceilings", "Broader claims than its records support"),
                ("hawkinsoperations-website", "Public rendering and presentation", "Source, validation, runtime, signal, or proof authority"),
            ),
        ),
        (
            "profile/START_HERE.md",
            "Seven-repository authority",
            "| Repository | Owns | Does not own |",
            r"^\|\s*\[[^\]]+\]\(https://github\.com/HawkinsOperations/([A-Za-z0-9_.-]+)\)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$",
            (
                (".github", "Organization routing and governance shell", "Proof or operational truth"),
                ("hoxline", "Product and ProofOps control", "Proof records or final approval"),
                ("hawkinsoperations-detections", "Detection source truth", "Validation, runtime, signal, or proof truth"),
                ("hawkinsoperations-validation", "Controlled validation truth", "Live runtime, signal, production, or disposition truth"),
                ("hawkinsoperations-platform", "Contracts and control mechanics", "Proof promotion or claim authority"),
                ("hawkinsoperations-proof", "Evidence records and claim ceilings", "Claims beyond the recorded ceiling"),
                ("hawkinsoperations-website", "Public rendering and presentation", "Source, validation, runtime, signal, or proof authority"),
            ),
        ),
        (
            "architecture/REPO_AUTHORITY_MAP.md",
            "Authority Summary",
            "| Repository | Authority plane | Owns | Boundary |",
            r"^\|\s*`([^`]+)`\s*\|\s*([^|]+?)\s*\|\s*[^|]+?\s*\|\s*([^|]+?)\s*\|$",
            (
                (".github", "Reviewer routing / governance shell", "Not proof; does not prove source, runtime, signal, evidence, public-safe status, or production readiness."),
                ("hawkinsoperations-detections", "Source truth", "Source does not prove validation, runtime, signal, or public proof."),
                ("hawkinsoperations-validation", "Validation truth", "Validation does not prove runtime deployment, public signal, or public-safe status."),
                ("hawkinsoperations-platform", "Contracts / orchestration / control logic", "Contracts do not prove public proof, production readiness, or current runtime state."),
                ("hawkinsoperations-proof", "Proof records / evidence truth", "Proof records do not publish raw private evidence or raise ceilings by presentation."),
                ("hawkinsoperations-website", "Public rendering only", "Rendering is not proof and cannot approve a claim."),
                ("hoxline", "Product / ProofOps control", "Product framing does not prove runtime, signal, evidence, public-safe status, production readiness, or approval."),
            ),
        ),
    )
    for rel, heading, expected_header, row_pattern, expected_rows in authority_tables:
        table_text = read_text(ROOT / rel, errors)
        section_match = re.search(
            rf"## {re.escape(heading)}\s+(.*?)(?=\n## |\Z)",
            table_text,
            re.DOTALL,
        )
        if not section_match:
            fail(f"{rel} missing parseable authority table: {heading}", errors)
            continue
        if expected_header not in section_match.group(1):
            fail(f"{rel} authority table must preserve its exact ownership-boundary headers", errors)
        actual_rows = tuple(
            (repository, role.strip(), boundary.strip())
            for repository, role, boundary in re.findall(row_pattern, section_match.group(1), re.MULTILINE)
        )
        if actual_rows != expected_rows:
            fail(f"{rel} authority rows must bind each repository to its exact role and boundary", errors)


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
