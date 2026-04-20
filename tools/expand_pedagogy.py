#!/usr/bin/env python3
"""Deterministic pedagogy expander for offshore-vault articles.

Scans an article body for acronyms and Norwegian terms already used
somewhere with their expansion/gloss (e.g., `BOP (Blowout Preventer)` or
`kranfører (crane operator)`), builds a mapping, and then inserts that
expansion/gloss after every bare occurrence elsewhere in the body.

This is the mechanical half of the every-use pedagogy rule (W-CON-03 and
W-CON-06). Running this post-content-agent and pre-review-agent drops the
acronym/Norwegian-term warning count to near zero without burning an LLM
turn on a task a regex can do reliably.

Scope carve-outs match the validator: headings, tables, code blocks,
HTML comments, the Sources section, and the Norwegian terminology
section are not expanded. Those are navigation, reference, or metadata,
not narrative prose.

Usage:
    python tools/expand_pedagogy.py <article_path> [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate import (  # noqa: E402
    _read_text, _write_text, load_article, FrontmatterMissingError,
    _FRONTMATTER_RE,
)


# ============================================================
# Regexes
# ============================================================

_ACRONYM_RE = re.compile(r"\b([A-Z]{2,8})(s?)\b")
_EXPANSION_AFTER = re.compile(r"\s*\([A-Za-zÀ-ÿ][^)]{0,250}\)")

# Acronym + (expansion) pair used to seed the mapping.
_ACRONYM_WITH_EXPANSION_RE = re.compile(
    r"\b([A-Z]{2,8})s?\s*\(([A-Za-zÀ-ÿ][^)]{1,250})\)"
)

_ACRONYM_FALSE_POSITIVES = {
    "I", "A", "B", "C", "D", "E", "F", "G", "H",
    "OK", "TV", "US", "UK", "EU",
}


# ============================================================
# Frozen ranges: parts of the body we do not touch
# ============================================================

def _compute_frozen_ranges(body: str) -> list[tuple[int, int]]:
    """Return (start, end) offsets of body regions that must not be expanded."""
    ranges: list[tuple[int, int]] = []
    patterns = [
        re.compile(r"```.*?```", re.DOTALL),        # fenced code blocks
        re.compile(r"`[^`]+`"),                     # inline code
        re.compile(r"^#{1,6}\s.*$", re.MULTILINE),  # headings
        re.compile(r"<!--.*?-->", re.DOTALL),       # HTML comments
        re.compile(r"^\s*\|.*$", re.MULTILINE),     # table rows
    ]
    for pat in patterns:
        for m in pat.finditer(body):
            ranges.append((m.start(), m.end()))

    # Sources section: heading + everything after
    sources_match = re.search(r"^##\s+Sources\b", body, re.MULTILINE)
    if sources_match:
        ranges.append((sources_match.start(), len(body)))

    # Norwegian terminology section: heading up to the next ## heading
    nt_match = re.search(r"^##\s+Norwegian terminology\b", body, re.MULTILINE)
    if nt_match:
        next_section = re.search(r"^##\s+\w", body[nt_match.end():], re.MULTILINE)
        if next_section:
            ranges.append((nt_match.start(), nt_match.end() + next_section.start()))
        else:
            ranges.append((nt_match.start(), len(body)))

    return ranges


def _in_frozen_range(pos: int, ranges: list[tuple[int, int]]) -> bool:
    for start, end in ranges:
        if start <= pos < end:
            return True
    return False


# ============================================================
# Acronym expansion
# ============================================================

def build_acronym_mapping(body: str, frozen: list[tuple[int, int]]) -> dict[str, str]:
    """Return acronym -> expansion, seeded from explicit uses in the body."""
    mapping: dict[str, str] = {}
    for m in _ACRONYM_WITH_EXPANSION_RE.finditer(body):
        if _in_frozen_range(m.start(), frozen):
            continue
        acronym = m.group(1)
        if acronym in _ACRONYM_FALSE_POSITIVES:
            continue
        expansion = m.group(2).strip()
        if acronym not in mapping:
            mapping[acronym] = expansion
    return mapping


def expand_acronyms(body: str, mapping: dict[str, str]) -> tuple[str, int]:
    """Return (new_body, count) with expansions inserted after bare occurrences."""
    if not mapping:
        return body, 0
    frozen = _compute_frozen_ranges(body)
    out: list[str] = []
    last = 0
    count = 0
    for m in _ACRONYM_RE.finditer(body):
        if _in_frozen_range(m.start(), frozen):
            continue
        acronym = m.group(1)
        if acronym in _ACRONYM_FALSE_POSITIVES:
            continue
        if acronym not in mapping:
            continue
        after = body[m.end():m.end() + 300]
        if _EXPANSION_AFTER.match(after):
            continue  # already expanded here
        out.append(body[last:m.end()])
        out.append(f" ({mapping[acronym]})")
        last = m.end()
        count += 1
    out.append(body[last:])
    return "".join(out), count


# ============================================================
# Norwegian term expansion
# ============================================================

def expand_norwegian_terms(body: str, norwegian_terms: list) -> tuple[str, int]:
    """Return (new_body, count) with English glosses inserted after bare Norwegian terms."""
    if not norwegian_terms:
        return body, 0

    mapping: dict[str, str] = {}
    for entry in norwegian_terms:
        if not isinstance(entry, dict):
            continue
        # YAML 1.1 parses unquoted `no:` as the boolean False; accept both.
        term = entry.get("no") or entry.get(False)
        en = entry.get("en")
        if not isinstance(term, str) or not isinstance(en, str):
            continue
        if not term or not en:
            continue
        mapping[term] = en

    if not mapping:
        return body, 0

    total = 0
    # Longer terms first, so a compound like "havbunnskompresjon" is
    # matched before a substring of it.
    for term in sorted(mapping.keys(), key=len, reverse=True):
        en = mapping[term]
        pat = re.compile(r"\b" + re.escape(term) + r"\b", re.IGNORECASE)
        # Recompute frozen ranges against the current (possibly modified) body.
        frozen = _compute_frozen_ranges(body)
        out: list[str] = []
        last = 0
        matches_this_round = 0
        for m in pat.finditer(body):
            if _in_frozen_range(m.start(), frozen):
                continue
            after = body[m.end():m.end() + 250]
            if _EXPANSION_AFTER.match(after):
                continue
            out.append(body[last:m.end()])
            out.append(f" ({en})")
            last = m.end()
            matches_this_round += 1
        if matches_this_round:
            out.append(body[last:])
            body = "".join(out)
            total += matches_this_round

    return body, total


# ============================================================
# CLI
# ============================================================

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="tools/expand_pedagogy.py",
        description="Deterministic pedagogy expander (acronyms + Norwegian terms).",
    )
    p.add_argument("article", help="path to the article (relative to vault or absolute)")
    p.add_argument("--dry-run", action="store_true", help="print counts, do not modify the file")
    args = p.parse_args(argv)

    vault = Path(__file__).resolve().parent.parent
    article_path = Path(args.article)
    if not article_path.is_absolute():
        article_path = (vault / article_path).resolve()

    if not article_path.is_file():
        print(f"error: article {article_path} does not exist", file=sys.stderr)
        return 2

    try:
        article = load_article(article_path, vault)
    except FrontmatterMissingError:
        print(f"error: no frontmatter in {article_path}", file=sys.stderr)
        return 2

    body = article.body
    frozen = _compute_frozen_ranges(body)
    mapping = build_acronym_mapping(body, frozen)

    new_body, acr_count = expand_acronyms(body, mapping)
    nts = article.frontmatter.get("norwegian_terms") or []
    newer_body, no_count = expand_norwegian_terms(new_body, nts)

    print(f"expand_pedagogy: {article.rel_path}")
    print(f"  acronyms mapped: {len(mapping)}")
    print(f"  acronym expansions inserted: {acr_count}")
    print(f"  norwegian expansions inserted: {no_count}")

    if args.dry_run:
        print("  dry-run: no file written")
        return 0

    if newer_body == body:
        print("  no changes needed")
        return 0

    # Rewrite file: keep frontmatter as-is, replace body.
    text = _read_text(article_path)
    m = _FRONTMATTER_RE.match(text)
    if not m:
        print(f"error: frontmatter regex failed on second read of {article_path}", file=sys.stderr)
        return 2
    new_text = m.group(0) + newer_body
    _write_text(article_path, new_text)
    print("  file updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
