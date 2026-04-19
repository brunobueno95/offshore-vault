# CLAUDE.md — crane-and-logistics tree

**Scope:** agents working in the `crane-and-logistics/` tree of `offshore-vault/` read this file and nothing else at the vault root. This file is self-contained.

**Last synced from root masters:** 2026-04-19 (initial build)  
**Schema version:** 1.0

---

## 1. What this tree covers

NCS (Norwegian Continental Shelf) offshore crane operation, rig and platform logistics, and lifting ecosystem. Everything a Norwegian G5 crane operator, dekksbas, lofteleder, rigger, or materialkoordinator touches in daily work.

Twenty-seven top-level chapters, organised in three thematic groupings (chapters were flattened from Area A / B / C during normalisation):

**Chapters 01-07: Core offshore crane operation**
1. G5 Offshorekran Fundamentals
2. Heave Compensation and Dynamic Lift Control
3. G4 Traverskran Offshore
4. G20 Fastmontert Hydraulisk Kran Offshore
5. Personnel Transfer Cranes and Man Riding
6. Crane Pre-Use and Periodic Inspection Regime
7. Certification Path for NCS Crane Operator

**Chapters 08-15: Offshore rig and platform logistics**
8. Installation Deck Layout and Zoning
9. DROPS (Dropped Object Prevention Offshore)
10. Cargo Carrying Units (CCU)
11. Tubular and Bulk Deck Handling
12. Offshore Cargo Securing and Sea Fastening
13. Hazardous Cargo Offshore
14. Offshore Materials Coordination
15. Offshore Forklift Operations Verified

**Chapters 16-27: Offshore lifting ecosystem**
16. Wire Rope Slings and Discard Criteria
17. Chain and Synthetic Slings
18. Shackles, Hooks and Rigging Hardware
19. Color Coding and Traceability Systems
20. Standards Stack for Offshore Lifting
21. Norwegian Regulatory Framework Offshore
22. Offshore Environmental and Operational Context
23. Fall Protection Offshore Specific
24. Supply Vessel Interface and Cargo Operations
25. Permit to Work and Lift Planning Offshore
26. NCS Industry Ecosystem and Career
27. Documentation and Emerging Technology

---

## 2. Scope boundaries (what this tree does NOT own)

- **Subsea lift dynamics and splash zone analysis quantitative treatment** beyond operator-facing envelopes: lives in `subsea/11-installation-methods-and-vessels/`. Crane owns the operational aspect (DAF awareness, DNV-RP-H103 reference, guide wire setup, AHC operator mode).
- **ROV-assisted subsea operations** (seabed landing, ROV tooling, metrology, umbilical lay): lives in `subsea/`. Crane owns only the above-water crane and rigging aspects.
- **Well-control and BOP content**: lives in `drilling/`. Crane may reference BOP stack handling (G4 in BOP shop, BOP transport on deck) but does not duplicate well-control equipment content.
- **Emergency response and beredskap**: lives in `emergency-response/`. Crane references LARA lifeboat davits (NORSOK R-002 Annex A) as an adjacent skill but does not own evacuation doctrine.
- **Helicopter operations and helideck regulation**: lives in `emergency-response/04-helicopter-transport-and-helideck-operations/`. Crane owns only the crane-side interface (G20 refueling crane, slew restrictions during helicopter ops, crane / HLO coordination).
- **Supply vessel deep technical details** (DP system architecture, vessel design, marine engineering): out of scope. Crane owns the cargo-operations-facing aspects of PSV, AHTS, OSCV, W2W vessels.
- **Drilling operations and drilling rig equipment** (drawworks, top drive, rotary table, mud pumps): lives in `drilling/04-rig-equipment-and-systems/`. Crane does not duplicate.

---

## 3. Frontmatter schema (v1.0)

Every leaf article in this tree uses the schema below. Validator enforces it.

