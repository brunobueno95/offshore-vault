"""Tests for tools/validate.py.

Each test builds a tiny vault in tmp_path and invokes the validator's main()
or internal check functions directly, then asserts the findings list.
"""
from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest

import validate  # noqa: F401  (conftest adds tools/ to sys.path)
from validate import (
    check_acronyms_every_use,
    check_body_structure,
    check_id_uniqueness,
    check_norwegian_terms_every_use,
    check_publication_gates,
    check_relationship_integrity,
    check_schema,
    compute_derived_fields,
    build_link_graph,
    load_article,
    main,
    FrontmatterMissingError,
)


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _write(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content), encoding="utf-8")
    return path


def _make_tree_skeleton(vault: Path, tree: str = "drilling") -> Path:
    """Create a minimal tree with a tree-root _INDEX.md."""
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


def _valid_article_text(slug: str, tree: str = "drilling", folder: str = "01-test") -> str:
    return dedent(f"""\
        ---
        schema_version: "1.0"
        id: "{tree}-{slug}"
        title: "Test article"
        slug: "{slug}"
        type: concept
        status: draft
        domain: {tree}
        folder: "{folder}"
        parents: []
        siblings: []
        topics: []
        life_cycle_phases: []
        depth: foundational
        perspective: []
        authoritative_sources: []
        reference_textbooks: []
        related_incidents: []
        related: []
        cross_domain: []
        relevant_to_roles: []
        ncs_specific: false
        norwegian_terms: []
        authors: []
        created: "2026-04-19"
        updated: "2026-04-19"
        review_due: null
        tags: []
        citation_density: null
        word_count: null
        ---

        <!-- CONTENT PLACEHOLDER. Agent fills per _AGENT_RULES.md. -->
        """)


