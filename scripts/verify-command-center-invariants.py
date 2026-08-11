#!/usr/bin/env python3
"""Fail-closed checks for the HawkinsOperations .github command center."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "governance" / "COMMAND_CENTER_INVARIANTS.json"
TEXT_SCOPES = ["README.md", "profile", "architecture", "governance", "wiki", ".github"]
# Stable public inventory order. This is not the promotion-ladder sequence,
# which is separately governed and verified from PROMOTION_LADDER_CONTRACT.yml.
SYSTEM_REPOSITORIES = (
    ".github",
    "hoxline",
    "hawkinsoperations-detections",
    "hawkinsoperations-validation",
    "hawkinsoperations-platform",
    "hawkinsoperations-proof",
    "hawkinsoperations-website",
)
# Fingerprint of the complete reviewed promotion contract. Any layer, top-level
# gate, blocked claim, status, or current-state change requires an intentional
# verifier update.
EXPECTED_PROMOTION_CONTRACT_SHA256 = "65522c07b7e2983379dcb3ea1ba5b4cd03ccb3e5116983931bb8c3e23b36c7c8"
# Fingerprint of the complete reviewed required-checks matrix. This binds each
# workflow/job context to its verifier command, display metadata, enforcement
# classification, and documented boundary; changes require intentional review.
EXPECTED_REQUIRED_CHECKS_MATRIX_SHA256 = "2cefa14bcd21ec9dfa1a491c791116d7806fe67c18c0f8bce5f669e7b2eb4f44"
# Fingerprint of the complete reviewed invariant manifest, including the exact
# required route list and seven-repository authority order.
EXPECTED_MANIFEST_SHA256 = "943483cc693072d519d5b397b89479f0efa4f0c027273f3a53f557d59af20cd3"
# Fingerprint of every reviewed Mermaid block in the organization system map.
# Any topology, alias, or edge change requires an intentional verifier update.
EXPECTED_SYSTEM_MAP_MERMAID_SHA256 = "5e0e2ce49506de2a02d3bb981be1823ae33194908c5d234e286c92f0a201edd8"
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


class UniqueKeySafeLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects ambiguous duplicate mapping keys."""


def construct_unique_mapping(
    loader: UniqueKeySafeLoader,
    node: yaml.MappingNode,
    deep: bool = False,
) -> dict:
    mapping: dict = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unhashable mapping key",
                key_node.start_mark,
            ) from exc
        if duplicate:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key ({key!r})",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeySafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_unique_mapping,
)


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def valid_markdown_fence_opening(line: str) -> re.Match[str] | None:
    match = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
    if match and match.group(1).startswith("`") and "`" in line[match.end():]:
        return None
    return match


def nested_markdown_fence_opening(line: str) -> re.Match[str] | None:
    """Recognize a fence opened directly inside list or blockquote containers."""
    match = re.match(
        r"^ {0,3}(?P<containers>(?:(?:> ?)|(?:(?:[-+*]|\d{1,9}[.)])[ \t]+))+?)"
        r" {0,3}(?P<run>`{3,}|~{3,})",
        line,
    )
    if match and match.group("run").startswith("`") and "`" in line[match.end():]:
        return None
    return match


def has_unclosed_inline_code_run(line: str) -> bool:
    active_length = 0
    for match in re.finditer(r"`+", line):
        backslashes = 0
        cursor = match.start() - 1
        while cursor >= 0 and line[cursor] == "\\":
            backslashes += 1
            cursor -= 1
        if backslashes % 2:
            continue
        run_length = len(match.group(0))
        if not active_length:
            active_length = run_length
        elif run_length == active_length:
            active_length = 0
    return bool(active_length)


def is_complete_type7_html_tag(text: str) -> bool:
    """Recognize one complete CommonMark type-7 opening or closing tag."""
    tag_name = r"[A-Za-z][A-Za-z0-9-]*"
    attribute_name = r"[A-Za-z_:][A-Za-z0-9_.:-]*"
    attribute_value = r'(?:[^ \t\r\n"\'=<>`]+|\'[^\']*\'|"[^"]*")'
    attribute = rf"[ \t]+{attribute_name}(?:[ \t]*=[ \t]*{attribute_value})?"
    opening = rf"<{tag_name}(?:{attribute})*[ \t]*/?>"
    closing = rf"</{tag_name}[ \t]*>"
    return bool(re.fullmatch(rf"(?:{opening}|{closing})[ \t]*", text))


