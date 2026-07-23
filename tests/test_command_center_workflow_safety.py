from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "verify-command-center-invariants.py"
SPEC = importlib.util.spec_from_file_location("command_center_invariants", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
VERIFIER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFIER)


class WorkflowSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = VERIFIER.WORKFLOW_PATH.read_text(encoding="utf-8")
        cls.source_manifest = VERIFIER.load_json_strict(VERIFIER.SOURCE_MANIFEST_PATH)

    def assert_rejected(self, value: str, label: str) -> None:
        self.assertTrue(
            VERIFIER.unsafe_workflow_findings(value),
            f"hostile workflow was accepted: {label}",
        )

    def test_current_workflow_is_structurally_safe(self) -> None:
        self.assertEqual([], VERIFIER.unsafe_workflow_findings(self.workflow))

    def test_permission_trigger_credential_and_action_attacks_fail(self) -> None:
        mutations = {
            "repository write token": self.workflow.replace(
                "contents: read", "contents: write", 1
            ),
            "issues write token": self.workflow.replace(
                "contents: read", "issues: write", 1
            ),
            "pull_request_target": self.workflow.replace(
                "pull_request:", "pull_request_target:", 1
            ),
            "persisted credentials": self.workflow.replace(
                "persist-credentials: false", "persist-credentials: true", 1
            ),
            "mutable action": self.workflow.replace(
                f"actions/checkout@{VERIFIER.PINNED_ACTIONS['actions/checkout']}",
                "actions/checkout@v4",
                1,
            ),
        }
        for label, value in mutations.items():
            with self.subTest(label=label):
                self.assert_rejected(value, label)

    def test_mutation_and_exit_neutralization_attacks_fail(self) -> None:
        marker = "set -euo pipefail"
        hostile_lines = {
            "direct push": "git push origin main",
            "PR creation": "gh pr create --title unsafe",
            "HTTP PR creation": "curl -X POST https://api.github.com/repos/x/y/pulls",
            "merge": "gh pr merge 1",
            "ledger mutation": "python ho_factory.py lifetime-ledger-append",
            "runtime mutation": "python tool.py runtime mutate",
            "proof promotion": "python tool.py proof promote",
            "swallowed failure": "false || true",
            "set plus e": "set +e",
            "unconditional success": "exit 0",
            "backgrounded command": "python unsafe.py &",
        }
        for label, hostile in hostile_lines.items():
            with self.subTest(label=label):
                self.assert_rejected(
                    self.workflow.replace(marker, f"{marker}\n          {hostile}", 1),
                    label,
                )
        self.assert_rejected(
            self.workflow.replace(
                "run: python scripts/verify-command-center-invariants.py --self-test",
                "continue-on-error: true\n        run: python scripts/verify-command-center-invariants.py --self-test",
                1,
            ),
            "continue-on-error",
        )
        self.assert_rejected(
            self.workflow.replace(
                "- name: Validate upload artifacts",
                "- name: Validate upload artifacts\n        if: always()",
                1,
            ),
            "always",
        )

    def test_duplicate_yaml_key_fails_closed(self) -> None:
        hostile = self.workflow.replace(
            "permissions:\n  contents: read",
            "permissions:\n  contents: read\npermissions:\n  issues: write",
            1,
        )
        findings = VERIFIER.unsafe_workflow_findings(hostile)
        self.assertTrue(any("duplicate workflow key" in value for value in findings))

    def test_missing_checkout_or_unsanitized_upload_fails(self) -> None:
        self.assert_rejected(
            self.workflow.replace(
                'git -C "source-set/$repo" fetch --quiet --depth=1 origin "$revision"',
                'printf "%s\\n" "$revision"',
                1,
            ),
            "missing sibling fetch",
        )
        self.assert_rejected(
            self.workflow.replace(
                "verification-artifacts/source-revisions.json\n"
                "            verification-artifacts/verification-summary.json",
                "verification-artifacts/",
                1,
            ),
            "broad upload",
        )

    def test_source_manifest_is_exact_closed_and_immutable(self) -> None:
        self.assertEqual(
            [], VERIFIER.validate_source_manifest(self.source_manifest)
        )
        attacks = []
        missing = json.loads(json.dumps(self.source_manifest))
        missing["repositories"].pop()
        attacks.append(missing)
        duplicate = json.loads(json.dumps(self.source_manifest))
        duplicate["repositories"].append(dict(duplicate["repositories"][0]))
        attacks.append(duplicate)
        mutable = json.loads(json.dumps(self.source_manifest))
        mutable["repositories"][1]["revision"] = "main"
        attacks.append(mutable)
        malformed_tree = json.loads(json.dumps(self.source_manifest))
        malformed_tree["repositories"][1]["reviewed_tree_sha"] = "not-a-tree"
        attacks.append(malformed_tree)
        spoofed = json.loads(json.dumps(self.source_manifest))
        spoofed["repositories"][1]["canonical_repository"] = (
            "HawkinsOperations/hawkinsoperations-detections-suffix"
        )
        attacks.append(spoofed)
        fallback = json.loads(json.dumps(self.source_manifest))
        fallback["constraints"]["default_branch_fallback"] = True
        attacks.append(fallback)
        unknown = json.loads(json.dumps(self.source_manifest))
        unknown["repositories"][1]["extension"] = "laundered"
        attacks.append(unknown)
        for candidate in attacks:
            with self.subTest(candidate=candidate):
                self.assertTrue(VERIFIER.validate_source_manifest(candidate))

    def test_resolved_manifest_digest_rejects_tampering(self) -> None:
        resolved = VERIFIER.resolved_source_manifest(
            self.source_manifest, "1" * 40, "2" * 40
        )
        self.assertEqual([], VERIFIER.validate_resolved_manifest(resolved))
        resolved["repositories"][1]["revision"] = "2" * 40
        self.assertIn(
            "resolved source manifest digest mismatch",
            VERIFIER.validate_resolved_manifest(resolved),
        )

    def test_main_content_observation_is_tree_bound_not_commit_bound(self) -> None:
        resolved = VERIFIER.resolved_source_manifest(
            self.source_manifest, "1" * 40, "2" * 40
        )
        observed = {
            entry["repository"]: entry["reviewed_tree_sha"]
            for entry in resolved["repositories"]
            if entry["repository"] != ".github"
        }
        self.assertEqual([], VERIFIER.compare_observed_main_trees(resolved, observed))
        observed["hoxline"] = "3" * 40
        errors = VERIFIER.compare_observed_main_trees(resolved, observed)
        self.assertTrue(any("hoxline" in error for error in errors))

    def test_duplicate_json_key_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "duplicate.json"
            path.write_text('{"schema":"one","SCHEMA":"two"}\n', encoding="utf-8")
            with self.assertRaises(VERIFIER.ValidationError):
                VERIFIER.load_json_strict(path)


