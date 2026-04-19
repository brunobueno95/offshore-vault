# _VERIFICATION_FINDINGS.md — Subsea tree

Research findings captured during the subsea tree design phase. These are "facts as of build date" and drive content in the tree. Items marked **re-verify** must be revisited quarterly or when a major event (acquisition, merger, regulation change) suggests the underlying fact has moved.

Build date of this file: see `created` field in `_INDEX.md` at tree root.

Schema version: `1.0`.

---

## Confirmed facts (stable at time of build)

### Norwegian regulatory bodies

- **Sokkeldirektoratet (Sodir)** replaced Oljedirektoratet (NPD) on 1 January 2024. Confirmed via sodir.no.
- **Havtil (Havindustritilsynet / Norwegian Ocean Industry Authority)** replaced Petroleumstilsynet (Ptil) on 1 January 2024. Confirmed via havtil.no.
- **Offshore Norge** is the industry association, formerly Norsk olje og gass, rebranded 2022. NHO-affiliated but operates as its own organisation. Not a merger. Guideline numbering (for example 070, 090, 117) remains stable across the rebrand.

### API 17 / ISO 13628 parallel series

- **ISO 13628-1:2025** published January 2025, technically equivalent to API RP 17A 6th Ed.
- **API 17J 5th Ed** published May 2024 (flexible pipe specification).
- **API 17E** at 5th Ed (umbilicals).
- **API 17D 3rd Ed** aligned with ISO 13628-4 (wellhead and tree equipment).
- **API 17H 3rd Ed** current (ROV interfaces). **ISO 13628-8:2002** is the lapsed international edition but remains referenced.
- Parallel relationship between ISO 13628 and API 17 is maintained as a policy, but revision cycles are no longer synchronised. Articles that cite one edition should acknowledge the other.

### IMCA guidance

- **IMCA R 004 Rev 6** published February 2024. Reference for ROV operations.
- **IMCA R 006 Rev 2** current (ROV audit).
- **IMCA C-series** — personnel competence (formerly R 002).

### NORSOK U-series

- **NORSOK U-100 Ed 5 (2015)** with 2020 corrigendum in force for manned underwater operations on the NCS.
- **NORSOK U-101 Ed 3** current (diving respiratory equipment).
- **NORSOK U-103 Ed 2** current (inshore manned underwater operations).

### ROV manufacturers

- **Schilling Robotics** wholly owned by TechnipFMC since 2012.
- **Kystdesign** acquired by Chouest Group on 19 March 2025. Folder name in this tree reflects this: `kystdesign-chouest-owned-2025/`. ROV manufacturer articles must reflect the new ownership.
- **Forum Energy Technologies** still markets the Perry/Triton legacy models (XLX-C, XLS, Comanche, Triton, Mohawk).
- **Saab Seaeye** current lineup: Leopard, Jaguar, Panther-Plus, Cougar-XT, Falcon, Tiger, Sabertooth (hybrid AUV/ROV).
- **SMD** current Q-series: Quasar, Quantum, Quest, plus Atom (compact WROV).
- **Oceaneering** current WROV fleet: Millennium Plus, Magnum Plus, NEXXUS, Isurus (high-current), Spectrum (observation), Freedom (resident).

### Contractor landscape (NCS)

- **Subsea7 / Saipem merger**: agreement signed 24 July 2025, closing expected H2 2026 under the **Saipem7** name. At time of build the two operate separately. Articles should cite either Subsea7 or Saipem (not Saipem7) for anything describing current operations.
- **DOF Group** (formerly DOF Subsea, rebranded to DOF).
- **DeepOcean** headquartered in Haugesund.
- **Reach Subsea** headquartered in Haugesund.
- **IKM Subsea** based in Bryne.
- **TechnipFMC** operates its own ROV fleet on the NCS.
- **Equinor does NOT operate in-house ROVs.** Equinor contracts all ROV services.
- **TIOS AS** is a joint venture between Subsea7 and Equinor that runs Riserless Light Well Intervention (RLWI) operations on the NCS.

### NCS subsea milestones

