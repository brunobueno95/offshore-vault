# _SCHEMA.md — master frontmatter contract

**Version:** 1.0  
**Status:** locked  
**Scope:** every article (leaf `.md` file) in every tree in `offshore-vault/`

This is the canonical schema. Per-tree `CLAUDE.md` files carry a copy of this contract for agent self-containment. When this file changes, the tree CLAUDE.md files must be resynced.

---

## The full frontmatter block

Every leaf article starts with this YAML block, enclosed in `---` delimiters. Folder `_INDEX.md` files use a simpler schema defined separately.

```yaml
---
# Schema version
schema_version: "1.0"

# Identity
id: "<tree>-<slug>"                  # unique across vault, required
title: "Article title in English"    # required, human-readable
title_no: "Artikkeltittel på norsk"  # nullable, Norwegian equivalent if one exists
slug: "kebab-case-slug"              # required, matches filename without extension
type: concept                        # REQUIRED enum, see _CONTROLLED_VOCABULARY.md
status: draft                        # REQUIRED enum: draft | review | published | archived

# Taxonomy
domain: drilling                     # REQUIRED enum, must match tree name
folder: "01-chapter/02-section"      # required, relative to tree root, no leading slash, no file extension
parents: []                          # list of vault-relative article paths
siblings: []                         # list of slugs in same folder

# Knowledge-map dimensions
topics: []                           # list, constrained by tree's _TOPICS.md
life_cycle_phases: []                # enum list, may be empty
depth: foundational                  # REQUIRED enum before publication: foundational | operational | advanced
perspective: []                      # free-form list: syllabi or standards this entry serves

# Provenance (structured objects)
authoritative_sources: []            # list of source objects, REQUIRED non-empty before publication
reference_textbooks: []              # list of textbook objects, optional
related_incidents: []                # list of incident slugs, optional

# Relationships
related: []                          # list of vault-relative paths within this tree
cross_domain: []                     # list of vault-relative paths in other trees

# Role relevance
relevant_to_roles: []                # enum list, may be empty

# NCS specificity
ncs_specific: true                   # REQUIRED boolean
norwegian_terms: []                  # list of {no, en} objects

# Housekeeping
authors: []                          # list of agent IDs or human names
created: "2026-04-19"                # required, ISO date
updated: "2026-04-19"                # required, ISO date
review_due: null                     # ISO date or null, set by agent after first publication
tags: []                             # free-form list

# Validator-computed (do NOT write manually)
citation_density: null               # claims per 100 words, computed at validation
word_count: null                     # computed at validation
---
```

---

## Field-by-field specification

### `schema_version` (required, string)

The schema version this article conforms to. Currently `"1.0"`. Articles that do not declare a version are rejected by the validator.

### `id` (required, string)

Globally unique identifier across the vault. Format: `<domain>-<slug>` where domain is the tree name and slug is the article's kebab-case slug.

Example: `drilling-blowout-preventer`, `subsea-schilling-uhd-iii`, `crane-and-logistics-kranforer-g5-certified`.

### `title` (required, string)

Human-readable English title. Maximum 120 characters. Use title case or sentence case consistently within a tree.

### `title_no` (optional, string or null)

Norwegian equivalent title when the concept has a distinct Norwegian working term. Null if not applicable or unknown.

### `slug` (required, string)

Kebab-case, lowercase, ASCII only. Matches the filename without the `.md` extension. Maximum 80 characters. No leading digits unless the prefix has semantic meaning (e.g. `iso-4309-discard-criteria`).

### `type` (required, enum)

See `_CONTROLLED_VOCABULARY.md`. Allowed values: `concept | equipment | procedure | incident | standard | role | view | tool`.

### `status` (required, enum)

Lifecycle state of the article. Allowed values: `draft | review | published | archived`. New leaves start as `draft`. Validator enforces that `published` articles meet all publication requirements (see below).

### `domain` (required, enum)

Must match the tree root folder name. Allowed values: `drilling | crane-and-logistics | subsea | emergency-response`. The validator cross-checks `domain` against the tree the file actually lives in and flags mismatches.

### `folder` (required, string)

Vault-relative path to the article's containing folder, no leading slash, no file extension. Example: `01-geology-and-reservoir/02-rock-types/sedimentary`. Used by the validator to confirm the article lives where it claims.

### `parents` (list of strings)

Vault-relative paths to parent articles. Used for hierarchical traversal when one article is a strict subtype or specialisation of another.

### `siblings` (list of strings)

Slugs of articles in the same folder. Populated by a sibling-sync pass after all articles in a folder are written.

### `topics` (list of strings)

Constrained by the tree's own `_TOPICS.md`. Agents may propose additions during drafting; additions require human approval before entering the tree's allowed list.

### `life_cycle_phases` (enum list)

Allowed values: `exploration | drilling | completion | production | intervention | suspension | p-and-a | decommissioning`. Use only phases relevant to the article's scope. Empty list is valid.

### `depth` (required enum, before publication)

Allowed values: `foundational | operational | advanced`. Controls minimum word count and citation density expectations. See `_VALIDATION.md`.

### `perspective` (list of strings, free-form)

Which syllabi, standards, or audiences this article serves. Examples: `["IWCF Level 2", "NORSOK D-010 Clause 6.2", "roustabout onboarding"]`.

### `authoritative_sources` (structured object list, required non-empty before publication)

Each source is an object:

```yaml
authoritative_sources:
  - id: "norsok-d-010-rev5"              # required, kebab-case identifier
    title: "NORSOK D-010 Rev 5"          # required, human-readable
    publisher: "Standards Norway"        # required
    year: 2021                           # required, integer
    url: "https://standard.no/..."       # optional
    access: "paywalled"                  # required enum: open | paywalled | restricted
    cited_sections: ["Clause 6.2"]       # optional, list of strings
    verified_date: "2026-04-18"          # required, ISO date
    verified_by: "bruno"                 # required, agent ID or human name
```

The `verified_date` is used by the validator to flag stale sources (default threshold: 365 days). The tree's CLAUDE.md specifies the authority whitelist; sources outside the whitelist are flagged for review.

### `reference_textbooks` (structured object list, optional)

Each textbook is an object:

```yaml
reference_textbooks:
  - title: "Applied Drilling Engineering"
    authors: ["Bourgoyne", "Millheim", "Chenevert", "Young"]
    publisher: "SPE"
    year: 1986
    isbn: "978-1555630010"               # optional
    cited_chapters: ["4", "6"]           # optional
```

Use `reference_textbooks` for pedagogical or historical textbook references that are NOT authoritative standards. Authoritative industry standards and regulations go in `authoritative_sources`.

### `related_incidents` (list of strings)

Slugs of incident articles. Typically reference case studies such as `piper-alpha-1988`, `macondo-2010`, `turoy-2016`.

### `related` (list of strings)

Vault-relative paths to other articles within the same tree. Used for lateral concept-to-concept links. Example: a `drillers-method-two-circulation.md` article might have `related: ["07-well-control/07-kill-methods/wait-and-weight-engineers-method.md"]`.

### `cross_domain` (list of strings)

Vault-relative paths to articles in other trees. Written at draft time without verification. The post-run validator confirms paths resolve.

Example: a subsea article on BOP external inspection has `cross_domain: ["drilling/08-well-control-equipment/02-subsea-bop-stack/lower-marine-riser-package-lmrp.md"]`.

### `relevant_to_roles` (enum list)

Allowed values: `roustabout | roughneck | floorman | derrickhand | assistant-driller | driller | toolpusher | crane-operator | rigger | banksman | rov-pilot | rov-supervisor | medic | radio-operator | hlo | oim | materialkoordinator | kranforer | lofteleder | anhuker | boredekksarbeider | tarnmann`.

Extensible: agents may propose additional role values. Proposals require human approval.

### `ncs_specific` (required boolean)

`true` if the article contains content specific to the Norwegian Continental Shelf (regulations, operators, fields, Norwegian terminology, NCS historical context). `false` if the content is general industry knowledge applicable anywhere. Validator uses this to filter content for NCS-only briefings and study material.

### `norwegian_terms` (object list)

Each entry is `{no: "norsk term", en: "english equivalent"}`. Example:

```yaml
norwegian_terms:
  - { no: "kranfører", en: "crane operator" }
  - { no: "løfteleder", en: "lift supervisor" }
```

### `authors` (list of strings)

Agent IDs or human names. Format for agents: `"agent:<agent-id>-<version>"`. Example: `"agent:drilling-filler-v1"`. Format for humans: plain name or GitHub handle.

### `created` (required, ISO date)

Date the article was first created. Set at file generation, never changed.

### `updated` (required, ISO date)

Date of last substantive update. Bumped on any content change.

### `review_due` (ISO date or null)

Date by which this article should be revalidated. Default policy: 12 months from `created` for `foundational`, 18 months for `operational`, 24 months for `advanced`. Null on new drafts; set by agent after first publication.

### `tags` (free-form list)

Agent-assigned tags. Validator does not constrain these but warns if the same tag is used with inconsistent capitalisation or spelling across a tree.

### `citation_density` and `word_count` (validator-computed)

Do NOT write manually. The validator computes these and writes them back into the frontmatter. Articles that do not pass the density threshold for their `depth` are flagged.

---

## Folder `_INDEX.md` schema

Simpler schema for folder indexes:

```yaml
---
schema_version: "1.0"
title: "Folder display title (parentheticals preserved, human-readable)"
slug: "kebab-case-folder-name"
folder_scope: "One-sentence description of what this folder contains."
contains_leaves: true                  # boolean: does this folder have direct leaf articles?
contains_subfolders: false             # boolean: does this folder have nested subfolders?
parent_folder: "01-geology-and-reservoir"  # relative path, empty string at tree root
---
```

---

## Publication requirements

An article can move from `status: draft` to `status: review` or `published` only if all of the following are true:

1. `schema_version` is set and matches the current version.
2. `title`, `slug`, `type`, `domain`, `depth` are all non-null.
3. `domain` matches the tree the file lives in.
4. `slug` matches the filename without extension.
5. `folder` matches the actual folder path.
6. `authoritative_sources` is non-empty.
7. Every source has `id`, `title`, `publisher`, `year`, `access`, `verified_date`, `verified_by`.
8. Word count meets minimum for declared `depth` (see `_VALIDATION.md`).
9. Citation density meets minimum for declared `depth`.
10. All `related` paths resolve within the same tree.
11. `cross_domain` paths, if any, either resolve or are logged in `_UNRESOLVED_LINKS.md` with acceptable justification.

The validator enforces these mechanically. No article is published by an agent; the validator either accepts or rejects the transition.

---

## Schema versioning policy

- Patch changes (field clarifications, typo fixes): same version.
- Minor changes (new optional fields, new enum values): bump to `1.1`, `1.2`, etc.
- Major changes (required field removals, type changes, enum removals): bump to `2.0`.

On any bump, all per-tree `CLAUDE.md` files must be resynced. The sync script (`_sync.sh`, to be implemented) handles this.
