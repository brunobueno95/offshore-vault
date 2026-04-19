# CLAUDE.md — Subsea tree

Self-contained rules for agents operating inside `subsea/`. This file copies the core schema, vocabulary, conventions, agent rules, and validation behaviour from the vault root, and adds subsea-specific rules on top. An agent working in this tree does not need to read other trees at write time, and must not.

Schema version: `1.0`.

---

## 1. What this tree covers

Twenty chapters, ordered by conceptual dependency from NCS context through installed infrastructure, operations, and workforce pathways.

1. `01-foundations-and-ncs-context/` — scope separation against drilling and topsides, NCS basins, Norwegian terminology, history, regulatory authorities, industry bodies.
2. `02-subsea-production-systems-sps/` — wellheads, Christmas trees, tree valves, tree caps, wellhead connectors, tubing hangers, manifolds, templates, protection structures, SSIV/HIPPS, PLEM/PLET/ILT/ILS/ILY.
3. `03-subsea-control-systems/` — control architectures, topsides equipment, subsea control module (SCM), instrumentation, all-electric subsea control (AES), installation/workover control system (IWOCS), control fluid.
4. `04-umbilicals-flying-leads-terminations/` — umbilical types and construction, terminations (UTA, SUTA, TUTA, JUTA), flying leads, installation methods.
5. `05-flowlines-pipelines-thermal-management/` — flowline architectures, rigid and flexible pipeline, thermal insulation, pipeline attributes, pigging infrastructure.
6. `06-production-risers/` — riser types, configurations, interfaces to host, integrity.
7. `07-tie-in-and-connection-systems/` — jumpers, tie-in methods, connectors, metrology, installation aids.
8. `08-subsea-processing-ncs-specialty/` — separation, boosting, compression, subsea power distribution, qualification and reliability.
9. `09-flow-assurance-and-chemical-systems/` — hydrate, wax, scale, asphaltene, corrosion, MEG loop, chemical injection architecture.
10. `10-ncs-field-architectures-and-developments/` — host archetypes, tieback patterns, NCS field references, export pipelines, operator landscape.
11. `11-installation-methods-and-vessels/` — pipelay methods, pipelay vessels, CSV/MPSV/DSV/AHTS, installation spreads, subsea lifts, foundations, trenching, surveys.
12. `12-inspection-repair-maintenance-irm/` — IRM strategy, inspection techniques, pipeline integrity, structure inspection, repair options, leak detection, bolted joint work.
13. `13-subsea-intervention-strategy/` — intervention categories, rig-based, RLWI, RLWI contractors, through-tree techniques, tree/hanger operations, planning.
14. `14-subsea-plug-and-abandonment-pa/` — P&A phases, barrier philosophy, execution, wellhead severance tools, regulatory framework.
15. `15-rov-systems-operations-missions/` — classes per IMCA R 004, manufacturers and models, LARS, TMS, tether/umbilical, propulsion, sensors, manipulators, tooling interfaces, tooling suite, navigation, piloting, control cabin, crew, envelopes, mission types (inspection, construction, intervention, BOP interface, well-intervention support, survey, salvage, diving support), regulatory, NCS contractors, career ladder.
16. `16-diving-manned-underwater/` — dive modes, saturation diving, surface-supplied, dive spread, NCS DSVs, regulations, IMCA references, diver-owned tasks, ROV-owned tasks, historical shift, dive-to-ROV skill transfer.
17. `17-decommissioning-and-seabed-environment/` — regulatory frameworks, strategies, removal operations, environmental considerations, safety/environment.
18. `18-standards-and-regulations-consolidated/` — Havtil primary regulations, Sokkeldirektoratet resource management, NORSOK U-series and cross-discipline, Offshore Norge guidelines, API 17 / ISO 13628 parallel, DNV, ISO/IEC, IMCA, client specifications.
19. `19-life-cycle-and-project-phases/` — concept/feasibility through cessation/decommissioning.
20. `20-ncs-workforce-and-career-pathways/` — roustabout-to-subsea bridge, ROV technical pathway, diver-to-ROV transition, simulator training, survey/data pathway, subsea engineer long term, remote operations frontier, NCS contractor employers.

---

## 2. Scope boundaries (what this tree does NOT own)

