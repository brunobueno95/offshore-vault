# _CONTROLLED_VOCABULARY.md — master enums

**Version:** 1.0  
**Scope:** root-level constrained fields applicable across all trees

This file defines the allowed values for enum fields in the schema. Per-tree `_TOPICS.md` files define tree-specific topic vocabularies separately; those are not in this file.

---

## `type` (article type)

Every leaf article has exactly one type.

| Value | Meaning | Example |
|---|---|---|
| `concept` | Fundamental idea, principle, physics, or theory. Not a specific piece of equipment or procedure. | `hydrostatic-pressure.md`, `cold-shock-response.md` |
| `equipment` | A specific tool, machine, piece of hardware, or identifiable product line. | `blowout-preventer.md`, `schilling-uhd-iii.md` |
| `procedure` | Step-by-step operation or method. | `hard-shut-in.md`, `driller-method-two-circulation.md` |
| `incident` | Case study of a named past event. | `piper-alpha-1988.md`, `macondo-2010.md` |
| `standard` | A regulation, specification, code, or company document. | `norsok-d-010.md`, `api-spec-16a.md` |
| `role` | A job function or responsibility description. | `roustabout.md`, `toolpusher.md`, `hlo.md` |
| `view` | A cross-cutting thematic index assembled from other articles. Lives in `_VIEWS/`. | `by-iwcf-level-2-topic.md` |
| `tool` | Software, calculator, or digital reference. Rare. | `drops-calculator.md` |

Choose based on the primary function of the article. If an article covers both a concept and a procedure, pick the one the reader is most likely to seek.

---

## `status` (lifecycle state)

| Value | Meaning |
|---|---|
| `draft` | New or in-progress. Not subject to validator acceptance checks beyond schema presence. |
| `review` | Agent has finished drafting. Awaiting human review or cross-validation. |
| `published` | Validator has confirmed all publication requirements (see `_SCHEMA.md`). Content is considered canonical. |
| `archived` | Superseded, deprecated, or no longer relevant. Kept in vault for historical traceability. |

Transitions are one-directional except `published` back to `review` (when a source goes stale or content needs update).

---

## `domain` (tree membership)

| Value | Tree folder |
|---|---|
| `drilling` | `drilling/` |
| `crane-and-logistics` | `crane-and-logistics/` |
| `subsea` | `subsea/` |
| `emergency-response` | `emergency-response/` |

An article's `domain` must match the tree it physically lives in. Validator enforces this.

---

## `depth` (content depth tier)

Controls minimum word count and citation density.

| Value | Use for | Min word count | Min citation density |
|---|---|---|---|
| `foundational` | Entry-level concepts, definitions, overview articles. Assumes no prior knowledge. | 800 | 1 claim per 150 words |
| `operational` | Working-level articles for someone performing the role. Assumes foundational knowledge. | 1500 | 1 claim per 100 words |
| `advanced` | Deep technical treatments suitable for experts, engineering analysis, standards interpretation. | 3000 | 1 claim per 75 words |

Depth is chosen by the agent at drafting based on what the article needs to convey. The validator enforces minimums.

---

## `life_cycle_phases` (field life-cycle applicability)

A single article may apply to multiple phases.

| Value | Meaning |
|---|---|
| `exploration` | Seismic, wildcat, pre-appraisal phase. |
| `drilling` | Well construction phase, from spud to TD. |
| `completion` | Completion running, perforation, clean-up to first flow. |
| `production` | Steady-state production, monitoring, routine intervention. |
| `intervention` | Wireline, CT, snubbing, workover operations. |
| `suspension` | Temporary abandonment with intent to return. |
| `p-and-a` | Permanent plug and abandonment. |
| `decommissioning` | Infrastructure removal, seabed reversion, cessation. |

---

## `access` (source accessibility; used inside `authoritative_sources`)

| Value | Meaning |
|---|---|
| `open` | Freely accessible on the public internet, no paywall, no login. |
| `paywalled` | Requires purchase or subscription. Examples: most NORSOK standards from Standard Norge, API standards. |
| `restricted` | Internal or operator-specific, access controlled by the originator. Examples: operator TRs, rig-specific procedures. |

---

## `relevant_to_roles` (NCS role taxonomy)

Allowed role values. Extensible via human-approved proposal.

### Drilling floor and leadership

- `roustabout` (dekksarbeider)
- `roughneck` (boredekksarbeider)
- `floorman`
- `derrickhand` (tårnmann)
- `assistant-driller` (assisterende borer)
- `driller` (borer)
- `toolpusher` (borebas / boresjef)
- `senior-toolpusher`
- `oim` (offshore installation manager / plattformsjef)

### Crane and deck

- `crane-operator` (kranfører)
- `rigger` (anhuker / rigger)
- `banksman` (signalgiver)
- `lift-supervisor` (løfteleder)
- `materialkoordinator` (materials coordinator)

### Subsea and diving

- `rov-pilot`
- `rov-supervisor`
- `rov-superintendent`
- `saturation-diver`

### Emergency response and support

- `medic` (sykepleier offshore)
- `radio-operator`
- `hlo` (helicopter landing officer)
- `hda` (helideck assistant)
- `fire-team-member` (brannlag)
- `rescue-team-member` (redningslag)

### Operator representatives

- `drilling-supervisor` (boreleder)
- `drilling-engineer`
- `wellsite-geologist`
- `completion-engineer`

### Service company

- `mud-engineer`
- `mud-logger`
- `directional-driller`
- `mwd-engineer`
- `cementer`
- `wireline-engineer`
- `coiled-tubing-supervisor`

---

## `ncs_specific` (boolean)

| Value | Use when |
|---|---|
| `true` | Article contains NCS-specific content: Norwegian regulations, NCS fields, Norwegian-language working terms, operator names active on NCS, NCS historical incidents. |
| `false` | General industry knowledge applicable anywhere: physics of drilling, global standards, universal equipment design. |

Default is `true` for this vault. Agents set `false` only when content is genuinely not NCS-specific.

---

## Proposing additions

To add a value to any enum here, write the proposal as a GitHub issue or append to a `_PROPOSALS.md` file at this root. Human approval required before the value enters this file. Per-tree `CLAUDE.md` files resync from this file via `_sync.sh`.
