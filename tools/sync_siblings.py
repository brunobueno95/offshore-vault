#!/usr/bin/env python3
"""Populate the `siblings` field of every leaf article from folder neighbours.

For each folder under a tree root, collect the slugs of all leaf articles in
that folder (excluding `_INDEX.md` and any underscore-prefixed infrastructure
file), then write that sorted list back to each article's `siblings`
frontmatter field.

Usage:
    python tools/sync_siblings.py [vault_path]

Default vault path is the current directory.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

# Reuse constants from validate.py so the two stay in lock-step.
sys.path.insert(0, str(Path(__file__).parent))
from validate import (  # noqa: E402
    TREES,
    EXCLUDED_DIRS,
    RULE_FILE_NAMES,
    _FRONTMATTER_RE,
    DOMAIN_VALUES,
    _read_text,
    _write_text,
)


def main(argv: list[str] | None = None) -> int:
    vault = Path(argv[0] if argv else ".").resolve()
    if not vault.is_dir():
        print(f"error: {vault} is not a directory", file=sys.stderr)
        return 2

    touched = 0
    for tree in TREES:
        tree_root = vault / tree
        if not tree_root.is_dir():
            continue
        for folder in _iter_folders(tree_root):
            siblings = sorted(_collect_sibling_slugs(folder))
            for md in folder.glob("*.md"):
                if md.name in RULE_FILE_NAMES or md.name == "_INDEX.md":
                    continue
                if _update_siblings(md, siblings):
                    touched += 1
    print(f"sync_siblings: updated {touched} file(s)")
    return 0


def _iter_folders(root: Path):
    yield root
    for d in root.rglob("*"):
        if not d.is_dir():
            continue
        rel = d.relative_to(root)
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue
        if "_VIEWS" in rel.parts:
            continue
        yield d


def _collect_sibling_slugs(folder: Path) -> list[str]:
    out: list[str] = []
    for md in folder.glob("*.md"):
        if md.name in RULE_FILE_NAMES or md.name == "_INDEX.md":
            continue
        out.append(md.stem)
    return out


def _update_siblings(path: Path, siblings: list[str]) -> bool:
    text = _read_text(path)
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return False
    raw = m.group(1)
    try:
        fm = yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        return False
    if not isinstance(fm, dict):
        return False
    current = fm.get("siblings") or []
    if current == siblings:
        return False

    # Surgical rewrite of the siblings field, preserving field order elsewhere.
    new_value = _dump_list(siblings)
    pattern = re.compile(r"^siblings:\s*(\[\]|\[[^\]]*\]|\n(?:\s+-.*\n)*)", re.MULTILINE)
    if pattern.search(raw):
        new_raw = pattern.sub(f"siblings: {new_value}", raw, count=1)
    else:
        # Field not declared; append before closing --- so the validator picks it up next run.
        new_raw = raw.rstrip() + f"\nsiblings: {new_value}\n"
    new_block = f"---\n{new_raw}\n---\n"
    new_text = new_block + text[m.end():]
    _write_text(path, new_text)
    return True


def _dump_list(items: list[str]) -> str:
    if not items:
        return "[]"
    # Inline flow style keeps one-line frontmatter diffs clean.
    return "[" + ", ".join(f'"{s}"' for s in items) + "]"


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
