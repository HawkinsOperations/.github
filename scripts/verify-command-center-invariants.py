#!/usr/bin/env python3
"""Fail-closed checks for the HawkinsOperations .github command center."""

from __future__ import annotations

import hashlib
import html
import json
import re
import sys
import unicodedata
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
    "not-",
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
    "remain",
    "requires",
    "exclude",
    "excludes",
    "may not",
    "must avoid",
    "fails closed",
    "gate",
    "neither",
    "no ",
    "without",
    "non-public",
    "not_public_safe",
    "coordination-only",
    "report-only",
    "separate",
    "pending",
)

AUTHORITY_COLLAPSE_PATTERNS = (
    (
        "Hoxline proof authority",
        re.compile(
            r"\bhoxline\s+(?:is|owns|has)\s+(?:the\s+)?proof\s+authority\b",
            re.IGNORECASE,
        ),
    ),
    (
        "Hoxline proof-record ownership",
        re.compile(
            r"\bhoxline\s+(?:is|owns|has|controls)\s+(?:the\s+)?"
            r"(?:proof\s+records?|claim\s+ceilings?|final\s+approval)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "Hoxline cross-plane authority",
        re.compile(
            r"\bhoxline\s+(?:is|owns|has|controls|approves|authorizes)\s+"
            r"(?:the\s+)?(?:merge\s+authority|approval\s+authority|"
            r"disposition\s+authority|case\s+closure|source\s+truth|"
            r"validation\s+truth|runtime\s+truth|signal\s+truth)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "rendering proof authority",
        re.compile(
            r"\b(?:website|github(?:\s+organization)?|\.github)\s+"
            r"(?:rendering\s+)?(?:is|owns|has)\s+(?:the\s+)?proof\s+authority\b",
            re.IGNORECASE,
        ),
    ),
    (
        "rendering proof-record ownership",
        re.compile(
            r"\b(?:website|github(?:\s+organization)?|\.github)\s+"
            r"(?:rendering\s+)?(?:is|owns|has|controls)\s+(?:the\s+)?"
            r"(?:proof\s+records?|claim\s+ceilings?|final\s+approval)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "rendering cross-plane authority",
        re.compile(
            r"\b(?:website|github(?:\s+organization)?|\.github)\s+"
            r"(?:rendering\s+)?(?:is|owns|has|controls|approves|authorizes)\s+"
            r"(?:the\s+)?(?:merge\s+authority|approval\s+authority|"
            r"disposition\s+authority|case\s+closure|source\s+truth|"
            r"validation\s+truth|runtime\s+truth|signal\s+truth)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "AI approval authority",
        re.compile(
            r"\bAI\s+(?:is|owns|has)\s+(?:the\s+)?"
            r"(?:approval|merge|disposition|proof)\s+authority\b",
            re.IGNORECASE,
        ),
    ),
    (
        "AI decision authority",
        re.compile(
            r"\bAI\s+(?:(?:approves?|authorizes?|controls?|owns|has|decides?)\s+"
            r"(?:the\s+)?(?:merges?|approval|disposition|claim\s+promotion|"
            r"proof\s+authority|case\s+closure)|merges?\s+pull\s+requests?)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "non-human direct authority action",
        re.compile(
            r"\b(?:AI|hoxline|website|github(?:\s+organization)?|\.github)\s+"
            r"(?:(?:can|may|will|must|could|might|should|would)\s+|"
            r"(?:is|are|was|were)(?:\s+being)?\s+|"
            r"(?:has|have|had)(?:\s+been)?\s+)?"
            r"(?:(?:approv|authoriz)(?:e|es|ed|ing)\s+merges?|"
            r"merg(?:e|es|ed|ing)\s+pull\s+requests?|"
            r"(?:decid|approv|authoriz)(?:e|es|ed|ing)\s+"
            r"(?:detection\s+|incident\s+)?disposition|"
            r"clos(?:e|es|ed|ing)\s+cases?|"
            r"promot(?:e|es|ed|ing)\s+claims?)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "non-human delegated authority action",
        re.compile(
            r"\b(?:AI|hoxline|website|github(?:\s+organization)?|\.github)\s+"
            r"(?:(?:is|was|were)(?:\s+being)?|(?:has|have|had)\s+been|"
            r"(?:can|may|will|must|could|might|should|would)\s+be)\s+"
            r"(?:authorized|delegated|empowered|permitted|allowed)\s+to\s+"
            r"(?:(?:approve|authorize)\s+merges?|merge\s+pull\s+requests?|"
            r"(?:decide|approve|authorize)\s+(?:detection\s+|incident\s+)?"
            r"disposition|close\s+cases?|promote\s+claims?)\b|"
            r"\b(?:merge|approval|disposition|claim\s+promotion|case\s+closure)\s+"
            r"authority\s+(?:(?:is|was|were)|(?:has|have|had)\s+been)\s+"
            r"(?:delegated|granted|assigned|given)\s+to\s+(?:the\s+)?"
            r"(?:AI|hoxline|website|github(?:\s+organization)?|\.github)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "non-human granted authority action",
        re.compile(
            r"\b(?:AI|hoxline|website|github(?:\s+organization)?|\.github)\s+"
            r"(?:(?:is|was|were)(?:\s+being)?|(?:has|have|had)\s+been|"
            r"(?:can|may|will|must|could|might|should|would)\s+be)\s+"
            r"(?:granted|given|assigned|delegated)\s+(?:the\s+)?"
            r"(?:authority|permission|power)\s+to\s+"
            r"(?:(?:approve|authorize)\s+merges?|merge\s+pull\s+requests?|"
            r"(?:decide|approve|authorize)\s+(?:detection\s+|incident\s+)?"
            r"disposition|close\s+cases?|promote\s+claims?)\b|"
            r"\b(?:AI|hoxline|website|github(?:\s+organization)?|\.github)\s+"
            r"(?:has|holds|possesses)\s+(?:the\s+)?"
            r"(?:authority|permission|power)\s+to\s+"
            r"(?:(?:approve|authorize)\s+merges?|merge\s+pull\s+requests?|"
            r"(?:decide|approve|authorize)\s+(?:detection\s+|incident\s+)?"
            r"disposition|close\s+cases?|promote\s+claims?)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "non-human passive authority action",
        re.compile(
            r"\b(?:(?:merges?|claims?|cases?)\s+(?:"
            r"(?:is|are|was|were)(?:\s+being)?|"
            r"(?:has|have|had)\s+been(?:\s+being)?|"
            r"(?:can|may|will|must|could|might|should|would)\s+be(?:\s+being)?)\s+"
            r"(?:approved|authorized|promoted|closed)|"
            r"(?:detection\s+|incident\s+)?disposition\s+(?:"
            r"(?:is|are|was|were)(?:\s+being)?|"
            r"(?:has|have|had)\s+been(?:\s+being)?|"
            r"(?:can|may|will|must|could|might|should|would)\s+be(?:\s+being)?)\s+"
            r"(?:decided|approved|authorized))\s+by\s+"
            r"(?:the\s+)?(?:AI|hoxline|website|github(?:\s+organization)?|\.github)\b",
            re.IGNORECASE,
        ),
    ),
)

REJECTED_WORDING_LABEL = r"(?:Rejected|Blocked|Forbidden) wording:"
EXPLICIT_REJECTED_EXAMPLE_PREFIX = re.compile(
    rf"^(?:HTML_(?:BODY|INLINE)\s+)?(?:"
    rf"{REJECTED_WORDING_LABEL}|"
    rf"(?:\*\*{REJECTED_WORDING_LABEL}\*\*|"
    rf"__{REJECTED_WORDING_LABEL}__|"
    rf"\*{REJECTED_WORDING_LABEL}\*|"
    rf"_{REJECTED_WORDING_LABEL}_|"
    rf"~~{REJECTED_WORDING_LABEL}~~|"
    rf"`{REJECTED_WORDING_LABEL}`)(?=$|[^\w])"
    rf")",
    re.IGNORECASE,
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


def is_complete_type7_html_tag(text: str) -> bool:
    """Recognize one complete CommonMark type-7 opening or closing tag."""
    tag_name = r"[A-Za-z][A-Za-z0-9-]*"
    attribute_name = r"[A-Za-z_:][A-Za-z0-9_.:-]*"
    attribute_value = r'(?:[^ \t\r\n"\'=<>`]+|\'[^\']*\'|"[^"]*")'
    attribute = rf"[ \t]+{attribute_name}(?:[ \t]*=[ \t]*{attribute_value})?"
    opening = rf"<{tag_name}(?:{attribute})*[ \t]*/?>"
    closing = rf"</{tag_name}[ \t]*>"
    return bool(re.fullmatch(rf"(?:{opening}|{closing})[ \t]*", text))


def parse_markdown_container_prefix(line: str) -> tuple[int, int, int] | None:
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
    return quote_depth, list_indent, cursor


def parse_markdown_delimited_html_block(line: str) -> tuple[str, int, int] | None:
    """Recognize CommonMark HTML blocks closed by a non-tag delimiter."""
    content = line.rstrip("\r\n")
    prefix = parse_markdown_container_prefix(line)
    if prefix is None:
        return None
    quote_depth, list_indent, cursor = prefix
    remainder = content[cursor:]
    if remainder.startswith("<?"):
        return "?>", quote_depth, list_indent
    if remainder.startswith("<![CDATA["):
        return "]]>", quote_depth, list_indent
    if re.match(r"<![A-Z]", remainder):
        return ">", quote_depth, list_indent
    return None


def parse_markdown_html_block_container(
    line: str,
    *,
    allow_type7: bool = True,
) -> tuple[int, int] | None:
    content = line.rstrip("\r\n")
    prefix = parse_markdown_container_prefix(line)
    if prefix is None:
        return None
    quote_depth, list_indent, cursor = prefix
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


def preserve_html_body_as_text(line: str) -> str:
    """Keep renderer-visible HTML body text without treating it as Markdown structure."""
    content = line.rstrip("\r\n")
    ending = line[len(content):]
    if not content:
        return ending
    return f"HTML_BODY {content}{ending}"


def neutralize_html_promoted_markdown_structure(source: str, stripped: str) -> str:
    """Prevent inline HTML text from becoming Markdown structure after tag removal."""
    source_lines = source.splitlines(keepends=True)
    stripped_lines = stripped.splitlines(keepends=True)
    if len(source_lines) != len(stripped_lines):
        return stripped

    html_line_flags: list[bool] = []
    in_tag = False
    attribute_quote = ""
    for line in source_lines:
        line_has_html_syntax = in_tag
        cursor = 0
        while cursor < len(line):
            character = line[cursor]
            if in_tag:
                line_has_html_syntax = True
                if attribute_quote:
                    if character == attribute_quote:
                        attribute_quote = ""
                elif character in {'"', "'"}:
                    attribute_quote = character
                elif character == ">":
                    in_tag = False
            elif character == "<" and cursor + 1 < len(line) and re.match(
                r"[A-Za-z/!?]", line[cursor + 1]
            ):
                in_tag = True
                line_has_html_syntax = True
            cursor += 1
        html_line_flags.append(line_has_html_syntax)

    markdown_structure = re.compile(
        r"^[ \t]*(?:#{1,6}(?:[ \t]+|$)|\|.*\|[ \t]*$|"
        r"(?:[-+*]|\d{1,9}[.)])[ \t]+|(?:=+|-+)[ \t]*$)"
    )
    neutralized: list[str] = []
    for line, had_html_syntax in zip(stripped_lines, html_line_flags):
        if had_html_syntax and markdown_structure.match(line.rstrip("\r\n")):
            neutralized.append(f"HTML_INLINE {line}")
        else:
            neutralized.append(line)
    return "".join(neutralized)


def strip_markdown_html_tags(text: str) -> str:
    """Remove non-rendered HTML tag syntax while preserving visible text and lines."""
    output: list[str] = []
    in_tag = False
    break_tag = False
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
                if break_tag:
                    output.append(" ")
                break_tag = False
            cursor += 1
            continue

        if character == "<" and cursor + 1 < len(text) and re.match(r"[A-Za-z/!?]", text[cursor + 1]):
            in_tag = True
            break_tag = bool(re.match(r"<br(?=[\s/>])", text[cursor:], re.IGNORECASE))
            cursor += 1
            continue
        output.append(character)
        cursor += 1
    stripped = "".join(output)
    return neutralize_html_promoted_markdown_structure(text, stripped)


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
    html_code_depth = 0
    html_nested_raw_tag = ""
    html_tag_buffer = ""
    html_attribute_quote = ""
    html_block_container: tuple[int, int] | None = None
    html_delimited_block: tuple[str, int, int] | None = None
    paragraph_open = False

    def advance_html_code_state(
        line: str,
        active_tag: str,
        active_depth: int,
        nested_raw_tag: str,
        tag_buffer: str,
        attribute_quote: str,
    ) -> tuple[str, int, str, str, str, bool]:
        cursor = 0
        contains_raw_code = bool(active_tag)
        if active_tag in {"script", "style", "textarea"}:
            closing = re.search(
                rf"</{re.escape(active_tag)}[ \t]*>",
                line,
                re.IGNORECASE,
            )
            if not closing:
                return active_tag, active_depth, nested_raw_tag, "", "", True
            cursor = closing.end()
            active_tag = ""
            active_depth = 0
            tag_buffer = ""
            attribute_quote = ""
        while cursor < len(line):
            if active_tag == "template" and nested_raw_tag:
                nested_closing = re.search(
                    rf"</{re.escape(nested_raw_tag)}[ \t]*>",
                    line[cursor:],
                    re.IGNORECASE,
                )
                if not nested_closing:
                    return active_tag, active_depth, nested_raw_tag, "", "", True
                cursor += nested_closing.end()
                nested_raw_tag = ""
                contains_raw_code = True
                continue

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
                    r"<(pre|script|style|textarea|template)(?=[ \t>/])",
                    tag_buffer,
                    re.IGNORECASE,
                )
                if pending_opening:
                    active_tag = pending_opening.group(1).lower()
                    active_depth = 0
                    contains_raw_code = True
            if character != ">":
                continue

            token = tag_buffer
            tag_buffer = ""
            if active_tag:
                nested_raw_opening = (
                    active_tag == "template"
                    and re.match(
                        r"<(script|style|textarea)(?=[ \t>/])",
                        token,
                        re.IGNORECASE,
                    )
                )
                nested_template = (
                    active_tag == "template"
                    and re.match(r"<template(?=[ \t>/])", token, re.IGNORECASE)
                )
                if nested_raw_opening:
                    nested_raw_tag = nested_raw_opening.group(1).lower()
                elif nested_template:
                    active_depth = max(active_depth, 0) + 1
                elif re.fullmatch(
                    rf"</{re.escape(active_tag)}[ \t]*>",
                    token,
                    re.IGNORECASE,
                ):
                    if active_tag == "template" and active_depth > 1:
                        active_depth -= 1
                    else:
                        active_tag = ""
                        active_depth = 0
                elif active_depth == 0:
                    active_depth = 1
                contains_raw_code = True
                continue
            opening_tag = re.match(
                r"<(pre|script|style|textarea|template)(?=[ \t>/])",
                token,
                re.IGNORECASE,
            )
            if opening_tag:
                active_tag = opening_tag.group(1).lower()
                active_depth = 1
                contains_raw_code = True
        if active_tag and tag_buffer and not attribute_quote:
            tag_buffer = ""
        return (
            active_tag,
            active_depth,
            nested_raw_tag,
            tag_buffer,
            attribute_quote,
            contains_raw_code,
        )

    for line in text.splitlines(keepends=True):
        if html_delimited_block is not None:
            terminator, quote_depth, list_indent = html_delimited_block
            if line_belongs_to_markdown_container(line, quote_depth, list_indent):
                output.append(preserve_html_body_as_text(line))
                if terminator in line:
                    html_delimited_block = None
                    paragraph_open = False
                continue
            html_delimited_block = None

        if html_block_container is not None:
            quote_depth, list_indent = html_block_container
            if line_belongs_to_markdown_container(line, quote_depth, list_indent):
                output.append(preserve_html_body_as_text(line))
                if is_blank_markdown_container_line(line):
                    html_block_container = None
                    paragraph_open = False
                continue
            html_block_container = None

        if html_code_tag or html_tag_buffer:
            (
                html_code_tag,
                html_code_depth,
                html_nested_raw_tag,
                html_tag_buffer,
                html_attribute_quote,
                _,
            ) = advance_html_code_state(
                line,
                html_code_tag,
                html_code_depth,
                html_nested_raw_tag,
                html_tag_buffer,
                html_attribute_quote,
            )
            output.append(preserve_html_body_as_text(line))
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

        delimited_html_start = parse_markdown_delimited_html_block(line)
        if delimited_html_start is not None:
            terminator, quote_depth, list_indent = delimited_html_start
            if terminator not in line[line.find("<"):]:
                html_delimited_block = (terminator, quote_depth, list_indent)
            output.append(preserve_html_body_as_text(line))
            paragraph_open = False
            continue

        (
            html_code_tag,
            html_code_depth,
            html_nested_raw_tag,
            html_tag_buffer,
            html_attribute_quote,
            contains_raw_code,
        ) = advance_html_code_state(
            line,
            "",
            0,
            "",
            "",
            "",
        )
        if contains_raw_code or html_tag_buffer:
            output.append(preserve_html_body_as_text(line))
            paragraph_open = False
            continue

        html_block_container_start = parse_markdown_html_block_container(
            line,
            allow_type7=not paragraph_open,
        )
        if html_block_container_start is not None:
            html_block_container = html_block_container_start
            output.append(preserve_html_body_as_text(line))
            paragraph_open = False
            continue

        output.append(line)
        if not line.strip() or interrupts_markdown_paragraph(line):
            paragraph_open = False
        else:
            paragraph_open = True
    return "".join(output)


def valid_markdown_link_title(text: str) -> bool:
    """Recognize the optional quoted or parenthesized CommonMark link title."""
    title = text.strip()
    if not title:
        return True
    closing_delimiter = {'"': '"', "'": "'", "(": ")"}.get(title[0])
    if not closing_delimiter or len(title) < 2 or title[-1] != closing_delimiter:
        return False
    cursor = 1
    while cursor < len(title) - 1:
        if title[cursor] == "\\":
            cursor += 2
            continue
        if title[cursor] == closing_delimiter:
            return False
        cursor += 1
    return True


def valid_markdown_inline_link_target(text: str) -> bool:
    """Validate a balanced parenthesized destination and optional title."""
    if len(text) < 2 or text[0] != "(" or text[-1] != ")":
        return False
    content = text[1:-1].strip()
    if not content:
        return True
    if content.startswith("<"):
        cursor = 1
        while cursor < len(content):
            if content[cursor] == "\\":
                cursor += 2
                continue
            if content[cursor] in "\r\n<":
                return False
            if content[cursor] == ">":
                return valid_markdown_link_title(content[cursor + 1:])
            cursor += 1
        return False

    cursor = 0
    while cursor < len(content):
        character = content[cursor]
        if character == "\\":
            cursor += 2
            continue
        if character.isspace():
            break
        if ord(character) < 0x20 or ord(character) == 0x7F or character in "<>":
            return False
        cursor += 1
    return valid_markdown_link_title(content[cursor:])


def markdown_link_destination_ranges(text: str) -> list[tuple[int, int]]:
    """Locate hidden inline/reference link destinations without parsing labels."""
    ranges: list[tuple[int, int]] = []
    cursor = 0
    while cursor < len(text):
        label_start = text.find("[", cursor)
        if label_start < 0:
            break
        label_end = label_start + 1
        bracket_depth = 1
        while label_end < len(text) and bracket_depth:
            if text[label_end] == "\\":
                label_end += 2
                continue
            if text[label_end] == "[":
                bracket_depth += 1
            elif text[label_end] == "]":
                bracket_depth -= 1
            label_end += 1
        if bracket_depth:
            cursor = label_start + 1
            continue

        if label_end < len(text) and text[label_end] == "(":
            destination_end = label_end + 1
            parenthesis_depth = 1
            while destination_end < len(text) and parenthesis_depth:
                if text[destination_end] == "\\":
                    destination_end += 2
                    continue
                if text[destination_end] == "(":
                    parenthesis_depth += 1
                elif text[destination_end] == ")":
                    parenthesis_depth -= 1
                destination_end += 1
            if parenthesis_depth == 0 and valid_markdown_inline_link_target(
                text[label_end:destination_end]
            ):
                ranges.append((label_end, destination_end))
                cursor = destination_end
                continue
        elif label_end < len(text) and text[label_end] == "[":
            reference_end = text.find("]", label_end + 1)
            if reference_end >= 0:
                ranges.append((label_end, reference_end + 1))
                cursor = reference_end + 1
                continue
        cursor = label_end
    return ranges


def reviewer_visible_edge_character(text: str, *, from_end: bool) -> str:
    """Return the nearest rendered character across links, emphasis, and Cf text."""
    visible = normalize_markdown_link_text(text)
    visible = "".join(
        character
        for character in html.unescape(visible)
        if unicodedata.category(character) != "Cf"
    )
    delimiters = ("**", "__", "~~", "*", "_", "~")
    changed = True
    while visible and changed:
        changed = False
        for delimiter in delimiters:
            if from_end:
                paired = visible.endswith(delimiter) and delimiter in visible[:-len(delimiter)]
                if paired:
                    visible = visible[:-len(delimiter)]
                    changed = True
                    break
            else:
                paired = visible.startswith(delimiter) and delimiter in visible[len(delimiter):]
                if paired:
                    visible = visible[len(delimiter):]
                    changed = True
                    break
    if not visible:
        return ""
    return visible[-1] if from_end else visible[0]


def strip_markdown_inline_code_spans(text: str) -> str:
    """Remove matched code spans while preserving unmatched delimiters as text."""
    output: list[str] = []
    cursor = 0
    destination_ranges = markdown_link_destination_ranges(text)
    while cursor < len(text):
        opening = re.search(r"`+", text[cursor:])
        if not opening:
            output.append(text[cursor:])
            break

        opening_start = cursor + opening.start()
        opening_run = opening.group(0)
        output.append(text[cursor:opening_start])
        if any(start <= opening_start < end for start, end in destination_ranges):
            output.append(opening_run)
            cursor = opening_start + len(opening_run)
            continue
        backslash_count = 0
        preceding_index = opening_start - 1
        while preceding_index >= 0 and text[preceding_index] == "\\":
            backslash_count += 1
            preceding_index -= 1
        if backslash_count % 2:
            output.append(opening_run)
            cursor = opening_start + len(opening_run)
            continue

        content_start = opening_start + len(opening_run)
        closing_start = 0
        closing_end = 0
        for closing in re.finditer(r"`+", text[content_start:]):
            if len(closing.group(0)) == len(opening_run):
                closing_start = content_start + closing.start()
                closing_end = content_start + closing.end()
                break
        if not closing_end:
            output.append(opening_run)
            cursor = content_start
            continue

        visible_left = reviewer_visible_edge_character(
            text[:opening_start], from_end=True
        )
        visible_right = reviewer_visible_edge_character(
            text[closing_end:], from_end=False
        )
        left_word = bool(visible_left and re.match(r"\w", visible_left))
        right_word = bool(visible_right and re.match(r"\w", visible_right))
        code_span = text[opening_start:closing_end]
        rendered_content = re.sub(r"\r?\n", " ", text[content_start:closing_start])
        if (
            len(rendered_content) >= 2
            and rendered_content.startswith(" ")
            and rendered_content.endswith(" ")
            and rendered_content.strip(" ")
        ):
            rendered_content = rendered_content[1:-1]
        if (left_word or right_word) and not re.search(r"\s", rendered_content):
            output.append(rendered_content)
        else:
            output.append("".join(
                character if character in "\r\n" else " "
                for character in code_span
            ))
        cursor = closing_end
    return "".join(output)


def mask_blocked_claim_inline_literals(text: str) -> str:
    """Mask standalone code spans that quote a complete blocked claim phrase."""
    output: list[str] = []
    cursor = 0
    destination_ranges = markdown_link_destination_ranges(text)
    while cursor < len(text):
        opening = re.search(r"`+", text[cursor:])
        if not opening:
            output.append(text[cursor:])
            break
        opening_start = cursor + opening.start()
        opening_run = opening.group(0)
        output.append(text[cursor:opening_start])
        if any(start <= opening_start < end for start, end in destination_ranges):
            output.append(opening_run)
            cursor = opening_start + len(opening_run)
            continue
        backslashes = 0
        preceding = opening_start - 1
        while preceding >= 0 and text[preceding] == "\\":
            backslashes += 1
            preceding -= 1
        if backslashes % 2:
            output.append(opening_run)
            cursor = opening_start + len(opening_run)
            continue

        content_start = opening_start + len(opening_run)
        closing_start = 0
        closing_end = 0
        for closing in re.finditer(r"`+", text[content_start:]):
            if len(closing.group(0)) == len(opening_run):
                closing_start = content_start + closing.start()
                closing_end = content_start + closing.end()
                break
        if not closing_end:
            output.append(opening_run)
            cursor = content_start
            continue

        content = html.unescape(text[content_start:closing_start]).lower()
        contains_complete_blocked_phrase = any(
            re.search(
                rf"(?<![A-Za-z]){re.escape(phrase.lower())}(?![A-Za-z])",
                content,
            )
            for phrase in BLOCKED_CLAIMS
        )
        code_span = text[opening_start:closing_end]
        if contains_complete_blocked_phrase:
            output.append("".join(
                character if character in "\r\n" else " "
                for character in code_span
            ))
        else:
            output.append(code_span)
        cursor = closing_end
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

    workflow_path = ROOT / ".github" / "workflows" / "command-center-invariants.yml"
    workflow = read_yaml_mapping(workflow_path, errors)
    triggers = workflow.get("on", workflow.get(True, {}))
    if not isinstance(triggers, dict):
        fail("command-center invariant workflow must define structured event triggers", errors)
        triggers = {}
    required_trigger_paths = {
        "README.md",
        "profile/**",
        "architecture/**",
        "governance/**",
        "wiki/**",
        ".github/**",
        "scripts/verify-command-center-invariants.py",
    }
    for event in ("pull_request", "push"):
        event_config = triggers.get(event, {})
        paths = event_config.get("paths", []) if isinstance(event_config, dict) else []
        actual_paths = {str(path) for path in paths} if isinstance(paths, list) else set()
        negated_paths = sorted(path for path in actual_paths if path.startswith("!"))
        missing_paths = sorted(required_trigger_paths - actual_paths)
        if missing_paths:
            fail(
                f"command-center invariant workflow {event} trigger is missing scanned paths: "
                f"{', '.join(missing_paths)}",
                errors,
            )
        if negated_paths:
            fail(
                f"command-center invariant workflow {event} trigger must not use "
                f"negative path patterns: {', '.join(negated_paths)}",
                errors,
            )
    push_config = triggers.get("push", {})
    push_branches = push_config.get("branches", []) if isinstance(push_config, dict) else []
    if not isinstance(push_branches, list) or "main" not in push_branches:
        fail("command-center invariant workflow push trigger must include main", errors)
    if isinstance(push_branches, list) and any(
        str(branch).startswith("!") for branch in push_branches
    ):
        fail("command-center invariant workflow push branches must not use negative patterns", errors)

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
        section_matches = re.findall(
            rf"## {re.escape(heading)}\s+(.*?)(?=\n## |\Z)",
            table_text,
            re.DOTALL,
        )
        html_heading_source = strip_markdown_inline_code_spans(
            strip_markdown_code_blocks(
                read_reviewer_visible_text(ROOT / rel, errors)
            )
        )
        html_heading_count = 0
        for html_heading in re.finditer(
            r"<h2\b[^>]*>(.*?)</h2\s*>",
            html_heading_source,
            re.IGNORECASE | re.DOTALL,
        ):
            rendered_heading = re.sub(r"<[^>]+>", "", html_heading.group(1))
            rendered_heading = " ".join(html.unescape(rendered_heading).split())
            if rendered_heading.casefold() == heading.casefold():
                html_heading_count += 1
        if len(section_matches) + html_heading_count != 1:
            fail(
                f"{rel} must contain exactly one parseable authority table: {heading}",
                errors,
            )
            continue
        table_lines = extract_contiguous_table_lines(section_matches[0], expected_header)
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


def contains_boundary_marker(text: str) -> bool:
    """Match boundary terms as rendered tokens, never as arbitrary substrings."""
    for marker in BOUNDARY_WORDS:
        token = marker.strip()
        if not token:
            continue
        prefix = r"(?<![A-Za-z])" if token[0].isalpha() else ""
        suffix = r"(?![A-Za-z])" if token[-1].isalpha() else ""
        if re.search(rf"{prefix}{re.escape(token)}{suffix}", text, re.IGNORECASE):
            return True
    return False


def unescape_markdown_punctuation(text: str) -> str:
    """Decode CommonMark backslash escapes for ASCII punctuation."""
    return re.sub(
        r"""\\([!"#$%&'()*+,\-./:;<=>?@\[\]\\^_`{|}~])""",
        r"\1",
        text,
    )


def contains_explicit_boundary_qualifier(text: str) -> bool:
    """Recognize reviewer-visible wording that explicitly bounds a claim."""
    return bool(re.search(
        r"\b(?:(?:does not|do not|must not|may not|cannot)\s+(?:be\s+)?"
        r"(?:establish|prove|support|authorize|grant|promote|claim|assert|"
        r"mean|constitute|show|indicate|confirm|publish|report|describe|"
        r"treat|own)(?:s|ed|ing)?|not established|"
        r"not proven|not proof|not authority|not public-safe|"
        r"not\b[^|.!?;]{0,180}\bpublic-safe|"
        r"(?:blocked|unproven|unsupported|forbidden|restricted|rejected|"
        r"withheld)\s+(?:claims?|wording|statuses?|promotions?|evidence)|"
        r"claim blocked|"
        r"not_public_safe|"
        r"requires? evidence|required next evidence|claim ceiling|"
        r"(?:runtime|signal|proof|evidence|authority|claim|truth|publication)"
        r"[ -]boundar(?:y|ies)|exclude(?:s|d)?|exclusions?)\b|"
        r"\bmay not\s*:\s*$",
        text,
        re.IGNORECASE,
    ))


def contains_strong_boundary_status(text: str) -> bool:
    """Recognize an explicit blocked status within one structured cell."""
    normalized = text.strip().strip('"\'`').strip()
    return bool(re.search(
        r"^(?:blocked|unproven|unsupported|forbidden|rejected|withheld|"
        r"not_public_safe|blocked claims register)$|"
        r"\bnot\b[^|,.!?;]{0,160}\bpublic-safe\b|"
        r"\buntil\s+(?:proof|evidence|claim|wording|privacy|public)\b"
        r"[^|.!?;]{0,160}\b(?:reviewed|approved?|proven)\b|"
        r"\bonly for reviewed\b[^|.!?;]{0,80}\b(?:records?|claims?|"
        r"evidence|proof)\b|\bafter public claim review\b",
        normalized,
        re.IGNORECASE,
    ))


def claim_has_bound_qualifier(context: str, claim_start: int, claim_end: int) -> bool:
    """Require an explicit negative construction tied to a blocked claim."""
    prefix = context[:claim_start]
    governing_prefix = re.compile(
        r"\b(?:(?:does not|do not|must not|may not|cannot)"
        r"(?:\s+[a-z-]+ly)?\s+(?:be\s+)?|fails closed (?:to|for)\s+|"
        r"is forbidden to\s+|is blocked from\s+)"
        r"(?:establish|prove|support|authorize|grant|promote|claim|assert|"
        r"mean|constitute|show|indicate|confirm|create|make|decide|control|"
        r"own|publish|report|describe|treat|become)(?:s|ed|ing)?\b"
        r"(?P<governed_tail>[^.!?;]{0,500})$",
        re.IGNORECASE,
    )
    immediate_prefix = re.compile(
        r"(?:\b(?:is|are|was|were|be|become|becomes|remain|remains)\s+)?"
        r"(?:not(?:\s+[a-z-]+ly)?|without|no)\s*$|"
        r"\b(?:blocked|rejected|forbidden|unsupported|unproven|withheld|"
        r"restricted)\s*(?:claim|wording|status|state)?\s*[:\-—]\s*$",
        re.IGNORECASE,
    )
    contextual_prefix = re.compile(
        r"\bno\s+(?:runtime|signal|proof|evidence|production|customer|fleet|"
        r"claim|approval|disposition)(?:[/\s-]+(?:runtime|signal|proof|"
        r"evidence|production|customer|fleet|claim|approval|disposition))*"
        r"[/\s-]*$|"
        r"\bblocked claims?\s+(?:needs?|requires?)\b[^.!?;]{0,500}$|"
        r"\bfails closed for\b[^.!?;]{0,500}$|"
        r"\bwithout\s+(?:becoming|creating|establishing|proving|promoting)\s+"
        r"(?:(?:proof|evidence|runtime|signal|approval|authority|status|"
        r"claims?|truth)\s+(?:or|and)\s+)*$|"
        r"\bneither\b[^.!?;]{0,100}\b(?:proves?|establishes?|supports?|"
        r"authorizes?|grants?|promotes?)\b[^.!?;]{0,500}$",
        re.IGNORECASE,
    )
    governing_match = governing_prefix.search(prefix)
    contextual_match = contextual_prefix.search(prefix)
    unrelated_clause = re.compile(
        r"(?:,|\b(?:and|but|or|while|whereas|although|though|yet)\b)\s+"
        r"[^.!?;]{0,500}?\b"
        r"(?:is|are|was|were|does|do|has|have|can|may|will|must)\b",
        re.IGNORECASE,
    )
    if governing_match and not unrelated_clause.search(
        governing_match.group("governed_tail")
    ):
        return True
    if immediate_prefix.search(prefix):
        return True
    if contextual_match and not unrelated_clause.search(contextual_match.group(0)):
        return True

    suffix = context[claim_end:]
    direct_suffix = re.compile(
        r"^\s+(?:status\s*(?::|remains?|is)\s*(?:not_public_safe|"
        r"separate|blocked|unproven|withheld)\b|"
        r"requires?\s+(?:reviewed?|review|evidence|approval|privacy|stale)\b|"
        r"(?:remains?|is|are|was|were|must remain)\s+"
        r"(?:not\s+)?(?:blocked|unproven|unestablished|unsupported|withheld|"
        r"unapproved|separate|required)\b)",
        re.IGNORECASE,
    )
    if direct_suffix.search(suffix):
        return True

    collective_qualifier = re.compile(
        r"\b(?:claims?|statuses?|wording|evidence|proof|coverage|operation|"
        r"behavior|disposition|closure|content|material|routes?|promotion)\b"
        r"[^.!?;]{0,160}\b(?:remain|remains|requires?|are|is|must)\b"
        r"[^.!?;]{0,60}\b(?:blocked|unproven|withheld|reviewed|approved|"
        r"required|not|unsafe|separate|gated|avoid)\b",
        re.IGNORECASE,
    )
    return bool(collective_qualifier.search(suffix))


def check_identity_and_claim_context(text_files: list[Path], errors: list[str]) -> None:
    for path in text_files:
        rel = path.relative_to(ROOT).as_posix()
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        for line_no, line in enumerate(lines, start=1):
            lowered = line.lower()
            if "hawkinsops" in lowered and not any(marker in lowered for marker in ("legacy", "reference", "v1", "prior", "not current")):
                fail(f"{rel}:{line_no} uses HawkinsOps outside legacy/reference context", errors)

        is_markdown = path.suffix.lower() == ".md"
        if is_markdown:
            semantic_lines = read_reviewer_semantic_text(path, errors).splitlines()
            claim_units = iter_reviewer_claim_units(semantic_lines)
        else:
            claim_units = list(enumerate(lines, start=1))

        for line_no, claim_unit in claim_units:
            if is_markdown:
                claim_unit = normalize_markdown_link_text(claim_unit)
                candidate_claim_unit = "".join(
                    character
                    for character in html.unescape(claim_unit)
                    if unicodedata.category(character) != "Cf"
                )
                candidate_claim_unit = unescape_markdown_punctuation(
                    candidate_claim_unit
                )
                candidate_lower = re.sub(
                    r"[*_~`]+", "", candidate_claim_unit
                ).lower()
                if not any(phrase.lower() in candidate_lower for phrase in BLOCKED_CLAIMS):
                    continue
                claim_unit = mask_blocked_claim_inline_literals(claim_unit)
                claim_unit = "".join(
                    character
                    for character in html.unescape(claim_unit)
                    if unicodedata.category(character) != "Cf"
                )
                claim_unit = unescape_markdown_punctuation(claim_unit)
                claim_unit = re.sub(r"[*~`]+", "", claim_unit)
                claim_unit = re.sub(
                    r"(?<![A-Za-z0-9])_+|_+(?![A-Za-z0-9])",
                    "",
                    claim_unit,
                )
                boundary_claim_unit = claim_unit
                source_line = semantic_lines[line_no - 1] if line_no <= len(semantic_lines) else ""
                next_line = semantic_lines[line_no] if line_no < len(semantic_lines) else ""
                if "|" in source_line and re.match(
                    r"^\s*\|?\s*:?-{3,}", next_line
                ):
                    continue
            lowered = claim_unit.lower()
            for phrase in BLOCKED_CLAIMS:
                phrase_pattern = re.compile(rf"(?<![A-Za-z]){re.escape(phrase.lower())}(?![A-Za-z])")
                for match in phrase_pattern.finditer(lowered):
                    sentence_boundaries = [
                        punctuation.end()
                        for punctuation in re.finditer(r"[.!?;](?=\s|$)", lowered)
                    ]
                    sentence_start = max(
                        (boundary for boundary in sentence_boundaries if boundary <= match.start()),
                        default=0,
                    )
                    sentence_end = min(
                        (boundary for boundary in sentence_boundaries if boundary >= match.end()),
                        default=len(lowered),
                    )
                    context = lowered[sentence_start:sentence_end]
                    explicit_rejected = EXPLICIT_REJECTED_EXAMPLE_PREFIX.match(
                        claim_unit[sentence_start:sentence_end].lstrip()
                    )
                    structured_boundary = False
                    if is_markdown:
                        source_line = semantic_lines[line_no - 1] if line_no <= len(semantic_lines) else ""
                        if "|" in source_line:
                            cells = [cell.strip().lower() for cell in source_line.strip().strip("|").split("|")]
                            phrase_cells = [index for index, cell in enumerate(cells) if phrase.lower() in cell]
                            separator_index = line_no - 2
                            while separator_index >= 0 and semantic_lines[separator_index].strip():
                                separator = semantic_lines[separator_index]
                                if re.match(r"^\s*\|?\s*:?-{3,}", separator):
                                    header_index = separator_index - 1
                                    headers = (
                                        [cell.strip().lower() for cell in semantic_lines[header_index].strip().strip("|").split("|")]
                                        if header_index >= 0
                                        else []
                                    )
                                    structured_boundary = any(
                                        cell_index < len(headers)
                                        and contains_explicit_boundary_qualifier(
                                            headers[cell_index]
                                        )
                                        for cell_index in phrase_cells
                                    )
                                    break
                                separator_index -= 1
                            if not structured_boundary:
                                structured_boundary = any(
                                    contains_strong_boundary_status(cell)
                                    for cell in cells
                                )
                        if not structured_boundary and re.match(
                            r"^ {0,3}(?:[-+*]|\d{1,9}[.)])[ \t]+", source_line
                        ):
                            previous_index = line_no - 2
                            blank_lines = 0
                            while previous_index >= 0:
                                previous = semantic_lines[previous_index].strip()
                                if not previous:
                                    blank_lines += 1
                                    if blank_lines > 1:
                                        break
                                    previous_index -= 1
                                    continue
                                if previous and not re.match(
                                    r"^(?:[-+*]|\d{1,9}[.)])[ \t]+", previous
                                ):
                                    structured_boundary = contains_explicit_boundary_qualifier(
                                        previous.lower()
                                    )
                                    break
                                previous_index -= 1
                    legacy_machine_boundary = (
                        not is_markdown
                        and any(
                            marker in "\n".join(
                                lines[max(0, line_no - 15):min(len(lines), line_no + 5)]
                            ).lower()
                            for marker in BOUNDARY_WORDS
                        )
                    )
                    bounded_context = claim_has_bound_qualifier(
                        context,
                        match.start() - sentence_start,
                        match.end() - sentence_start,
                    )
                    if not explicit_rejected and not structured_boundary and not legacy_machine_boundary and not bounded_context:
                        fail(
                            f"{rel}:{line_no} uses blocked claim phrase without boundary context: {phrase}",
                            errors,
                        )


def normalize_markdown_link_text(line: str) -> str:
    """Reduce inline and reference links to their reviewer-visible label text."""
    output: list[str] = []
    cursor = 0
    while cursor < len(line):
        if line[cursor] != "[":
            output.append(line[cursor])
            cursor += 1
            continue

        label_start = cursor + 1
        label_end = label_start
        bracket_depth = 1
        while label_end < len(line) and bracket_depth:
            if line[label_end] == "\\":
                label_end += 2
                continue
            if line[label_end] == "[":
                bracket_depth += 1
            elif line[label_end] == "]":
                bracket_depth -= 1
            label_end += 1
        if bracket_depth:
            output.append(line[cursor])
            cursor += 1
            continue

        label = line[label_start:label_end - 1]
        after_label = label_end
        if after_label < len(line) and line[after_label] == "(":
            destination_end = after_label + 1
            parenthesis_depth = 1
            while destination_end < len(line) and parenthesis_depth:
                if line[destination_end] == "\\":
                    destination_end += 2
                    continue
                if line[destination_end] == "(":
                    parenthesis_depth += 1
                elif line[destination_end] == ")":
                    parenthesis_depth -= 1
                destination_end += 1
            if parenthesis_depth == 0 and valid_markdown_inline_link_target(
                line[after_label:destination_end]
            ):
                output.append(label)
                cursor = destination_end
                continue
        elif after_label < len(line) and line[after_label] == "[":
            reference_end = line.find("]", after_label + 1)
            if reference_end >= 0:
                output.append(label)
                cursor = reference_end + 1
                continue

        output.append(label)
        cursor = after_label
    return "".join(output)


def iter_reviewer_claim_units(lines: list[str]) -> list[tuple[int, str]]:
    """Join soft wraps while preserving visible Markdown block boundaries."""
    units: list[tuple[int, str]] = []
    current: list[str] = []
    start_line = 1
    current_quote_depth = 0
    current_list_indent: int | None = None

    def flush() -> None:
        nonlocal current, current_list_indent
        if current:
            units.append((start_line, " ".join(current)))
            current = []
            current_list_indent = None

    for line_no, line in enumerate(lines, start=1):
        if not line.strip():
            flush()
            continue

        visible_line = line.rstrip("\r\n")
        quote_depth = 0
        quote_marker = re.match(r"^ {0,3}>[ \t]?", visible_line)
        while quote_marker:
            quote_depth += 1
            visible_line = visible_line[quote_marker.end():]
            quote_marker = re.match(r"^ {0,3}>[ \t]?", visible_line)
        if not visible_line.strip():
            flush()
            continue
        leading_spaces = len(visible_line) - len(visible_line.lstrip(" "))
        list_marker = re.match(r"^ {0,3}(?:[-+*]|\d{1,9}[.)])[ \t]+", visible_line)
        standalone_structure = (
            (not list_marker and interrupts_markdown_paragraph(visible_line))
            or visible_line.startswith(("HTML_BODY ", "HTML_INLINE "))
            or bool(re.match(r"^ {0,3}\|.*\|[ \t]*$", visible_line))
        )

        starts_new_block = bool(
            current
            and (
                quote_depth != current_quote_depth
                or list_marker
                or standalone_structure
                or (
                    current_list_indent is not None
                    and leading_spaces < current_list_indent
                )
            )
        )
        if starts_new_block:
            flush()
        if not current:
            start_line = line_no
            current_quote_depth = quote_depth
        if list_marker:
            current_list_indent = len(list_marker.group(0).expandtabs(4))
            visible_line = visible_line[list_marker.end():]
        visible_fragment = visible_line.strip()
        trailing_backslashes = len(visible_fragment) - len(
            visible_fragment.rstrip("\\")
        )
        if trailing_backslashes % 2:
            visible_fragment = visible_fragment[:-1].rstrip()
        current.append(visible_fragment)
        if standalone_structure:
            flush()
    flush()
    return units


def check_semantic_authority_collapse(text_files: list[Path], errors: list[str]) -> None:
    """Reject unbounded authority promotion in reviewer-visible Markdown text."""
    for path in text_files:
        if path.suffix.lower() != ".md":
            continue
        rel = path.relative_to(ROOT).as_posix()
        semantic_lines = read_reviewer_semantic_text(path, errors).splitlines()
        for line_no, claim_unit in iter_reviewer_claim_units(semantic_lines):
            claim_unit = strip_markdown_inline_code_spans(claim_unit)
            claim_unit = normalize_markdown_link_text(claim_unit)
            decoded_claim = html.unescape(claim_unit)
            decoded_claim = "".join(
                character
                for character in decoded_claim
                if unicodedata.category(character) != "Cf"
            )
            visible_claim_line = normalize_markdown_link_text(decoded_claim)
            claim_line = re.sub(r"[*_~`]+", "", visible_claim_line)
            for label, pattern in AUTHORITY_COLLAPSE_PATTERNS:
                if not pattern.search(claim_line):
                    continue
                if not EXPLICIT_REJECTED_EXAMPLE_PREFIX.match(visible_claim_line):
                    fail(f"{rel}:{line_no} uses unbounded authority-collapse wording: {label}", errors)


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
    check_semantic_authority_collapse(text_files, errors)

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