def _seed_folder(vault: Path, tree: str, folder: str) -> None:
    """Ensure a folder and its _INDEX.md exist."""
    folder_root = vault / tree / folder
    _write(folder_root / "_INDEX.md", f"""\
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


# ------------------------------------------------------------------
# Schema checks
# ------------------------------------------------------------------

def test_valid_article_no_schema_findings(tmp_path: Path) -> None:
    _make_tree_skeleton(tmp_path)
    _seed_folder(tmp_path, "drilling", "01-test")
    md = _write(tmp_path / "drilling" / "01-test" / "foo.md", _valid_article_text("foo"))
    a = load_article(md, tmp_path)
    findings = check_schema(a)
    assert findings == [], [f.rule_id for f in findings]


def test_missing_frontmatter_flags_E_SCH_01(tmp_path: Path) -> None:
    _make_tree_skeleton(tmp_path)
    _seed_folder(tmp_path, "drilling", "01-test")
    md = _write(tmp_path / "drilling" / "01-test" / "nofm.md", "just body, no frontmatter\n")
    with pytest.raises(FrontmatterMissingError):
        load_article(md, tmp_path)


def test_missing_required_field_flags_E_SCH_03(tmp_path: Path) -> None:
    _make_tree_skeleton(tmp_path)
    _seed_folder(tmp_path, "drilling", "01-test")
    content = _valid_article_text("foo").replace('title: "Test article"\n', "")
    md = _write(tmp_path / "drilling" / "01-test" / "foo.md", content)
    a = load_article(md, tmp_path)
    findings = check_schema(a)
    assert any(f.rule_id == "E-SCH-03" and f.field_name == "title" for f in findings)


def test_invalid_enum_flags_E_SCH_05(tmp_path: Path) -> None:
    _make_tree_skeleton(tmp_path)
    _seed_folder(tmp_path, "drilling", "01-test")
    content = _valid_article_text("foo").replace("type: concept\n", "type: nonsense\n")
    md = _write(tmp_path / "drilling" / "01-test" / "foo.md", content)
    a = load_article(md, tmp_path)
    findings = check_schema(a)
    assert any(f.rule_id == "E-SCH-05" and f.field_name == "type" for f in findings)


def test_unknown_field_flags_E_SCH_06(tmp_path: Path) -> None:
    _make_tree_skeleton(tmp_path)
    _seed_folder(tmp_path, "drilling", "01-test")
    content = _valid_article_text("foo").replace(
        "tags: []\n",
        "tags: []\nmystery_field: 123\n",
    )
    md = _write(tmp_path / "drilling" / "01-test" / "foo.md", content)
    a = load_article(md, tmp_path)
    findings = check_schema(a)
    assert any(f.rule_id == "E-SCH-06" and f.field_name == "mystery_field" for f in findings)


# ------------------------------------------------------------------
# Identity checks
# ------------------------------------------------------------------

def test_slug_mismatch_flags_E_ID_02(tmp_path: Path) -> None:
    _make_tree_skeleton(tmp_path)
    _seed_folder(tmp_path, "drilling", "01-test")
    # Write a file named foo.md but declare slug: bar
    content = _valid_article_text("foo").replace('slug: "foo"', 'slug: "bar"')
    md = _write(tmp_path / "drilling" / "01-test" / "foo.md", content)
    rc = main([str(tmp_path), "--quiet"])
    # Validator should return 1 because of errors (including E-ID-02)
    import json
    report = json.loads((tmp_path / "_VALIDATION_REPORT.json").read_text(encoding="utf-8"))
    assert any(f["rule_id"] == "E-ID-02" for f in report["findings"])
    assert rc == 1


def test_domain_mismatch_flags_E_ID_03(tmp_path: Path) -> None:
    _make_tree_skeleton(tmp_path)
    _seed_folder(tmp_path, "drilling", "01-test")
    # Article lives under drilling/ but declares domain: subsea
    content = _valid_article_text("foo").replace("domain: drilling", "domain: subsea")
    _write(tmp_path / "drilling" / "01-test" / "foo.md", content)
    main([str(tmp_path), "--quiet"])
    import json
    report = json.loads((tmp_path / "_VALIDATION_REPORT.json").read_text(encoding="utf-8"))
    assert any(f["rule_id"] == "E-ID-03" for f in report["findings"])


def test_duplicate_id_flags_E_ID_01(tmp_path: Path) -> None:
    _make_tree_skeleton(tmp_path)
    _seed_folder(tmp_path, "drilling", "01-test")
    _write(tmp_path / "drilling" / "01-test" / "foo.md", _valid_article_text("foo"))
    # Create a second article that uses the same id
    content = _valid_article_text("bar").replace('id: "drilling-bar"', 'id: "drilling-foo"')
    _write(tmp_path / "drilling" / "01-test" / "bar.md", content)
    main([str(tmp_path), "--quiet"])
    import json
    report = json.loads((tmp_path / "_VALIDATION_REPORT.json").read_text(encoding="utf-8"))
    assert any(f["rule_id"] == "E-ID-01" for f in report["findings"])


# ------------------------------------------------------------------
# Body structure and content
# ------------------------------------------------------------------

def test_em_dash_flags_W_CON_02(tmp_path: Path) -> None:
    _make_tree_skeleton(tmp_path)
    _seed_folder(tmp_path, "drilling", "01-test")
    # Real body, not placeholder, containing an em dash
    content = _valid_article_text("foo").replace(
        "<!-- CONTENT PLACEHOLDER. Agent fills per _AGENT_RULES.md. -->\n",
        "## Overview\n\nThis uses an em dash \u2014 which is forbidden.\n\n## Details\n\nMore.\n\n## Sources\n\n1. Nothing.\n",
    )
    md = _write(tmp_path / "drilling" / "01-test" / "foo.md", content)
    a = load_article(md, tmp_path)
    findings = check_body_structure(a)
    assert any(f.rule_id == "W-CON-02" for f in findings)


def test_bare_acronym_flags_W_CON_03(tmp_path: Path) -> None:
    _make_tree_skeleton(tmp_path)
    _seed_folder(tmp_path, "drilling", "01-test")
    body = "## Overview\n\nThe BOP is important. BOP activation matters.\n\n## Details\n\nx.\n\n## Sources\n\n1. ref.\n"
    content = _valid_article_text("foo").replace(
        "<!-- CONTENT PLACEHOLDER. Agent fills per _AGENT_RULES.md. -->\n",
        body,
    )
    md = _write(tmp_path / "drilling" / "01-test" / "foo.md", content)
    a = load_article(md, tmp_path)
    findings = check_acronyms_every_use(a)
    assert any(f.rule_id == "W-CON-03" for f in findings)


def test_acronym_with_expansion_passes(tmp_path: Path) -> None:
    _make_tree_skeleton(tmp_path)
    _seed_folder(tmp_path, "drilling", "01-test")
    body = (
        "## Overview\n\nThe BOP (Blowout Preventer) is important. "
        "The BOP (Blowout Preventer) activates.\n\n"
        "## Details\n\nx.\n\n## Sources\n\n1. ref.\n"
    )
    content = _valid_article_text("foo").replace(
        "<!-- CONTENT PLACEHOLDER. Agent fills per _AGENT_RULES.md. -->\n",
        body,
    )
    md = _write(tmp_path / "drilling" / "01-test" / "foo.md", content)
    a = load_article(md, tmp_path)
    findings = check_acronyms_every_use(a)
    assert not any(f.rule_id == "W-CON-03" for f in findings)


def test_bare_norwegian_term_flags_W_CON_06(tmp_path: Path) -> None:
    _make_tree_skeleton(tmp_path)
    _seed_folder(tmp_path, "drilling", "01-test")
    body = (
        "## Overview\n\nThe kranforer operates the crane. "
        "The kranforer makes decisions.\n\n"
        "## Details\n\nx.\n\n## Sources\n\n1. ref.\n"
    )
    # Note: quote the "no" key to dodge the YAML 1.1 gotcha where `no:`
    # without quotes parses as the boolean False.
    content = _valid_article_text("foo").replace(
        "norwegian_terms: []",
        'norwegian_terms:\n  - { "no": "kranforer", en: "crane operator" }',
    ).replace(
        "<!-- CONTENT PLACEHOLDER. Agent fills per _AGENT_RULES.md. -->\n",
        body,
    )
    md = _write(tmp_path / "drilling" / "01-test" / "foo.md", content)
    a = load_article(md, tmp_path)
    findings = check_norwegian_terms_every_use(a)
    assert any(f.rule_id == "W-CON-06" for f in findings)


# ------------------------------------------------------------------
# Derived fields
# ------------------------------------------------------------------

def test_compute_word_count(tmp_path: Path) -> None:
    _make_tree_skeleton(tmp_path)
    _seed_folder(tmp_path, "drilling", "01-test")
    body = (
        "## Overview\n\n"
        + "word " * 300
        + "\n\n## Details\n\n"
        + "word " * 200
        + "\n\n## Sources\n\n1. ref.\n"
    )
    content = _valid_article_text("foo").replace(
        "<!-- CONTENT PLACEHOLDER. Agent fills per _AGENT_RULES.md. -->\n",
        body,
    )
    md = _write(tmp_path / "drilling" / "01-test" / "foo.md", content)
    a = load_article(md, tmp_path)
    compute_derived_fields(a)
    # 500 'word' tokens plus 'Overview', 'Details', 'Sources', '1.', 'ref.' etc.
    # The exact count depends on tokenisation. Assert it is in the expected range.
    assert 500 <= a.word_count <= 520


def test_citation_density_counts_valid_citations(tmp_path: Path) -> None:
    _make_tree_skeleton(tmp_path)
    _seed_folder(tmp_path, "drilling", "01-test")
    # Source list with id "norsok-d-010"
    content = _valid_article_text("foo").replace(
        "authoritative_sources: []",
        'authoritative_sources:\n'
        '  - id: "norsok-d-010"\n'
        '    title: "NORSOK D-010"\n'
        '    publisher: "Standards Norway"\n'
        '    year: 2021\n'
        '    access: paywalled\n'
        '    verified_date: "2026-04-18"\n'
        '    verified_by: "bruno"',
    ).replace(
        "<!-- CONTENT PLACEHOLDER. Agent fills per _AGENT_RULES.md. -->\n",
        "## Overview\n\nThis is a claim (norsok-d-010, Clause 6.2). "
        "Another claim (norsok-d-010). A third claim (unknown-source).\n\n"
        "## Details\n\nBody.\n\n## Sources\n\n1. ref.\n",
    )
    md = _write(tmp_path / "drilling" / "01-test" / "foo.md", content)
    a = load_article(md, tmp_path)
    compute_derived_fields(a)
    # Two of three parenthetical refs should count (third has id not in sources)
    assert a.citation_count == 2


# ------------------------------------------------------------------
# Link resolution
# ------------------------------------------------------------------

def test_broken_related_flags_E_REL_01(tmp_path: Path) -> None:
    _make_tree_skeleton(tmp_path)
    _seed_folder(tmp_path, "drilling", "01-test")
    # Article declares a related path to a non-existent file
    content = _valid_article_text("foo").replace(
        "related: []",
        'related: ["drilling/01-test/does-not-exist.md"]',
    )
    _write(tmp_path / "drilling" / "01-test" / "foo.md", content)
    rc = main([str(tmp_path), "--quiet"])
    import json
    report = json.loads((tmp_path / "_VALIDATION_REPORT.json").read_text(encoding="utf-8"))
    assert any(f["rule_id"] == "E-REL-01" for f in report["findings"])
    assert rc == 1


def test_broken_cross_domain_flags_W_REL_01(tmp_path: Path) -> None:
    _make_tree_skeleton(tmp_path)
    _seed_folder(tmp_path, "drilling", "01-test")
    content = _valid_article_text("foo").replace(
        "cross_domain: []",
        'cross_domain: ["subsea/99-missing/fake.md"]',
    )
    _write(tmp_path / "drilling" / "01-test" / "foo.md", content)
    main([str(tmp_path), "--quiet"])
    import json
    report = json.loads((tmp_path / "_VALIDATION_REPORT.json").read_text(encoding="utf-8"))
    assert any(f["rule_id"] == "W-REL-01" for f in report["findings"])


# ------------------------------------------------------------------
# Publication gates
# ------------------------------------------------------------------

def test_published_under_word_count_flags_P_PUB_04(tmp_path: Path) -> None:
    _make_tree_skeleton(tmp_path)
    _seed_folder(tmp_path, "drilling", "01-test")
    # Published foundational article with short body (well under 800 words)
    content = (
        _valid_article_text("foo")
        .replace("status: draft", "status: published")
        .replace(
            "authoritative_sources: []",
            'authoritative_sources:\n'
            '  - id: "norsok-d-010"\n'
            '    title: "NORSOK D-010"\n'
            '    publisher: "Standards Norway"\n'
            '    year: 2021\n'
            '    access: paywalled\n'
            '    verified_date: "2026-04-18"\n'
            '    verified_by: "bruno"',
        )
        .replace(
            "<!-- CONTENT PLACEHOLDER. Agent fills per _AGENT_RULES.md. -->\n",
            "## Overview\n\nShort.\n\n## Details\n\nShort.\n\n## Sources\n\n1. ref.\n",
        )
    )
    _write(tmp_path / "drilling" / "01-test" / "foo.md", content)
    main([str(tmp_path), "--quiet"])
    import json
    report = json.loads((tmp_path / "_VALIDATION_REPORT.json").read_text(encoding="utf-8"))
    assert any(f["rule_id"] == "P-PUB-04" for f in report["findings"])


# ------------------------------------------------------------------
# End-to-end: a clean minimal vault passes with zero errors
# ------------------------------------------------------------------

def test_clean_minimal_vault_exits_zero(tmp_path: Path) -> None:
    _make_tree_skeleton(tmp_path)
    _seed_folder(tmp_path, "drilling", "01-test")
    _write(tmp_path / "drilling" / "01-test" / "foo.md", _valid_article_text("foo"))
    rc = main([str(tmp_path), "--quiet"])
    assert rc == 0
    assert (tmp_path / "_VALIDATION_REPORT.md").exists()
    assert (tmp_path / "_MANIFEST.txt").exists()
