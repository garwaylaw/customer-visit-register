#!/usr/bin/env python3
"""Offline package checks; no network, installation, or business data writes."""
import json
import re
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    skill = root / "skills/customer-visit-register"
    errors = []
    entry = (skill / "SKILL.md").read_text(encoding="utf-8")
    if not entry.startswith("---\n"):
        errors.append("Missing frontmatter")
    if "name: customer-visit-register\n" not in entry:
        errors.append("Incorrect skill name")
    if not re.search(r"^description: .+", entry, re.M):
        errors.append("Missing description")
    roles = {
        "customer_name", "region", "cluster", "customer_type", "visit_date",
        "visit_type", "owner", "storefront_photo", "visit_history", "general_notes",
        "intention", "interested_products", "materials", "competitors",
    }
    fields = (skill / "references/fields.md").read_text(encoding="utf-8")
    actual = set(re.findall(r"^\| ([a-z_]+) \|", fields, re.M))
    if actual != roles:
        errors.append(f"Expected exactly 14 semantic roles; got {sorted(actual)}")
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix in {".md", ".yaml", ".json"}:
            text = path.read_text(encoding="utf-8")
            if re.search(r"/Users/|https?://docs\.qq\.com/smartsheet/\w+", text):
                errors.append(f"Potential private path/link: {path.relative_to(root)}")
            if "[TODO" in text:
                errors.append(f"Unfinished scaffold: {path.name}")
            if path.suffix == ".md":
                for link in re.findall(r"\]\(([^)]+)\)", text):
                    if "://" not in link and not link.startswith("#"):
                        if not (path.parent / link.split("#")[0]).exists():
                            errors.append(f"Broken link in {path.name}: {link}")
            if path.suffix == ".json":
                try:
                    json.loads(text)
                except ValueError as exc:
                    errors.append(f"Invalid JSON {path.name}: {exc}")
    profile = json.loads((skill / "references/profile.example.json").read_text(encoding="utf-8"))
    if not profile.get("example_only"):
        errors.append("Profile must be explicitly marked as an example")
    for binding in profile["bindings"]:
        if binding["role"] not in roles or binding["mapping_confirmed"]:
            errors.append("Invalid role or preconfirmed mapping in example")
    if not (root / "LICENSE").is_file():
        errors.append("Missing license")
    if errors:
        raise SystemExit("\n".join(errors))
    print("PASS: metadata, 14-role scope, local references, example JSON, private-path/link checks")
    print("Not tested: live platform access, approval enforcement, actual write behavior")


if __name__ == "__main__":
    main()
