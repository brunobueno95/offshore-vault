"""Tests for tools/priority.py."""
from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest

from priority import (
    BatchItem,
    compute_batch,
    load_progress,
    load_urgent_paths,
    save_progress,
)


# ---------------------------------------------------------------------
# Helpers (duplicated-ish from test_validator to keep tests independent)
# ---------------------------------------------------------------------

def _write(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content), encoding="utf-8")
    return path


def _seed_tree(vault: Path, tree: str = "drilling") -> Path:
    tree_root = vault / tree
    _write(tree_root / "_INDEX.md", """\
        ---
        schema_version: "1.0"
        title: "Drilling"
        slug: "drilling"
        folder_scope: "root"
        contains_leaves: false
        contains_subfolders: true
        parent_folder: ""
        ---
        """)
    return tree_root


def _seed_folder(vault: Path, tree: str, folder: str) -> None:
    root = vault / tree / folder
    _write(root / "_INDEX.md", f"""\
        ---
        schema_version: "1.0"
        title: "{folder}"
        slug: "{folder}"
        folder_scope: "test"
        contains_leaves: true
        contains_subfolders: false
        parent_folder: ""
        ---
        """)


def _stub(
    slug: str,
    tree: str = "drilling",
    folder: str = "01-test",
    depth: str | None = "foundational",
    ncs: bool = True,
    created: str = "2026-04-01",
    status: str = "draft",
    placeholder: bool = True,
) -> str:
    body_marker = (
        "<!-- CONTENT PLACEHOLDER. Agent fills per _AGENT_RULES.md. -->"
        if placeholder
        else "## Overview\n\nReal body.\n\n## Details\n\nMore.\n\n## Sources\n\n1. Ref.\n"
    )
    depth_line = f"depth: {depth}" if depth else "depth: null"
    return dedent(f"""\
        ---
        schema_version: "1.0"
        id: "{tree}-{slug}"
        title: "Test {slug}"
        title_no: null
        slug: "{slug}"
        type: concept
        status: {status}
        domain: {tree}
        folder: "{folder}"
        parents: []
        siblings: []
        topics: []
        life_cycle_phases: []
        {depth_line}
        perspective: []
        authoritative_sources: []
        reference_textbooks: []
        related_incidents: []
        related: []
        cross_domain: []
        relevant_to_roles: []
        ncs_specific: {"true" if ncs else "false"}
        norwegian_terms: []
        authors: []
        created: "{created}"
        updated: "{created}"
        review_due: null
        tags: []
        citation_density: null
        word_count: null
        ---

        {body_marker}
        """)


_PRIORITY_CFG = {
    "urgent_file": "_URGENT_QUEUE.md",
    "foundational_bonus": 20,
    "ncs_specific_bonus": 15,
    "age_bonus_per_day": 1,
    "age_bonus_cap": 30,
    "tier_urgent_score": 10000,
    "tier_pull_forward_base": 1000,
    "tier_chapter_sweep_base": 100,
    "tier_backfill_base": 10,
}


# ---------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------

def test_compute_batch_returns_sorted_by_score(tmp_path: Path) -> None:
    _seed_tree(tmp_path)
    _seed_folder(tmp_path, "drilling", "01-test")
    # foundational + ncs_specific: score 135+ (plus age)
    _write(tmp_path / "drilling" / "01-test" / "a.md", _stub("a", depth="foundational", ncs=True))
    # operational, not ncs: score 100 (plus age)
    _write(tmp_path / "drilling" / "01-test" / "b.md", _stub("b", depth="operational", ncs=False))
    # foundational only: score 120 (plus age)
    _write(tmp_path / "drilling" / "01-test" / "c.md", _stub("c", depth="foundational", ncs=False))

    batch = compute_batch(
        vault=tmp_path, tree="drilling", batch_size=10,
        progress={}, urgent_paths=set(), priority_cfg=_PRIORITY_CFG,
    )
    # Score ranking: a (foundational+ncs) > c (foundational only) > b (neither bonus)
    assert [b.path for b in batch] == [
        "drilling/01-test/a.md",
        "drilling/01-test/c.md",
        "drilling/01-test/b.md",
    ]


def test_compute_batch_respects_size(tmp_path: Path) -> None:
    _seed_tree(tmp_path)
    _seed_folder(tmp_path, "drilling", "01-test")
    for i in range(5):
        _write(tmp_path / "drilling" / "01-test" / f"a{i}.md", _stub(f"a{i}"))
    batch = compute_batch(
        vault=tmp_path, tree="drilling", batch_size=3,
        progress={}, urgent_paths=set(), priority_cfg=_PRIORITY_CFG,
    )
    assert len(batch) == 3


