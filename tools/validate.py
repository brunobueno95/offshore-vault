#!/usr/bin/env python3
"""offshore-vault validator.

Enforces the rules defined in `_VALIDATION.md` against every leaf article in
the four vault trees. Writes output files at vault root:

- `_UNRESOLVED_LINKS.md`    cross-tree link resolution report
- `_VALIDATION_REPORT.md`   human-readable findings summary
- `_VALIDATION_REPORT.json` same data, parseable
- `_TODO_QUEUE.md`          extracted TODO / AGENT / REVIEW comments
- `_MANIFEST.txt`            list of every markdown path in the vault

Also writes back computed `word_count` and `citation_density` into each
article's frontmatter in place.

Usage:
    python tools/validate.py [vault_path]

Vault path defaults to the current working directory. Exit codes:
    0  no errors (warnings may exist)
    1  one or more errors
    2  validator itself encountered a fatal error
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable

import yaml


# Windows MAX_PATH is 260 by default; some vault paths exceed it. Use the
# `\\?\` prefix to bypass the limit on any Windows host regardless of the
# LongPathsEnabled registry setting.

def _long_path(path: Path) -> str:
    s = str(path.resolve())
    if os.name == "nt" and not s.startswith("\\\\?\\"):
        s = "\\\\?\\" + s
    return s


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError):
        if os.name == "nt":
            with open(_long_path(path), "r", encoding="utf-8") as f:
                return f.read()
        raise


def _write_text(path: Path, content: str) -> None:
    try:
        path.write_text(content, encoding="utf-8")
    except (FileNotFoundError, OSError):
        if os.name == "nt":
            with open(_long_path(path), "w", encoding="utf-8") as f:
                f.write(content)
            return
        raise


# ==========================================================================
# Controlled vocabulary (mirror of `_CONTROLLED_VOCABULARY.md`)
# ==========================================================================

SCHEMA_VERSION = "1.0"

TREES: tuple[str, ...] = (
    "drilling",
    "crane-and-logistics",
    "subsea",
    "emergency-response",
)

TYPE_VALUES = {
    "concept", "equipment", "procedure", "incident",
    "standard", "role", "view", "tool",
}
STATUS_VALUES = {"draft", "review", "published", "archived"}
DOMAIN_VALUES = set(TREES)
DEPTH_VALUES = {"foundational", "operational", "advanced"}
LIFE_CYCLE_VALUES = {
    "exploration", "drilling", "completion", "production",
    "intervention", "suspension", "p-and-a", "decommissioning",
}
ACCESS_VALUES = {"open", "paywalled", "restricted"}

REQUIRED_FIELDS = {
    "schema_version", "id", "title", "slug", "type", "status",
    "domain", "folder", "ncs_specific", "created", "updated",
}

ALL_KNOWN_FIELDS = {
    "schema_version",
    "id", "title", "title_no", "slug", "type", "status",
    "domain", "folder", "parents", "siblings",
    "topics", "life_cycle_phases", "depth", "perspective",
    "authoritative_sources", "reference_textbooks", "related_incidents",
    "related", "cross_domain",
    "relevant_to_roles",
    "ncs_specific", "norwegian_terms",
    "authors", "created", "updated", "review_due", "tags",
    "citation_density", "word_count",
}

AUTHORITATIVE_SOURCE_REQUIRED = {
    "id", "title", "publisher", "year",
    "access", "verified_date", "verified_by",
}

DEPTH_WORD_COUNT_MIN = {
    "foundational": 800,
    "operational": 1500,
    "advanced": 3000,
}
DEPTH_CITATION_DENSITY_MIN = {
    # citations per 100 words
    "foundational": 0.67,
    "operational": 1.00,
    "advanced": 1.33,
}

# Reserved infrastructure files that are not leaf articles. Filename check.
RULE_FILE_NAMES = {
    "CLAUDE.md", "_SCHEMA.md", "_SCHEMA_VERSION.md",
    "_CONTROLLED_VOCABULARY.md", "_PATH_CONVENTIONS.md",
    "_AGENT_RULES.md", "_VALIDATION.md",
    "_UNRESOLVED_LINKS.md", "_VALIDATION_REPORT.md",
    "_TODO_QUEUE.md", "_MANIFEST.txt",
    "_PIPELINE_REPORT.md", "_CROSS_TREE_FINDINGS.md",
    "_TOPICS.md", "_VERIFICATION_FINDINGS.md",
    "_URGENT_QUEUE.md", "_LINK_REPAIR_PROPOSALS.md",
    "_TOPIC_PROPOSALS.md",
}

# Directories to skip when walking the vault.
EXCLUDED_DIRS = {
    ".git", ".github", ".claude", "tools",
    "node_modules", "__pycache__", ".pytest_cache",
    "_VIEWS",  # reserved cross-cutting index folders, separate schema
}


# ==========================================================================
# Data model
# ==========================================================================

@dataclass
class Article:
    path: Path
    rel_path: str
    tree: str
    frontmatter: dict
    frontmatter_raw: str
    body: str
    raw_text: str
    word_count: int = 0
    citation_count: int = 0
    citation_density: float = 0.0
    was_modified: bool = False


@dataclass
class Finding:
    rule_id: str
    severity: str  # error | warning | info
    path: str
    detail: str
    field_name: str | None = None


@dataclass
class LinkEdge:
    source: str
    target: str
    field_name: str
    resolution: str  # RESOLVED | BROKEN-NO-MATCH | BROKEN-FUZZY-MATCH | AMBIGUOUS
    candidate: str | None = None


class FrontmatterMissingError(Exception):
    """Raised when a file lacks the `---\\n...\\n---\\n` frontmatter block."""


# ==========================================================================
# Entry point
# ==========================================================================

def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    vault = Path(args.vault).resolve()
    if not vault.is_dir():
        print(f"error: vault path {vault} is not a directory", file=sys.stderr)
        return 2

    findings: list[Finding] = []
    articles: list[Article] = []
    index_paths: list[Path] = []

    # Stage 1: discover and parse
    for md_path in iter_markdown_files(vault):
        name = md_path.name
        if name == "_INDEX.md":
            index_paths.append(md_path)
            continue
        if name in RULE_FILE_NAMES:
            continue
        rel = md_path.relative_to(vault).as_posix()
        # Only validate files inside a known tree
        tree = rel.split("/", 1)[0]
        if tree not in DOMAIN_VALUES:
            continue
        try:
            article = load_article(md_path, vault)
        except FrontmatterMissingError:
            findings.append(Finding(
                "E-SCH-01", "error", rel,
                "frontmatter block missing or incomplete",
            ))
            continue
        except yaml.YAMLError as exc:
            findings.append(Finding(
                "E-SCH-01", "error", rel,
                f"malformed YAML frontmatter: {exc}",
            ))
            continue
        articles.append(article)

    if not args.quiet:
        print(f"validate: scanned {len(articles)} articles, {len(index_paths)} folder indexes")

    # Stage 2: per-article checks
    for a in articles:
        findings.extend(check_schema(a))
        findings.extend(check_identity(a))
        findings.extend(check_path(a))
        findings.extend(check_body_structure(a))
        findings.extend(check_ncs(a))
        findings.extend(check_freshness(a))
        compute_derived_fields(a)
        findings.extend(check_acronyms_every_use(a))
        findings.extend(check_norwegian_terms_every_use(a))

    # Stage 3: global checks
    findings.extend(check_id_uniqueness(articles))
    findings.extend(check_folder_indexes_present(vault, index_paths))
    edges = build_link_graph(articles, vault, index_paths)
    findings.extend(check_relationship_integrity(articles, edges))
    findings.extend(check_publication_gates(articles))

    # Stage 4: writeback derived fields
    for a in articles:
        if a.was_modified:
            write_article_derived_fields(a)

    # Stage 5: output files
    write_unresolved_links(vault, edges)
    write_validation_report(vault, findings, articles)
    write_todo_queue(vault, articles)
    write_manifest(vault)

    # Stage 6: exit code
    errors = [f for f in findings if f.severity == "error"]
    if not args.quiet:
        warns = sum(1 for f in findings if f.severity == "warning")
        infos = sum(1 for f in findings if f.severity == "info")
        print(f"validate: {len(errors)} error(s), {warns} warning(s), {infos} info")
    if errors and not args.warn_only:
        return 1
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="tools/validate.py",
        description="Validate an offshore-vault repository.",
    )
    p.add_argument(
        "vault", nargs="?", default=".",
        help="path to the vault root (default: current directory)",
    )
    p.add_argument(
        "--warn-only", action="store_true",
        help="always exit 0, even on error-level findings",
    )
    p.add_argument(
        "--quiet", action="store_true",
        help="suppress progress output",
    )
    return p.parse_args(argv)


# ==========================================================================
# File discovery and parsing
# ==========================================================================

def iter_markdown_files(vault: Path) -> Iterable[Path]:
    """Yield every `.md` file under `vault`, skipping infrastructure dirs."""
    for md in vault.rglob("*.md"):
        rel = md.relative_to(vault)
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue
        yield md


_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def load_article(path: Path, vault: Path) -> Article:
    text = _read_text(path)
    m = _FRONTMATTER_RE.match(text)
    if not m:
        raise FrontmatterMissingError()
    raw_yaml = m.group(1)
    fm = yaml.safe_load(raw_yaml)
    if not isinstance(fm, dict):
        raise yaml.YAMLError("frontmatter is not a YAML mapping")
    body = text[m.end():]
    rel = path.relative_to(vault).as_posix()
    tree = rel.split("/", 1)[0]
    return Article(
        path=path,
        rel_path=rel,
        tree=tree,
        frontmatter=fm,
        frontmatter_raw=raw_yaml,
        body=body,
        raw_text=text,
    )


# ==========================================================================
# Rule checks
# ==========================================================================

# -- Schema (E-SCH-*) ------------------------------------------------------

def check_schema(a: Article) -> list[Finding]:
    out: list[Finding] = []
    fm = a.frontmatter
    rel = a.rel_path

    # E-SCH-02
    sv = fm.get("schema_version")
    if sv is None:
        out.append(Finding("E-SCH-02", "error", rel, "schema_version missing"))
    elif str(sv) != SCHEMA_VERSION:
        out.append(Finding(
            "E-SCH-02", "error", rel,
            f"schema_version is {sv!r}, expected {SCHEMA_VERSION!r}",
        ))

    # E-SCH-03
    for fname in REQUIRED_FIELDS:
        if fname not in fm:
            out.append(Finding(
                "E-SCH-03", "error", rel,
                f"required field {fname!r} missing",
                field_name=fname,
            ))

    # E-SCH-04: wrong types for list fields
    list_fields = (
        "parents", "siblings", "topics", "life_cycle_phases", "perspective",
        "authoritative_sources", "reference_textbooks", "related_incidents",
        "related", "cross_domain", "relevant_to_roles", "norwegian_terms",
        "authors", "tags",
    )
    for fname in list_fields:
        v = fm.get(fname)
        if v is not None and not isinstance(v, list):
            out.append(Finding(
                "E-SCH-04", "error", rel,
                f"field {fname!r} must be a list, got {type(v).__name__}",
                field_name=fname,
            ))

    if "ncs_specific" in fm and fm["ncs_specific"] is not None and not isinstance(fm["ncs_specific"], bool):
        out.append(Finding(
            "E-SCH-04", "error", rel,
            f"field 'ncs_specific' must be a boolean, got {type(fm['ncs_specific']).__name__}",
            field_name="ncs_specific",
        ))

    # E-SCH-05: enum values
    enum_checks = (
        ("type", TYPE_VALUES),
        ("status", STATUS_VALUES),
        ("domain", DOMAIN_VALUES),
    )
    for fname, allowed in enum_checks:
        v = fm.get(fname)
        if v is not None and v != "" and v not in allowed:
            out.append(Finding(
                "E-SCH-05", "error", rel,
                f"{fname} is {v!r}, not in allowed set {sorted(allowed)}",
                field_name=fname,
            ))
    # depth is enum but may be null on draft
    depth = fm.get("depth")
    if depth not in (None, "") and depth not in DEPTH_VALUES:
        out.append(Finding(
            "E-SCH-05", "error", rel,
            f"depth is {depth!r}, not in allowed set {sorted(DEPTH_VALUES)}",
            field_name="depth",
        ))
    lcp = fm.get("life_cycle_phases") or []
    if isinstance(lcp, list):
        for v in lcp:
            if v not in LIFE_CYCLE_VALUES:
                out.append(Finding(
                    "E-SCH-05", "error", rel,
                    f"life_cycle_phases value {v!r} not in allowed set",
                    field_name="life_cycle_phases",
                ))

    # E-SCH-06: unknown fields
    for fname in fm:
        if fname not in ALL_KNOWN_FIELDS:
            out.append(Finding(
                "E-SCH-06", "error", rel,
                f"unknown field {fname!r} (not in _SCHEMA.md)",
                field_name=fname,
            ))

    # E-SCH-07: authoritative_sources sub-fields
    srcs = fm.get("authoritative_sources") or []
    if isinstance(srcs, list):
        for i, src in enumerate(srcs):
            if not isinstance(src, dict):
                out.append(Finding(
                    "E-SCH-04", "error", rel,
                    f"authoritative_sources[{i}] must be an object",
                ))
                continue
            for req in AUTHORITATIVE_SOURCE_REQUIRED:
                if req not in src:
                    out.append(Finding(
                        "E-SCH-07", "error", rel,
                        f"authoritative_sources[{i}].{req} missing",
                    ))
            if "access" in src and src["access"] not in ACCESS_VALUES:
                out.append(Finding(
                    "E-SCH-05", "error", rel,
                    f"authoritative_sources[{i}].access is {src['access']!r}, not in allowed set",
                ))

    return out


# -- Identity and path (E-ID-*, E-PATH-*) ----------------------------------

def check_identity(a: Article) -> list[Finding]:
    out: list[Finding] = []
    fm = a.frontmatter
    rel = a.rel_path
    parts = rel.split("/")

    # E-ID-02: slug matches filename
    slug = fm.get("slug")
    stem = a.path.stem
    if slug and slug != stem:
        out.append(Finding(
            "E-ID-02", "error", rel,
            f"slug {slug!r} does not match filename stem {stem!r}",
            field_name="slug",
        ))

    # E-ID-03: domain matches tree
    domain = fm.get("domain")
    if domain and domain != a.tree:
        out.append(Finding(
            "E-ID-03", "error", rel,
            f"domain {domain!r} does not match tree {a.tree!r}",
            field_name="domain",
        ))

    # E-ID-04: folder matches actual folder path (relative to tree root)
    declared = fm.get("folder")
    if declared is not None:
        actual = "/".join(parts[1:-1]) if len(parts) > 2 else ""
        if str(declared).strip("/") != actual:
            out.append(Finding(
                "E-ID-04", "error", rel,
                f"folder {declared!r} does not match actual path {actual!r}",
                field_name="folder",
            ))
    return out


_FILENAME_ALLOWED = re.compile(r"^[a-z0-9][a-z0-9\-]*\.md$")
_FOLDER_ALLOWED = re.compile(r"^[a-z0-9][a-z0-9\-]*$")


def check_path(a: Article) -> list[Finding]:
    out: list[Finding] = []
    rel = a.rel_path
    parts = rel.split("/")
    fname = parts[-1]
    if not _FILENAME_ALLOWED.match(fname):
        out.append(Finding(
            "E-PATH-01", "error", rel,
            f"filename {fname!r} contains disallowed characters",
        ))
    for folder in parts[:-1]:
        if not _FOLDER_ALLOWED.match(folder):
            out.append(Finding(
                "E-PATH-02", "error", rel,
                f"folder segment {folder!r} contains disallowed characters",
            ))
    return out


# -- Body structure and content (W-CON-*, W-NCS-*) -------------------------

_EM_DASH = "\u2014"
_CODE_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)
_INLINE_CODE_RE = re.compile(r"`[^`]+`")


def _strip_code(text: str) -> str:
    text = _CODE_BLOCK_RE.sub("", text)
    text = _INLINE_CODE_RE.sub("", text)
    return text


def _is_placeholder(body: str) -> bool:
    return "CONTENT PLACEHOLDER" in body


def check_body_structure(a: Article) -> list[Finding]:
    out: list[Finding] = []
    body = a.body
    rel = a.rel_path
    placeholder = _is_placeholder(body)
    body_stripped = _strip_code(body)

    # W-CON-02: em dashes
    if _EM_DASH in body_stripped:
        count = body_stripped.count(_EM_DASH)
        out.append(Finding(
            "W-CON-02", "warning", rel,
            f"body contains {count} em dash character(s) (U+2014)",
        ))

    if placeholder:
        return out

    # W-CON-01: required sections
    has_overview = re.search(r"^##\s+Overview\b", body, re.MULTILINE) is not None
    has_details = re.search(r"^##\s+Details\b", body, re.MULTILINE) is not None
    has_sources = re.search(r"^##\s+Sources\b", body, re.MULTILINE) is not None
    missing = []
    if not has_overview:
        missing.append("## Overview")
    if not has_details:
        missing.append("## Details")
    if not has_sources:
        missing.append("## Sources")
    if missing:
        out.append(Finding(
            "W-CON-01", "warning", rel,
            f"body missing required section(s): {', '.join(missing)}",
        ))

    # W-CON-04: paragraph length
    for para in _split_paragraphs(body_stripped):
        words = len(para.split())
        if words > 200:
            out.append(Finding(
                "W-CON-04", "warning", rel,
                f"paragraph exceeds 200 words ({words})",
            ))
            break  # one warning per article is enough for readability signal

    # W-CON-05: raw URLs outside ## Sources
    sources_split = re.split(r"^##\s+Sources\b", body_stripped, maxsplit=1, flags=re.MULTILINE)
    pre = sources_split[0]
    cleaned = re.sub(r"\[[^\]]*\]\(https?://[^)]+\)", "", pre)
    raw_urls = re.findall(r"https?://[^\s)\"'>]+", cleaned)
    if raw_urls:
        out.append(Finding(
            "W-CON-05", "warning", rel,
            f"body contains {len(raw_urls)} raw URL(s) outside ## Sources",
        ))
    return out


def _split_paragraphs(text: str) -> list[str]:
    return [
        p.strip() for p in re.split(r"\n\s*\n", text)
        if p.strip() and not p.strip().startswith(("#", "|", "-", "*", ">"))
    ]


def check_ncs(a: Article) -> list[Finding]:
    out: list[Finding] = []
    fm = a.frontmatter
    if fm.get("ncs_specific") is not True:
        return out
    if _is_placeholder(a.body):
        return out
    rel = a.rel_path
    has_ncs = re.search(r"^##\s+NCS-specific context\b", a.body, re.MULTILINE) is not None
    if not has_ncs:
        out.append(Finding(
            "W-NCS-01", "warning", rel,
            "ncs_specific is true but no '## NCS-specific context' section",
        ))
    nt = fm.get("norwegian_terms") or []
    if not nt:
        out.append(Finding(
            "W-NCS-02", "warning", rel,
            "ncs_specific is true but norwegian_terms is empty",
        ))
    return out


# -- Acronyms (W-CON-03) and Norwegian terms (W-CON-06) -------------------

_ACRONYM_RE = re.compile(r"\b([A-Z]{2,8})s?\b")
_ACRONYM_FALSE_POSITIVES = {
    "I", "A", "B", "C", "D", "E", "F", "G", "H",
    "OK", "TV", "US", "UK", "EU",
}
_EXPANSION_AFTER = re.compile(r"\s*\([A-Za-zÀ-ÿ][^)]{0,250}\)")


def check_acronyms_every_use(a: Article) -> list[Finding]:
    out: list[Finding] = []
    body = a.body
    if _is_placeholder(body):
        return out
    stripped = _strip_code(body)
    sources_split = re.split(r"^##\s+Sources\b", stripped, maxsplit=1, flags=re.MULTILINE)
    pre = sources_split[0]
    bare = 0
    for m in _ACRONYM_RE.finditer(pre):
        acronym = m.group(1)
        if acronym in _ACRONYM_FALSE_POSITIVES:
            continue
        end = m.end()
        remainder = pre[end:end + 300]
        if not _EXPANSION_AFTER.match(remainder):
            bare += 1
    if bare > 0:
        out.append(Finding(
            "W-CON-03", "warning", a.rel_path,
            f"{bare} bare acronym occurrence(s) not followed by parenthetical expansion",
        ))
    return out


def check_norwegian_terms_every_use(a: Article) -> list[Finding]:
    out: list[Finding] = []
    body = a.body
    if _is_placeholder(body):
        return out
    nts = a.frontmatter.get("norwegian_terms") or []
    if not isinstance(nts, list) or not nts:
        return out
    stripped = _strip_code(body)
    # Exclude the terminology section and the Sources section
    for header in (r"^##\s+Norwegian terminology\b", r"^##\s+Sources\b"):
        split = re.split(header, stripped, maxsplit=1, flags=re.MULTILINE)
        stripped = split[0]
    bare = 0
    for entry in nts:
        if not isinstance(entry, dict):
            continue
        # YAML 1.1 parses an unquoted `no:` key as the boolean False.
        # Accept both the intended `"no"` string key and the False fallback.
        term = entry.get("no") or entry.get(False)
        if not term or not isinstance(term, str):
            continue
        pattern = r"\b" + re.escape(term) + r"\b"
        for m in re.finditer(pattern, stripped, flags=re.IGNORECASE):
            end = m.end()
            remainder = stripped[end:end + 250]
            if not _EXPANSION_AFTER.match(remainder):
                bare += 1
    if bare > 0:
        out.append(Finding(
            "W-CON-06", "warning", a.rel_path,
            f"{bare} bare Norwegian-term occurrence(s) without inline English translation",
        ))
    return out


# -- Freshness (W-FRESH-*) -------------------------------------------------

def check_freshness(a: Article) -> list[Finding]:
    out: list[Finding] = []
    today = date.today()
    srcs = a.frontmatter.get("authoritative_sources") or []
    if not isinstance(srcs, list):
        return out
    for i, src in enumerate(srcs):
        if not isinstance(src, dict):
            continue
        vd = src.get("verified_date")
        if not vd:
            continue
        try:
            vd_date = vd if isinstance(vd, date) else date.fromisoformat(str(vd))
        except (ValueError, TypeError):
            continue
        if today - vd_date > timedelta(days=365):
            out.append(Finding(
                "W-FRESH-01", "warning", a.rel_path,
                f"authoritative_sources[{i}].verified_date {vd_date} older than 365 days",
            ))
    return out


# -- Derived fields: word_count, citation_density -------------------------

_CITATION_RE = re.compile(r"\(([a-z0-9][a-z0-9\-]+)(?:\s*,\s*[^)]+)?\)")


def compute_derived_fields(a: Article) -> None:
    body = a.body
    if _is_placeholder(body):
        return
    stripped = _strip_code(body)
    text_only = re.sub(r"[#*_`\[\]>]", " ", stripped)
    words = [w for w in text_only.split() if any(c.isalnum() for c in w)]
    wc = len(words)
    a.word_count = wc

    source_ids: set[str] = set()
    srcs = a.frontmatter.get("authoritative_sources") or []
    if isinstance(srcs, list):
        for src in srcs:
            if isinstance(src, dict) and src.get("id"):
                source_ids.add(str(src["id"]))
    citations = 0
    for m in _CITATION_RE.finditer(stripped):
        if m.group(1) in source_ids:
            citations += 1
    a.citation_count = citations
    a.citation_density = (citations / wc * 100) if wc > 0 else 0.0

    fm_wc = a.frontmatter.get("word_count")
    fm_cd = a.frontmatter.get("citation_density")
    if fm_wc != wc or fm_cd is None or abs((fm_cd or 0) - a.citation_density) > 0.01:
        a.was_modified = True


def write_article_derived_fields(a: Article) -> None:
    text = a.raw_text
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return
    fm_block = m.group(0)
    new_block = fm_block
    wc_str = str(a.word_count)
    cd_str = f"{a.citation_density:.2f}"
    if re.search(r"^word_count:\s*.*$", new_block, re.MULTILINE):
        new_block = re.sub(
            r"^word_count:\s*.*$",
            f"word_count: {wc_str}",
            new_block, flags=re.MULTILINE,
        )
    if re.search(r"^citation_density:\s*.*$", new_block, re.MULTILINE):
        new_block = re.sub(
            r"^citation_density:\s*.*$",
            f"citation_density: {cd_str}",
            new_block, flags=re.MULTILINE,
        )
    if new_block != fm_block:
        new_text = new_block + text[m.end():]
        _write_text(a.path, new_text)
        a.raw_text = new_text


# -- Global checks ---------------------------------------------------------

def check_id_uniqueness(articles: list[Article]) -> list[Finding]:
    out: list[Finding] = []
    seen: dict[str, str] = {}
    for a in articles:
        aid = a.frontmatter.get("id")
        if not aid:
            continue
        if aid in seen:
            out.append(Finding(
                "E-ID-01", "error", a.rel_path,
                f"id {aid!r} already used by {seen[aid]}",
            ))
        else:
            seen[aid] = a.rel_path
    return out


def check_folder_indexes_present(vault: Path, index_paths: list[Path]) -> list[Finding]:
    out: list[Finding] = []
    index_dirs = {p.parent for p in index_paths}
    for tree in TREES:
        tree_root = vault / tree
        if not tree_root.is_dir():
            continue
        for d in tree_root.rglob("*"):
            if not d.is_dir():
                continue
            rel_parts = d.relative_to(vault).parts
            if "_VIEWS" in rel_parts:
                continue
            if d not in index_dirs:
                out.append(Finding(
                    "E-PATH-03", "error",
                    d.relative_to(vault).as_posix(),
                    "folder missing _INDEX.md",
                ))
    return out


def build_link_graph(articles: list[Article], vault: Path, index_paths: list[Path]) -> list[LinkEdge]:
    out: list[LinkEdge] = []
    paths = {a.rel_path for a in articles}
    for p in index_paths:
        paths.add(p.relative_to(vault).as_posix())

    for a in articles:
        for field_name in ("related", "cross_domain", "parents"):
            targets = a.frontmatter.get(field_name) or []
            if not isinstance(targets, list):
                continue
            for target in targets:
                if not isinstance(target, str) or not target.strip():
                    continue
                t = target.strip().lstrip("/")
                t_md = t if t.endswith(".md") else t + ".md"
                if t_md in paths:
                    out.append(LinkEdge(
                        source=a.rel_path, target=target,
                        field_name=field_name, resolution="RESOLVED",
                    ))
                    continue
                candidate = _fuzzy_find(t_md, paths)
                if candidate:
                    out.append(LinkEdge(
                        source=a.rel_path, target=target,
                        field_name=field_name,
                        resolution="BROKEN-FUZZY-MATCH", candidate=candidate,
                    ))
                else:
                    out.append(LinkEdge(
                        source=a.rel_path, target=target,
                        field_name=field_name,
                        resolution="BROKEN-NO-MATCH",
                    ))
    return out


def _fuzzy_find(target: str, paths: set[str]) -> str | None:
    parts = target.split("/")
    if not parts:
        return None
    slug = parts[-1]
    tree = parts[0] if parts[0] in DOMAIN_VALUES else None
    candidates = [
        p for p in paths
        if (not tree or p.startswith(tree + "/")) and p.endswith("/" + slug)
    ]
    if len(candidates) == 1:
        return candidates[0]
    return None


def check_relationship_integrity(articles: list[Article], edges: list[LinkEdge]) -> list[Finding]:
    out: list[Finding] = []
    for e in edges:
        if e.resolution == "RESOLVED":
            continue
        if e.field_name == "related":
            out.append(Finding(
                "E-REL-01", "error", e.source,
                f"related path {e.target!r} does not resolve",
            ))
        elif e.field_name == "cross_domain":
            msg = f"cross_domain path {e.target!r} does not resolve"
            if e.candidate:
                msg += f" (closest match: {e.candidate})"
            out.append(Finding("W-REL-01", "warning", e.source, msg))
        elif e.field_name == "parents":
            out.append(Finding(
                "W-REL-03", "warning", e.source,
                f"parents path {e.target!r} does not resolve",
            ))
    return out


def check_publication_gates(articles: list[Article]) -> list[Finding]:
    out: list[Finding] = []
    for a in articles:
        fm = a.frontmatter
        if fm.get("status") != "published":
            continue
        rel = a.rel_path
        if fm.get("type") in (None, ""):
            out.append(Finding("P-PUB-02", "error", rel, "type required for status: published"))
        if fm.get("depth") in (None, ""):
            out.append(Finding("P-PUB-02", "error", rel, "depth required for status: published"))
        srcs = fm.get("authoritative_sources") or []
        if not srcs:
            out.append(Finding("P-PUB-03", "error", rel, "authoritative_sources empty; required for status: published"))
        depth = fm.get("depth")
        if depth in DEPTH_WORD_COUNT_MIN:
            min_wc = DEPTH_WORD_COUNT_MIN[depth]
            if a.word_count < min_wc:
                out.append(Finding(
                    "P-PUB-04", "error", rel,
                    f"word_count {a.word_count} below minimum {min_wc} for depth {depth!r}",
                ))
            if a.citation_density < DEPTH_CITATION_DENSITY_MIN[depth]:
                out.append(Finding(
                    "P-PUB-05", "error", rel,
                    f"citation_density {a.citation_density:.2f} below minimum "
                    f"{DEPTH_CITATION_DENSITY_MIN[depth]} for depth {depth!r}",
                ))
    return out


# ==========================================================================
# Output writers
# ==========================================================================

def write_unresolved_links(vault: Path, edges: list[LinkEdge]) -> None:
    path = vault / "_UNRESOLVED_LINKS.md"
    lines = [
        "# _UNRESOLVED_LINKS.md",
        "",
        "**Auto-generated by `tools/validate.py`. Do not edit manually.**",
        "",
    ]
    broken = [e for e in edges if e.resolution.startswith("BROKEN")]
    ambiguous = [e for e in edges if e.resolution == "AMBIGUOUS"]
    if not broken and not ambiguous:
        lines.append("No unresolved links at this time.")
    else:
        if broken:
            lines.append(f"## Broken links ({len(broken)})")
            lines.append("")
            for e in broken:
                lines.append(f"### {e.target}")
                lines.append(f"- From: `{e.source}` ({e.field_name})")
                lines.append(f"- Status: {e.resolution}")
                if e.candidate:
                    lines.append(f"- Closest candidate: `{e.candidate}`")
                lines.append("")
    _write_text(path, "\n".join(lines) + "\n")


def write_validation_report(vault: Path, findings: list[Finding], articles: list[Article]) -> None:
    path = vault / "_VALIDATION_REPORT.md"
    errors = [f for f in findings if f.severity == "error"]
    warnings = [f for f in findings if f.severity == "warning"]
    infos = [f for f in findings if f.severity == "info"]
    lines = [
        "# _VALIDATION_REPORT.md",
        "",
        "**Auto-generated by `tools/validate.py`. Do not edit manually.**",
        "",
        "## Summary",
        "",
        f"- Articles scanned: {len(articles)}",
        f"- Errors: {len(errors)}",
        f"- Warnings: {len(warnings)}",
        f"- Info: {len(infos)}",
        "",
    ]

    def _group(subset: list[Finding]) -> list[tuple[str, list[Finding]]]:
        g: dict[str, list[Finding]] = {}
        for f in subset:
            g.setdefault(f.rule_id, []).append(f)
        return sorted(g.items())

    for label, subset, cap in (
        ("Errors", errors, 100),
        ("Warnings", warnings, 50),
        ("Info", infos, 20),
    ):
        if not subset:
            continue
        lines.append(f"## {label}")
        lines.append("")
        for rule_id, items in _group(subset):
            lines.append(f"### {rule_id} ({len(items)})")
            for f in items[:cap]:
                lines.append(f"- `{f.path}`: {f.detail}")
            if len(items) > cap:
                lines.append(f"- ... {len(items) - cap} more not shown")
            lines.append("")

    _write_text(path, "\n".join(lines) + "\n")

    json_path = vault / "_VALIDATION_REPORT.json"
    data = {
        "summary": {
            "articles": len(articles),
            "errors": len(errors),
            "warnings": len(warnings),
            "info": len(infos),
        },
        "findings": [
            {
                "rule_id": f.rule_id,
                "severity": f.severity,
                "path": f.path,
                "detail": f.detail,
                "field": f.field_name,
            }
            for f in findings
        ],
    }
    _write_text(json_path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


_TODO_RE = re.compile(r"<!--\s*(TODO|AGENT|REVIEW(?:-FLAG)?)\s*:?\s*(.*?)-->", re.DOTALL)


def write_todo_queue(vault: Path, articles: list[Article]) -> None:
    path = vault / "_TODO_QUEUE.md"
    lines = [
        "# _TODO_QUEUE.md",
        "",
        "**Auto-generated by `tools/validate.py`. Extracted TODO, AGENT, REVIEW comments from article bodies.**",
        "",
    ]
    total = 0
    for a in articles:
        matches = list(_TODO_RE.finditer(a.body))
        if not matches:
            continue
        lines.append(f"## {a.rel_path}")
        for m in matches:
            kind = m.group(1)
            content = m.group(2).strip().replace("\n", " ")
            lines.append(f"- **{kind}:** {content}")
            total += 1
        lines.append("")
    if total == 0:
        lines.append("No TODO / AGENT / REVIEW comments at this time.")
    _write_text(path, "\n".join(lines) + "\n")


def write_manifest(vault: Path) -> None:
    path = vault / "_MANIFEST.txt"
    lines = [
        md.relative_to(vault).as_posix()
        for md in sorted(iter_markdown_files(vault))
    ]
    _write_text(path, "\n".join(lines) + "\n")


if __name__ == "__main__":
    sys.exit(main())
