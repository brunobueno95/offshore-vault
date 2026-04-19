# CLAUDE.md — drilling tree

**Scope:** agents working in the `drilling/` tree of `offshore-vault/` read this file and nothing else at the vault root. This file is self-contained.

**Last synced from root masters:** 2026-04-19 (initial build)  
**Schema version:** 1.0

---

## 1. What this tree covers

NCS (Norwegian Continental Shelf) drilling knowledge from geology through well integrity and P&A. Spans everything a Norwegian driller touches between Vg2 Brønnteknikk, Boreoperatørfaget (Vg3), Fagskole Boring, and IWCF (International Well Control Forum) Levels 2 through 4.

Eighteen top-level chapters:

1. Geology and Reservoir
2. Well Planning and Design
3. Drilling Installations
4. Rig Equipment and Systems
5. Drilling Fluids (Mud)
6. Well Hydraulics
7. Well Control
8. Well Control Equipment
9. Drilling Operations
10. Cementing
11. Well Completion
12. Well Intervention
13. Formation Evaluation
14. Well Integrity and P&A
15. HSE and Regulatory Framework
16. Crew Organization and Roles
17. Maintenance and Reliability
18. Digital and Emerging

---

## 2. Scope boundaries (what this tree does NOT own)

Duplication is prohibited. When content overlaps another tree, one tree owns it; the other references via `cross_domain`.

- **ROV-facing BOP interface tasks** (external inspection, hot stab, pod retrieval, emergency shear ram via hot stab, EDS monitoring, LMRP separation video): lives in `subsea/15-rov-systems-operations-missions/rov-missions-bop-interface/`. Drilling owns BOP theory, ram taxonomy, stack configuration, internal mechanics, API 16A/16D/53 compliance, and kick response using BOP equipment.
- **Post-ignition emergency response** (fire after loss of containment, platform evacuation, SAR mobilisation, oil spill response): lives in `emergency-response/`. Drilling owns well-control response up to the moment of ignition or evacuation trigger.
- **Crane and rigging mechanics for tubular handling**: lives in `crane-and-logistics/`. Drilling references crane operations as a context but does not duplicate G4/G5/G20 content.
- **Subsea production system equipment** (christmas trees, manifolds, templates, umbilicals, flowlines): lives in `subsea/`. Drilling owns wellhead housings, casing hangers, tubing hangers, and completion hardware that is installed during drilling operations.
- **Crew resource management (CRM) general theory**: drilling owns CRM applied to drilling operations (flow-check discipline, kick-response crew coordination, driller handover). Generic human factors theory is cross-cutting metadata, not a drilling folder.

---

## 3. Frontmatter schema (v1.0)

Every leaf article in this tree uses this schema. Validator enforces it.

```yaml
---
schema_version: "1.0"

id: "drilling-<slug>"                # unique across vault
title: "Article title in English"
title_no: "Artikkeltittel på norsk"  # nullable
slug: "kebab-case-slug"
type: concept                        # ENUM: concept | equipment | procedure | incident | standard | role | view | tool
status: draft                        # ENUM: draft | review | published | archived

domain: drilling                     # always "drilling" for this tree
folder: "01-chapter/02-section"      # relative to tree root
parents: []
siblings: []

topics: []                           # constrained by _TOPICS.md (this tree)
life_cycle_phases: []                # ENUM list: exploration | drilling | completion | production | intervention | suspension | p-and-a | decommissioning
depth: foundational                  # ENUM: foundational | operational | advanced
perspective: []

authoritative_sources: []            # structured objects, see section 5
reference_textbooks: []
related_incidents: []

related: []                          # intra-tree paths
cross_domain: []                     # inter-tree paths

relevant_to_roles: []                # ENUM list, see section 4

ncs_specific: true
norwegian_terms: []                  # list of {no, en} objects

authors: []
created: "2026-04-19"
updated: "2026-04-19"
review_due: null
tags: []

citation_density: null               # validator-computed, do NOT write
word_count: null                     # validator-computed, do NOT write
---
```

---

## 4. Allowed enum values

### `type`
`concept | equipment | procedure | incident | standard | role | view | tool`

### `status`
`draft | review | published | archived`