def test_urgent_paths_sort_first(tmp_path: Path) -> None:
    _seed_tree(tmp_path)
    _seed_folder(tmp_path, "drilling", "01-test")
    # Non-urgent ones with high sweep bonus
    _write(tmp_path / "drilling" / "01-test" / "a.md", _stub("a", depth="foundational", ncs=True))
    # Urgent one with low bonus (operational, not ncs)
    _write(tmp_path / "drilling" / "01-test" / "b.md", _stub("b", depth="operational", ncs=False))
    urgent = {"drilling/01-test/b.md"}
    batch = compute_batch(
        vault=tmp_path, tree="drilling", batch_size=10,
        progress={}, urgent_paths=urgent, priority_cfg=_PRIORITY_CFG,
    )
    assert batch[0].path == "drilling/01-test/b.md"
    assert batch[0].reason == "urgent"


def test_progress_excludes_promoted_articles(tmp_path: Path) -> None:
    _seed_tree(tmp_path)
    _seed_folder(tmp_path, "drilling", "01-test")
    _write(tmp_path / "drilling" / "01-test" / "a.md", _stub("a"))
    _write(tmp_path / "drilling" / "01-test" / "b.md", _stub("b"))
    progress = {
        "drilling/01-test/a.md": {"status_at_last_touch": "published"},
    }
    batch = compute_batch(
        vault=tmp_path, tree="drilling", batch_size=10,
        progress=progress, urgent_paths=set(), priority_cfg=_PRIORITY_CFG,
    )
    assert [b.path for b in batch] == ["drilling/01-test/b.md"]


def test_non_placeholder_articles_excluded(tmp_path: Path) -> None:
    _seed_tree(tmp_path)
    _seed_folder(tmp_path, "drilling", "01-test")
    _write(tmp_path / "drilling" / "01-test" / "a.md", _stub("a", placeholder=True))
    _write(tmp_path / "drilling" / "01-test" / "b.md", _stub("b", placeholder=False))
    batch = compute_batch(
        vault=tmp_path, tree="drilling", batch_size=10,
        progress={}, urgent_paths=set(), priority_cfg=_PRIORITY_CFG,
    )
    assert [b.path for b in batch] == ["drilling/01-test/a.md"]


def test_flagged_for_human_excluded(tmp_path: Path) -> None:
    _seed_tree(tmp_path)
    _seed_folder(tmp_path, "drilling", "01-test")
    _write(tmp_path / "drilling" / "01-test" / "a.md", _stub("a"))
    progress = {
        "drilling/01-test/a.md": {"flagged_for_human": True},
    }
    batch = compute_batch(
        vault=tmp_path, tree="drilling", batch_size=10,
        progress=progress, urgent_paths=set(), priority_cfg=_PRIORITY_CFG,
    )
    assert batch == []


def test_infrastructure_files_skipped(tmp_path: Path) -> None:
    _seed_tree(tmp_path)
    _seed_folder(tmp_path, "drilling", "01-test")
    _write(tmp_path / "drilling" / "01-test" / "a.md", _stub("a"))
    # _INDEX.md and _TOPICS.md must not appear in the batch.
    batch = compute_batch(
        vault=tmp_path, tree="drilling", batch_size=10,
        progress={}, urgent_paths=set(), priority_cfg=_PRIORITY_CFG,
    )
    assert all("_INDEX" not in b.path and "_TOPICS" not in b.path for b in batch)
    assert [b.path for b in batch] == ["drilling/01-test/a.md"]


def test_load_urgent_parses_bullet_list(tmp_path: Path) -> None:
    (tmp_path / "_URGENT_QUEUE.md").write_text(
        "# Urgent queue\n\n"
        "- drilling/01-test/a.md\n"
        "- drilling/07-well-control/02-kick-detection/flow-check-procedure.md\n"
        "* subsea/foo.md\n"
        "`drilling/plain.md`\n"
        "\n"
        "# Comment line ignored\n",
        encoding="utf-8",
    )
    paths = load_urgent_paths(tmp_path)
    assert paths == {
        "drilling/01-test/a.md",
        "drilling/07-well-control/02-kick-detection/flow-check-procedure.md",
        "subsea/foo.md",
        "drilling/plain.md",
    }


def test_load_urgent_missing_file_returns_empty(tmp_path: Path) -> None:
    assert load_urgent_paths(tmp_path) == set()


def test_progress_roundtrip(tmp_path: Path) -> None:
    data = {
        "drilling/foo.md": {"last_touched_run_id": "abc", "status_at_last_touch": "draft"},
    }
    save_progress(tmp_path, data)
    loaded = load_progress(tmp_path)
    assert loaded == data
