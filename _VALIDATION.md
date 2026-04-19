# _VALIDATION.md — validator rules

**Version:** 1.0  
**Scope:** rules enforced by the validator script on every article in `offshore-vault/`

The validator is a script (to be built in Phase 4, target language Python) that reads every `.md` file in the vault, parses frontmatter with PyYAML, and enforces these rules. This file is the specification.

---

## Validation severity levels

Every rule violation has a severity:

| Severity | Effect |
|---|---|
| `error` | Validator exits with non-zero code. Blocks CI. Blocks `status: published` transition. |
| `warning` | Validator completes but reports. Does not block CI by default. Flagged for human review. |
| `info` | Informational. Reported in validator log. |

Errors are structural problems the validator can detect mechanically. Warnings are quality signals that require human judgment.

---

## Schema compliance (errors)

1. **E-SCH-01:** Frontmatter block is missing or malformed YAML.
2. **E-SCH-02:** `schema_version` is missing or does not match current (`1.0`).
3. **E-SCH-03:** Required field is missing: `id`, `title`, `slug`, `type`, `status`, `domain`, `folder`, `ncs_specific`, `created`, `updated`.
4. **E-SCH-04:** Field has wrong type (string where list expected, integer where string expected, etc.).
5. **E-SCH-05:** Field contains an enum value outside the allowed set defined in `_CONTROLLED_VOCABULARY.md`.
6. **E-SCH-06:** Unknown field present (not defined in `_SCHEMA.md`).
7. **E-SCH-07:** `authoritative_sources` object missing required sub-field (`id`, `title`, `publisher`, `year`, `access`, `verified_date`, `verified_by`).

---

## Identity and path integrity (errors)

8. **E-ID-01:** `id` is not unique across the vault.
9. **E-ID-02:** `slug` does not match filename (without extension).
10. **E-ID-03:** `domain` does not match the tree the file lives in.
11. **E-ID-04:** `folder` does not match the actual folder path relative to tree root.
12. **E-PATH-01:** Filename contains characters forbidden by `_PATH_CONVENTIONS.md`.
13. **E-PATH-02:** Folder name contains characters forbidden by `_PATH_CONVENTIONS.md`.
14. **E-PATH-03:** Folder does not contain an `_INDEX.md`.

---

## Relationship integrity (errors and warnings)

15. **E-REL-01:** `related` entry does not resolve to an existing article within the same tree. (error)
16. **W-REL-01:** `cross_domain` entry does not resolve to an existing article. Logged to `_UNRESOLVED_LINKS.md`. (warning)
17. **W-REL-02:** `related_incidents` slug does not resolve. (warning)
18. **W-REL-03:** `parents` entry does not resolve. (warning)
19. **W-REL-04:** An article is referenced in another article's `related` but does not reference back (one-way link). (info)

---

## Publication requirements (block `published` transition)

An article at `status: published` must satisfy all of:

20. **P-PUB-01:** All E-SCH, E-ID, and E-PATH checks pass.
21. **P-PUB-02:** `type`, `depth` are non-null.
22. **P-PUB-03:** `authoritative_sources` is non-empty.
23. **P-PUB-04:** `word_count` meets minimum for declared `depth`:
    - `foundational`: minimum 800 words
    - `operational`: minimum 1500 words
    - `advanced`: minimum 3000 words
24. **P-PUB-05:** `citation_density` meets minimum for declared `depth`:
    - `foundational`: at least 1 citation per 150 words (density >= 0.67 citations per 100 words)
    - `operational`: at least 1 citation per 100 words (density >= 1.0)
    - `advanced`: at least 1 citation per 75 words (density >= 1.33)
25. **P-PUB-06:** All `related` paths resolve.
26. **P-PUB-07:** `updated` date is within 30 days of publication request.
27. **P-PUB-08:** All authoritative sources have `verified_date` within 365 days of publication request.

Articles not at `published` are not subject to rules 20-27 but are subject to rules 1-19.

---

## Authority whitelist (warnings)

28. **W-AUTH-01:** An entry in `authoritative_sources` has an `id` that is not on the tree's authority whitelist (defined in the tree's `CLAUDE.md`). Flagged for human review.