- **Ekofisk 1971**: first NCS production (fixed platform, not subsea).
- **Tommeliten 1978**: first NCS subsea production well.
- **Troll A 1996**: first long subsea tieback on NCS.
- **Snøhvit 2007**: first Arctic subsea-to-LNG (143 km to Melkøya).
- **Tordis 2007**: world's first Subsea Separation, Boosting, and Injection (SSBI).
- **Åsgard 2015**: world's first subsea gas compression, onstream September 2015.
- **Gullfaks 2015**: wet gas compression.
- **Aasta Hansteen**: first oil 16 December 2018, with 482 km Polarled gas export to Nyhamna.
- **Vigdis Booster Station 2022**: **world's first all-electric subsea control system**. Not Snorre Expansion. This is a commonly-misattributed milestone and must be written correctly in any article.
- **Ormen Lange subsea compression station**: installed 2023 (second subsea gas compression on NCS after Åsgard).

### All-electric subsea control clarifications

- **Vigdis Booster Station (2022)** is the world-first all-electric subsea control (AES).
- **Snorre Expansion** uses **MUX (electro-hydraulic multiplex)**, not AES.
- **Troll C** is moving toward AES but not yet operational at build date.

### Field architecture classifications (listed NCS fields)

- **Pure subsea tiebacks with no platform at the field**: Nova, Dvalin.
- **Surface hosts present (subsea tie-ins to a surface facility at field)**: Martin Linge, Njord, Skarv.
- **Platform complex with subsea tie-in wells**: Johan Sverdrup.
- Articles must use the correct classification. "Subsea field" without qualification is wrong for Martin Linge, Njord, Skarv, and Johan Sverdrup.

### Scope separation (owned by other trees)

- BOP internal mechanics, API 16A/16D/53 compliance, ram taxonomy, well-control kick/choke hydraulics, marine drilling risers, and casing/cementing operations: **owned by `drilling/`**.
- However, every ROV task that interfaces against a BOP (stack inspection, hot stabbing, pod retrieval, emergency shear ram activation, disconnect monitoring, LMRP separation video): **stays in subsea**, under `15-rov-systems-operations-missions/rov-missions-bop-interface/`. Those leaves reference drilling BOP theory via `cross_domain`.

---

## Items to re-verify quarterly

These facts move. The build date of this file is the reference point.

- **ROV manufacturer model lineups** (Saab Seaeye, SMD, Oceaneering, Forum, Schilling). Lineups evolve with new releases and discontinuations.
- **NCS subsea and ROV contractor list**. Market consolidation, new entrants, and exits.
- **Subsea7 / Saipem merger closing status**. Once closed, all affected articles need editing to reflect the Saipem7 name and single-entity operations.
- **ISO 13628 revision schedule**. Parts revise independently.
- **API 17 series revisions**. Parts revise independently.
- **IMCA guidance revisions**. R-series, D-series, C-series, S-series can all bump independently.
- **Kystdesign product lineup and branding** under Chouest Group ownership. Products may be renamed or discontinued.
- **Troll C AES status**. Not operational at build date; check operational status each quarter.

---

## Known open questions

These remain unresolved at build time. Content-fill agents should leave articles touching these in `status: draft` and flag `tag: unresolved` until a human reviewer closes the question.

1. Exact revision status of NORSOK U-002 (subsea structures). Last confirmed edition and date need re-verification.
2. Current Equinor ROV framework contract structure and incumbents. Known to be contracted-out, but per-field contractor assignments change.
3. Hyperbaric rescue vessel coverage on the NCS. Specific vessels and rotation schedule need confirmation per area.
4. Status of OSPAR Decision 98/3 amendments relevant to subsea infrastructure leave-in-place.
5. Per-operator alliance standard disclosure rules. Articles citing Aker BP alliance standards or Equinor TRs may be restricted from reproducing content; paraphrase and cite only.

---

## Source notes

This findings block was compiled from:

- sodir.no and havtil.no (regulatory authority transitions)
- offshorenorge.no (industry body identity)
- iso.org, api.org (standards status)
- imca-int.com (IMCA guidance revisions)
- Standard Norge catalogue (NORSOK editions)
- Operator press releases and annual reports (milestones, field architectures)
- ROV manufacturer product pages (active lineups)
- Subsea7 and Saipem joint press release of 24 July 2025 (merger status)
- Edison Chouest Offshore press release of 19 March 2025 (Kystdesign acquisition)

Articles in this tree may cite the underlying standards and operator sources directly. This findings file is a design artefact and is not itself cited in article bodies.