def parse_markdown_html_block_container(
    line: str,
    *,
    allow_type7: bool = True,
) -> tuple[int, int] | None:
    content = line.rstrip("\r\n")
    cursor = 0
    quote_depth = 0
    list_indent = 0
    while cursor < len(content):
        marker_indent = len(content[cursor:]) - len(content[cursor:].lstrip(" "))
        if marker_indent > 3:
            return None
        cursor += marker_indent
        if cursor >= len(content):
            return None
        if content[cursor] == ">":
            quote_depth += 1
            cursor += 1
            if cursor < len(content) and content[cursor] in " \t":
                cursor += 1
            continue
        list_marker = re.match(r"(?:[-+*]|\d{1,9}[.)])(?P<padding>[ \t]+)", content[cursor:])
        if list_marker:
            list_indent += marker_indent + len(list_marker.group(0).expandtabs(4))
            cursor += list_marker.end()
            continue
        break
    remainder = content[cursor:]
    type6_opening = re.match(
        r"</?(?:address|article|aside|base|basefont|blockquote|body|caption|center|col|"
        r"colgroup|dd|details|dialog|dir|div|dl|dt|fieldset|figcaption|figure|footer|form|"
        r"frame|frameset|h[1-6]|head|header|hr|html|iframe|legend|li|link|main|menu|menuitem|"
        r"nav|noframes|ol|optgroup|option|p|param|search|section|summary|table|tbody|td|tfoot|"
        r"th|thead|title|tr|track|ul)(?:[ \t]+|/?>|$)",
        remainder,
        re.IGNORECASE,
    )
    if type6_opening:
        return quote_depth, list_indent

    if allow_type7 and is_complete_type7_html_tag(remainder):
        return quote_depth, list_indent
    return None


def line_belongs_to_markdown_container(line: str, quote_depth: int, list_indent: int) -> bool:
    content = line.rstrip("\r\n")
    cursor = 0
    for _ in range(quote_depth):
        spaces = len(content[cursor:]) - len(content[cursor:].lstrip(" "))
        if spaces > 3:
            return False
        cursor += spaces
        if cursor >= len(content) or content[cursor] != ">":
            return False
        cursor += 1
        if cursor < len(content) and content[cursor] in " \t":
            cursor += 1
    if list_indent:
        whitespace = re.match(r"[ \t]*", content[cursor:]).group(0)
        if len(whitespace.expandtabs(4)) < list_indent:
            return False
    return True


def is_blank_markdown_container_line(line: str) -> bool:
    content = line.rstrip("\r\n")
    while True:
        marker = re.match(r"^ {0,3}>[ \t]?", content)
        if not marker:
            break
        content = content[marker.end():]
    return not content.strip()


def strip_markdown_html_tags(text: str) -> str:
    """Remove non-rendered HTML tag syntax while preserving visible text and lines."""
    output: list[str] = []
    in_tag = False
    attribute_quote = ""
    cursor = 0
    while cursor < len(text):
        character = text[cursor]
        if in_tag:
            if character in "\r\n":
                output.append(character)
            if attribute_quote:
                if character == attribute_quote:
                    attribute_quote = ""
            elif character in {'"', "'"}:
                attribute_quote = character
            elif character == ">":
                in_tag = False
            cursor += 1
            continue

        if character == "<" and cursor + 1 < len(text) and re.match(r"[A-Za-z/!?]", text[cursor + 1]):
            in_tag = True
            cursor += 1
            continue
        output.append(character)
        cursor += 1
    return "".join(output)


def interrupts_markdown_paragraph(line: str) -> bool:
    content = line.rstrip("\r\n")
    if not content.strip():
        return True
    if valid_markdown_fence_opening(content):
        return True
    return bool(
        re.match(
            r"^ {0,3}(?:"
            r"#{1,6}(?:[ \t]+|$)|"
            r">|"
            r"(?:[-+*]|0{0,8}1[.)])[ \t]+|"
            r"(?:=+|-+)[ \t]*$|"
            r"(?:(?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,})$|"
            r"<!--|<\?|<![A-Z]|<!\[CDATA\[|"
            r"</?(?:script|pre|style|textarea)(?:[ \t]+|>|$)|"
            r"</?(?:address|article|aside|base|basefont|blockquote|body|caption|center|col|"
            r"colgroup|dd|details|dialog|dir|div|dl|dt|fieldset|figcaption|figure|footer|"
            r"form|frame|frameset|h[1-6]|head|header|hr|html|iframe|legend|li|link|main|"
            r"menu|menuitem|nav|noframes|ol|optgroup|option|p|param|search|section|summary|"
            r"table|tbody|td|tfoot|th|thead|title|tr|track|ul)(?:[ \t]+|/?>|$)"
            r")",
            content,
            re.IGNORECASE,
        )
    )