```yaml
---
schema_version: "1.0"

id: "crane-and-logistics-<slug>"
title: "Article title in English"
title_no: "Artikkeltittel på norsk"
slug: "kebab-case-slug"
type: concept                        # ENUM: concept | equipment | procedure | incident | standard | role | view | tool
status: draft                        # ENUM: draft | review | published | archived

domain: crane-and-logistics          # always this value for this tree
folder: "01-chapter/02-section"
parents: []
siblings: []

topics: []                           # constrained by _TOPICS.md (this tree)
life_cycle_phases: []                # ENUM list: exploration | drilling | completion | production | intervention | suspension | p-and-a | decommissioning
depth: foundational                  # ENUM: foundational | operational | advanced
perspective: []

authoritative_sources: []            # structured objects, see section 5
reference_textbooks: []
related_incidents: []

related: []
cross_domain: []

relevant_to_roles: []                # ENUM list, see section 4

ncs_specific: true
norwegian_terms: []

authors: []
created: "2026-04-19"
updated: "2026-04-19"
review_due: null
tags: []

citation_density: null               # validator-computed
word_count: null                     # validator-computed
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

Minimums:
- `foundational`: 800 words, 1 citation per 150 words
- `operational`: 1500 words, 1 citation per 100 words
- `advanced`: 3000 words, 1 citation per 75 words

### `life_cycle_phases`
`exploration | drilling | completion | production | intervention | suspension | p-and-a | decommissioning`

### `access` (inside `authoritative_sources`)
`open | paywalled | restricted`

### `relevant_to_roles` (crane-and-logistics subset)

Crane and deck:
- `crane-operator` (kranfører)
- `rigger` (anhuker)
- `banksman` (signalgiver)
- `lift-supervisor` (løfteleder)
- `materialkoordinator` (materials coordinator)
- `dekksarbeider` (deckhand, entry role)
- `dekksbas` (deck foreman)

Drilling floor (interface roles relevant to lifting):
- `roustabout`
- `roughneck`
- `driller`
- `toolpusher`

Emergency response interface:
- `hlo` (helicopter landing officer)
- `hda` (helideck assistant)

Leadership:
- `oim` (offshore installation manager / plattformsjef)

### `ncs_specific`
`true | false`

---

## 5. Authoritative source whitelist

Sources accepted without flagging. Outside this list triggers `W-AUTH-01` warning.

### Norwegian regulatory

- **Havtil** (Havindustritilsynet, formerly Petroleumstilsynet) regulations
  - Rammeforskriften, Styringsforskriften, Innretningsforskriften
  - Aktivitetsforskriften, Teknisk og operasjonell forskrift (MODU regime)
  - Havtil tilsynsrapporter (audit reports as learning material)
- **Sjøfartsdirektoratet**
  - FOR 2017-12-21-2381 (kran og løft)
  - MODU lifting equipment regime
- **FUA** (Forskrift om utførelse av arbeid, chapter 10 — løfteutstyr og løfteoperasjoner)
  - §10-3, §10-4, §10-5
  - Chapter 17 (arbeid i høyden), Chapter 18 (fallsikring)
- **Arbeidstilsynet** guidance where applicable (onshore interface, lifting basics)
- **Samarbeidsrådet Petroleum** opplæringsplaner (renamed from Samarbeidsrådet in 2019)
  - Modul 1-1, 2-3, P-2.1, P-3.1, P-4.1, P-4.2
- **Sentralregisteret** (Stiftelsen) kompetansebevis registry
- **Stralevernet / DSA** (Direktoratet for strålevern og atomsikkerhet) for NORM
- **Miljødirektoratet** for environmental regulations on waste and chemical discharge
- **Luftfartstilsynet** (CAA Norway) for helideck interface (BSL D 5-1)

### NORSOK standards

- NORSOK R-002 — Lifting equipment (design) Ed 3 (2017) with AC:2019
  - Annex A (LARA lifesaving), D (drilling area), G (cranes), H (foundations and suspensions)
- NORSOK R-003 — Safe use of lifting equipment
  - Roles per kap 4-7 and Annex A
  - Sakkyndig kontroll regime
  - §6.5 (lifting and stacking trucks)
  - Annex E-H (inspection scope)
- NORSOK R-005 — Onshore petroleum plants (brief reference only)
- NORSOK C-004 — Helideck design (referenced when helideck crane interface discussed)
- NORSOK N-003 — Climatic loads (cold-climate crane operations)
- NORSOK S-001 — Technical safety (brief reference)

### Offshore Norge guidelines

- 024 — Drilling and well competence (man-riding reference)
- 102 — Historical lifting reference (noted as historical, not primary)
- 113 — Fall protection (fallsikring og fallredning, 20 October 2020)
- 116 — Packing, securing and transport of cargo (replacing OLF 116)

### ISO and EN standards

- ISO 4306 — Crane vocabulary
- ISO 4309 — Wire rope discard criteria
- ISO 10855 — Offshore containers (harmonised with DNV 2.7-1)
- ISO 13849 — Safety of machinery (performance levels)
- ISO 16715 — Crane hand signals
- EN 818 — Chain sling assemblies
- EN 361 — Full body harness
- EN 355 — Energy absorbing lanyard
- EN 360 — Retractable fall arrester
- EN 1492-1 — Webbing slings
- EN 1492-2 — Synthetic round slings
- EN 12079 — Offshore containers
- EN 13852-1 — General purpose offshore crane
- EN 13852-2 — Floating offshore crane
- EN 13852-3 — Light offshore crane

### DNV standards

- DNV 2.7-1 — Offshore containers
- DNV 2.7-2 — Offshore service modules
- DNV 2.7-3 — Portable offshore units
- DNV-ST-0378 — Offshore and platform lifting appliances
- DNV-RP-H103 — Modelling of marine operations
- DNV-OS-H205 — Lifting operations
- DNV class interface (ABS, BV, LR) as context

### API standards

- API Spec 2C — Offshore pedestal crane design
- API RP 2D — Operation and maintenance

### IMCA

- IMCA M 179 — Lifting operations
- IMCA M 187 — Lifting on vessels
- IMCA SEL series (for diving interface awareness)

### Vendor manuals (when sole authoritative source)

- Konecranes, Stahl, Demag (G4 bridge cranes)
- Palfinger, HIAB, Heila, Dreggen (G20 knuckle boom cranes)
- Reflex Marine (FROG / TORO personnel transfer capsules)
- Billy Pugh (X-904 personnel net)
- Ampelmann, Uptime International, Barge Master (W2W gangways)
- Crosby, Green Pin (shackles)
- NOV, MacGregor, Huisman (large offshore cranes)
- Kongsberg (MRU motion reference units)
- Parker, Sauer Danfoss (hydraulic systems)
- Pyroban, Miretti (ATEX forklift conversion)

Vendor manuals are whitelisted only when the primary source for a specific product. Prefer neutral standards otherwise.

### Operator-specific (restricted access, cite with approval)

- Equinor TRs (Technical Requirements) — governance docs for Equinor-operated installations
- Aker BP governing documents
- Shell DEPs (Design and Engineering Practices)
- TotalEnergies General Specifications
- Var Energi client specifications

---

## 6. Article body structure

Every leaf article body follows this shape. Skip only if genuinely not applicable.

```markdown
## Overview

