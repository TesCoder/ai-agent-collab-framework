#!/usr/bin/env python3
"""
packetlint.py

Small, dependency-free linter for Work Packet markdown files.

Usage:
  python3 tools/packetlint.py path/to/work-packet.md
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ALLOWED_SCOPE_CLASSES = {"DOCS_ONLY", "VERIFICATION_ONLY", "CODE_CHANGE"}


@dataclass(frozen=True)
class Issue:
    line_no: int
    message: str


def _find_first_line_index(lines: list[str], predicate) -> int | None:
    for idx, line in enumerate(lines):
        if predicate(line):
            return idx
    return None


def lint_work_packet(md: str) -> list[Issue]:
    lines = md.splitlines()
    issues: list[Issue] = []

    # 1) Basic identity: at least one Work Packet heading style.
    has_heading = any(
        re.match(r"^(#{2,4})\s+Work Packet:", line)
        or re.match(r"^(#{4})\s+WORK PACKET\s+—\s+Agent\s+", line)
        for line in lines
    )
    if not has_heading:
        issues.append(
            Issue(
                1,
                "Missing Work Packet heading. Expected a heading like '## Work Packet: ...' or '#### WORK PACKET — Agent ...'.",
            )
        )

    # 2) Required fields.
    implementer_idx = _find_first_line_index(lines, lambda l: re.match(r"^\s*-\s*Implementer:\s*\S+", l))
    if implementer_idx is None:
        issues.append(Issue(1, "Missing required field: '- Implementer: <ID>'"))

    scope_idx = _find_first_line_index(lines, lambda l: re.match(r"^\s*-\s*Scope Class:\s*\S+", l))
    if scope_idx is None:
        issues.append(Issue(1, "Missing required field: '- Scope Class: <DOCS_ONLY|VERIFICATION_ONLY|CODE_CHANGE>'"))
    else:
        m = re.match(r"^\s*-\s*Scope Class:\s*(\S+)", lines[scope_idx])
        if m:
            scope = m.group(1).strip()
            if scope not in ALLOWED_SCOPE_CLASSES:
                issues.append(
                    Issue(
                        scope_idx + 1,
                        f"Invalid Scope Class '{scope}'. Allowed: {', '.join(sorted(ALLOWED_SCOPE_CLASSES))}.",
                    )
                )

    # 3) Blocking header must be exact if present.
    for idx, line in enumerate(lines):
        if "BLOCKING QUESTIONS" in line and line.strip() != "BLOCKING QUESTIONS — DO NOT PROCEED":
            issues.append(
                Issue(
                    idx + 1,
                    "If you use a blocking header, it must be exactly: 'BLOCKING QUESTIONS — DO NOT PROCEED'",
                )
            )

    # 4) Soft sanity: discourage copy/paste of repo-internal placeholders.
    placeholder_idx = _find_first_line_index(lines, lambda l: "<PROJECT_" in l or "<project-" in l)
    if placeholder_idx is not None:
        issues.append(
            Issue(
                placeholder_idx + 1,
                "Found template placeholder text (e.g., '<PROJECT_SLUG>'). Replace placeholders for real packets (ok in examples).",
            )
        )

    return issues


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Lint a Work Packet markdown file.")
    parser.add_argument("path", type=str, help="Path to a Work Packet markdown file.")
    args = parser.parse_args(argv)

    path = Path(args.path)
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    md = path.read_text(encoding="utf-8")
    issues = lint_work_packet(md)

    # Treat placeholder warning as non-fatal unless other issues exist.
    fatal = [i for i in issues if "placeholder" not in i.message.lower()]
    warnings = [i for i in issues if i not in fatal]

    for i in fatal:
        print(f"{path}:{i.line_no}: ERROR: {i.message}")
    for i in warnings:
        print(f"{path}:{i.line_no}: WARN: {i.message}")

    if fatal:
        return 1

    print(f"OK: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
