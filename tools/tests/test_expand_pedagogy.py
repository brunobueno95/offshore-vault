"""Tests for tools/expand_pedagogy.py."""
from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest

from expand_pedagogy import (
    build_acronym_mapping,
    expand_acronyms,
    expand_norwegian_terms,
    _compute_frozen_ranges,
)


# ---------------------------------------------------------------
# Acronym tests
# ---------------------------------------------------------------

def test_build_mapping_from_explicit_pair() -> None:
    body = "The BOP (Blowout Preventer) is the primary barrier."
    frozen = _compute_frozen_ranges(body)
    mapping = build_acronym_mapping(body, frozen)
    assert mapping == {"BOP": "Blowout Preventer"}


def test_build_mapping_uses_first_occurrence() -> None:
    body = "API (American Petroleum Institute) first. API (Application Programming Interface) elsewhere."
    frozen = _compute_frozen_ranges(body)
    mapping = build_acronym_mapping(body, frozen)
    assert mapping["API"] == "American Petroleum Institute"


def test_expand_basic_repeats() -> None:
    body = "BOP (Blowout Preventer) first. BOP second. BOP third."
    frozen = _compute_frozen_ranges(body)
    mapping = build_acronym_mapping(body, frozen)
    new_body, count = expand_acronyms(body, mapping)
    assert count == 2
    assert new_body == (
        "BOP (Blowout Preventer) first. BOP (Blowout Preventer) second. "
        "BOP (Blowout Preventer) third."
    )


def test_expand_does_not_touch_already_expanded() -> None:
    body = "BOP (Blowout Preventer) first. BOP (Blowout Preventer) second."
    frozen = _compute_frozen_ranges(body)
    mapping = build_acronym_mapping(body, frozen)
    new_body, count = expand_acronyms(body, mapping)
    assert count == 0
    assert new_body == body


def test_expand_skips_headings() -> None:
    body = "## BOP section\n\nThe BOP (Blowout Preventer) is primary. BOP handles pressure."
    frozen = _compute_frozen_ranges(body)
    mapping = build_acronym_mapping(body, frozen)
    new_body, count = expand_acronyms(body, mapping)
    # Only the second bare "BOP" in prose should be expanded.
    assert count == 1
    assert "## BOP section" in new_body  # heading unchanged
    assert "BOP (Blowout Preventer) handles pressure." in new_body


def test_expand_skips_tables() -> None:
    body = dedent("""\
        BOP (Blowout Preventer) first.

        | Standard | Abbr |
        |---|---|
        | Blowout Preventer | BOP |

        BOP is the bare occurrence in prose.
        """)
    frozen = _compute_frozen_ranges(body)
    mapping = build_acronym_mapping(body, frozen)
    new_body, count = expand_acronyms(body, mapping)
    # Only the bare prose occurrence should be expanded.
    assert count == 1
    assert "| Blowout Preventer | BOP |" in new_body  # table unchanged


def test_expand_skips_html_comments() -> None:
    body = "BOP (Blowout Preventer) first. <!-- REVIEW-FLAG: BOP needs check --> BOP later."
    frozen = _compute_frozen_ranges(body)
    mapping = build_acronym_mapping(body, frozen)
    new_body, count = expand_acronyms(body, mapping)
    assert count == 1
    assert "<!-- REVIEW-FLAG: BOP needs check -->" in new_body  # comment unchanged


def test_expand_skips_sources_section() -> None:
    body = dedent("""\
        BOP (Blowout Preventer) first. BOP in prose.

        ## Sources

        1. BOP standards documentation.
        """)
    frozen = _compute_frozen_ranges(body)
    mapping = build_acronym_mapping(body, frozen)
    new_body, count = expand_acronyms(body, mapping)
    assert count == 1  # only the prose one
    assert "BOP standards documentation" in new_body  # Sources unchanged


def test_expand_handles_plural() -> None:
    body = "The BOP (Blowout Preventer) matters. Two BOPs are better than one."
    frozen = _compute_frozen_ranges(body)
    mapping = build_acronym_mapping(body, frozen)
    new_body, count = expand_acronyms(body, mapping)
    assert count == 1
    assert "Two BOPs (Blowout Preventer)" in new_body


