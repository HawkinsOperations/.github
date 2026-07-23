#!/usr/bin/env python3
"""Fail-closed checks for the HawkinsOperations command-center workflow."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any
from urllib.parse import unquote

try:
    import yaml
except ImportError:  # pragma: no cover - reported as a deterministic verifier failure
    yaml = None


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "governance" / "COMMAND_CENTER_INVARIANTS.json"
SOURCE_MANIFEST_PATH = ROOT / "governance" / "CONVERGENCE_SOURCE_MANIFEST.json"
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
CANONICAL_ORIGINS = {
    repository: f"https://github.com/HawkinsOperations/{repository}.git"
    for repository in EXACT_REPOSITORIES
}
PINNED_ACTIONS = {
    "actions/checkout": "11d5960a326750d5838078e36cf38b85af677262",
    "actions/setup-python": "a26af69be951a213d495a4c3e4e4022e16d87065",
    "actions/setup-node": "49933ea5288caeca8642d1e84afbd3f7d6820020",
    "actions/upload-artifact": "ea165f8d65b6e75b540449e92b4886f43607fa02",
}
EXPECTED_ARTIFACT_FILES = {"source-revisions.json", "verification-summary.json"}
PROOF_CEILING = "CONTROLLED_REPO_CONVERGENCE_AND_LOCAL_FIXTURE_REVIEW_ONLY"
EXPECTED_VERIFICATION_CHECKS = [
    "command_center_invariants",
    "command_center_hostile_workflow_tests",
    "exact_seven_source_checkout",
    "detection_contract",
    "detection_promotion_matrix",
    "detection_reverse_inventory_and_hostile_tests",
    "validation_registry",
    "validation_package_sweep",
    "validation_source_and_report_parity",
    "validation_claim_boundary",
    "proof_status_index",
    "proof_reverse_inventory",
    "proof_integrity",
    "platform_public_status_source_contract",
    "platform_case_growth_convergence",
    "platform_mutation_boundary",
    "hoxline_case_growth_pair",
    "hoxline_expanded_batch",
    "hoxline_replay",
    "hoxline_hostile_tests",
    "website_source_owner_and_freshness",
    "website_nested_claim_and_eol_tests",
    "website_static_build",
]
EXPECTED_MANIFEST_ROOT_KEYS = {
    "schema",
    "scope",
    "required_route_files",
    "cross_repo_repositories",
    "invariants",
}
EXPECTED_INVARIANT_KEYS = {
    "github_repo_role",
    "project_2_role",
    "project_1_boundary",
    "project_metadata_boundary",
    "rendering_boundary",
    "proof_authority_repo",
    "command_center_proof_ceiling",
    "ledger_public_safe_status",
    "reviewer_metrics_pipeline",
    "reviewer_metrics_counts",
    "cross_repo_convergence",
    "ho_det_001_public_ceiling",
    "runtime_signal_public_promotions",
    "standing_controls",
    "standing_control_replacement",
}

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


class ValidationError(ValueError):
    """Raised when a machine-readable control fails closed."""


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def read_text(path: Path, errors: list[str]) -> str:
    if not path.exists():
        fail(f"missing file: {path.relative_to(ROOT).as_posix()}", errors)
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        fail(f"cannot read {path.relative_to(ROOT).as_posix()}: {exc}", errors)
        return ""


def iter_text_files() -> list[Path]:
    files: list[Path] = []
    for scope in TEXT_SCOPES:
        path = ROOT / scope
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(
                candidate
                for candidate in path.rglob("*")
                if candidate.is_file()
                and candidate.suffix.lower() in {".md", ".json", ".yml", ".yaml"}
            )
    return sorted(set(files))


def reject_duplicate_object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    normalized: set[str] = set()
    for key, value in pairs:
        if not isinstance(key, str):
            raise ValidationError("JSON object keys must be strings")
        folded = key.casefold()
        if folded in normalized:
            raise ValidationError(f"duplicate JSON key: {key}")
        normalized.add(folded)
        result[key] = value
    return result


def load_json_strict(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_object_pairs,
        )
    except (OSError, UnicodeError, json.JSONDecodeError, ValidationError) as exc:
        raise ValidationError(f"{path.name}: invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationError(f"{path.name}: top-level value must be an object")
    return value


def load_yaml_strict(text: str) -> dict[str, Any]:
    if yaml is None:
        raise ValidationError("PyYAML is required for structural workflow validation")

    class UniqueKeyLoader(yaml.SafeLoader):
        pass

    # GitHub uses YAML 1.2 semantics for the ``on`` key. PyYAML's legacy 1.1
    # boolean resolver would otherwise turn it into True.
    for initial, resolvers in list(UniqueKeyLoader.yaml_implicit_resolvers.items()):
        UniqueKeyLoader.yaml_implicit_resolvers[initial] = [
            resolver
            for resolver in resolvers
            if resolver[0] != "tag:yaml.org,2002:bool"
        ]

    def construct_mapping(
        loader: UniqueKeyLoader, node: Any, deep: bool = False
    ) -> dict[str, Any]:
        pairs = loader.construct_pairs(node, deep=deep)
        result: dict[str, Any] = {}
        normalized: set[str] = set()
        for key, value in pairs:
            if not isinstance(key, str):
                raise ValidationError("workflow mapping keys must be strings")
            folded = key.casefold()
            if folded in normalized:
                raise ValidationError(f"duplicate workflow key: {key}")
            normalized.add(folded)
            result[key] = value
        return result

    UniqueKeyLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping
    )
    try:
        value = yaml.load(text, Loader=UniqueKeyLoader)
    except ValidationError:
        raise
    except yaml.YAMLError as exc:
        raise ValidationError(f"workflow YAML parse failed: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationError("workflow top-level value must be an object")
    return value


def load_manifest(errors: list[str]) -> dict[str, Any]:
    try:
        manifest = load_json_strict(MANIFEST_PATH)
    except ValidationError as exc:
        fail(str(exc), errors)
        return {}
    if manifest.get("schema") != "hawkinsoperations-command-center-invariants-v1":
        fail("manifest schema mismatch", errors)
    if set(manifest) != EXPECTED_MANIFEST_ROOT_KEYS:
        fail("manifest root shape is not closed", errors)
    invariants = manifest.get("invariants")
    if not isinstance(invariants, dict):
        fail("manifest invariants must be an object", errors)
    elif set(invariants) != EXPECTED_INVARIANT_KEYS:
        fail("manifest invariant shape is not closed", errors)
    elif any(not isinstance(value, str) or not value.strip() for value in invariants.values()):
        fail("manifest invariant values must be non-empty strings", errors)
    if not isinstance(manifest.get("scope"), str) or not manifest["scope"].strip():
        fail("manifest scope must be a non-empty string", errors)
    if not isinstance(manifest.get("required_route_files"), list):
        fail("manifest required_route_files must be an array", errors)
    if manifest.get("cross_repo_repositories") != EXACT_REPOSITORIES:
        fail("manifest cross-repository list is not canonical", errors)
    return manifest


def validate_source_manifest(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    allowed_root = {"schema", "manifest_id", "repositories", "constraints"}
    if set(value) != allowed_root:
        errors.append(
            f"source manifest root keys must be exactly {sorted(allowed_root)}"
        )
    if value.get("schema") != "hawkinsoperations-convergence-source-manifest-v1":
        errors.append("source manifest schema mismatch")
    if value.get("manifest_id") != "HAWKINSOPERATIONS_SEVEN_SOURCE_PR_HEAD_MATRIX_V1":
        errors.append("source manifest ID mismatch")
    entries = value.get("repositories")
    if not isinstance(entries, list):
        return [*errors, "source manifest repositories must be an ordered list"]
    if len(entries) != 7:
        errors.append("source manifest must contain exactly seven entries")
    seen: set[str] = set()
    observed: list[str] = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"source manifest entry {index} must be an object")
            continue
        repository = entry.get("repository")
        if not isinstance(repository, str):
            errors.append(f"source manifest entry {index} repository must be a string")
            continue
        folded = repository.casefold()
        if folded in seen:
            errors.append(f"source manifest repository duplicated: {repository}")
        seen.add(folded)
        observed.append(repository)
        expected_full = f"HawkinsOperations/{repository}"
        if entry.get("canonical_repository") != expected_full:
            errors.append(f"source manifest canonical owner mismatch: {repository}")
        if repository == ".github":
            if set(entry) != {
                "repository",
                "canonical_repository",
                "revision_source",
                "tree_source",
            }:
                errors.append(".github source entry has an unsupported shape")
            if entry.get("revision_source") != "github_event_sha":
                errors.append(".github source entry must use github_event_sha")
            if entry.get("tree_source") != "github_event_tree":
                errors.append(".github source entry must use github_event_tree")
        else:
            if set(entry) != {
                "repository",
                "canonical_repository",
                "revision",
                "reviewed_tree_sha",
            }:
                errors.append(f"source manifest entry has an unsupported shape: {repository}")
            if re.fullmatch(r"[0-9a-f]{40}", str(entry.get("revision", ""))) is None:
                errors.append(f"source manifest revision is not immutable: {repository}")
            if re.fullmatch(
                r"[0-9a-f]{40}", str(entry.get("reviewed_tree_sha", ""))
            ) is None:
                errors.append(f"source manifest reviewed tree is not immutable: {repository}")
    if observed != EXACT_REPOSITORIES:
        errors.append("source manifest repositories must equal the exact canonical order")
    constraints = value.get("constraints")
    expected_constraints = {
        "exact_repository_count": 7,
        "read_only": True,
        "default_branch_fallback": False,
        "require_detached_exact_revision": True,
        "record_checked_revisions": True,
        "consumer_outputs_are_not_authority": True,
        "proof_ceiling": PROOF_CEILING,
    }
    if constraints != expected_constraints:
        errors.append("source manifest constraints do not match the fail-closed contract")
    return errors


def load_source_manifest(errors: list[str]) -> dict[str, Any]:
    try:
        manifest = load_json_strict(SOURCE_MANIFEST_PATH)
    except ValidationError as exc:
        fail(str(exc), errors)
        return {}
    for error in validate_source_manifest(manifest):
        fail(error, errors)
    return manifest


def check_required_files(manifest: dict[str, Any], errors: list[str]) -> None:
    required = manifest.get("required_route_files", [])
    if not isinstance(required, list) or not required:
        fail("manifest required_route_files must be a non-empty list", errors)
        return
    if "governance/CONVERGENCE_SOURCE_MANIFEST.json" not in required:
        fail("command-center manifest must require the convergence source manifest", errors)
    for item in required:
        rel = PurePosixPath(str(item))
        if rel.is_absolute() or ".." in rel.parts or "\\" in str(item):
            fail(f"invalid required route path: {item}", errors)
            continue
        if not (ROOT / Path(*rel.parts)).is_file():
            fail(f"missing required route file: {item}", errors)


def walk(value: Any, path: tuple[str, ...] = ()):
    yield path, value
    if isinstance(value, dict):
        for key, nested in value.items():
            yield from walk(nested, (*path, str(key)))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            yield from walk(nested, (*path, str(index)))


def scalar_is_false(value: Any) -> bool:
    return value is False or (isinstance(value, str) and value.casefold() == "false")


def unsafe_workflow_findings(text: str) -> list[str]:
    findings: list[str] = []
    try:
        workflow = load_yaml_strict(text)
    except ValidationError as exc:
        return [str(exc)]

    allowed_root_keys = {"name", "on", "permissions", "jobs"}
    if set(workflow) != allowed_root_keys:
        findings.append("workflow root shape is not closed")
    triggers = workflow.get("on")
    if not isinstance(triggers, dict):
        findings.append("workflow trigger declaration must be an object")
    else:
        allowed_triggers = {"pull_request", "push", "workflow_dispatch", "schedule"}
        if set(triggers) != allowed_triggers:
            findings.append("workflow triggers differ from the approved read-only set")
        if "pull_request_target" in triggers:
            findings.append("pull_request_target is forbidden")
        schedule = triggers.get("schedule")
        if not isinstance(schedule, list) or not schedule:
            findings.append("scheduled drift detection is required")
        if not isinstance(triggers.get("workflow_dispatch"), dict):
            findings.append("manual read-only dispatch is required")
        pull_request = triggers.get("pull_request")
        push = triggers.get("push")
        required_paths = {
            "README.md",
            "profile/**",
            "architecture/**",
            "governance/**",
            "wiki/**",
            ".github/pull_request_template.md",
            ".github/workflows/command-center-invariants.yml",
            "scripts/verify-command-center-invariants.py",
            "tests/**",
        }
        if not isinstance(pull_request, dict) or set(pull_request) != {"paths"}:
            findings.append("pull_request trigger shape must be unrestricted except approved paths")
        elif set(pull_request.get("paths", [])) != required_paths:
            findings.append("pull_request paths must cover every governed verifier surface")
        if not isinstance(push, dict) or set(push) != {"branches", "paths"}:
            findings.append("push trigger shape must be exactly branches and paths")
        else:
            if push.get("branches") != ["main"]:
                findings.append("push trigger must govern main exactly")
            if set(push.get("paths", [])) != required_paths:
                findings.append("push paths must cover every governed verifier surface")

    if workflow.get("permissions") != {"contents": "read"}:
        findings.append("root permissions must be exactly contents: read")
    jobs = workflow.get("jobs")
    if not isinstance(jobs, dict) or set(jobs) != {
        "command-center-invariants",
        "seven-repository-convergence",
    }:
        findings.append("workflow jobs must be the exact approved pair")
    else:
        expected_step_names = {
            "command-center-invariants": [
                "Checkout command-center authority",
                "Set up Python",
                "Install structural verifier dependency",
                "Verify command-center invariants",
                "Run hostile command-center unit tests",
                "Verify patch whitespace",
            ],
            "seven-repository-convergence": [
                "Checkout workflow authority at the event revision",
                "Set up Python",
                "Set up Node",
                "Install bounded verifier dependencies",
                "Resolve governance/CONVERGENCE_SOURCE_MANIFEST.json",
                "Checkout six immutable sibling revisions without credentials",
                "Verify the exact clean detached source set",
                "Detect durable sibling main-content drift",
                "Verify detection authority and hostile paths",
                "Verify validation authority and fail-closed parity",
                "Verify proof authority and reverse inventory",
                "Verify platform source contract and seven-source convergence",
                "Install Hoxline from the checked immutable source",
                "Verify Hoxline Case Growth pair and replay integrity",
                "Install Website dependencies from the checked lockfile",
                "Verify Website rendering-only status plane and static build",
                "Write closed-schema verification summary",
                "Validate upload artifacts",
                "Upload sanitized convergence records",
            ],
        }
        for job_name, expected_names in expected_step_names.items():
            job = jobs.get(job_name)
            if not isinstance(job, dict):
                findings.append(f"{job_name} job must be an object")
                continue
            if "if" in job:
                findings.append(f"{job_name} mandatory job must not be conditional")
            steps = job.get("steps")
            if not isinstance(steps, list):
                findings.append(f"{job_name} steps must be an array")
                continue
            names = [step.get("name") if isinstance(step, dict) else None for step in steps]
            if names != expected_names:
                findings.append(f"{job_name} step order differs from the approved contract")
            for step in steps:
                if not isinstance(step, dict):
                    findings.append(f"{job_name} contains a non-object step")
                    continue
                condition = step.get("if")
                if step.get("name") == "Detect durable sibling main-content drift":
                    if condition != "github.event_name != 'pull_request'":
                        findings.append("durable main observation condition is not exact")
                elif condition is not None:
                    findings.append(f"mandatory step is conditional: {step.get('name')}")
        convergence_steps = jobs["seven-repository-convergence"].get("steps", [])
        if isinstance(convergence_steps, list):
            names = [step.get("name") for step in convergence_steps if isinstance(step, dict)]
            try:
                validate_index = names.index("Validate upload artifacts")
                upload_index = names.index("Upload sanitized convergence records")
                if upload_index != validate_index + 1:
                    findings.append("artifact validation must be immediately before upload")
            except ValueError:
                findings.append("artifact validation/upload steps are missing")

    checkout_count = 0
    source_set_checkout = False
    upload_count = 0
    for path, value in walk(workflow):
        key = path[-1].casefold() if path else ""
        if key == "continue-on-error":
            findings.append("continue-on-error is forbidden")
        if key == "permissions":
            if path != ("permissions",):
                findings.append("job or step permission override is forbidden")
        if key in {"contents", "actions", "checks", "issues", "packages", "pages",
                   "pull-requests", "security-events", "statuses", "id-token"}:
            if isinstance(value, str) and value.casefold() == "write":
                findings.append(f"write permission is forbidden at {'/'.join(path)}")
        if key == "if" and isinstance(value, str):
            if re.search(r"\balways\s*\(\s*\)", value, re.IGNORECASE):
                findings.append("always() is forbidden because it can neutralize failure ordering")
        if key == "run" and isinstance(value, str) and "\n" in value:
            if "set -euo pipefail" not in value:
                findings.append("multiline shell steps must enable strict exit propagation")
        if key == "run" and isinstance(value, str):
            if re.search(r"(?im)^\s*(?:echo|printf)\b.*\b(?:python|git)\b", value):
                findings.append("required command may not be replaced by inert output")
        if key == "uses" and isinstance(value, str):
            match = re.fullmatch(r"([^@]+)@([0-9a-f]{40})", value)
            if match is None:
                findings.append(f"action must be pinned to an immutable SHA: {value}")
            elif PINNED_ACTIONS.get(match.group(1)) != match.group(2):
                findings.append(f"action SHA is not allowlisted: {value}")
            if value.startswith("actions/checkout@"):
                checkout_count += 1
                step_path = path[:-1]
                step: Any = workflow
                for component in step_path:
                    step = step[int(component)] if isinstance(step, list) else step[component]
                checkout_with = step.get("with") if isinstance(step, dict) else None
                if not isinstance(checkout_with, dict) or not scalar_is_false(
                    checkout_with.get("persist-credentials")
                ):
                    findings.append("checkout must set persist-credentials: false")
                if isinstance(checkout_with, dict) and checkout_with.get("path") == "source-set/.github":
                    source_set_checkout = True
                    expected_ref = "${{ github.event.pull_request.head.sha || github.sha }}"
                    if checkout_with.get("ref") != expected_ref:
                        findings.append(
                            "source-set .github checkout must use the immutable event SHA"
                        )
            if value.startswith("actions/upload-artifact@"):
                upload_count += 1
                step_path = path[:-1]
                step = workflow
                for component in step_path:
                    step = step[int(component)] if isinstance(step, list) else step[component]
                upload_with = step.get("with") if isinstance(step, dict) else None
                expected_paths = (
                    "verification-artifacts/source-revisions.json\n"
                    "verification-artifacts/verification-summary.json\n"
                )
                if (
                    not isinstance(upload_with, dict)
                    or upload_with.get("path") != expected_paths
                    or upload_with.get("if-no-files-found") != "error"
                ):
                    findings.append(
                        "artifact upload must use the exact sanitized two-file allowlist"
                    )

    if checkout_count != 2:
        findings.append(
            "workflow must perform exactly one credential-bounded checkout in each job"
        )
    if not source_set_checkout:
        findings.append("seven-source job must checkout .github under source-set/.github")
    if upload_count != 1:
        findings.append("workflow must contain exactly one sanitized artifact upload")

    forbidden_text_patterns = {
        "pull_request_target": r"(?m)^\s*pull_request_target\s*:",
        "direct push": r"\bgit\s+push\b",
        "remote mutation": r"\bgit\s+(?:commit|tag)\b",
        "PR mutation": r"\b(?:gh\s+pr\s+(?:create|merge|ready|review)|gh\s+api[^\n]*(?:POST|PATCH|PUT|DELETE))\b",
        "HTTP PR mutation": r"\bcurl\b[^\n]*(?:-X|--request)\s*(?:POST|PATCH|PUT|DELETE)[^\n]*(?:api\.github\.com|/pulls\b)",
        "auto-merge": r"\bauto-merge\b",
        "ledger mutation": r"\b(?:lifetime|ledger)[^\n]*(?:append|correct|mutate|write)\b",
        "runtime mutation": r"\b(?:runtime|endpoint|wazuh|splunk|cribl)[^\n]*(?:mutate|deploy|configure|restart|write)\b",
        "proof promotion": r"\b(?:proof|public.safe)[^\n]*(?:promote|publish|approve)\b",
        "swallowed failure": r"(?:\|\|\s*(?:true|echo|printf)\b|\bset\s+\+e\b|\btrap\b[^\n]*\bexit\s+0\b)",
        "backgrounded command": r"(?m)(?<!&)&(?!&)(?:\s*(?:wait\b.*)?)?\s*$",
        "unconditional success": r"(?m)^\s*(?:exit\s+0|true)\s*$",
        "mutable branch fallback": r"\b(?:main|master)\b[^\n]*(?:fallback|default)|ref\s*=\s*[\"']?(?:main|master)",
        "credential persistence": r"persist-credentials\s*:\s*(?:true|yes|on|1)\b",
    }
    for label, pattern in forbidden_text_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            findings.append(label)

    required_fragments = [
        "seven-repository-convergence:",
        "governance/CONVERGENCE_SOURCE_MANIFEST.json",
        "--emit-source-manifest",
        "--verify-source-set",
        "--verify-remote-main-content",
        "while IFS=$'\\t' read -r repo revision",
        'git -C "source-set/$repo" fetch --quiet --depth=1 origin "$revision"',
        'git -C "source-set/$repo" checkout --quiet --detach "$revision"',
        "source-revisions.json",
        "HAWKINS_PROOF_IMMUTABLE_MANIFEST_SHA",
        "verify_detection_contract.py",
        "verify_detection_promotion_matrix.py",
        "verify_validation_registry.py",
        "verify_all_validation_packages.py",
        "verify_validation_contract.py",
        "verify_detection_proof_status_index.py",
        "verify_proof_integrity.py",
        "verify-public-status-source-contract.py",
        "hoxline-case-growth-convergence-verify",
        "case-growth index",
        "case-growth verify",
        "review batch run",
        "review batch verify",
        "public-status:generate:check",
        "public-status:verify",
        "public-status:self-test",
        "public-status:owner-self-test",
        "public-status:source-checkout-test",
        "public-status:freshness-reachability-test",
        "public-status:nested-claim-test",
        "public-status:eol-self-test",
        "git diff --check",
        "--write-verification-summary",
        "--validate-artifacts",
        "verification-artifacts/source-revisions.json",
        "verification-artifacts/verification-summary.json",
    ]
    for fragment in required_fragments:
        if fragment not in text:
            findings.append(f"workflow missing required behavior: {fragment}")
    exact_executed_patterns = {
        "detection contract": r"(?m)^\s*python -B source-set/hawkinsoperations-detections/scripts/verify_detection_contract\.py\s*$",
        "detection matrix": r"(?m)^\s*python -B source-set/hawkinsoperations-detections/scripts/verify_detection_promotion_matrix\.py\s*$",
        "sibling fetch": r'(?m)^\s*git -C "source-set/\$repo" fetch --quiet --depth=1 origin "\$revision"\s*$',
        "sibling checkout": r'(?m)^\s*git -C "source-set/\$repo" checkout --quiet --detach "\$revision"\s*$',
    }
    for label, pattern in exact_executed_patterns.items():
        if re.search(pattern, text) is None:
            findings.append(f"workflow does not execute exact required command: {label}")
    return sorted(set(findings))


def check_cross_repo_workflow(
    manifest: dict[str, Any],
    source_manifest: dict[str, Any],
    errors: list[str],
) -> None:
    workflow_text = read_text(WORKFLOW_PATH, errors)
    declared = manifest.get("cross_repo_repositories")
    if declared != EXACT_REPOSITORIES:
        fail(
            "manifest cross_repo_repositories must list the exact seven repositories in canonical order",
            errors,
        )
    if [entry.get("repository") for entry in source_manifest.get("repositories", [])] != EXACT_REPOSITORIES:
        fail("source manifest and invariant repository order disagree", errors)
    for finding in unsafe_workflow_findings(workflow_text):
        fail(f"cross-repo workflow permits unsafe behavior: {finding}", errors)


def check_workflow_hostile_self_test(errors: list[str]) -> None:
    base = WORKFLOW_PATH.read_text(encoding="utf-8")
    hostile_cases = {
        "write permission": base.replace("contents: read", "issues: write", 1),
        "pull_request_target": base.replace("pull_request:", "pull_request_target:", 1),
        "continue-on-error": base.replace(
            "run: python scripts/verify-command-center-invariants.py --self-test",
            "continue-on-error: true\n        run: python scripts/verify-command-center-invariants.py --self-test",
            1,
        ),
        "persisted credentials": base.replace(
            "persist-credentials: false", "persist-credentials: true", 1
        ),
        "mutable action": base.replace(
            f"actions/checkout@{PINNED_ACTIONS['actions/checkout']}",
            "actions/checkout@v4",
            1,
        ),
        "swallowed failure": base.replace("set -euo pipefail", "set -euo pipefail\n          false || true", 1),
        "direct push": base.replace("set -euo pipefail", "set -euo pipefail\n          git push origin main", 1),
        "always step": base.replace(
            "- name: Validate upload artifacts",
            "- name: Validate upload artifacts\n        if: always()",
            1,
        ),
    }
    for name, hostile in hostile_cases.items():
        if not unsafe_workflow_findings(hostile):
            fail(f"workflow hostile self-test accepted {name}", errors)

    try:
        source = load_json_strict(SOURCE_MANIFEST_PATH)
    except ValidationError as exc:
        fail(f"source-manifest hostile self-test precondition failed: {exc}", errors)
        return
    for name, mutate in {
        "missing repository": lambda value: value["repositories"].pop(),
        "duplicate repository": lambda value: value["repositories"].append(
            dict(value["repositories"][0])
        ),
        "mutable revision": lambda value: value["repositories"][1].update(
            {"revision": "main"}
        ),
        "owner spoof": lambda value: value["repositories"][1].update(
            {"canonical_repository": "NotHawkinsOperations/hawkinsoperations-detections"}
        ),
        "fallback enabled": lambda value: value["constraints"].update(
            {"default_branch_fallback": True}
        ),
    }.items():
        candidate = json.loads(json.dumps(source))
        mutate(candidate)
        if not validate_source_manifest(candidate):
            fail(f"source-manifest hostile self-test accepted {name}", errors)


def canonical_origin(value: str) -> str:
    normalized = value.strip().rstrip("/").casefold()
    if normalized.startswith("git@github.com:"):
        normalized = "https://github.com/" + normalized.removeprefix("git@github.com:")
    elif normalized.startswith("ssh://git@github.com/"):
        normalized = "https://github.com/" + normalized.removeprefix(
            "ssh://git@github.com/"
        )
    if not normalized.endswith(".git"):
        normalized += ".git"
    return normalized


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise ValidationError(
            f"{repo.name}: git {' '.join(args)} failed: {result.stderr.strip()}"
        )
    return result.stdout.strip()


def resolved_source_manifest(
    manifest: dict[str, Any], event_sha: str, event_tree_sha: str | None = None
) -> dict[str, Any]:
    if re.fullmatch(r"[0-9a-f]{40}", event_sha) is None:
        raise ValidationError("event SHA must be a lowercase 40-character Git SHA")
    if validate_source_manifest(manifest):
        raise ValidationError("cannot resolve an invalid source manifest")
    if event_tree_sha is None:
        event_tree_sha = git(ROOT, "rev-parse", f"{event_sha}^{{tree}}")
    if re.fullmatch(r"[0-9a-f]{40}", event_tree_sha) is None:
        raise ValidationError("event tree SHA must be a lowercase 40-character Git SHA")
    entries = []
    for entry in manifest["repositories"]:
        revision = event_sha if entry["repository"] == ".github" else entry["revision"]
        reviewed_tree = (
            event_tree_sha
            if entry["repository"] == ".github"
            else entry["reviewed_tree_sha"]
        )
        entries.append(
            {
                "repository": entry["repository"],
                "canonical_repository": entry["canonical_repository"],
                "revision": revision,
                "reviewed_tree_sha": reviewed_tree,
            }
        )
    payload = {
        "schema": "hawkinsoperations-resolved-convergence-source-set-v1",
        "manifest_id": manifest["manifest_id"],
        "repositories": entries,
        "constraints": manifest["constraints"],
    }
    payload["manifest_sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return payload


def validate_resolved_manifest(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    allowed = {
        "schema",
        "manifest_id",
        "repositories",
        "constraints",
        "manifest_sha256",
    }
    if set(value) != allowed:
        errors.append("resolved source manifest has unsupported fields")
        return errors
    if value.get("schema") != "hawkinsoperations-resolved-convergence-source-set-v1":
        errors.append("resolved source manifest schema mismatch")
    repositories = value.get("repositories")
    if not isinstance(repositories, list) or len(repositories) != 7:
        errors.append("resolved source manifest must contain exactly seven entries")
        return errors
    observed: list[str] = []
    for entry in repositories:
        if not isinstance(entry, dict) or set(entry) != {
            "repository",
            "canonical_repository",
            "revision",
            "reviewed_tree_sha",
        }:
            errors.append("resolved source entry has unsupported shape")
            continue
        repository = entry.get("repository")
        observed.append(str(repository))
        if entry.get("canonical_repository") != f"HawkinsOperations/{repository}":
            errors.append(f"resolved source owner mismatch: {repository}")
        if re.fullmatch(r"[0-9a-f]{40}", str(entry.get("revision", ""))) is None:
            errors.append(f"resolved source revision invalid: {repository}")
        if re.fullmatch(
            r"[0-9a-f]{40}", str(entry.get("reviewed_tree_sha", ""))
        ) is None:
            errors.append(f"resolved source reviewed tree invalid: {repository}")
    if observed != EXACT_REPOSITORIES or len(set(observed)) != 7:
        errors.append("resolved source repositories differ from exact canonical set")
    if value.get("constraints") != {
        "exact_repository_count": 7,
        "read_only": True,
        "default_branch_fallback": False,
        "require_detached_exact_revision": True,
        "record_checked_revisions": True,
        "consumer_outputs_are_not_authority": True,
        "proof_ceiling": PROOF_CEILING,
    }:
        errors.append("resolved source constraints mismatch")
    unsigned = {key: nested for key, nested in value.items() if key != "manifest_sha256"}
    expected = hashlib.sha256(
        json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    if value.get("manifest_sha256") != expected:
        errors.append("resolved source manifest digest mismatch")
    return errors


def verify_source_set(
    source_set: Path, resolved: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[str]]:
    errors = validate_resolved_manifest(resolved)
    if errors:
        return [], errors
    if not source_set.is_dir() or source_set.is_symlink():
        return [], ["source-set root must be a real directory"]
    actual_names = sorted(
        path.name
        for path in source_set.iterdir()
        if path.is_dir() and not path.is_symlink()
    )
    if actual_names != sorted(EXACT_REPOSITORIES):
        errors.append("source-set directory inventory must equal exactly seven repositories")
        return [], errors
    records: list[dict[str, Any]] = []
    for entry in resolved["repositories"]:
        repository = entry["repository"]
        repo_path = source_set / repository
        try:
            if repo_path.resolve().parent != source_set.resolve():
                raise ValidationError(f"{repository}: repository path escapes source-set root")
            head = git(repo_path, "rev-parse", "HEAD")
            if head != entry["revision"]:
                raise ValidationError(
                    f"{repository}: checked HEAD {head} differs from manifest {entry['revision']}"
                )
            tree = git(repo_path, "rev-parse", "HEAD^{tree}")
            if tree != entry["reviewed_tree_sha"]:
                raise ValidationError(
                    f"{repository}: checked tree {tree} differs from reviewed content "
                    f"{entry['reviewed_tree_sha']}"
                )
            branch = git(repo_path, "rev-parse", "--abbrev-ref", "HEAD")
            if branch != "HEAD":
                raise ValidationError(f"{repository}: checkout must be detached at exact revision")
            origin = git(repo_path, "remote", "get-url", "origin")
            if canonical_origin(origin) != canonical_origin(CANONICAL_ORIGINS[repository]):
                raise ValidationError(f"{repository}: canonical origin mismatch")
            status = git(repo_path, "status", "--porcelain=v1", "--untracked-files=all")
            if status:
                raise ValidationError(f"{repository}: source checkout is dirty")
            records.append(
                {
                    "repository": repository,
                    "canonical_repository": entry["canonical_repository"],
                    "checked_sha": head,
                    "checked_tree_sha": tree,
                    "detached": True,
                    "clean": True,
                }
            )
        except ValidationError as exc:
            errors.append(str(exc))
    return records, errors


def compare_observed_main_trees(
    resolved: dict[str, Any], observed: dict[str, str]
) -> list[str]:
    errors = validate_resolved_manifest(resolved)
    if errors:
        return errors
    expected = {
        entry["repository"]: entry["reviewed_tree_sha"]
        for entry in resolved["repositories"]
        if entry["repository"] != ".github"
    }
    if set(observed) != set(expected):
        return ["remote main observations must cover exactly the six sibling repositories"]
    for repository, expected_tree in expected.items():
        actual_tree = observed.get(repository)
        if actual_tree != expected_tree:
            errors.append(
                f"{repository}: current main content tree {actual_tree} differs from "
                f"reviewed tree {expected_tree}; refresh the reviewed source matrix"
            )
    return errors


def verify_remote_main_content(
    source_set: Path, resolved: dict[str, Any]
) -> list[str]:
    errors = validate_resolved_manifest(resolved)
    if errors:
        return errors
    observed: dict[str, str] = {}
    for entry in resolved["repositories"]:
        repository = entry["repository"]
        if repository == ".github":
            continue
        url = CANONICAL_ORIGINS[repository]
        result = subprocess.run(
            ["git", "ls-remote", "--exit-code", url, "refs/heads/main"],
            check=False,
            capture_output=True,
            text=True,
        )
        fields = result.stdout.strip().split()
        if result.returncode != 0 or len(fields) != 2 or fields[1] != "refs/heads/main":
            errors.append(f"{repository}: current main observation is unavailable")
            continue
        main_sha = fields[0]
        if re.fullmatch(r"[0-9a-f]{40}", main_sha) is None:
            errors.append(f"{repository}: current main observation is malformed")
            continue
        repo_path = source_set / repository
        fetch = subprocess.run(
            ["git", "-C", str(repo_path), "fetch", "--quiet", "--depth=1", "origin", main_sha],
            check=False,
            capture_output=True,
            text=True,
        )
        if fetch.returncode:
            errors.append(f"{repository}: current main content cannot be fetched")
            continue
        try:
            observed[repository] = git(repo_path, "rev-parse", f"{main_sha}^{{tree}}")
        except ValidationError as exc:
            errors.append(str(exc))
    if errors:
        return errors
    return compare_observed_main_trees(resolved, observed)


def is_private_scalar(value: str) -> bool:
    decoded = value
    for _ in range(3):
        next_value = unquote(decoded)
        if next_value == decoded:
            break
        decoded = next_value
    variants = {value, decoded, decoded.replace("\\", "/")}
    for candidate in variants:
        lowered = candidate.casefold()
        if (
            PureWindowsPath(candidate).is_absolute()
            or PurePosixPath(candidate).is_absolute()
            or re.match(r"^[a-z]:[^/\\]", lowered)
            or lowered.startswith(("\\\\", "//", "file:", "~", "$home", "${home}"))
            or "../" in lowered
            or "/users/" in lowered
            or "/home/" in lowered
            or "/raylee/" in lowered
        ):
            return True
        if re.search(
            r"(?:github[_-]?pat_|ghp_|begin (?:rsa |openssh )?private key|"
            r"\bAKIA[0-9A-Z]{16}\b|\bbearer\s+[a-z0-9._~+/=-]{12,}\b|"
            r"\beyJ[a-z0-9_-]{8,}\.[a-z0-9_-]{8,}\.[a-z0-9_-]{8,}\b|"
            r"\b(?:10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}\b|"
            r"\b172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}\b|"
            r"\b192\.168\.\d{1,3}\.\d{1,3}\b|"
            r"@[a-z0-9.-]+\.[a-z]{2,}\b|"
            r"\b(?:customer|mufg)\b)",
            lowered,
        ):
            return True
    return False


def validate_artifact_payloads(directory: Path) -> list[str]:
    errors: list[str] = []
    if not directory.is_dir() or directory.is_symlink():
        return ["artifact path must be a real directory"]
    files = {path.name for path in directory.iterdir() if path.is_file()}
    if files != EXPECTED_ARTIFACT_FILES:
        errors.append(
            f"artifact file set must be exactly {sorted(EXPECTED_ARTIFACT_FILES)}"
        )
        return errors
    for path in directory.iterdir():
        if path.is_symlink() or not path.is_file():
            errors.append(f"artifact directory contains unsupported entry: {path.name}")
    payloads: dict[str, dict[str, Any]] = {}
    for name in EXPECTED_ARTIFACT_FILES:
        try:
            payloads[name] = load_json_strict(directory / name)
        except ValidationError as exc:
            errors.append(str(exc))
    revisions = payloads.get("source-revisions.json")
    if revisions is not None:
        resolved_fields = {
            key: value
            for key, value in revisions.items()
            if key != "checked_repositories"
        }
        for error in validate_resolved_manifest(resolved_fields):
            errors.append(f"source-revisions.json: {error}")
        checked = revisions.get("checked_repositories")
        expected_by_repo = {
            entry["repository"]: entry["revision"]
            for entry in revisions.get("repositories", [])
            if isinstance(entry, dict)
        }
        if not isinstance(checked, list) or len(checked) != 7:
            errors.append("source-revisions.json: checked_repositories must contain seven records")
        else:
            observed_checked: list[str] = []
            for entry in checked:
                if not isinstance(entry, dict) or set(entry) != {
                    "repository",
                    "canonical_repository",
                    "checked_sha",
                    "checked_tree_sha",
                    "detached",
                    "clean",
                }:
                    errors.append(
                        "source-revisions.json: checked repository record has unsupported fields"
                    )
                    continue
                repository = entry.get("repository")
                observed_checked.append(str(repository))
                if entry.get("canonical_repository") != f"HawkinsOperations/{repository}":
                    errors.append(
                        f"source-revisions.json: checked owner mismatch: {repository}"
                    )
                if entry.get("checked_sha") != expected_by_repo.get(str(repository)):
                    errors.append(
                        f"source-revisions.json: checked SHA mismatch: {repository}"
                    )
                reviewed_trees = {
                    item["repository"]: item.get("reviewed_tree_sha")
                    for item in revisions.get("repositories", [])
                    if isinstance(item, dict)
                }
                if entry.get("checked_tree_sha") != reviewed_trees.get(str(repository)):
                    errors.append(
                        f"source-revisions.json: checked tree mismatch: {repository}"
                    )
                if entry.get("detached") is not True or entry.get("clean") is not True:
                    errors.append(
                        f"source-revisions.json: checked state is not clean and detached: {repository}"
                    )
            if observed_checked != EXACT_REPOSITORIES:
                errors.append(
                    "source-revisions.json: checked repositories differ from exact order"
                )
    summary = payloads.get("verification-summary.json")
    if summary is not None:
        allowed = {
            "schema",
            "status",
            "repository_count",
            "repositories",
            "checks",
            "mutation_boundary",
            "proof_ceiling",
        }
        if set(summary) != allowed:
            errors.append("verification summary has unsupported fields")
        if summary.get("schema") != "hawkinsoperations-convergence-verification-summary-v1":
            errors.append("verification summary schema mismatch")
        if summary.get("status") != "PASS":
            errors.append("verification summary status must be PASS")
        if summary.get("repository_count") != 7:
            errors.append("verification summary repository count must be seven")
        if summary.get("repositories") != EXACT_REPOSITORIES:
            errors.append("verification summary repository set mismatch")
        checks = summary.get("checks")
        if checks != EXPECTED_VERIFICATION_CHECKS:
            errors.append("verification summary check list differs from the exact approved checks")
        if summary.get("mutation_boundary") != {
            "repository_writes": False,
            "pull_request_mutation": False,
            "merge": False,
            "ledger_mutation": False,
            "runtime_mutation": False,
            "proof_promotion": False,
        }:
            errors.append("verification summary mutation boundary mismatch")
        if summary.get("proof_ceiling") != PROOF_CEILING:
            errors.append("verification summary proof ceiling mismatch")
    for name, payload in payloads.items():
        for path, value in walk(payload):
            if isinstance(value, str) and is_private_scalar(value):
                errors.append(
                    f"{name}: private or unsafe scalar at {'/'.join(path) or '<root>'}"
                )
    return errors


def write_json_atomic(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=False) + "\n", encoding="utf-8", newline="\n"
    )
    temporary.replace(path)


def write_verification_summary(path: Path) -> None:
    write_json_atomic(
        path,
        {
            "schema": "hawkinsoperations-convergence-verification-summary-v1",
            "status": "PASS",
            "repository_count": 7,
            "repositories": EXACT_REPOSITORIES,
            "checks": EXPECTED_VERIFICATION_CHECKS,
            "mutation_boundary": {
                "repository_writes": False,
                "pull_request_mutation": False,
                "merge": False,
                "ledger_mutation": False,
                "runtime_mutation": False,
                "proof_promotion": False,
            },
            "proof_ceiling": PROOF_CEILING,
        },
    )


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
    required = (
        "Do not close unless Raylee explicitly approves replacing "
        "the standing-control role"
    )
    if required not in all_text:
        fail("missing explicit replacement-approval boundary for .github#8/#10", errors)


def check_exposure(text_files: list[Path], errors: list[str]) -> None:
    token_prefixes = ["AK" + "IA", "ghp" + "_", "github" + "_pat" + "_"]
    private_ip = re.compile(
        r"\b(10\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
        r"172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|"
        r"192\.168\.\d{1,3}\.\d{1,3})\b"
    )
    drive_path = re.compile(r"\b[A-Za-z]:\\")
    private_key = re.compile(r"BEGIN (?:RSA |OPENSSH )?PRIVATE KEY")
    for path in text_files:
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line_no, line in enumerate(text.splitlines(), start=1):
            # Defensive test literals in this verifier are never uploaded or public data.
            if rel == "scripts/verify-command-center-invariants.py":
                continue
            if drive_path.search(line):
                fail(f"{rel}:{line_no} exposes a local Windows path", errors)
            if private_ip.search(line):
                fail(f"{rel}:{line_no} exposes a private IP address", errors)
            if private_key.search(line):
                fail(f"{rel}:{line_no} exposes a private-key marker", errors)
            for prefix in token_prefixes:
                if prefix in line:
                    fail(f"{rel}:{line_no} exposes a token-looking prefix", errors)


def check_identity_and_claim_context(
    text_files: list[Path], errors: list[str]
) -> None:
    for path in text_files:
        rel = path.relative_to(ROOT).as_posix()
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        for line_no, line in enumerate(lines, start=1):
            lowered = line.lower()
            if "hawkinsops" in lowered and not any(
                marker in lowered
                for marker in ("legacy", "reference", "v1", "prior", "not current")
            ):
                fail(
                    f"{rel}:{line_no} uses HawkinsOps outside legacy/reference context",
                    errors,
                )
            for phrase in BLOCKED_CLAIMS:
                phrase_pattern = re.compile(
                    rf"(?<![A-Za-z]){re.escape(phrase.lower())}(?![A-Za-z])"
                )
                if not phrase_pattern.search(lowered):
                    continue
                context_start = max(0, line_no - 15)
                context_end = min(len(lines), line_no + 5)
                context = "\n".join(lines[context_start:context_end]).lower()
                if not any(marker in context for marker in BOUNDARY_WORDS):
                    fail(
                        f"{rel}:{line_no} uses blocked claim phrase without boundary context: {phrase}",
                        errors,
                    )


def run_full_verification(self_test: bool) -> list[str]:
    errors: list[str] = []
    manifest = load_manifest(errors)
    source_manifest = load_source_manifest(errors)
    check_required_files(manifest, errors)
    check_cross_repo_workflow(manifest, source_manifest, errors)
    if self_test:
        check_workflow_hostile_self_test(errors)
    check_required_text(errors)
    text_files = iter_text_files()
    all_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore") for path in text_files
    )
    check_project_boundaries(all_text, errors)
    check_ceiling_boundaries(all_text, errors)
    check_standing_controls(all_text, errors)
    check_exposure(text_files, errors)
    check_identity_and_claim_context(text_files, errors)
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--emit-source-manifest", type=Path)
    parser.add_argument("--event-sha")
    parser.add_argument("--verify-source-set", type=Path)
    parser.add_argument("--verify-remote-main-content", type=Path)
    parser.add_argument("--resolved-manifest", type=Path)
    parser.add_argument("--source-revisions-output", type=Path)
    parser.add_argument("--write-verification-summary", type=Path)
    parser.add_argument("--validate-artifacts", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors: list[str] = []

    if args.emit_source_manifest is not None:
        try:
            source_manifest = load_json_strict(SOURCE_MANIFEST_PATH)
            resolved = resolved_source_manifest(source_manifest, str(args.event_sha or ""))
            write_json_atomic(args.emit_source_manifest, resolved)
        except ValidationError as exc:
            errors.append(str(exc))
    elif args.verify_source_set is not None:
        if args.resolved_manifest is None or args.source_revisions_output is None:
            errors.append(
                "--verify-source-set requires --resolved-manifest and --source-revisions-output"
            )
        else:
            try:
                resolved = load_json_strict(args.resolved_manifest)
                records, source_errors = verify_source_set(args.verify_source_set, resolved)
                errors.extend(source_errors)
                if not errors:
                    output = dict(resolved)
                    output["checked_repositories"] = records
                    # The uploaded source-revisions artifact deliberately omits origins
                    # and local paths; only canonical owner and immutable revisions remain.
                    write_json_atomic(args.source_revisions_output, output)
            except ValidationError as exc:
                errors.append(str(exc))
    elif args.verify_remote_main_content is not None:
        if args.resolved_manifest is None:
            errors.append("--verify-remote-main-content requires --resolved-manifest")
        else:
            try:
                resolved = load_json_strict(args.resolved_manifest)
                errors.extend(
                    verify_remote_main_content(args.verify_remote_main_content, resolved)
                )
            except ValidationError as exc:
                errors.append(str(exc))
    elif args.write_verification_summary is not None:
        write_verification_summary(args.write_verification_summary)
    elif args.validate_artifacts is not None:
        errors.extend(validate_artifact_payloads(args.validate_artifacts))
    else:
        errors.extend(run_full_verification(args.self_test))

    if errors:
        print("COMMAND_CENTER_INVARIANTS=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("COMMAND_CENTER_INVARIANTS=PASS")
    if args.emit_source_manifest:
        print("resolved_source_manifest=written")
    elif args.verify_source_set:
        print("checked_repositories=7")
    elif args.verify_remote_main_content:
        print("reviewed_main_content=6")
    elif args.write_verification_summary:
        print("verification_summary=written")
    elif args.validate_artifacts:
        print("sanitized_artifacts=2")
    else:
        print(f"checked_files={len(iter_text_files())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
