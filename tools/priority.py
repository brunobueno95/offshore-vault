#!/usr/bin/env python3
"""Priority selection for the offshore-vault pipeline.

Given a vault root, a tree name, a batch size, and cross-run progress
state, return an ordered list of `BatchItem` objects representing the
articles the pipeline should fill this run.

Priority tiers (Milestone 2 implements T1 and T3, T2 is a placeholder
until the pull-forward graph has meaningful data):

    T1 URGENT      - listed in _URGENT_QUEUE.md or via CLI flag
    T2 PULL-FORWARD- referenced by filled articles (placeholder)
    T3 SWEEP       - sequential sweep, biased by depth, ncs, age
    T4 BACKFILL    - anything else

Score formula used by the sweep tier:

    score = tier_base
          + (foundational_bonus  if depth == 'foundational' else 0)
          + (ncs_specific_bonus  if ncs_specific is True else 0)
          + min(age_days * age_bonus_per_day, age_bonus_cap)

Ties are broken by lexical sort of path, so every run is reproducible
given the same vault state and progress.json.
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from validate import (  # noqa: E402
    TREES,
    iter_markdown_files,
    load_article,
    FrontmatterMissingError,
    _is_placeholder,
    RULE_FILE_NAMES,
)


@dataclass
class BatchItem:
    path: str
    tree: str
    score: float
    reason: str
    title: str
    depth: str | None
    ncs_specific: bool

    def to_dict(self) -> dict:
        return asdict(self)


def compute_batch(
    vault: Path,
    tree: str,
    batch_size: int,
    progress: dict,
    urgent_paths: set[str],
    priority_cfg: dict,
) -> list[BatchItem]:
    """Return up to `batch_size` items sorted by priority score descending."""
    tree_root = vault / tree
    if not tree_root.is_dir():
        return []

    today = date.today()
    candidates: list[BatchItem] = []

    for md_path in iter_markdown_files(tree_root):
        name = md_path.name
        if name in RULE_FILE_NAMES or name == "_INDEX.md":
            continue
        if name.startswith("_"):
            continue

        rel_path = md_path.relative_to(vault).as_posix()

        # Skip articles the pipeline previously promoted or flagged.
        prog = progress.get(rel_path, {})
        last_status = prog.get("status_at_last_touch", "")
        if last_status in ("review", "published"):
            continue
        if prog.get("flagged_for_human"):
            continue

        try:
            article = load_article(md_path, vault)
        except (FrontmatterMissingError, yaml.YAMLError):
            # Broken frontmatter; validator will flag. Skip in priority.
            continue

        # Skip articles whose body has already been filled.
        if not _is_placeholder(article.body):
            continue

        score, reason = _score_article(
            rel_path, article.frontmatter, urgent_paths, today, priority_cfg
        )

        candidates.append(BatchItem(
            path=rel_path,
            tree=tree,
            score=score,
            reason=reason,
            title=str(article.frontmatter.get("title", "")),
            depth=article.frontmatter.get("depth"),
            ncs_specific=bool(article.frontmatter.get("ncs_specific", False)),
        ))

    candidates.sort(key=lambda b: (-b.score, b.path))
    return candidates[:batch_size]


def _score_article(
    rel_path: str,
    fm: dict,
    urgent_paths: set[str],
    today: date,
    cfg: dict,
) -> tuple[float, str]:
    # T1: urgent
    if rel_path in urgent_paths:
        return float(cfg.get("tier_urgent_score", 10000)), "urgent"

    # T3: sweep (default tier when nothing else matches)
    score = float(cfg.get("tier_chapter_sweep_base", 100))
    reasons: list[str] = ["sweep"]

    if fm.get("depth") == "foundational":
        score += cfg.get("foundational_bonus", 20)
        reasons.append("foundational")

    if fm.get("ncs_specific") is True:
        score += cfg.get("ncs_specific_bonus", 15)
        reasons.append("ncs")

    created = fm.get("created")
    if isinstance(created, str):
        try:
            c = date.fromisoformat(created)
            age = max(0, (today - c).days)
            bonus = min(age * cfg.get("age_bonus_per_day", 1), cfg.get("age_bonus_cap", 30))
            score += bonus
            if bonus > 0:
                reasons.append(f"age{age}d")
        except ValueError:
            pass

    return score, "+".join(reasons)


def load_urgent_paths(vault: Path, urgent_file_name: str = "_URGENT_QUEUE.md") -> set[str]:
    """Parse `_URGENT_QUEUE.md` at the vault root into a set of paths."""
    path = vault / urgent_file_name
    if not path.is_file():
        return set()
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return set()
    out: set[str] = set()
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        line = re.sub(r"^[-*]\s+", "", line).strip("`").strip()
        if line.endswith(".md"):
            out.add(line)
    return out


def load_progress(state_dir: Path) -> dict:
    path = state_dir / "progress.json"
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_progress(state_dir: Path, progress: dict) -> None:
    state_dir.mkdir(parents=True, exist_ok=True)
    path = state_dir / "progress.json"
    path.write_text(json.dumps(progress, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def plan_summary(batches: dict[str, list[BatchItem]]) -> str:
    """Human-readable summary of a batch plan."""
    lines = ["Batch plan:"]
    for tree, items in batches.items():
        lines.append(f"  {tree}: {len(items)} article(s)")
        for b in items[:10]:
            lines.append(f"    - [{b.score:.0f} {b.reason}] {b.path}  \"{b.title}\"")
        if len(items) > 10:
            lines.append(f"    - ... {len(items) - 10} more")
    return "\n".join(lines)