def strip_html_comments(text: str) -> str:
    """Remove Markdown HTML comments while preserving reviewer-visible code."""
    output: list[str] = []
    in_comment = False
    inline_ticks = 0
    fence_marker = ""
    fence_length = 0
    line_offset = 0

    def has_matching_tick_run(start: int, length: int) -> bool:
        remainder = text[start:]
        offset = 0
        for line_number, candidate_line in enumerate(remainder.splitlines(keepends=True)):
            if line_number and interrupts_markdown_paragraph(candidate_line):
                remainder = remainder[:offset]
                break
            offset += len(candidate_line)
        return any(
            len(match.group(0)) == length
            for match in re.finditer(r"`+", remainder)
        )

    for line in text.splitlines(keepends=True):
        if fence_marker:
            output.append(line)
            closing = re.match(rf"^ {{0,3}}{re.escape(fence_marker)}{{{fence_length},}}[ \t]*(?:\r?\n)?$", line)
            if closing:
                fence_marker = ""
                fence_length = 0
            line_offset += len(line)
            continue

        if not in_comment and inline_ticks == 0:
            if re.match(r"^(?: {4}| {0,3}\t)", line):
                output.append(line)
                line_offset += len(line)
                continue
            opening = valid_markdown_fence_opening(line)
            if opening:
                marker_run = opening.group(1)
                fence_marker = marker_run[0]
                fence_length = len(marker_run)
                output.append(line)
                line_offset += len(line)
                continue

        index = 0
        while index < len(line):
            if in_comment:
                closing_index = line.find("-->", index)
                if closing_index < 0:
                    index = len(line)
                    continue
                in_comment = False
                index = closing_index + 3
                continue

            if inline_ticks:
                tick_match = re.search(r"`+", line[index:])
                if not tick_match:
                    output.append(line[index:])
                    index = len(line)
                    continue
                tick_start = index + tick_match.start()
                tick_run = tick_match.group(0)
                output.append(line[index:tick_start + len(tick_run)])
                index = tick_start + len(tick_run)
                if len(tick_run) == inline_ticks:
                    inline_ticks = 0
                continue

            if line.startswith("<!--", index):
                in_comment = True
                index += 4
                continue
            if line[index] == "`":
                tick_match = re.match(r"`+", line[index:])
                tick_run = tick_match.group(0) if tick_match else "`"
                global_index = line_offset + index
                backslash_count = 0
                preceding_index = global_index - 1
                while preceding_index >= 0 and text[preceding_index] == "\\":
                    backslash_count += 1
                    preceding_index -= 1
                if backslash_count % 2 or not has_matching_tick_run(
                    global_index + len(tick_run), len(tick_run)
                ):
                    output.append(tick_run)
                    index += len(tick_run)
                    continue
                inline_ticks = len(tick_run)
                output.append(tick_run)
                index += len(tick_run)
                continue
            output.append(line[index])
            index += 1

        line_offset += len(line)

    return "".join(output)