def test_false_positives_not_expanded() -> None:
    body = "OK this is fine. No mapping for OK because it is a false positive."
    frozen = _compute_frozen_ranges(body)
    mapping = build_acronym_mapping(body, frozen)
    new_body, count = expand_acronyms(body, mapping)
    assert count == 0
    assert new_body == body


def test_unknown_acronym_not_expanded() -> None:
    body = "UNKNOWNACR was never defined here. It just appears."
    frozen = _compute_frozen_ranges(body)
    mapping = build_acronym_mapping(body, frozen)
    # UNKNOWNACR is 10 chars, exceeds the 2-8 range, not matched.
    # Use a valid-size unknown acronym.
    body2 = "XYZW was never defined. It appears bare."
    new_body, count = expand_acronyms(body2, mapping)
    assert count == 0


# ---------------------------------------------------------------
# Norwegian term tests
# ---------------------------------------------------------------

def test_expand_norwegian_basic() -> None:
    body = "The kranfører (crane operator) runs the crane. The kranfører decides lift plans."
    nts = [{"no": "kranfører", "en": "crane operator"}]
    new_body, count = expand_norwegian_terms(body, nts)
    assert count == 1
    assert new_body == (
        "The kranfører (crane operator) runs the crane. "
        "The kranfører (crane operator) decides lift plans."
    )


def test_expand_norwegian_accepts_false_key() -> None:
    # YAML 1.1 parses unquoted `no:` as the boolean False. Expander accepts both.
    body = "The boreleder (drilling supervisor) runs the rig. The boreleder makes calls."
    nts = [{False: "boreleder", "en": "drilling supervisor"}]
    new_body, count = expand_norwegian_terms(body, nts)
    assert count == 1


def test_expand_norwegian_skips_tables() -> None:
    body = dedent("""\
        The kranfører (crane operator) runs the crane.

        | Norwegian | English |
        |---|---|
        | kranfører | crane operator |

        The kranfører in prose.
        """)
    nts = [{"no": "kranfører", "en": "crane operator"}]
    new_body, count = expand_norwegian_terms(body, nts)
    assert count == 1
    assert "| kranfører | crane operator |" in new_body


def test_expand_norwegian_skips_terminology_section() -> None:
    body = dedent("""\
        The kranfører (crane operator) is first. The kranfører in prose.

        ## Norwegian terminology

        | kranfører | crane operator | The NCS standard term. |
        """)
    nts = [{"no": "kranfører", "en": "crane operator"}]
    new_body, count = expand_norwegian_terms(body, nts)
    assert count == 1  # only the bare prose occurrence


def test_expand_norwegian_handles_case() -> None:
    body = "The Kranfører (crane operator) first. The kranfører later."
    nts = [{"no": "kranfører", "en": "crane operator"}]
    new_body, count = expand_norwegian_terms(body, nts)
    assert count == 1  # second occurrence gets expansion


def test_expand_norwegian_empty_terms() -> None:
    body = "The boreleder is a role."
    new_body, count = expand_norwegian_terms(body, [])
    assert count == 0
    assert new_body == body


# ---------------------------------------------------------------
# Frozen-range tests
# ---------------------------------------------------------------

def test_frozen_ranges_include_sources() -> None:
    body = dedent("""\
        Normal prose here.

        ## Sources

        1. Reference.
        """)
    ranges = _compute_frozen_ranges(body)
    sources_start = body.index("## Sources")
    # The frozen range that includes Sources should start at or before
    # sources_start and extend to the end of the body.
    covers_sources = any(
        start <= sources_start and end >= len(body) for start, end in ranges
    )
    assert covers_sources


def test_frozen_ranges_include_terminology_section() -> None:
    body = dedent("""\
        Prose.

        ## Norwegian terminology

        | term | english |

        ## Sources

        1. Reference.
        """)
    ranges = _compute_frozen_ranges(body)
    term_start = body.index("## Norwegian terminology")
    sources_start = body.index("## Sources")
    # Norwegian terminology section should be frozen from its heading
    # until the start of the next section.
    covered = any(
        start <= term_start and end >= sources_start - 1 for start, end in ranges
    )
    assert covered