The validator does not block on this; new sources may be legitimate and only a human can approve. However, the warning count per tree is tracked in the validator log.

---

## NCS-specific content (warnings)

29. **W-NCS-01:** `ncs_specific: true` but no `## NCS-specific context` section detected in article body.
30. **W-NCS-02:** `ncs_specific: true` but `norwegian_terms` is empty.
31. **W-NCS-03:** Article cites only non-NCS sources (API, ISO, IMCA) without any Norwegian regulatory or industry source (Havtil, NORSOK, Offshore Norge, Sodir).

These are content-quality signals. The vault's purpose is NCS-specific, so articles without NCS grounding are suspect.

---

## Content structure (warnings)

32. **W-CON-01:** Article body does not contain `## Overview`, `## Details`, or `## Sources` sections.
33. **W-CON-02:** Article contains em dashes. (See `_AGENT_RULES.md`: forbidden.)
34. **W-CON-03:** Article uses an acronym without expansion on first use.
35. **W-CON-04:** Article paragraph exceeds 200 words (readability warning).
36. **W-CON-05:** Article body contains raw URLs outside the `## Sources` section.

---

## Freshness (warnings and info)

37. **W-FRESH-01:** An authoritative source has `verified_date` older than 365 days. Flag for re-verification.
38. **I-FRESH-01:** Article `updated` date is older than `review_due`. Due for review.
39. **I-FRESH-02:** No updates to the tree in 180 days. Tree freshness flag.

---

## Cross-tree link validation (detailed behaviour)

The validator walks `cross_domain` and `related` entries and categorises each as:

- **RESOLVED:** path exists, file found.
- **BROKEN-NO-MATCH:** path does not exist, no close match in target tree.
- **BROKEN-FUZZY-MATCH:** path does not exist, but a close-match slug exists in the target tree. Validator records the candidate.
- **AMBIGUOUS:** multiple files in the target tree could match the slug. Human chooses.

Output is written to `_UNRESOLVED_LINKS.md` at the vault root with one entry per broken or ambiguous link:

```markdown
### drilling/07-well-control/kill-methods/drillers-method.md
- From: drilling/07-well-control/07-kill-methods/drillers-method-two-circulation.md (cross_domain)
- Status: BROKEN-FUZZY-MATCH
- Closest candidate: drilling/07-well-control/07-kill-methods/drillers-method-two-circulation.md
- Suggested action: update source path to match canonical target, or confirm target does not yet exist.
```

Broken links are warnings. The vault tolerates them during construction. Agents do not block on unresolved links.

---

## Validator output files

On each run, the validator writes:

- **`_UNRESOLVED_LINKS.md`** at vault root: full cross-tree link report.
- **`_TODO_QUEUE.md`** at vault root: parsed `<!-- TODO: -->` comments from article bodies.
- **`_VALIDATION_REPORT.md`** at vault root: summary statistics (total articles, errors, warnings by severity and by tree).
- **`_MANIFEST.txt`** at vault root: every path in the vault, updated.

The validator also writes back to articles:

- `citation_density` field (computed)
- `word_count` field (computed)

---

## CI integration

The validator is invoked by `.github/workflows/validate.yml` on every push and pull request:

- Exit 0 if no errors.
- Exit 1 if any errors.
- Warnings do not block CI by default; a separate warning-threshold policy may be added later.

---

## Validator implementation target

**Language:** Python 3.11+  
**Dependencies:** `pyyaml`, `pathlib` (stdlib)  
**Entry point:** `tools/validate.py` (to be built)  
**Invocation:** `python tools/validate.py offshore-vault/`

The implementation is deferred to Phase 4. This file specifies what it must do.

---

## Rule ID prefix conventions

- `E-` Error
- `W-` Warning
- `I-` Info
- `P-` Publication gate

Rule categories:

- `SCH` Schema
- `ID` Identity
- `PATH` Path / naming
- `REL` Relationships
- `PUB` Publication
- `AUTH` Authority whitelist
- `NCS` NCS-specific content
- `CON` Content structure
- `FRESH` Freshness

New rules are added by appending to the appropriate category with the next sequential number. Rule IDs are never reused once deprecated.