def strip_markdown_code_blocks(text: str) -> str:
    """Remove code blocks from Markdown used for rendered semantic scans."""
    output: list[str] = []
    fence_marker = ""
    fence_length = 0
    html_code_tag = ""
    html_tag_buffer = ""
    html_attribute_quote = ""
    html_block_container: tuple[int, int] | None = None
    paragraph_open = False

    def advance_html_code_state(
        line: str,
        active_tag: str,
        tag_buffer: str,
        attribute_quote: str,
    ) -> tuple[str, str, str, bool]:
        cursor = 0
        contains_raw_code = bool(active_tag)
        if active_tag in {"script", "style", "textarea"}:
            closing = re.search(
                rf"</{re.escape(active_tag)}[ \t]*>",
                line,
                re.IGNORECASE,
            )
            if not closing:
                return active_tag, "", "", True
            cursor = closing.end()
            active_tag = ""
            tag_buffer = ""
            attribute_quote = ""
        while cursor < len(line):
            if not tag_buffer:
                opening = re.search(r"<(?=[A-Za-z/!?])", line[cursor:])
                if not opening:
                    break
                cursor += opening.start() + 1
                tag_buffer = "<"
                continue

            character = line[cursor]
            tag_buffer += character
            cursor += 1
            if attribute_quote:
                if character == attribute_quote:
                    attribute_quote = ""
                continue
            if character in {'"', "'"}:
                attribute_quote = character
                continue
            if not active_tag:
                pending_opening = re.match(
                    r"<(pre|script|style|textarea)(?=[ \t>/])",
                    tag_buffer,
                    re.IGNORECASE,
                )
                if pending_opening:
                    active_tag = pending_opening.group(1).lower()
                    contains_raw_code = True
            if character != ">":
                continue

            token = tag_buffer
            tag_buffer = ""
            if active_tag:
                if re.fullmatch(
                    rf"</{re.escape(active_tag)}[ \t]*>",
                    token,
                    re.IGNORECASE,
                ):
                    active_tag = ""
                contains_raw_code = True
                continue
            opening_tag = re.match(
                r"<(pre|script|style|textarea)(?=[ \t>/])",
                token,
                re.IGNORECASE,
            )
            if opening_tag:
                active_tag = opening_tag.group(1).lower()
                contains_raw_code = True
        if active_tag and tag_buffer and not attribute_quote:
            tag_buffer = ""
        return active_tag, tag_buffer, attribute_quote, contains_raw_code

    for line in text.splitlines(keepends=True):
        if html_block_container is not None:
            quote_depth, list_indent = html_block_container
            if line_belongs_to_markdown_container(line, quote_depth, list_indent):
                output.append("\n" if line.endswith("\n") else "")
                if is_blank_markdown_container_line(line):
                    html_block_container = None
                    paragraph_open = False
                continue
            html_block_container = None

        if html_code_tag or html_tag_buffer:
            html_code_tag, html_tag_buffer, html_attribute_quote, _ = advance_html_code_state(
                line,
                html_code_tag,
                html_tag_buffer,
                html_attribute_quote,
            )
            output.append("\n" if line.endswith("\n") else "")
            paragraph_open = False
            continue

        if fence_marker:
            closing = re.match(
                rf"^ {{0,3}}{re.escape(fence_marker)}{{{fence_length},}}[ \t]*(?:\r?\n)?$",
                line,
            )
            output.append("\n" if line.endswith("\n") else "")
            if closing:
                fence_marker = ""
                fence_length = 0
                paragraph_open = False
            continue

        if re.match(r"^(?: {4}| {0,3}\t)", line):
            output.append("\n" if line.endswith("\n") else "")
            paragraph_open = False
            continue

        if nested_markdown_fence_opening(line):
            output.append("\n" if line.endswith("\n") else "")
            break

        opening = valid_markdown_fence_opening(line)
        if opening:
            marker_run = opening.group(1)
            fence_marker = marker_run[0]
            fence_length = len(marker_run)
            output.append("\n" if line.endswith("\n") else "")
            paragraph_open = False
            continue

        html_block_container_start = parse_markdown_html_block_container(
            line,
            allow_type7=not paragraph_open,
        )
        if html_block_container_start is not None:
            html_block_container = html_block_container_start
            output.append("\n" if line.endswith("\n") else "")
            paragraph_open = False
            continue

        if has_unclosed_inline_code_run(line):
            output.append("\n" if line.endswith("\n") else "")
            break

        html_code_tag, html_tag_buffer, html_attribute_quote, contains_raw_code = advance_html_code_state(
            line,
            "",
            "",
            "",
        )
        if contains_raw_code or html_tag_buffer:
            output.append("\n" if line.endswith("\n") else "")
            paragraph_open = False
            continue
        output.append(line)
        if not line.strip():
            paragraph_open = False
        elif not paragraph_open:
            paragraph_open = not interrupts_markdown_paragraph(line)
    return "".join(output)


def extract_mermaid_blocks(text: str) -> list[str]:
    """Extract Mermaid fence bodies using CommonMark marker and length rules."""
    blocks: list[str] = []
    fence_marker = ""
    fence_length = 0
    collect_mermaid = False
    body: list[str] = []

    for line in text.splitlines(keepends=True):
        if fence_marker:
            closing = re.match(
                rf"^ {{0,3}}{re.escape(fence_marker)}{{{fence_length},}}[ \t]*(?:\r?\n)?$",
                line,
            )
            if closing:
                if collect_mermaid:
                    blocks.append("".join(body))
                fence_marker = ""
                fence_length = 0
                collect_mermaid = False
                body = []
            elif collect_mermaid:
                body.append(line)
            continue

        opening = valid_markdown_fence_opening(line)
        if not opening:
            continue
        marker_run = opening.group(1)
        fence_marker = marker_run[0]
        fence_length = len(marker_run)
        info = line[opening.end():].strip()
        collect_mermaid = bool(re.match(r"^mermaid(?:[ \t]|$)", info, re.IGNORECASE))
        body = []

    if fence_marker and collect_mermaid:
        blocks.append("".join(body))
    return blocks


