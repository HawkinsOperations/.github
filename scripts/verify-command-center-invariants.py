#!/usr/bin/env python3
"""Fail-closed checks for the HawkinsOperations .github command center."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "governance" / "COMMAND_CENTER_INVARIANTS.json"
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "command-center-invariants.yml"
TEXT_SCOPES = ["README.md", "profile", "architecture", "governance", "wiki", ".github"]
EXACT_REPOSITORIES = [
    ".github",
    "hawkinsoperations-detections",
    "hawkinsoperations-validation",
    "hawkinsoperations-platform",
    "hawkinsoperations-proof",
    "hawkinsoperations-website",
    "hoxline",
]

REQUIRED_TEXT = {
    "README.md": [
        ".github is routing/governance only",
        "Project #1 is not an active reviewer route",
        "SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY",
        "NOT_PUBLIC_SAFE",
        "CONTROLLED_TEST_VALIDATED",
    ],
    "profile/README.md": [
        "Project #1 is not an active reviewer route",
        "project metadata is not proof",
        "SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY",
        "NOT_PUBLIC_SAFE",
        "CONTROLLED_TEST_VALIDATED",
    ],
    "profile/START_HERE.md": [
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


def unsafe_workflow_findings(text: str) -> list[str]:
    patterns = {
        "contents write permission": r"contents:\s*write",
        "pull-request write permission": r"pull-requests:\s*write",
        "direct git push": r"\bgit\s+push\b",
        "git commit mutation": r"\bgit\s+commit\b",
        "PR create or merge mutation": r"\bgh\s+pr\s+(?:create|merge)\b",
        "auto-merge mutation": r"\bauto-merge\b",
        "Lifetime Case Ledger mutation": r"ho_factory[^\n]*(?:lifetime|ledger)[^\n]*(?:append|correct|mutate)",
    }
    return [label for label, pattern in patterns.items() if re.search(pattern, text, re.IGNORECASE)]


def extract_workflow_repositories(text: str) -> list[str]:
    match = re.search(r"^\s*repos=\(\s*$([\s\S]*?)^\s*\)\s*$", text, re.MULTILINE)
    if not match:
        return []
    return [line.strip() for line in match.group(1).splitlines() if line.strip() and not line.lstrip().startswith("#")]


def check_cross_repo_workflow(manifest: dict, errors: list[str]) -> None:
    workflow = read_text(WORKFLOW_PATH, errors)
    declared = manifest.get("cross_repo_repositories")
    if declared != EXACT_REPOSITORIES:
        fail("manifest cross_repo_repositories must list the exact seven repositories in canonical order", errors)
    required_fragments = [
        "permissions:\n  contents: read",
        "seven-repository-convergence:",
        "REQUESTED_REF:",
        "git ls-remote --exit-code --heads",
        'ref="main"',
        "actions/setup-python@v5",
        "pip install --disable-pip-version-check -e source-set/hoxline",
        "source-revisions.txt",
        "hoxline-case-growth-convergence-verify",
        "case-growth verify",
        "public-status:verify",
        "Sanitize convergence diagnostics",
        "[local-path-redacted]",
        "actions/upload-artifact@v4",
        "if: always()",
        "if: always() && steps.sanitize.outcome == 'success'",
    ]
    for fragment in required_fragments:
        if fragment not in workflow:
            fail(f"cross-repo workflow missing required behavior: {fragment}", errors)
    workflow_repositories = extract_workflow_repositories(workflow)
    if workflow_repositories != EXACT_REPOSITORIES:
        fail("cross-repo workflow checkout array must equal the exact ordered seven-repository set with no duplicates", errors)
    for finding in unsafe_workflow_findings(workflow):
        fail(f"cross-repo workflow permits unsafe behavior: {finding}", errors)


def check_workflow_hostile_self_test(errors: list[str]) -> None:
    hostile_cases = {
        "contents write": "permissions:\n  contents: write",
        "direct main push": "run: git push origin main",
        "commit mutation": "run: git commit -m unsafe",
        "PR merge": "run: gh pr merge 1",
        "ledger append": "run: python ho_factory.py lifetime-ledger-append",
    }
    for name, hostile in hostile_cases.items():
        if not unsafe_workflow_findings(hostile):
            fail(f"workflow hostile self-test failed to detect {name}", errors)
    missing_repo = "repos=(\n  .github\n  hoxline\n)"
    duplicate_repo = "repos=(\n  .github\n  .github\n  hoxline\n)"
    if extract_workflow_repositories(missing_repo) == EXACT_REPOSITORIES:
        fail("workflow hostile self-test accepted a missing-repository checkout set", errors)
    if len(set(extract_workflow_repositories(duplicate_repo))) == len(extract_workflow_repositories(duplicate_repo)):
        fail("workflow hostile self-test did not recognize a duplicate-repository checkout set", errors)


def check_required_text(errors: list[str]) -> None:
    for rel, needles in REQUIRED_TEXT.items():
        text = read_text(ROOT / rel, errors)
        lowered = text.lower()
        for needle in needles:
            if needle.lower() not in lowered:
                fail(f"{rel} missing required wording: {needle}", errors)


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
    check_cross_repo_workflow(manifest, errors)
    if "--self-test" in sys.argv:
        check_workflow_hostile_self_test(errors)
    check_required_text(errors)

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