class SourceSetTests(unittest.TestCase):
    def run_git(self, repo: Path, *args: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def create_source_set(self, root: Path) -> dict:
        entries = []
        for repository in VERIFIER.EXACT_REPOSITORIES:
            repo = root / repository
            repo.mkdir()
            self.run_git(repo, "init", "--quiet")
            self.run_git(repo, "config", "user.name", "Command Center Test")
            self.run_git(repo, "config", "user.email", "test@invalid.example")
            (repo / "authority.txt").write_text(repository + "\n", encoding="utf-8")
            self.run_git(repo, "add", "authority.txt")
            self.run_git(repo, "commit", "--quiet", "-m", "fixture")
            sha = self.run_git(repo, "rev-parse", "HEAD")
            tree = self.run_git(repo, "rev-parse", "HEAD^{tree}")
            self.run_git(
                repo, "remote", "add", "origin", VERIFIER.CANONICAL_ORIGINS[repository]
            )
            self.run_git(repo, "checkout", "--quiet", "--detach", sha)
            entries.append(
                {
                    "repository": repository,
                    "canonical_repository": f"HawkinsOperations/{repository}",
                    "revision": sha,
                    "reviewed_tree_sha": tree,
                }
            )
        payload = {
            "schema": "hawkinsoperations-resolved-convergence-source-set-v1",
            "manifest_id": "HAWKINSOPERATIONS_SEVEN_SOURCE_PR_HEAD_MATRIX_V1",
            "repositories": entries,
            "constraints": {
                "exact_repository_count": 7,
                "read_only": True,
                "default_branch_fallback": False,
                "require_detached_exact_revision": True,
                "record_checked_revisions": True,
                "consumer_outputs_are_not_authority": True,
                "proof_ceiling": VERIFIER.PROOF_CEILING,
            },
        }
        payload["manifest_sha256"] = VERIFIER.hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        return payload

    def test_exact_clean_detached_source_set_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "source-set"
            root.mkdir()
            resolved = self.create_source_set(root)
            records, errors = VERIFIER.verify_source_set(root, resolved)
            self.assertEqual([], errors)
            self.assertEqual(7, len(records))

    def test_dirty_wrong_origin_branch_and_missing_repo_fail(self) -> None:
        for attack in ("dirty", "origin", "branch", "missing", "extra"):
            with self.subTest(attack=attack), tempfile.TemporaryDirectory() as temp:
                root = Path(temp) / "source-set"
                root.mkdir()
                resolved = self.create_source_set(root)
                target = root / "hawkinsoperations-detections"
                if attack == "dirty":
                    (target / "untracked.txt").write_text("dirty\n", encoding="utf-8")
                elif attack == "origin":
                    self.run_git(
                        target,
                        "remote",
                        "set-url",
                        "origin",
                        "https://github.com/Other/hawkinsoperations-detections.git",
                    )
                elif attack == "branch":
                    self.run_git(target, "switch", "--quiet", "-c", "main")
                elif attack == "missing":
                    target.rename(root / "missing")
                else:
                    (root / "eighth-repository").mkdir()
                _, errors = VERIFIER.verify_source_set(root, resolved)
                self.assertTrue(errors)


class ArtifactSanitizerTests(unittest.TestCase):
    def create_valid_artifacts(self, root: Path) -> None:
        source = VERIFIER.resolved_source_manifest(
            VERIFIER.load_json_strict(VERIFIER.SOURCE_MANIFEST_PATH),
            "1" * 40,
            "2" * 40,
        )
        source["checked_repositories"] = [
            {
                "repository": entry["repository"],
                "canonical_repository": entry["canonical_repository"],
                "checked_sha": entry["revision"],
                "checked_tree_sha": entry["reviewed_tree_sha"],
                "detached": True,
                "clean": True,
            }
            for entry in source["repositories"]
        ]
        VERIFIER.write_json_atomic(root / "source-revisions.json", source)
        VERIFIER.write_verification_summary(root / "verification-summary.json")

    def test_closed_sanitized_artifact_pair_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.create_valid_artifacts(root)
            self.assertEqual([], VERIFIER.validate_artifact_payloads(root))

    def test_private_and_unsupported_artifacts_fail(self) -> None:
        hostile_values = [
            r"C:\private\output",
            r"\\server\share\output",
            "/home/operator/output",
            "%2fhome%2foperator%2foutput",
            "ghp_example",
            "192.168.1.12",
            "private@example.com",
            "customer evidence",
        ]
        for hostile in hostile_values:
            with self.subTest(hostile=hostile), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                self.create_valid_artifacts(root)
                path = root / "verification-summary.json"
                value = json.loads(path.read_text(encoding="utf-8"))
                value["checks"][0] = hostile
                VERIFIER.write_json_atomic(path, value)
                self.assertTrue(VERIFIER.validate_artifact_payloads(root))
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.create_valid_artifacts(root)
            (root / "raw.log").write_text("not approved\n", encoding="utf-8")
            self.assertTrue(VERIFIER.validate_artifact_payloads(root))
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.create_valid_artifacts(root)
            (root / "verification-summary.json").write_text("{", encoding="utf-8")
            self.assertTrue(VERIFIER.validate_artifact_payloads(root))


if __name__ == "__main__":
    unittest.main()
