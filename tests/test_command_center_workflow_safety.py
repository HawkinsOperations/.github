from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


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

    def test_tracked_vocabulary_guard_rejects_content_and_filename(self) -> None:
        retired = "".join(("syn", "thetic"))
        fullwidth = "".join(chr(ord(character) + 0xFEE0) for character in retired)
        zero_width = retired[:3] + "\u200b" + retired[3:]
        combining = retired[:3] + "\u034f" + retired[3:]
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(
                ["git", "init", "--quiet"],
                cwd=root,
                check=True,
                capture_output=True,
            )
            content_path = root / "content-fixture.txt"
            filename_path = root / f"fixture-{fullwidth}.txt"
            utf16_path = root / "utf16-fixture.md"
            content_path.write_text(
                (
                    f"controlled-test boundary rejects {fullwidth}\n"
                    f"controlled-test boundary rejects {zero_width}\n"
                    f"controlled-test boundary rejects {combining}\n"
                ),
                encoding="utf-8",
            )
            filename_path.write_text(
                "controlled-test boundary\n",
                encoding="utf-8",
            )
            zero_width_filename_path = root / f"fixture-{zero_width}.txt"
            combining_filename_path = root / f"fixture-{combining}.txt"
            zero_width_filename_path.write_text(
                "controlled-test boundary\n",
                encoding="utf-8",
            )
            combining_filename_path.write_text(
                "controlled-test boundary\n",
                encoding="utf-8",
            )
            utf16_path.write_bytes(
                f"controlled-test {retired}\n".encode("utf-16-le")
            )
            subprocess.run(
                [
                    "git",
                    "add",
                    "--",
                    content_path.name,
                    filename_path.name,
                    zero_width_filename_path.name,
                    combining_filename_path.name,
                    utf16_path.name,
                ],
                cwd=root,
                check=True,
                capture_output=True,
            )
            findings = VERIFIER.tracked_vocabulary_findings(root)
        self.assertTrue(any("tracked content" in item for item in findings))
        self.assertGreaterEqual(
            sum("tracked filename" in item for item in findings),
            3,
        )
        self.assertTrue(any("utf16-fixture.md" in item for item in findings))

    def test_vocabulary_security_view_preserves_benign_unicode_semantics(self) -> None:
        normalized = VERIFIER.normalize_vocabulary_security_text(
            "Café résumé – review 👩‍💻 only"
        )
        retired = "".join(("syn", "thetic"))
        self.assertNotIn(retired, normalized.casefold())
        self.assertIn("Cafe resume", normalized)

    def test_tracked_vocabulary_guard_fails_on_indexed_read_error(self) -> None:
        listed = subprocess.CompletedProcess(
            args=["git", "ls-files"],
            returncode=0,
            stdout=b"fixture.md\0",
            stderr=b"",
        )
        unreadable = subprocess.CompletedProcess(
            args=["git", "show"],
            returncode=128,
            stdout=b"",
            stderr=b"unreadable",
        )
        with mock.patch.object(
            VERIFIER.subprocess,
            "run",
            side_effect=(listed, unreadable),
        ):
            findings = VERIFIER.tracked_vocabulary_findings(REPO_ROOT)
        self.assertTrue(any("could not read indexed content" in item for item in findings))

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
            "background and wait": "python unsafe.py & wait",
            "swallowed echo": "false || echo ignored",
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

    def test_required_commands_cannot_be_echoed_or_conditionally_disabled(self) -> None:
        mutations = {
            "echo detection verifier": self.workflow.replace(
                "python -B source-set/hawkinsoperations-detections/scripts/verify_detection_contract.py",
                "echo python -B source-set/hawkinsoperations-detections/scripts/verify_detection_contract.py",
                1,
            ),
            "echo sibling fetch": self.workflow.replace(
                'git -C "source-set/$repo" fetch --quiet origin "$revision"',
                'echo git -C "source-set/$repo" fetch --quiet origin "$revision"',
                1,
            ),
            "validation detached source omitted": self.workflow.replace(
                ' --detections-root source-set/hawkinsoperations-detections --detections-ref "$(git -C source-set/hawkinsoperations-detections rev-parse HEAD)" --source-manifest source-set/hawkinsoperations-validation/validation/SOURCE_AUTHORITY_MANIFEST.json',
                "",
                1,
            ),
            "validation unit import root omitted": self.workflow.replace(
                'PYTHONPATH="$GITHUB_WORKSPACE/source-set/hawkinsoperations-validation" ',
                "",
                1,
            ),
            "platform observed SHA omitted": self.workflow.replace(
                "HAWKINS_PLATFORM_IMMUTABLE_OBSERVED_SHA",
                "HAWKINS_PLATFORM_OBSERVATION_OMITTED",
                1,
            ),
            "command-center observed SHA omitted": self.workflow.replace(
                "HAWKINS_COMMAND_CENTER_IMMUTABLE_OBSERVED_SHA",
                "HAWKINS_COMMAND_CENTER_OBSERVATION_OMITTED",
                1,
            ),
            "conditional job": self.workflow.replace(
                "  seven-repository-convergence:\n    needs: command-center-invariants\n    runs-on:",
                "  seven-repository-convergence:\n    needs: command-center-invariants\n    if: false\n    runs-on:",
                1,
            ),
            "conditional principal step": self.workflow.replace(
                "      - name: Verify command-center invariants\n        run:",
                "      - name: Verify command-center invariants\n        if: false\n        run:",
                1,
            ),
        }
        for label, value in mutations.items():
            with self.subTest(label=label):
                self.assert_rejected(value, label)

    def test_convergence_summary_cannot_outlive_owning_invariant_job(self) -> None:
        self.assertIn(
            "  seven-repository-convergence:\n"
            "    needs: command-center-invariants\n"
            "    runs-on:",
            self.workflow,
        )
        self.assert_rejected(
            self.workflow.replace(
                "    needs: command-center-invariants\n",
                "",
                1,
            ),
            "missing owning-job dependency",
        )

    def test_sibling_fetch_retry_is_bounded_and_fails_closed(self) -> None:
        for fragment in (
            "for attempt in 1 2 3 4 5 6; do",
            "fetch_complete=1",
            'if [ "$attempt" -lt 6 ]; then',
            "sleep 5",
            'test "$fetch_complete" -eq 1',
        ):
            self.assertIn(fragment, self.workflow)

        self.assert_rejected(
            self.workflow.replace('test "$fetch_complete" -eq 1', "true", 1),
            "unconditional success",
        )

    def test_exact_run_allowlist_rejects_command_laundering(self) -> None:
        command = (
            "python -B source-set/hawkinsoperations-detections/scripts/"
            "verify_detection_contract.py"
        )
        mutations = {
            "or colon": self.workflow.replace(command, f"{command} || :", 1),
            "or exit zero": self.workflow.replace(command, f"{command} || exit 0", 1),
            "semicolon true": self.workflow.replace(command, f"{command}; true", 1),
            "compound swallowed exit": self.workflow.replace(
                command,
                f"{command} || {{ echo swallowed; exit 0; }}",
                1,
            ),
            "no-op command prefix": self.workflow.replace(command, f": {command}", 1),
            "function override": self.workflow.replace(
                command,
                f"python() {{ :; }}\n          {command}",
                1,
            ),
            "alias override": self.workflow.replace(
                command,
                f"alias python=:\n          {command}",
                1,
            ),
            "PATH shadow": self.workflow.replace(
                command,
                f"PATH=/tmp/hostile:$PATH\n          {command}",
                1,
            ),
        }
        for label, value in mutations.items():
            with self.subTest(label=label):
                self.assert_rejected(value, label)

    def test_shell_and_job_default_overrides_fail_closed(self) -> None:
        mutations = {
            "shell suffix": self.workflow.replace(
                "shell: bash", "shell: bash {0}; true", 1
            ),
            "shell nested exit": self.workflow.replace(
                "shell: bash", "shell: bash -c '$0; exit 0' {0}", 1
            ),
            "job default shell": self.workflow.replace(
                "  command-center-invariants:\n    runs-on: ubuntu-latest",
                "  command-center-invariants:\n"
                "    defaults:\n"
                "      run:\n"
                "        shell: bash {0}; true\n"
                "    runs-on: ubuntu-latest",
                1,
            ),
            "step working directory": self.workflow.replace(
                "      - name: Verify command-center invariants\n        run:",
                "      - name: Verify command-center invariants\n"
                "        working-directory: /tmp\n"
                "        run:",
                1,
            ),
        }
        for label, value in mutations.items():
            with self.subTest(label=label):
                self.assert_rejected(value, label)

    def test_trigger_neutralization_and_test_path_omission_fail(self) -> None:
        mutations = {
            "closed-only PR": self.workflow.replace(
                "  pull_request:\n    paths:",
                "  pull_request:\n    types: [closed]\n    paths:",
                1,
            ),
            "ignored main": self.workflow.replace(
                "  pull_request:\n    paths:",
                "  pull_request:\n    branches-ignore: [main]\n    paths:",
                1,
            ),
            "tests omitted": self.workflow.replace('      - "tests/**"\n', "", 1),
        }
        for label, value in mutations.items():
            with self.subTest(label=label):
                self.assert_rejected(value, label)

    def test_artifact_validation_must_be_immediately_before_upload(self) -> None:
        hostile = self.workflow.replace(
            "      - name: Upload sanitized convergence records",
            "      - name: Corrupt artifact after validation\n"
            "        run: echo invalid > verification-artifacts/verification-summary.json\n\n"
            "      - name: Upload sanitized convergence records",
            1,
        )
        self.assert_rejected(hostile, "post-validation artifact mutation")

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
                'git -C "source-set/$repo" fetch --quiet origin "$revision"',
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
        missing_self_content = json.loads(json.dumps(self.source_manifest))
        missing_self_content["repositories"][0].pop("authority_content_revision")
        attacks.append(missing_self_content)
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

    def test_command_center_manifest_shape_is_closed(self) -> None:
        original = VERIFIER.load_json_strict(VERIFIER.MANIFEST_PATH)
        for mutation in ("root", "invariant"):
            with self.subTest(mutation=mutation):
                candidate = json.loads(json.dumps(original))
                if mutation == "root":
                    candidate["extension"] = {"ai_authority": True}
                else:
                    candidate["invariants"]["ai_authority"] = True
                with tempfile.TemporaryDirectory() as temp:
                    path = Path(temp) / "manifest.json"
                    path.write_text(json.dumps(candidate), encoding="utf-8")
                    prior = VERIFIER.MANIFEST_PATH
                    try:
                        VERIFIER.MANIFEST_PATH = path
                        errors = []
                        VERIFIER.load_manifest(errors)
                    finally:
                        VERIFIER.MANIFEST_PATH = prior
                    self.assertTrue(errors)


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
            authority_path = VERIFIER.CANONICAL_AUTHORITY_PATHS[repository]
            authority_file = repo / Path(authority_path)
            authority_file.parent.mkdir(parents=True, exist_ok=True)
            authority_file.write_text(repository + "\n", encoding="utf-8")
            self.run_git(repo, "add", authority_path)
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
                    "authority_content_revision": sha,
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

    def test_origin_rewrite_cannot_launder_wrong_stored_origin(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "source-set"
            root.mkdir()
            resolved = self.create_source_set(root)
            repository = "hawkinsoperations-detections"
            target = root / repository
            canonical = VERIFIER.CANONICAL_ORIGINS[repository]
            wrong = "https://local.invalid/hawkinsoperations-detections.git"
            self.run_git(target, "remote", "set-url", "origin", wrong)
            rewrite_env = {
                "GIT_CONFIG_COUNT": "1",
                "GIT_CONFIG_KEY_0": f"url.{canonical}.insteadOf",
                "GIT_CONFIG_VALUE_0": wrong,
            }
            with mock.patch.dict(os.environ, rewrite_env, clear=False):
                self.assertEqual(
                    canonical,
                    self.run_git(target, "remote", "get-url", "origin"),
                    "attack precondition: interpreted Git URL must look canonical",
                )
                _, errors = VERIFIER.verify_source_set(root, resolved)
            self.assertTrue(
                any("canonical origin mismatch" in error for error in errors),
                errors,
            )

    def test_git_environment_scrub_rejects_every_ambient_git_control(self) -> None:
        hostile = {
            "GIT_DIR": "decoy",
            "GIT_WORK_TREE": "decoy",
            "GIT_COMMON_DIR": "decoy",
            "GIT_INDEX_FILE": "decoy",
            "GIT_OBJECT_DIRECTORY": "decoy",
            "GIT_ALTERNATE_OBJECT_DIRECTORIES": "decoy",
            "GIT_CONFIG": "decoy",
            "GIT_CONFIG_GLOBAL": "decoy",
            "GIT_CONFIG_SYSTEM": "decoy",
            "GIT_CONFIG_NOSYSTEM": "0",
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "core.repositoryformatversion",
            "GIT_CONFIG_VALUE_0": "1",
            "GIT_CEILING_DIRECTORIES": "decoy",
            "GIT_DISCOVERY_ACROSS_FILESYSTEM": "1",
            "GIT_SHALLOW_FILE": "decoy",
            "GIT_NAMESPACE": "decoy",
            "GIT_REPLACE_REF_BASE": "refs/decoy",
            "GIT_IMPLICIT_WORK_TREE": "1",
            "GIT_NO_REPLACE_OBJECTS": "0",
            "GIT_TERMINAL_PROMPT": "1",
        }
        with mock.patch.dict(os.environ, hostile, clear=False):
            sanitized = VERIFIER.sanitized_git_environment()
        self.assertEqual("1", sanitized["GIT_NO_REPLACE_OBJECTS"])
        self.assertEqual("0", sanitized["GIT_TERMINAL_PROMPT"])
        self.assertEqual(
            {"git_no_replace_objects", "git_terminal_prompt"},
            {
                key.casefold()
                for key in sanitized
                if key.casefold().startswith("git_")
            },
        )

    def test_git_dir_decoy_cannot_redirect_stored_origin_authority(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            root = base / "source-set"
            root.mkdir()
            resolved = self.create_source_set(root)
            repository = "hawkinsoperations-detections"
            target = root / repository
            canonical = VERIFIER.CANONICAL_ORIGINS[repository]
            wrong = "https://local.invalid/hawkinsoperations-detections.git"
            self.run_git(target, "remote", "set-url", "origin", wrong)
            decoy = base / "decoy"
            decoy.mkdir()
            self.run_git(decoy, "init", "--quiet")
            self.run_git(decoy, "remote", "add", "origin", canonical)
            raw_env = os.environ.copy()
            raw_env["GIT_DIR"] = str(decoy / ".git")
            interpreted = subprocess.run(
                [
                    "git",
                    "-C",
                    str(target),
                    "config",
                    "--local",
                    "--get-all",
                    "remote.origin.url",
                ],
                check=True,
                capture_output=True,
                text=True,
                env=raw_env,
            ).stdout.strip()
            self.assertEqual(canonical, interpreted)
            with mock.patch.dict(
                os.environ, {"GIT_DIR": str(decoy / ".git")}, clear=False
            ):
                self.assertEqual(wrong, VERIFIER.stored_origin(target))
                _, errors = VERIFIER.verify_source_set(root, resolved)
            self.assertTrue(
                any("canonical origin mismatch" in error for error in errors),
                errors,
            )

    def test_git_index_file_cannot_hide_staged_dirty_authority(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            root = base / "source-set"
            root.mkdir()
            resolved = self.create_source_set(root)
            repository = "hawkinsoperations-detections"
            target = root / repository
            clean_index = base / "clean.index"
            alternate_env = os.environ.copy()
            alternate_env["GIT_INDEX_FILE"] = str(clean_index)
            subprocess.run(
                ["git", "-C", str(target), "read-tree", "HEAD"],
                check=True,
                capture_output=True,
                env=alternate_env,
            )
            authority_file = target / VERIFIER.CANONICAL_AUTHORITY_PATHS[repository]
            original = authority_file.read_text(encoding="utf-8")
            authority_file.write_text("staged contradiction\n", encoding="utf-8")
            self.run_git(
                target,
                "add",
                VERIFIER.CANONICAL_AUTHORITY_PATHS[repository],
            )
            authority_file.write_text(original, encoding="utf-8")
            hidden = subprocess.run(
                [
                    "git",
                    "-C",
                    str(target),
                    "status",
                    "--porcelain=v1",
                    "--untracked-files=all",
                ],
                check=True,
                capture_output=True,
                text=True,
                env=alternate_env,
            ).stdout.strip()
            self.assertEqual("", hidden, "attack precondition: alternate index is clean")
            with mock.patch.dict(
                os.environ, {"GIT_INDEX_FILE": str(clean_index)}, clear=False
            ):
                _, errors = VERIFIER.verify_source_set(root, resolved)
            self.assertTrue(
                any("source checkout is dirty" in error for error in errors),
                errors,
            )

    def test_missing_empty_or_multiple_stored_origins_fail_closed(self) -> None:
        for attack in ("missing", "empty", "multiple"):
            with self.subTest(attack=attack), tempfile.TemporaryDirectory() as temp:
                root = Path(temp) / "source-set"
                root.mkdir()
                resolved = self.create_source_set(root)
                target = root / "hawkinsoperations-detections"
                self.run_git(target, "config", "--unset-all", "remote.origin.url")
                if attack == "empty":
                    self.run_git(target, "config", "--add", "remote.origin.url", "")
                elif attack == "multiple":
                    self.run_git(
                        target,
                        "config",
                        "--add",
                        "remote.origin.url",
                        VERIFIER.CANONICAL_ORIGINS["hawkinsoperations-detections"],
                    )
                    self.run_git(
                        target,
                        "config",
                        "--add",
                        "remote.origin.url",
                        "https://local.invalid/hawkinsoperations-detections.git",
                    )
                _, errors = VERIFIER.verify_source_set(root, resolved)
                self.assertTrue(
                    any("exactly one nonempty local URL" in error for error in errors),
                    errors,
                )

    def test_authority_content_revision_is_bound_to_canonical_current_blob(self) -> None:
        for attack in ("unreachable", "wrong-blob"):
            with self.subTest(attack=attack), tempfile.TemporaryDirectory() as temp:
                root = Path(temp) / "source-set"
                root.mkdir()
                resolved = self.create_source_set(root)
                target = root / "hawkinsoperations-detections"
                entry = resolved["repositories"][1]
                if attack == "unreachable":
                    entry["authority_content_revision"] = "f" * 40
                else:
                    authority_file = target / Path(
                        VERIFIER.CANONICAL_AUTHORITY_PATHS[
                            "hawkinsoperations-detections"
                        ]
                    )
                    authority_file.write_text("contradictory authority\n", encoding="utf-8")
                    self.run_git(target, "add", authority_file.relative_to(target).as_posix())
                    self.run_git(target, "commit", "--quiet", "-m", "contradiction")
                    entry["authority_content_revision"] = self.run_git(
                        target, "rev-parse", "HEAD"
                    )
                    self.run_git(target, "checkout", "--quiet", "--detach", entry["revision"])
                unsigned = {
                    key: value
                    for key, value in resolved.items()
                    if key != "manifest_sha256"
                }
                resolved["manifest_sha256"] = VERIFIER.hashlib.sha256(
                    json.dumps(
                        unsigned, sort_keys=True, separators=(",", ":")
                    ).encode("utf-8")
                ).hexdigest()
                _, errors = VERIFIER.verify_source_set(root, resolved)
                self.assertTrue(errors)

    def test_uploaded_authority_blob_record_is_reverified_against_source_set(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source_root = base / "source-set"
            source_root.mkdir()
            resolved = self.create_source_set(source_root)
            records, errors = VERIFIER.verify_source_set(source_root, resolved)
            self.assertEqual([], errors)
            artifacts = base / "artifacts"
            artifacts.mkdir()
            source_record = dict(resolved)
            source_record["checked_repositories"] = records
            VERIFIER.write_json_atomic(
                artifacts / "source-revisions.json", source_record
            )
            VERIFIER.write_verification_summary(
                artifacts / "verification-summary.json"
            )
            self.assertEqual(
                [], VERIFIER.validate_artifact_payloads(artifacts, source_root)
            )
            path = artifacts / "source-revisions.json"
            tampered = VERIFIER.load_json_strict(path)
            tampered["checked_repositories"][0][
                "authority_git_blob_sha"
            ] = "f" * 40
            VERIFIER.write_json_atomic(path, tampered)
            errors = VERIFIER.validate_artifact_payloads(
                artifacts, source_root
            )
            self.assertTrue(
                any("exact current source set" in error for error in errors)
            )


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
                "authority_path": VERIFIER.CANONICAL_AUTHORITY_PATHS[
                    entry["repository"]
                ],
                "authority_content_revision": entry[
                    "authority_content_revision"
                ],
                "authority_git_blob_sha": "a" * 40,
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
            "AKIAIOSFODNN7EXAMPLE",
            "Bearer abcdefghijklmnopqrstuvwxyz",
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

    def test_fabricated_check_set_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.create_valid_artifacts(root)
            path = root / "verification-summary.json"
            value = json.loads(path.read_text(encoding="utf-8"))
            value["checks"] = [f"fabricated_check_{index}" for index in range(23)]
            VERIFIER.write_json_atomic(path, value)
            self.assertTrue(VERIFIER.validate_artifact_payloads(root))
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.create_valid_artifacts(root)
            (root / "verification-summary.json").write_text("{", encoding="utf-8")
            self.assertTrue(VERIFIER.validate_artifact_payloads(root))


if __name__ == "__main__":
    unittest.main()