def construct_unique_json_object(pairs: list[tuple[str, object]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def read_text(path: Path, errors: list[str]) -> str:
    if not path.exists():
        fail(f"missing file: {path.relative_to(ROOT).as_posix()}", errors)
        return ""
    return path.read_text(encoding="utf-8")


def read_reviewer_visible_text(path: Path, errors: list[str]) -> str:
    text = read_text(path, errors)
    return strip_html_comments(text) if path.suffix.lower() == ".md" else text


def read_reviewer_semantic_text(path: Path, errors: list[str]) -> str:
    text = read_reviewer_visible_text(path, errors)
    if path.suffix.lower() != ".md":
        return text
    return strip_markdown_html_tags(strip_markdown_code_blocks(text))


def read_yaml_mapping(path: Path, errors: list[str]) -> dict:
    text = read_text(path, errors)
    if not text:
        return {}
    try:
        document = yaml.load(text, Loader=UniqueKeySafeLoader)
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
        manifest = json.loads(text, object_pairs_hook=construct_unique_json_object)
    except ValueError as exc:
        fail(f"manifest JSON parse failed: {exc}", errors)
        return {}
    manifest_payload = json.dumps(
        manifest,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    if hashlib.sha256(manifest_payload).hexdigest() != EXPECTED_MANIFEST_SHA256:
        fail("complete invariant manifest does not match the reviewed machine-readable mapping", errors)
    if manifest.get("schema") != "hawkinsoperations-command-center-invariants-v1":
        fail("manifest schema mismatch", errors)
    if manifest.get("system_repository_order_semantics") != (
        "Stable front-door inventory display order; promotion flow is separately governed "
        "by PROMOTION_LADDER_CONTRACT.yml."
    ):
        fail("manifest must distinguish inventory display order from promotion-ladder sequence", errors)
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
        text = read_reviewer_visible_text(ROOT / rel, errors)
        lowered = text.lower()
        for needle in needles:
            if needle.lower() not in lowered:
                fail(f"{rel} missing required wording: {needle}", errors)


def check_front_door_authority_model(manifest: dict, errors: list[str]) -> None:
    manifest_repositories = tuple(manifest.get("system_repositories", []))
    if manifest_repositories != SYSTEM_REPOSITORIES:
        fail("manifest system_repositories must preserve the exact seven-repository inventory display order", errors)

    for rel in ("README.md", "profile/README.md", "profile/START_HERE.md", "architecture/REPO_AUTHORITY_MAP.md"):
        text = read_reviewer_semantic_text(ROOT / rel, errors).lower()
        for repository in SYSTEM_REPOSITORIES:
            if repository.lower() not in text:
                fail(f"{rel} missing system repository role: {repository}", errors)

    profile_text = read_reviewer_semantic_text(ROOT / "profile" / "README.md", errors)
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
    governed_route_markers = (
        "https://github.com/HawkinsOperations/hawkinsoperations-detections/tree/main/detections/successor/ho-det-001",
        "https://github.com/HawkinsOperations/hawkinsoperations-validation/blob/main/reports/ho-det-001/validation-result.md",
        "https://hawkinsoperations.com/hoxline/",
        "https://hawkinsoperations.com/claim-firewall/",
        "https://github.com/HawkinsOperations/hawkinsoperations-platform/blob/main/contracts/examples/ho-det-001-runtime-contract.sample.json",
        "https://github.com/HawkinsOperations/hawkinsoperations-proof/blob/main/proof/records/HO-DET-001.md",
    )
    profile_fast_path = re.search(
        r"^\| \*\*3 minutes\*\* \| (.+)$",
        profile_text,
        re.MULTILINE,
    )
    start_here_text = read_reviewer_semantic_text(ROOT / "profile" / "START_HERE.md", errors)
    start_here_fast_path = re.search(
        r"## 3-minute command-center path\s+(.*?)(?=\n## |\Z)",
        start_here_text,
        re.DOTALL,
    )
    for route_name, route_section in (
        ("profile/README.md fast reviewer path", profile_fast_path),
        ("profile/START_HERE.md 3-minute path", start_here_fast_path),
    ):
        route_text = "" if route_section is None else route_section.group(1)
        positions = tuple(route_text.find(marker) for marker in governed_route_markers)
        if any(position < 0 for position in positions) or positions != tuple(sorted(positions)):
            fail(f"{route_name} must preserve source -> validation -> Hoxline -> Claim Firewall -> platform -> proof order", errors)
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
        table_text = read_reviewer_semantic_text(ROOT / rel, errors)
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
    promotion_contract_payload = json.dumps(
        promotion_document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    promotion_contract_fingerprint = hashlib.sha256(promotion_contract_payload).hexdigest()
    if promotion_contract_fingerprint != EXPECTED_PROMOTION_CONTRACT_SHA256:
        fail("complete promotion contract does not match the reviewed machine-readable mapping", errors)
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
    non_human_review_layers = [
        layer.get("owner_repo")
        for layer in promotion_layers
        if layer.get("human_review_requirement") is not True
    ]
    if non_human_review_layers:
        fail(
            "every promotion layer must preserve human_review_requirement: true; "
            f"invalid layers: {non_human_review_layers}",
            errors,
        )
    hoxline_layers = [layer for layer in promotion_layers if layer.get("owner_repo") == "hoxline"]
    if len(hoxline_layers) != 1 or hoxline_layers[0] != EXPECTED_HOXLINE_PROMOTION_LAYER:
        fail("Hoxline promotion layer must preserve its exact position, boundaries, gates, statuses, and human-review requirement", errors)

    required_checks_document = read_yaml_mapping(ROOT / "governance" / "ORG_REQUIRED_CHECKS_MATRIX.yml", errors)
    required_checks_payload = json.dumps(
        required_checks_document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    required_checks_fingerprint = hashlib.sha256(required_checks_payload).hexdigest()
    if required_checks_fingerprint != EXPECTED_REQUIRED_CHECKS_MATRIX_SHA256:
        fail("complete required-checks matrix does not match the reviewed machine-readable mapping", errors)
    if required_checks_document.get("status") != "PHASE_2B_ORG_INVARIANT_AND_VALIDATION_ENFORCEMENT_RECORDED":
        fail("required-checks matrix must preserve the current Phase 2B status", errors)
    expected_phase_2b_boundary = {
        "creates_reusable_workflows": False,
        "changes_github_settings": False,
        "changes_branch_protection": False,
        "changes_rulesets": False,
        "dispatches_workflows": False,
        "promotes_proof": False,
        "promotes_public_safe": False,
    }
    if required_checks_document.get("phase_2b_boundary") != expected_phase_2b_boundary:
        fail("required-checks matrix must preserve the exact Phase 2B authority boundary", errors)
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
            (".github/workflows/command-center-invariants.yml",),
            (),
            (("command-center-invariants", "command-center-invariants"),),
        ),
        "hoxline": (
            "Product / ProofOps control experience and Claim Authority capabilities.",
            (".github/workflows/ci.yml",),
            (),
            (("ci", "test"),),
        ),
        "hawkinsoperations-detections": (
            "Detection source truth.",
            (
                ".github/workflows/baseline-detection-contract.yml",
                ".github/workflows/governance-gate.yml",
            ),
            (
                ("baseline-detection-contract", "baseline-hero-artifact-contract"),
                ("Governance Gate", "required-files"),
            ),
            (),
        ),
        "hawkinsoperations-validation": (
            "Validation behavior, fixtures, reports, and claim-boundary scan truth.",
            (
                ".github/workflows/baseline-validation-contract.yml",
                ".github/workflows/governance-gate.yml",
                ".github/workflows/ho-det-012-fixture-loop.yml",
                ".github/workflows/id-det-001-fixture-loop.yml",
                ".github/workflows/ho-det-001-proof-loop.yml",
                ".github/workflows/public-ho-det-001-report.yml",
                ".github/workflows/aws-det-001-fixture-loop.yml",
                ".github/workflows/ho-det-011-fixture-loop.yml",
                ".github/workflows/security-onion-visibility-contract.yml",
                ".github/workflows/cross-repo-claim-parity.yml",
            ),
            (
                ("baseline-validation-contract", "baseline-hero-validation-contract"),
                ("Governance Gate", "required-files"),
                ("HO-DET-012 Fixture Loop", "ho-det-012-fixture-loop"),
                ("ID-DET-001 Fixture Loop", "id-det-001-fixture-loop"),
                ("HO-DET-001 Proof Loop", "ho-det-001-proof-loop"),
                ("Public HO-DET-001 Controlled-Test Report", "public-ho-det-001-controlled-test-report"),
                ("AWS-DET-001 Fixture Loop", "aws-det-001-fixture-loop"),
                ("HO-DET-011 Fixture Loop", "ho-det-011-fixture-loop"),
                ("security-onion-visibility-contract", "security-onion-visibility-contract"),
            ),
            (("Cross Repo Claim Parity", "cross-repo-claim-parity"),),
        ),
        "hawkinsoperations-platform": (
            "Platform runtime/agent boundary contracts and status/plan visibility.",
            (
                ".github/workflows/governance-gate.yml",
                ".github/workflows/local-gpu-triage-gate.yml",
            ),
            (
                ("Governance Gate", "required-files"),
                ("Governance Gate", "ho-det-011-case-packet"),
            ),
            (("Local GPU Triage Gate", "local-gpu-triage-status"),),
        ),
        "hawkinsoperations-proof": (
            "Proof records, proof indexes, claim ceilings, and public-proof linkage.",
            (
                ".github/workflows/baseline-proof-integrity.yml",
                ".github/workflows/governance-gate.yml",
                ".github/workflows/ho-det-001-proof-integrity.yml",
                ".github/workflows/publish-proof-release.yml",
            ),
            (
                ("baseline-proof-integrity", "baseline-hod001-proof-integrity"),
                ("Governance Gate", "required-files"),
                ("ho-det-001-proof-integrity", "ho-det-001-proof-integrity"),
                ("Proof Pack 001 Release Check", "proof-pack-001-release-check"),
            ),
            (),
        ),
        "hawkinsoperations-website": (
            "Public rendering of approved public state.",
            (".github/workflows/governance-gate.yml",),
            (
                ("Governance Gate", "required-files"),
                ("Governance Gate", "build"),
            ),
            (),
        ),
    }
    for repository, (
        truth_surface,
        expected_workflow_files,
        expected_required_jobs,
        expected_non_required_jobs,
    ) in expected_required_check_markers.items():
        block = required_checks_blocks.get(repository, {})
        workflow_files = block.get("workflow_file", []) if isinstance(block, dict) else []
        job_contexts = block.get("job_check_context", []) if isinstance(block, dict) else []
        if not isinstance(job_contexts, list) or any(not isinstance(context, dict) for context in job_contexts):
            fail(f"{repository} job_check_context must be a list of mappings", errors)
            job_contexts = []
        observed_workflow_jobs = {
            (context.get("workflow_name"), context.get("job_id"))
            for context in job_contexts
        }
        if (
            block.get("truth_surface") != truth_surface
            or not isinstance(workflow_files, list)
            or tuple(workflow_files) != expected_workflow_files
            or observed_workflow_jobs != set((*expected_required_jobs, *expected_non_required_jobs))
        ):
            fail(f"required-checks matrix metadata is not bound to {repository}", errors)
        declared_pairs: list[tuple[str, str]] = []
        for declaration_field, expected_pairs in (
            ("required_checks_observed", expected_required_jobs),
            ("important_non_required_checks", expected_non_required_jobs),
        ):
            declarations = block.get(declaration_field, []) if isinstance(block, dict) else []
            if not isinstance(declarations, list) or any(not isinstance(item, str) for item in declarations):
                fail(f"{repository} {declaration_field} must be a list of workflow / job strings", errors)
                continue
            field_pairs: list[tuple[str, str]] = []
            for declaration in declarations:
                match = re.match(r"^(.+?) / ([A-Za-z0-9_.-]+)(?:\s|$)", declaration)
                if not match:
                    fail(f"{repository} {declaration_field} has an unparseable workflow / job declaration", errors)
                    continue
                pair = (match.group(1), match.group(2))
                field_pairs.append(pair)
                declared_pairs.append(pair)
            if set(field_pairs) != set(expected_pairs):
                fail(f"{repository} {declaration_field} does not match its canonical check classification", errors)
        if len(declared_pairs) != len(set(declared_pairs)):
            fail(f"{repository} check declarations contain duplicate workflow / job pairs", errors)
        actual_pairs = [
            (context.get("workflow_name"), context.get("job_id"))
            for context in job_contexts
        ]
        if len(actual_pairs) != len(set(actual_pairs)):
            fail(f"{repository} job_check_context contains duplicate workflow / job pairs", errors)
        if set(actual_pairs) != set(declared_pairs):
            fail(f"{repository} declared checks and structured workflow / job contexts must match exactly", errors)

    template_text = read_reviewer_visible_text(
        ROOT / ".github" / "pull_request_template.md", errors
    )
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

    system_map_text = read_reviewer_visible_text(ROOT / "wiki" / "11_ORG_SYSTEM_MAP.md", errors)
    mermaid_blocks = extract_mermaid_blocks(system_map_text)
    normalized_mermaid = "\n\n--- mermaid block ---\n\n".join(
        "\n".join(line.rstrip() for line in block.strip().splitlines())
        for block in mermaid_blocks
    ).encode("utf-8")
    if hashlib.sha256(normalized_mermaid).hexdigest() != EXPECTED_SYSTEM_MAP_MERMAID_SHA256:
        fail("organization system-map Mermaid topology does not match the complete reviewed graph", errors)
    required_hoxline_routes = (
        'hox["hoxline<br/>product / ProofOps control',
        "org --> hox",
        "val --> hox",
        "hox --> plat",
        "plat --> proof",
        "validation --> hoxline --> platform --> proof",
    )
    for route in required_hoxline_routes:
        if route not in system_map_text:
            fail(f"wiki/11_ORG_SYSTEM_MAP.md missing Hoxline routing: {route}", errors)
    if "plat --> hox" in system_map_text:
        fail("wiki/11_ORG_SYSTEM_MAP.md must not route platform backward through Hoxline", errors)
    mermaid_node_decoration = (
        r"(?:\s*(?:\[[^\n]*?\]|\([^\n]*?\)|\{[^\n]*?\}|@\{[^\n]*?\}|:::[A-Za-z0-9_-]+))*"
    )
    mermaid_edge_segment = r"[ox<]?[-.=~]{2,}[>ox]?"
    mermaid_label_start = r"[-.=~]{2,}"
    mermaid_label_end = r"[-.=~]{2,}[>ox]?"
    mermaid_quoted_label = r'"(?:\\.|[^"\\])*"'
    mermaid_inline_label = rf"(?:{mermaid_quoted_label}|[^|>\n]+?)"
    mermaid_pipe_label = rf"(?:{mermaid_quoted_label}|[^|\n]*)"
    mermaid_link = (
        rf"(?:{mermaid_label_start}\s+{mermaid_inline_label}\s+{mermaid_label_end}|{mermaid_edge_segment})"
        rf"(?:\|{mermaid_pipe_label}\|)?"
    )
    mermaid_node_ref = rf"[A-Za-z_][A-Za-z0-9_-]*{mermaid_node_decoration}"
    mermaid_node_group = rf"{mermaid_node_ref}(?:\s*&\s*{mermaid_node_ref})*"
    mermaid_edge_id = r"(?:\s+[A-Za-z_][A-Za-z0-9_-]*@)?"
    mermaid_edge_statement = re.compile(
        rf"(?=(?P<left>{mermaid_node_group}){mermaid_edge_id}\s*{mermaid_link}\s*(?P<right>{mermaid_node_group}))"
    )
    mermaid_node_identifier = re.compile(
        rf"(?:^|&)\s*([A-Za-z_][A-Za-z0-9_-]*){mermaid_node_decoration}"
    )
    forbidden_hoxline_peers = {"proof", "web", "website"}
    for line in system_map_text.splitlines():
        for edge in mermaid_edge_statement.finditer(line):
            left_ids = {
                match.group(1).lower()
                for match in mermaid_node_identifier.finditer(edge.group("left"))
            }
            right_ids = {
                match.group(1).lower()
                for match in mermaid_node_identifier.finditer(edge.group("right"))
            }
            left_has_hoxline = bool(left_ids & {"hox", "hoxline"})
            right_has_hoxline = bool(right_ids & {"hox", "hoxline"})
            if (
                (left_has_hoxline and right_ids & forbidden_hoxline_peers)
                or (right_has_hoxline and left_ids & forbidden_hoxline_peers)
            ):
                fail(
                    "wiki/11_ORG_SYSTEM_MAP.md must not bypass platform and proof between Hoxline and public output",
                    errors,
                )
                break
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
    all_text = "\n".join(
        strip_html_comments(text) if path.suffix.lower() == ".md" else text
        for path in text_files
        for text in (path.read_text(encoding="utf-8", errors="ignore"),)
    )
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