### `depth`
`foundational | operational | advanced`

Minimums for publication:
- `foundational`: 800 words, 1 citation per 150 words minimum
- `operational`: 1500 words, 1 citation per 100 words minimum
- `advanced`: 3000 words, 1 citation per 75 words minimum

### `life_cycle_phases`
`exploration | drilling | completion | production | intervention | suspension | p-and-a | decommissioning`

### `access` (inside `authoritative_sources`)
`open | paywalled | restricted`

### `relevant_to_roles` (drilling-relevant subset)

Drilling floor: `roustabout | roughneck | floorman | derrickhand | assistant-driller | driller | toolpusher | senior-toolpusher | oim`

Operator reps: `drilling-supervisor | drilling-engineer | wellsite-geologist | completion-engineer`

Service company: `mud-engineer | mud-logger | directional-driller | mwd-engineer | cementer | wireline-engineer | coiled-tubing-supervisor | rov-pilot`

Emergency interface: `medic | radio-operator`

Propose additions in `_PROPOSALS.md` at tree root if a required role is missing.

### `ncs_specific`
`true | false`

---

## 5. Authoritative source whitelist

The following sources are the ONLY sources accepted for drilling tree articles without flagging. Sources outside this list trigger `W-AUTH-01` warning from the validator and require human approval before entering the whitelist.

### Norwegian regulatory

- **Havtil regulations** (Havindustritilsynet / Norwegian Ocean Industry Authority, formerly Petroleumstilsynet)
  - Rammeforskriften (Framework Regulations)
  - Styringsforskriften (Management Regulations)
  - Innretningsforskriften (Facilities Regulations)
  - Aktivitetsforskriften (Activities Regulations)
  - Teknisk og operasjonell forskrift (MODU regime)
- **Havtil investigation reports** (specific incident case studies)
- **Sokkeldirektoratet (Sodir, formerly NPD/Norwegian Petroleum Directorate)**
  - Sodir Factpages (factpages.npd.no / factpages.sodir.no)
  - Diskos repository
  - Resource management regulations
- **Petroleumsloven** (Petroleum Act)

### NORSOK standards

- NORSOK D-001 — Drilling facilities
- NORSOK D-002 — Well intervention equipment
- NORSOK D-010 — Well integrity in drilling and well operations (primary standard)
- NORSOK S-001 — Technical safety
- NORSOK Z-013 — Risk and emergency preparedness assessment

### Offshore Norge guidelines

- Guideline 024 — Drilling and well competence
- Guideline 117 — Well integrity
- Guideline 135 — Well control incident classification and notification

### International standards (well control and drilling)

- **IWCF** Level 2, 3, 4 syllabi (International Well Control Forum)
- **IADC** Drilling Manual, IADC guidelines
- **API Spec 16A** — Drill-through equipment
- **API Spec 16C** — Choke and kill systems
- **API Spec 16D** — Control systems for drilling-through equipment
- **API STD 53** — BOP system requirements
- **API RP 59** — Well control operations
- **API RP 10B** — Well cement testing
- **API Class A, B, C, G, H** — Cement specifications
- **ISO 16530-1** — Well integrity (life cycle)

### Peer-reviewed and industry literature

- **SPE** (Society of Petroleum Engineers) peer-reviewed papers
- **IOGP** (International Association of Oil and Gas Producers) reports

### Vendor manuals (when sole authoritative source)

- Schlumberger / SLB drilling equipment manuals
- Halliburton drilling equipment manuals
- Baker Hughes drilling equipment manuals
- NOV (National Oilwell Varco) drilling rig equipment manuals
- Transocean, Seadrill, Odfjell Drilling rig-specific procedures (when cited with operator approval)

Vendor manuals are whitelisted only when they are the primary source for a specific piece of equipment. Default is to prefer neutral standards.

---

## 6. Article body structure

Every leaf article body follows this shape. Skip sections only if genuinely not applicable.

