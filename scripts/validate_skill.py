#!/usr/bin/env python3
"""Validate this skill's portable package, not the quality of agent conclusions."""
import argparse
import re
from pathlib import Path

import yaml


def validate_skill(root: Path) -> list[str]:
    root = Path(root).resolve()
    errors: list[str] = []

    def read(path: Path):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            errors.append(f"{path.relative_to(root)}: missing or unreadable UTF-8 file ({error})")
            return None
        if "\ufffd" in text:
            errors.append(f"{path.relative_to(root)}: contains Unicode replacement characters")
        return text

    def parse_mapping(text: str, label: str):
        try:
            value = yaml.safe_load(text)
        except yaml.YAMLError as error:
            errors.append(f"{label}: invalid YAML ({error})")
            return None
        if not isinstance(value, dict):
            errors.append(f"{label}: expected a YAML mapping")
            return None
        return value

    text = read(root / "SKILL.md")
    if text is None:
        return errors
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", text, re.DOTALL)
    if not match:
        return errors + ["SKILL.md: missing YAML frontmatter"]
    frontmatter = parse_mapping(match.group(1), "SKILL.md")
    if frontmatter is None:
        return errors
    name = frontmatter.get("name")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        errors.append("SKILL.md: name must be a lowercase hyphenated identifier of at most 64 characters")
    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        errors.append("SKILL.md: description must contain 1–1024 characters")
    if not text[match.end():].strip():
        errors.append("SKILL.md: instructions are empty")

    ui_text = read(root / "agents/openai.yaml")
    metadata = parse_mapping(ui_text, "agents/openai.yaml") if ui_text is not None else None
    if metadata is not None:
        interface = metadata.get("interface")
        if not isinstance(interface, dict):
            errors.append("agents/openai.yaml: interface must be a mapping")
        else:
            for key in ("display_name", "short_description", "default_prompt"):
                if not isinstance(interface.get(key), str) or not interface[key].strip():
                    errors.append(f"agents/openai.yaml: {key} must be a nonempty string")
            short = interface.get("short_description")
            if isinstance(short, str) and not 25 <= len(short) <= 64:
                errors.append("agents/openai.yaml: short_description must contain 25–64 characters")
            prompt = interface.get("default_prompt")
            if isinstance(name, str) and isinstance(prompt, str) and not re.search(
                rf"(?<![\w-])\${re.escape(name)}(?![\w-])", prompt
            ):
                errors.append(f"agents/openai.yaml: default_prompt must invoke ${name}")
        policy = metadata.get("policy", {})
        if not isinstance(policy, dict) or (
            "allow_implicit_invocation" in policy and not isinstance(policy["allow_implicit_invocation"], bool)
        ):
            errors.append("agents/openai.yaml: invocation policy must use a boolean")

    documents = [root / "SKILL.md", *sorted((root / "references").rglob("*.md"))]
    for document in documents:
        content = text if document.name == "SKILL.md" and document.parent == root else read(document)
        if content is None:
            continue
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
            target = target.strip().strip("<>")
            if target.startswith("#") or re.match(r"^[a-zA-Z][\w+.-]*:", target):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            resolved = (document.parent / target).resolve()
            if not resolved.is_relative_to(root) or not resolved.is_file():
                errors.append(f"{document.relative_to(root)}: missing or nonportable local reference {target}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    errors = validate_skill(args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Skill package valid: frontmatter, UTF-8 UI metadata, invocation and local references.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