Subsea is the installed seabed infrastructure plus its operations. Do not duplicate content that lives elsewhere in the vault. Use `cross_domain` references instead.

- **BOP internal mechanics, ram taxonomy, API 16A/16D/53 compliance, well-control kick/choke hydraulics, marine drilling risers, casing and cementing operations** live in `drilling/`. Subsea owns ROV-facing BOP interface tasks only, which live in `15-rov-systems-operations-missions/rov-missions-bop-interface/`.
- **Well-control theory and procedures** live in `drilling/07-well-control/` (exact path subject to the drilling tree's own structure). Subsea references these via `cross_domain` when relevant to intervention or P&A.
- **Crane and rigging mechanics above water** live in `crane-and-logistics/`. Subsea owns the below-water operational aspects of subsea lifts: splash-zone crossing plan, dynamic amplification factor per DNV-RP-H103, ROV interface and seabed landing, guide-wire systems, active heave compensation (AHC) for subsea cranes.
- **Post-ignition emergency response, fire, evacuation, search and rescue (SAR), oil spill response** live in `emergency-response/`. Subsea owns only pre-ignition subsea leak classification and reporting pathways.
- **Drilling rig equipment** (drawworks, top drive, mud pumps, drilling floor crew) lives in `drilling/`. Subsea does not duplicate.
- **Generic human factors theory** is cross-cutting metadata, not a subsea folder.

---

## 3. Frontmatter schema v1.0

Every leaf article uses this frontmatter verbatim. Unknown or not-yet-populated fields stay as shown.

```yaml
---
schema_version: "1.0"

id: "subsea-<slug>"
title: "Article title in English"
title_no: null
slug: "kebab-case-slug"
type: null
status: draft

domain: "subsea"
folder: "01-chapter/02-section"
parents: []
siblings: []

topics: []
life_cycle_phases: []
depth: null
perspective: []

authoritative_sources: []
reference_textbooks: []
related_incidents: []

related: []
cross_domain: []

relevant_to_roles: []

ncs_specific: true
norwegian_terms: []

authors: []
created: "<ISO-DATE>"
updated: "<ISO-DATE>"
review_due: null
tags: []

citation_density: null
word_count: null
---
```

Folder `_INDEX.md` uses this reduced frontmatter:

```yaml
---
schema_version: "1.0"
title: "Folder display title (parentheticals preserved)"
slug: "kebab-case-folder-name"
folder_scope: ""
contains_leaves: true
contains_subfolders: false
parent_folder: "relative/path/or/empty-string-at-root"
---
```

---

## 4. Allowed enum values

- `type`: `concept` | `equipment` | `procedure` | `incident` | `standard` | `role` | `view` | `tool`
- `status`: `draft` | `review` | `published` | `archived`
- `depth`: `foundational` | `operational` | `advanced`
- `life_cycle_phases` (list): `exploration` | `drilling` | `completion` | `production` | `intervention` | `suspension` | `p-and-a` | `decommissioning`
- `access` (if used downstream): defined in vault root `_CONTROLLED_VOCABULARY.md`
- `relevant_to_roles`: defined in vault root `_CONTROLLED_VOCABULARY.md` (common subsea values include `rov-pilot-technician`, `rov-supervisor`, `subsea-engineer`, `intervention-engineer`, `integrity-engineer`, `surveyor`, `diver`, `dive-supervisor`, `roustabout`, `crane-operator`)
- `ncs_specific`: boolean. Default `true` for this tree. Set `false` only when the article is generic and not NCS-tailored.

---

## 5. Authoritative source whitelist

Agents may cite only the sources listed here, plus any source explicitly added to the vault root `_CONTROLLED_VOCABULARY.md`. Citations to sources outside the whitelist fail validation.

**Norwegian regulatory**
- Havtil (Havindustritilsynet / Norwegian Ocean Industry Authority) regulations: Rammeforskriften, Styringsforskriften, Innretningsforskriften, Aktivitetsforskriften, Teknisk og operasjonell forskrift (TOF)
- Sokkeldirektoratet (Sodir) Ressursforskriften, Factpages, Diskos
- Klima- og miljødepartementet, Miljødirektoratet
- Arbeidstilsynet (inshore diving interface)

**NORSOK U-series (manned underwater and subsea)**
- NORSOK U-001 — Subsea production systems
- NORSOK U-002 — Subsea structures
- NORSOK U-009 — Life extension
- NORSOK U-100 Ed 5 (2015) with 2020 corrigendum — Manned underwater operations
- NORSOK U-101 Ed 3 — Diving respiratory equipment
- NORSOK U-103 Ed 2 — Inshore manned underwater operations

**NORSOK cross-discipline**
- NORSOK L-002, L-005, M-001, M-501, M-503, R-002, S-001, S-002, D-010 (reference only), Z-015

**API 17 series (subsea)**
- API 17A / ISO 13628-1 — General design operation
- API 17B / ISO 13628-11 — Flexible pipe recommended practice
- API 17C / ISO 13628-3 — Through-flowline (TFL)
- API 17D / ISO 13628-4 — Wellhead and tree equipment (3rd Ed aligned)
- API 17E / ISO 13628-5 — Umbilicals (5th Ed)
- API 17F / ISO 13628-6 — Production control
- API 17G / ISO 13628-7 — Completion / workover riser
- API 17H / ISO 13628-8 — ROV interfaces (API 17H 3rd Ed is current; ISO 13628-8:2002 has lapsed but is referenced)
- API 17I / ISO 13628-9 — ROV intervention systems
- API 17J — Flexible pipe specification (5th Ed, May 2024)
- API 17K, 17L, 17N, 17Q, 17R, 17S, 17T, 17TR, 17V

**ISO standards**
- ISO 13628 series (parallel to API 17)
- ISO 9001, 14001, 45001 (management systems)
- IEC 61508, 61511 (functional safety)

**IMCA guidance**
- IMCA R 004 Rev 6 (February 2024) — ROV operations
- IMCA R 006 Rev 2 — ROV audit
- IMCA R 025 — Simulator requirements
- IMCA C-series — Personnel competence (formerly R 002)
- IMCA D-series — Diving (D 014, D 022, D 023, D 024, D 040, D 050)
- IMCA S, M, SEL, HSE series

**DNV standards**
- DNV-OS-F101 — Submarine pipeline systems
- DNV-RP-F105 — Free spanning pipelines
- DNV-RP-F109 — On-bottom stability
- DNV-RP-F116 — Pipeline integrity management
- DNV-OS-F201 — Dynamic risers
- DNV-ST-N001 — Marine operations
- DNV-RP-A203 — Technology qualification
- DNV-RP-H103 — Modelling of marine operations (referenced for subsea lifts)

**Offshore Norge guidelines**
- 070 — SIL application (IEC 61508/61511)
- 090 — Common competence
- 117 — Well integrity
- 130 — Installation maintenance
- 135 — SIMOPS guidance

**Industry bodies**
- Society for Underwater Technology (SUT) publications
- IOGP reports
- Subsea 7, TechnipFMC, Saipem, Aker Solutions technical papers (when primary sources)

**Client specifications (restricted circulation)**
- Equinor TRs, Aker BP alliance standards, Shell DEPs, TotalEnergies GS, Var Energi specs

**ROV OEM manuals (when sole source)**
- TechnipFMC Schilling Robotics (HD, UHD III, Gemini, Titan 4, Orion)
- Oceaneering (Millennium Plus, Magnum Plus, NEXXUS, Isurus, Spectrum, Freedom)
- Forum Energy Technologies (XLX-C, XLS, Comanche, Triton, Mohawk)
- Saab Seaeye (Leopard, Jaguar, Panther-Plus, Cougar-XT, Falcon, Tiger, Sabertooth)
- Kystdesign, owned by Chouest Group since 19 March 2025 (Surveyor, Supporter, Constructor, Installer)
- SMD (Atom, Quantum, Quasar, Quest)
- Fugro (FCV), IKM Subsea (Merlin WR200), Argus Remote Systems
- Kongsberg (MRU, K-Sim ROV simulator, HiPAP, Seapath)
- Sonardyne (Ranger 2, Sprint MK2)
- Tritech (Gemini, Super SeaKing)
- Parker, Sauer Danfoss (hydraulic systems)

**Subsea OEM manuals**
- Aker Solutions, TechnipFMC, Dril-Quip, Cameron (subsea trees and wellheads)
- Framo (multiphase boosting pumps)
- MAN Hofim (subsea compression)
- Subsea 7, Saipem, Allseas (installation vessels and procedures)

---

## 6. Article body structure

Every leaf follows this body layout below the frontmatter. Sections may be empty in draft state but the headings must be present.

1. **Overview** — what the thing is, in plain English. One to three paragraphs. Acronym expansion on first use every article.
2. **Details** — the technical substance. Subsections depend on `type`. Equipment articles describe construction, ratings, interfaces, manufacturers. Procedures describe steps, hazards, witness points, acceptance criteria. Standards describe scope, key requirements, relationship to other standards. Concepts describe definitions, distinctions, mental models.
3. **NCS-specific context** — where and how this applies on the Norwegian Continental Shelf. Named fields, named operators, named contractors, named regulators. If nothing NCS-specific applies, say so and justify why the article belongs in this tree.
4. **Norwegian terminology** — Norwegian terms paired with English. Use the pairing format `Norwegian term (English gloss)`. Populate `norwegian_terms` in frontmatter with the same terms.
5. **Sources** — every substantive claim must have a citation from the section 5 whitelist. Include the standard name and the clause or chapter where practical.

---

## 7. Writing rules

### Pedagogical accessibility with technical depth (foundation rule, binding)

Every article is written for a reader who needs to become technically competent but is a beginner in the field. The article must be deeply technical AND easy to understand. Both together. Dense jargon that assumes prior domain knowledge fails the rule. Shallow summary that avoids the technical substance also fails the rule. Never assume prior knowledge. Always be pedagogical.

The foundation is repetition. Human memory decays. A reader who sees a term defined once, on page one, will not remember the definition on page three. The article keeps the definitions in front of the reader at all times, so the reader learns through repeated exposure rather than through effort. This is binding, not a style preference.

Concrete:

- **Every acronym is expanded at every single use**, not only at first use. If `ROV` appears thirty times, `ROV (Remotely Operated Vehicle)` appears thirty times. No exception for recent repetition in the same paragraph.
- **Every specialist term is redefined in plain language at every single use.** A single-clause gloss in parentheses. Example: `the christmas tree (the valve assembly sitting on top of a subsea well that controls flow)` every time the term appears.
- **Every Norwegian term is translated at every single use.** Example: `the undervannsfartøy (ROV, Remotely Operated Vehicle)` every time, not only first appearance.
- **Mechanisms are explained, not just named.** Describe how the thing works, not just what it is called.
- **Why a thing exists and what problem it solves comes before how it is used.**
- **Examples are NCS-concrete** when possible: specific fields, specific operators, specific equipment models and standards.
- **Analogies are allowed when they genuinely help the reader learn.** Never forced.
- **Paragraphs that would stack three or more undefined technical terms in a row must be broken up or rewritten.**

Prose runs longer under this rule. That cost is accepted. Depth floors absorb the overhead. Validator rules W-CON-03 (acronyms) and W-CON-06 (Norwegian terms) enforce the mechanical portion on every occurrence. The review agent catches specialist-term violations and articles that are dense-and-incomprehensible or simple-but-shallow.

**Mandatory**

1. Acronym expansion at every single use in every article. See the Pedagogical accessibility section above. Every acronym, every occurrence. Examples: `SPS (Subsea Production System)`, `SURF (Subsea Umbilicals Risers Flowlines)`, `HXT (Horizontal Xmas Tree)`, `SCM (Subsea Control Module)`, `SSIV (Subsea Isolation Valve)`, `HIPPS (High Integrity Pressure Protection System)`, `ILT / ILS / ILY (In-Line Tee / Sled / Wye)`, `MEG (Mono-Ethylene Glycol)`, `PLEM / PLET (Pipeline End Manifold / Termination)`, `ROV (Remotely Operated Vehicle)`, `AHC (Active Heave Compensation)`, `TMS (Tether Management System)`, `LARS (Launch and Recovery System)`, `USBL / LBL (Ultra-Short / Long Baseline acoustic positioning)`, `DVL (Doppler Velocity Log)`, `INS (Inertial Navigation System)`, `RLWI (Riserless Light Well Intervention)`, `EDP / LRP (Emergency Disconnect / Lower Riser Package)`, `IRM (Inspection Repair Maintenance)`.
2. Norwegian term pairing at every single use. See the Pedagogical accessibility section above. Every use, not only first. Canonical pairs: `undervannsproduksjon (subsea production)`, `juletre (christmas tree)`, `bronnramme (template)`, `havbunnskompresjon (subsea compression)`, `havbunnsseparasjon (subsea separation)`, `stigerorsystem (riser system)`, `kontrollkabel (umbilical)`, `rorledning (pipeline)`, `undervannsfartoy (ROV)`, `metningsdykking (saturation diving)`. Extend the list in `_CONTROLLED_VOCABULARY.md` if needed.
3. No em dashes. Use commas, periods, or restructure the sentence.
4. Cite every substantive claim from the section 5 whitelist.
5. Subsea content is authored one notch gentler than the equivalent tier in other trees. Subsea is a dense specialist domain and the intended reader population includes dive instructors transitioning to ROV work. Readability matters. Favour short paragraphs and explicit definitions over dense jargon walls.
6. Dive-to-ROV skill-transfer content in Chapter 16: always map the specific dive competence to the specific ROV competence. Every skill-transfer leaf includes both the transferable skill (for example: three-dimensional spatial awareness, current reading, buoyancy intuition, gas-budget planning) and the difference (no physical feedback, camera-mediated perception, longer task duration, remote team structure). This serves Bruno's specific transition path from 1000-plus dive PADI/CMAS instructor to ROV pilot-technician.

**Forbidden**

1. Do not read other trees at write time. Content must be self-contained within subsea plus the section 5 whitelist.
2. Do not duplicate BOP theory from `drilling/`. Reference via `cross_domain`.
3. Do not duplicate crane mechanics from `crane-and-logistics/`. Reference via `cross_domain`.
4. Do not reproduce NORSOK, API, ISO, IMCA, or DNV text verbatim. Paraphrase and cite. Quote only short excerpts where exact wording carries legal or technical weight.
5. Do not mark `status: published`. Skeleton agents and content-fill agents leave status at `draft` or `review`. Only a human reviewer sets `published`.

---

## 8. Cross-domain link construction

Cross-domain links point into sibling trees. Format: `tree/chapter/section/article-slug` without extension. Examples:

- From a subsea P&A leaf: `cross_domain: ["drilling/07-well-control/barrier-philosophy/two-barrier-principle"]`
- From a subsea lift leaf: `cross_domain: ["crane-and-logistics/11-offshore-lifting/dynamic-amplification-factor"]`
- From a pre-ignition subsea leak leaf: `cross_domain: ["emergency-response/hydrocarbon-release/post-ignition-response-playbook"]`
- From a Chapter 15 BOP interface leaf: `cross_domain: ["drilling/08-well-control-equipment/bop-stack-architecture", "drilling/08-well-control-equipment/ram-taxonomy"]`

Skeleton-build agents leave `cross_domain: []`. Content-fill agents populate.

---

## 9. Special content rules for subsea

- **Polyhierarchy via `related`**: some articles are referenced from more than one folder but have one canonical home. Canonical homes are fixed:
  - Torque tools: canonical in `15-rov-systems-operations-missions/rov-tooling-suite/` or `tooling-interfaces/`. Referenced from tie-in, IRM, and intervention chapters via `related`.
  - Templates: canonical in `02-subsea-production-systems-sps/templates-and-integrated-templates/`. Referenced from installation, IRM, and decommissioning.
  - Hot stabs: canonical in `15-rov-systems-operations-missions/tooling-interfaces/`. Referenced from control systems, flowlines, intervention.
  - Flying leads: canonical in `04-umbilicals-flying-leads-terminations/flying-leads/`. Referenced from control systems and intervention.

- **Chapter 15 ROV classes per IMCA R 004 Rev 6 (Feb 2024)**: every ROV-class article explicitly distinguishes Class I (pure observation), Class II (observation with payload), Class III (work-class, with light and heavy subdivisions), Class IV (towed and seabed working), Class V (prototype and development). No class article should leave the reader guessing which class a given vehicle belongs to.

- **Chapter 16 diving-to-ROV skill transfer**: targets Bruno's 1000-plus dive PADI/CMAS instructor background. Each skill-transfer leaf maps one specific dive competence to one specific ROV competence and explicitly states the key difference.

- **Chapter 15 BOP interface articles** (`rov-missions-bop-interface/`): operational ROV task focus only. Reference drilling BOP theory articles via `cross_domain`. Do not re-explain BOP taxonomy or ram types in subsea leaves.

- **ISO 13628 vs API 17 parallel**: both are cited where applicable. Note that parallel revision cycles are no longer synchronised: API 17J 5th Ed (May 2024), ISO 13628-1:2025 (January 2025, technically equivalent to API RP 17A 6th Ed), API 17D 3rd Ed aligned with ISO 13628-4, API 17H 3rd Ed current, ISO 13628-8:2002 lapsed but referenced.

- **Current NCS ROV and subsea contractors**: DeepOcean (Haugesund), Reach Subsea, Subsea7, Saipem, TechnipFMC (which operates its own ROV fleet), Oceaneering, DOF Group (DOF Subsea rebranded to DOF), IKM Subsea (Bryne). Equinor does NOT operate in-house ROVs; Equinor contracts all ROV services. TIOS AS joint venture (Subsea7 + Equinor) runs RLWI operations on NCS.

- **Field architecture nuance on NCS**: pure subsea tiebacks with no platform at field include Nova and Dvalin. Martin Linge, Njord, and Skarv have surface hosts. Johan Sverdrup is a platform complex with subsea tie-in wells. Article wording must not imply "subsea field" without qualification where a surface host is present.

- **NCS milestones to keep straight**: Åsgard subsea compression onstream September 2015 (world's first subsea gas compression), Tordis subsea separation/boosting/injection onstream 2007 (world's first SSBI), Ormen Lange subsea compression station installed 2023, Aasta Hansteen first oil 16 December 2018 with 482 km Polarled gas export. **All-electric subsea control world-first was Vigdis Booster Station (2022), not Snorre Expansion.** Snorre Expansion uses MUX (electro-hydraulic multiplex). Troll C is moving toward AES but not yet operational at time of writing.

- **Subsea7 / Saipem merger**: agreement signed 24 July 2025, closing expected H2 2026 under the Saipem7 name. At time of writing the two operate separately. Articles should not pre-empt the merger closing.

- **Kystdesign**: acquired by Chouest Group on 19 March 2025. Update ROV manufacturer entries accordingly.

---

## 10. Validator behaviour (summary)

The vault root `_VALIDATION.md` is authoritative. Summary of what the validator enforces for this tree:

- Frontmatter present and `schema_version: "1.0"` on every `.md` file.
- `id` unique across the whole vault, prefix `subsea-`.
- `slug` matches the filename (minus `.md`).
- `domain: "subsea"` on every leaf in this tree.
- `folder` matches the on-disk relative path.
- `type`, `status`, `depth`, `life_cycle_phases` members within the allowed enum set.
- `authoritative_sources` entries within the section 5 whitelist.
- `related` paths resolve within subsea.
- `cross_domain` paths start with a sibling tree name (`drilling/`, `crane-and-logistics/`, `emergency-response/`).
- No em dashes anywhere in body text.
- Acronyms expanded at every occurrence in body text (per W-CON-03). Bare-acronym occurrences flagged.
- Norwegian terms from `norwegian_terms` frontmatter translated inline at every occurrence (per W-CON-06). Bare-Norwegian-term occurrences flagged.
- `_INDEX.md` present in every folder; `contains_leaves` and `contains_subfolders` consistent with the folder contents.

---

## 11. Escalation

If the agent encounters ambiguity it cannot resolve from this file plus `_TOPICS.md`, `_VERIFICATION_FINDINGS.md`, and the section 5 whitelist, the agent:

1. Logs the ambiguity in `_VIEWS/_OPEN_QUESTIONS.md` (create if missing) with timestamp, file path, and a one-line statement of the ambiguity.
2. Leaves the article at `status: draft` and `authoritative_sources: []` rather than inventing.
3. Does not escalate by reading other trees. Does not escalate by searching the web during write.
4. Flags the article's frontmatter `tags` list with `tag: unresolved`.

---

## 12. Version and sync

- Schema version: `1.0`.
- This `CLAUDE.md` is a snapshot of vault-root rules plus subsea-specific additions. When the vault root `_SCHEMA_VERSION.md` bumps, this file must be re-synced before agents resume writing in the tree.
- Last built: see `created` field of `_INDEX.md` at tree root.