```markdown
## Overview

One to three paragraphs. What this is, why it matters on the NCS. No lists. Assumes prerequisite knowledge per the article's depth tier.

## Details

Main content. Subheadings (###) as needed. Depth-specific:
- foundational: principles, classifications, definitions
- operational: how it works in practice, operational envelopes, day-to-day use
- advanced: quantitative treatment, failure modes, standards interpretation

## NCS-specific context

How this manifests on the Norwegian Continental Shelf. Regulatory references, NCS operators and fields, NCS incident history, Norwegian working terms.

## Norwegian terminology

| Norwegian | English | Notes |
|---|---|---|
| example | example | context |

## Sources

1. NORSOK D-010 Rev 5 (2021). Standards Norway. Clause 6.2. Paywalled. Verified 2026-04-18.
2. ...
```

Optional sections: `## Related concepts`, `## Historical incidents`, `## Equipment and tools`.

---

## 7. Writing rules

### Pedagogical accessibility with technical depth (foundation rule, binding)

Every article is written for a reader who needs to become technically competent but is a beginner in the field. The article must be deeply technical AND easy to understand. Both together. Dense jargon that assumes prior domain knowledge fails the rule. Shallow summary that avoids the technical substance also fails the rule. Never assume prior knowledge. Always be pedagogical.

The foundation is repetition. Human memory decays. A reader who sees a term defined once, on page one, will not remember the definition on page three. The article keeps the definitions in front of the reader at all times, so the reader learns through repeated exposure rather than through effort. This is binding, not a style preference.

Concrete:

- **Every acronym is expanded at every single use**, not only at first use. If `BOP` appears thirty times, `BOP (Blowout Preventer)` appears thirty times. No exception for recent repetition in the same paragraph.
- **Every specialist term is redefined in plain language at every single use.** A single-clause gloss in parentheses. Example: `the driller (the worker who operates the drilling controls)` every time the term appears.
- **Every Norwegian term is translated at every single use.** Example: `the boreleder (drilling supervisor)` every time, not only first appearance.
- **Mechanisms are explained, not just named.** Describe how the thing works, not just what it is called.
- **Why a thing exists and what problem it solves comes before how it is used.**
- **Examples are NCS-concrete** when possible: specific fields, specific operators, specific equipment models and standards.
- **Analogies are allowed when they genuinely help the reader learn.** Never forced.
- **Paragraphs that would stack three or more undefined technical terms in a row must be broken up or rewritten.**

Prose runs longer under this rule. That cost is accepted. Depth floors absorb the overhead. Validator rules W-CON-03 (acronyms) and W-CON-06 (Norwegian terms) enforce the mechanical portion on every occurrence. The review agent catches specialist-term violations and articles that are dense-and-incomprehensible or simple-but-shallow.

### Mandatory

1. **Acronym expansion at every single use.** See the Pedagogical accessibility section above. Every acronym, every occurrence, every article. Examples: `BOP (Blowout Preventer)`, `ROP (Rate of Penetration)`, `NCS (Norwegian Continental Shelf)`.
2. **Norwegian term pairing at every single use.** See the Pedagogical accessibility section above. Every use, not only first. Examples: `the boreleder (drilling supervisor)`, `the boresjef (toolpusher)`, `the brønntekniker (well technician)`.
3. **No em dashes.** Use commas, periods, or restructure.
4. **Cite every substantive claim** with an `authoritative_sources` entry. In-text: `(<source-id>, <cited-section>)`.
5. **Meet the `depth` minimum word count and citation density** before marking `status: review`.
6. **NCS-specific context section mandatory** when `ncs_specific: true`.
7. **Cross-reference NCS drilling data against Sodir Factpages** (factpages.npd.no or factpages.sodir.no) and Diskos when discussing real NCS well data, field geology, or regional drilling history.

### Forbidden

1. Do not read other trees at write time. Scope is `drilling/` only.
2. Do not invent frontmatter fields.
3. Do not use enum values outside the sets in section 4.
4. Do not duplicate content owned by another tree (see section 2). Use `cross_domain`.
5. Do not reproduce NORSOK, API, ISO, or IWCF text verbatim. Summarize and cite.
6. Do not mark `status: published`. Only the validator promotes.
7. Do not write articles shorter than the `depth` minimum.

---

## 8. Cross-domain link construction

When linking to another tree, construct the path as:

```
<target-tree>/<chapter-folder>/<section-folder>/<slug>.md
```