One to three paragraphs. What this is, why it matters on the NCS. No lists.

## Details

Main content. Subheadings (###) as needed.

## NCS-specific context

Regulatory references, NCS operators and installations, Norwegian working terms, NCS incident or inspection history.

## Norwegian terminology

| Norwegian | English | Notes |
|---|---|---|
| kranfører | crane operator | G5 competence holder on NCS |

## Sources

1. NORSOK R-003N (current edition). Standards Norway. §6.5. Paywalled. Verified 2026-04-18.
2. ...
```

Optional sections: `## Related concepts`, `## Historical incidents`, `## Equipment and tools`.

---

## 7. Writing rules

### Mandatory

1. **Acronym expansion on first use.** `G5 (NCS Offshore Pedestal Crane)`, `CCU (Cargo Carrying Unit)`, `SWL (Safe Working Load)`, `WLL (Working Load Limit)`, `LMI (Load Moment Indicator)`, `AHC (Active Heave Compensation)`, `DROPS (Dropped Object Prevention Scheme)`, `SIMOPS (Simultaneous Operations)`, `LMRA (Last Minute Risk Assessment)`, `SJA (Sikker Jobb Analyse)`.
2. **Norwegian term pairing on first use.** `kranfører (crane operator)`, `løfteleder (lift supervisor)`, `anhuker (rigger)`, `signalgiver (banksman)`, `sakkyndig kontroll (competent inspection)`, `kranbok (crane logbook)`, `rødsone (red zone under crane)`.
3. **Rigging angle convention: dual reference mandatory.** Any article discussing sling angles MUST state both the Crosby/international horizontal reference AND the Norwegian arbeidsvinkel (working angle from vertical, summing to 90). Include the mini conversion table in every rigging section:

| Horizontal | Arbeidsvinkel | WLL |
|---|---|---|
| 60° | 30° | Full |
| 45° | 45° | ~70% |
| 30° | 60° | ~50% |
| < 30° | > 60° | Forbidden |

This is a safety-critical repetition rule. Every rigging section. Every time.

4. **Bolt-type bow shackle standard on NCS.** When shackle type is mentioned, name the full spec on first use: "bolt-type safety bow shackle with double-locking pin (bolt, nut, cotter) per NORSOK R-003 and R-005". D-shackles and screw-pin shackles are NOT used offshore on NCS.

5. **No em dashes.** Use commas, periods, or restructure.

6. **Cite every substantive claim** from the whitelist in section 5.

7. **Meet `depth` word count and citation density before `status: review`.**

### Forbidden

1. Do not read other trees at write time.
2. Do not invent frontmatter fields.
3. Do not reproduce NORSOK, ISO, DNV, API, EN text verbatim. Summarize and cite.
4. Do not duplicate subsea lift analysis beyond operator-facing envelopes.
5. Do not mark `status: published`. Validator only.
6. Do not write shorter than the `depth` minimum.
7. Do not frame D-shackle or screw-pin shackle as an NCS rigger's choice. NORSOK makes the choice.

---

## 8. Cross-domain link construction

```
<target-tree>/<chapter-folder>/<section-folder>/<slug>.md
```

Common crane cross-domain targets:

- Subsea lift analysis (crane → subsea):  
  `cross_domain: ["subsea/11-installation-methods-and-vessels/subsea-lifts/dnv-st-n001-marine-operations.md"]`
- Helideck interface (crane → emergency-response):  
  `cross_domain: ["emergency-response/04-helicopter-transport-and-helideck-operations/helideck-regulation-stack/norsok-c-004-helideck-design.md"]`
- LARA lifeboat davits (crane → emergency-response):  
  `cross_domain: ["emergency-response/08-evacuation-means-lifeboats-and-liferafts/free-fall-lifeboat-ffl/norsok-r-002-reference-for-launch-appliance.md"]`
- BOP stack handling (crane → drilling):  
  `cross_domain: ["drilling/08-well-control-equipment/02-subsea-bop-stack/stack-configurations.md"]`

Validator resolves. Do not block.

---

## 9. Special content rules for crane-and-logistics

### Crane lifting articles

- All articles discussing crane capacity must state the SWL (Safe Working Load) reference convention being used and the boom radius at which the SWL is quoted.
- Load chart interpretation articles must reference API Spec 2C and note the derating effects for side loading, heave, and dynamic amplification.
- AHC articles must distinguish closed-loop AHC from passive heave compensation (PHC) and note the typical AHC efficiency rating of >95%.

### G4 / G5 / G20 certification articles

- G5 card implicitly covers G4 traverskran, G20 fastmontert kran, and G7 vinsj offshore (not onshore). State this explicitly in any article touching crane operator competence.
- G20 theory (Modul P-2.1, 16 hours) is a mandatory prerequisite before G5 theory (Modul P-3.1, 24 hours). Reference Samarbeidsrådet Petroleum training matrix.

### Rigging articles

- Mini angle-conversion table (rule 3 in section 7) mandatory.
- Bolt-type safety bow shackle with double-locking pin as the only NCS offshore shackle type (rule 4 in section 7).
- Wire rope discard criteria must cite ISO 4309. Discard thresholds for broken wire count, diameter reduction, corrosion, deformation, and heat damage.
- Sling WLL articles must distinguish between angle-at-horizontal convention and arbeidsvinkel convention.

### SIMOPS articles

- Must reference the installation's SIMOPS matrix and specify the stand-down triggers.
- Crane vs helicopter ops: crane slew restriction during helicopter approach is absolute. Note coordination with HLO via HSAC-lineage safety rationale.
- Crane vs diving/ROV ops: separation requirements from IMCA SEL ops guidance.
- Crane vs hot work: permit cross-check requirement.

### Forklift articles

- Standard NCS cert bundle is T1 + T2 + T4. State explicitly.
- T3 (narrow-aisle / order-picker / VNA / førerløftet) is effectively absent offshore. T5-T8 live at onshore supply bases (Dusavik, Tananger, Mongstad, CCB Ågotnes, Polarbase Hammerfest), not on installations.
- ATEX zoning drives electric-vs-diesel choice. Electric for non-classified or Zone 2 areas (stores, galley corridors, workshops). Diesel (Pyroban or Miretti ATEX conversion) for pipe deck and process areas under Zone 1 or Zone 2.
- No universal zone mandate across NCS operators; each installation sets its own per area classification drawing.

### Inspection regime articles

- Pre-use check (daglig kontroll) by operator, logged in kranbok.
- Annual sakkyndig kontroll by sakkyndig virksomhet A-1.
- Five-year major inspection per FOR 2017-12-21-2381, Sjøfartsdirektoratet A-1 approval on MODUs.
- NDT methods: MPI, UT, DP, eddy current, acoustic emission (awareness for slew ring).

### Incident case studies

- NCS lifting-related Havtil tilsynsrapporter preferred.
- HSAC (Helicopter Safety Advisory Conference) case of 19 fatalities from helicopter-crane collision referenced as historical safety rationale for crane slew restrictions.
- DROPS events library as cross-industry learning.

---

## 10. Validator behaviour (summary)

- Schema compliance: errors block publication.
- Identity integrity: unique `id`, `slug` matches filename, `domain` matches tree.
- Path integrity: per `_PATH_CONVENTIONS.md` rules.
- Relationship resolution: `related` in-tree (error if broken), `cross_domain` logged to `_UNRESOLVED_LINKS.md` (warning).
- Publication gates: word count, citation density, source verification dates.
- Authority whitelist: sources outside section 5 trigger warnings.
- Rigging rule compliance: articles with topics `rigging`, `slings`, `shackles`, `lift-planning` must contain the mini angle-conversion table (automated check when implemented).

Full rule reference at vault root: `_VALIDATION.md`.

---

## 11. Escalation

- Authority whitelist miss → draft the article, flag TODO for human review, do not block.
- Ambiguity between crane tree and subsea tree for a given lift topic → default to crane if the article is operator-facing (how the crane operator handles it) and subsea if the article is engineering-analysis-facing (dynamic amplification factor derivation, slamming force calculation).
- NORSOK vs Offshore Norge conflict → cite both, note the conflict, do not pick sides.
- G20 versus LARA overlap → LARA lifeboat davits (NORSOK R-002 Annex A) sit in the crane tree as an adjacent-skill article only. Full LARA content lives in `emergency-response/08-evacuation-means-lifeboats-and-liferafts/`.

---

## 12. Version and sync

This file is a self-contained copy of the root masters (as of 2026-04-19) plus crane-and-logistics-specific additions (sections 1, 2, 5, 9, 11). When root masters change, run `_sync.sh` from vault root.

Crane-specific content in sections 1, 2, 5, 9, 11 is maintained in this file directly, not synced.
