#!/usr/bin/env python3
"""Update the semantic version in the skill frontmatter."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


VERSION_RE = re.compile(r"(?m)^version:\s*(\d+)\.(\d+)\.(\d+)\s*$")


def level_from_message(message: str) -> str | None:
    text = message.strip()
    lowered = text.lower()
    if "[skip version]" in lowered:
        return None
    if "breaking change:" in lowered or re.search(r"^[a-z]+(?:\([^)]*\))?!:", lowered):
        return "major"
    if re.search(r"^feat(?:\([^)]*\))?:", lowered):
        return "minor"
    return "patch"


def bump(version: tuple[int, int, int], level: str) -> tuple[int, int, int]:
    major, minor, patch = version
    if level == "major":
        return major + 1, 0, 0
    if level == "minor":
        return major, minor + 1, 0
    return major, minor, patch + 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default="skills/customer-visit-register/SKILL.md")
    parser.add_argument("--level", choices=("auto", "major", "minor", "patch"), default="auto")
    parser.add_argument("--message", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    level = level_from_message(args.message) if args.level == "auto" else args.level
    path = Path(args.file)
    content = path.read_text(encoding="utf-8")
    match = VERSION_RE.search(content)
    if not match:
        raise SystemExit(f"version not found in {path}")

    current = tuple(map(int, match.groups()))
    if level is None:
        print("skipped")
        return 0

    next_version = bump(current, level)
    rendered = ".".join(map(str, next_version))
    if not args.dry_run:
        content = VERSION_RE.sub(f"version: {rendered}", content, count=1)
        path.write_text(content, encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