Target trees: `subsea/`, `crane-and-logistics/`, `emergency-response/`.

Examples of typical drilling cross-domain links:

- BOP external interface (drilling → subsea):  
  `cross_domain: ["subsea/15-rov-systems-operations-missions/rov-missions-bop-interface/bop-stack-gvi-external.md"]`
- Post-kick emergency response escalation (drilling → emergency-response):  
  `cross_domain: ["emergency-response/22-major-accident-hazards-rnnp-and-investigation/major-accident-categories-storulykker/uncontrolled-well-flow-cross-link-only.md"]`
- Casing running crane operations (drilling → crane-and-logistics):  
  `cross_domain: ["crane-and-logistics/11-tubular-and-bulk-deck-handling/01-drill-pipe-and-casing-on-pipe-deck/tubular-slings-and-nylon-strops.md"]`

Write best-guess paths. The validator resolves or flags. Do not block on unverified links.

---

## 9. Special content rules for drilling

### Well-control articles

- Must reference NORSOK D-010 two-barrier philosophy explicitly.
- Kill-sheet articles must include an example calculation.
- Articles on shut-in procedures must distinguish hard vs soft shut-in and specify when each is used.
- Articles touching subsea well control must account for choke-line friction.

### BOP articles

- Must distinguish surface vs subsea BOP stack configurations.
- Ram taxonomy articles reference API Spec 16A.
- Control system articles reference API Spec 16D.
- Testing articles reference API STD 53 and NORSOK D-010 test interval requirements.

### Cement and P&A articles

- Primary cementing articles must reference API RP 10B testing.
- P&A articles must reference NORSOK D-010 plug categories (primary, secondary, environmental).
- NCS P&A articles must cite the 100m MD primary plug rule where applicable.

### Directional drilling

- Must distinguish sliding vs rotating modes.
- Tool articles (mud motors, RSS) must reference torque and drag implications.
- Anti-collision articles must reference the ellipse of uncertainty from the survey chapter.

### Incident case studies

- NCS incidents preferred: Bravo blowout Ekofisk 1977, Snorre A gas blowout 2004, Gullfaks C well control incident 2010, Alexander L Kielland 1980 (structural, not well-control).
- Macondo 2010 and Piper Alpha 1988 permitted as cross-industry context articles.
- Every incident article must cite the authoritative investigation report (Havtil, AIBN, BOEMRE, Cullen Inquiry as applicable).

---

## 10. Validator behaviour (summary)

The validator runs on every push and enforces:

- Schema compliance (errors: block publication)
- Identity integrity: `id` unique, `slug` matches filename, `domain` matches tree
- Path integrity: folder names conform to `_PATH_CONVENTIONS.md` conventions
- Relationship resolution: `related` must resolve in-tree (error); `cross_domain` may be unresolved temporarily (warning, logged to `_UNRESOLVED_LINKS.md`)
- Publication gates: word count, citation density, source verification dates, complete frontmatter

Full rule reference at vault root: `_VALIDATION.md`.

---

## 11. Escalation

If an agent encounters:

- A topic that cannot be cited from the whitelist → write at `status: draft`, flag with `TODO` for human review.
- A genuine cross-tree boundary ambiguity (is this drilling or well-control?) → write to drilling side with a TODO noting the ambiguity.
- A conflict between IWCF and NORSOK D-010 guidance → cite both, note the conflict, do not pick sides.
- Content that could fit multiple drilling chapters → prefer the canonical home specified in the folder's `_INDEX.md`; if none, write to the most specific chapter.

All escalations surface to the `_TODO_QUEUE.md` that the validator compiles.

---

## 12. Version and sync

This file is a self-contained copy of the root masters plus drilling-specific additions. When the root masters change (`offshore-vault/_SCHEMA.md`, `_CONTROLLED_VOCABULARY.md`, `_PATH_CONVENTIONS.md`, `_AGENT_RULES.md`, `_VALIDATION.md`), run `_sync.sh` from the vault root to propagate changes into this file.

Drilling-specific content (sections 1, 2, 5, 9, 11) is NOT synced from masters. Those sections are maintained in this file directly.
