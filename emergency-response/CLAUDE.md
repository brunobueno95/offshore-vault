# CLAUDE.md — emergency-response tree

Self-contained rules for agents writing, reading, or validating content inside `offshore-vault/emergency-response/`.

Agents scoped to this tree do not read `drilling/`, `crane-and-logistics/`, or `subsea/` at write time. Cross-domain links are constructed by reference only.

---

## 1. What this tree covers

22 chapters, organised by hazard class and response capability, not by career track.

1. NCS regulatory framework and authorities
2. NORSOK and Offshore Norge standards reference
3. GSK and basic safety training
4. Helicopter transport and helideck operations
5. Helicopter emergencies, HUET and ditching
6. SAR and area preparedness (områdeberedskap)
7. Alarm, muster and escape routes
8. Evacuation means: lifeboats and liferafts
9. Personal survival equipment and immersion
10. Man overboard and sea rescue (FRC, ERRV)
11. Fire safety detection and response
12. Gas detection and toxic atmosphere response
13. Process safety, ESD and barrier philosophy
14. Hazardous areas, ATEX and ignition sources
15. Permit to work, SJA and energy isolation
16. Confined space entry and rescue
17. Work at height, fall protection and rescue
18. First aid, medic and medevac
19. Emergency command and response organisation
20. Drills, exercises and safety culture
21. Cold water, Barents and polar operations
22. Major accident hazards, RNNP and investigation

---

## 2. Scope boundaries

This tree is the foundation safety layer every offshore worker touches regardless of role. The three career-track trees inherit from it.

**Excluded by design, living in other trees:**

- **Well-control kick response and BOP taxonomy.** Lives in `drilling/well-control/`. Not duplicated here.
- **Crane rigging mechanics and lift-plan detail.** Lives in `crane-and-logistics/`. Not duplicated here.
- **Drilling operation procedures.** Lives in `drilling/drilling-operations/`. Not duplicated here.
- **Subsea production equipment.** Lives in `subsea/`. Not duplicated here.
- **Pre-ignition loss of containment events** are covered only by their trigger pathway in Chapter 13 (Process Safety) leak classification. Full well-control response belongs to drilling. Full subsea leak remediation belongs to subsea.

**Boundary rule.** Before ignition or evacuation trigger, content lives in the source tree (drilling, subsea). After ignition or evacuation trigger, content lives here.

**Deep human-factors theory** is treated as cross-cutting metadata (tag `human-factors-light`), not a dedicated folder. Chapter 22 carries the light human-factors slice for incident investigation.

---

## 3. Frontmatter schema v1.0

Every leaf uses this frontmatter:

```yaml
---
schema_version: "1.0"

id: "emergency-response-<slug>"
title: "Article title in English"
title_no: null
slug: "kebab-case-slug"
type: null                           # enum: concept | equipment | procedure | incident | standard | role | view | tool
status: draft                        # enum: draft | review | published | archived

domain: "emergency-response"
folder: "01-chapter/02-section"
parents: []
siblings: []

topics: []
life_cycle_phases: []                # enum list
depth: null                          # enum: foundational | operational | advanced
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

<!-- CONTENT PLACEHOLDER. Agent fills per _AGENT_RULES.md. -->
```

Every folder carries an `_INDEX.md`:

```yaml
---
schema_version: "1.0"
title: "Folder display title"
slug: "kebab-case-folder-name"
folder_scope: ""
contains_leaves: true
contains_subfolders: false
parent_folder: "relative/path/or/empty-at-root"
---
```

---

## 4. Allowed enum values

- `type`: `concept`, `equipment`, `procedure`, `incident`, `standard`, `role`, `view`, `tool`
- `status`: `draft`, `review`, `published`, `archived`
- `depth`: `foundational`, `operational`, `advanced`
- `life_cycle_phases`: `design`, `construction`, `commissioning`, `operation`, `maintenance`, `modification`, `decommissioning`, `incident-response`, `post-incident-learning`
- `perspective`: `regulator`, `operator`, `contractor`, `installation-crew`, `vessel-crew`, `aviation-crew`, `onshore-support`, `training-provider`

---

## 5. Authoritative source whitelist

### Havtil regulations (current, confirmed 2024)

- Rammeforskriften (Framework Regulations)
- Styringsforskriften (Management Regulations)
- Innretningsforskriften (Facilities Regulations)
- Aktivitetsforskriften (Activities Regulations)
- Teknisk og operasjonell forskrift (TOF, onshore and MODU)
- Havtil tilsynsrapporter (audit reports)
- Havtil RNNP annual reports

### Other Norwegian regulators

- Luftfartstilsynet (CAA Norway) BSL D 5-1 (FOR 2019-05-14-604, helideck regulation)
- Sjøfartsdirektoratet (maritime interface on MOUs)
- DSB (Direktoratet for samfunnssikkerhet og beredskap)
- Arbeidstilsynet (working environment interface)
- Miljødirektoratet (discharge and spill interface)
- Sokkeldirektoratet (Sodir, replaced NPD 1 January 2024)

### Core Norwegian legislation

- Petroleumsloven (Petroleum Act 1996)
- Arbeidsmiljøloven (Working Environment Act)
- Produktkontrolloven (Product Control Act)
- Forurensningsloven (Pollution Control Act)

### Ministries

- Arbeids- og inkluderingsdepartementet
- Energidepartementet (successor to Olje- og energidepartementet)
- Justis- og beredskapsdepartementet (SAR policy)

### NORSOK (safety and emergency)

- NORSOK S-001 Edition 5 (June 2018), Technical safety
- NORSOK S-002 Edition 5 (2018) with AC:2021, Working environment
- NORSOK S-003 Edition 4 (2017), Environmental care
- prNORSOK S-003 (public enquiry to 21 April 2026)
- NORSOK Z-013 Edition 3 (October 2010), Risk and emergency preparedness
- NORSOK Z-008:2017, Risk-based maintenance
- NORSOK C-004, Helideck design
- NORSOK R-002 Edition 3 (2017) with AC:2019, Lifting equipment (for LARA and lifeboat launch appliance references)
- NORSOK D-010, Well integrity (cross-reference only, not a boundary violation)

### Offshore Norge guidelines (confirmed numbering)

- 002, Safety and emergency preparedness training (rev 24, 20 June 2022)
- 064, Etablering av områdeberedskap (2015)
- 066, Offshore helicopter operations (rev 31 March 2025). NOT 064 as sometimes mislabelled.
- 074, Helideck Manual (rev 04, July 2025, amended December 2025)
- 088, Common model for work permits (rev 6, 2018)
- 090, Common model for Safe Job Analysis (2017). NOT competence.
- 096, Man overboard preparedness
- 113, Fallsikring og fallredning (20 October 2020)
- Offshore Norge approved course provider list (rev 2024)

### International instruments as referenced on NCS

- SOLAS Chapter II and III (LSA and fire)
- MOU Code 2009 (for mobile offshore units)
- Polar Code (application north of 74N)
- MARPOL Annex I-VI (pollution touchpoints)
- ICAO Annex 14 Volume II (heliports)

### Helicopter safety

- HSS-4 (SINTEF, January 2023), current Helicopter Safety Study, covering 2010-2020 with forward outlook
- HSS-3b (2017), superseded, historical trend analysis only
- Helicopter operator safety bulletins: CHC, Bristow, Lufttransport RW AS

### SAR and rescue

- Hovedredningssentralen (HRS Sør-Norge at Sola, HRS Nord-Norge at Bodø) SAR documentation
- Regjeringen policy documents on NAWSARH and state SAR system
- Kystverket (oil spill response)
- Kystvakten (Coast Guard)
- Redningsselskapet (RS, rescue boats)

### Industry bodies

- Offshore Norge (rebranded from Norsk olje og gass in 2022, NHO-affiliated)
- Norsk Industri
- IOGP
- Standards Norway (governance of NORSOK)
- Helideck Certification Agency

### Training providers (approved)

- RelyOn Nutec (Bergen, Stavanger)
- Falck Safety Services Norge
- Maersk Training (Stavanger)
- ResQ (Haugesund, Stavanger)
- Stavanger Offshore Tekniske Skole (SOTS)
- NOSEFO (Bergen, Tau, Stavanger)
- Kompetansebedriften (Sandefjord)

### Equipment and manufacturer standards

- Kongsberg (MRU, communications)
- Helly Hansen, Hansen Protection, Viking (survival suits)
- Shark 7, LAPP 5 (rebreather EBS)
- Drager (Pac 6500, 8500, SCBA PSS 7000)
- MSA (Altair 4X/5X, M1 SCBA, S-Cap)
- BW (Clip, Max XT II gas monitors)
- Umoe Schat-Harding, Norsafe (merged with Viking 2018), Jyb (free-fall lifeboats)
- Kirby Morgan (KMB 37, KMB 77 diving helmets), Divex (Ultrajewel 601)
- Marioff Hi-Fog (water mist)
- Firenor (DIFFS foam firefighting)

---

## 6. Article body structure

Every published leaf carries five sections after the frontmatter, in this order:

1. **Overview.** One paragraph, 80 to 150 words. States what the article covers and why it matters on the NCS. Expands any acronyms introduced in the title.
2. **Details.** Technical content. Subheadings allowed. Diagrams and tables allowed. No em dashes.
3. **NCS-specific context.** What is different on the Norwegian Continental Shelf versus generic offshore. References Havtil regulations, NORSOK, and Offshore Norge guidelines where applicable.
4. **Norwegian terminology.** A short glossary table. English term, Norwegian term, notes. Always paired for critical safety vocabulary.
5. **Sources.** Numbered list. Whitelist only. Each substantive claim in the body cites by number.

Leaf length target: 800 to 2500 words for `operational` depth. `foundational` leaves can be shorter. `advanced` leaves can be longer but stay under 4000 words.

---

## 7. Writing rules

### Pedagogical accessibility with technical depth (foundation rule, binding)

Every article is written for a reader who needs to become technically competent but is a beginner in the field. The article must be deeply technical AND easy to understand. Both together. Dense jargon that assumes prior domain knowledge fails the rule. Shallow summary that avoids the technical substance also fails the rule. Never assume prior knowledge. Always be pedagogical.

The foundation is targeted repetition. Human memory decays most for terms that are genuinely opaque to a newcomer, where repeated exposure is the fastest way to retain them. For terms that are self-evident from English or that carry their meaning from context once introduced, repeated glossing adds noise without helping retention. Apply repetition where it earns its cost.

Concrete:

- **Every acronym is expanded at every single use**, not only at first use. If `GSK` appears thirty times, `GSK (Grunnleggende Sikkerhets- og Beredskapskurs)` appears thirty times. Acronyms are genuinely opaque without expansion and are the highest-value category for every-use repetition. No exceptions.
- **Every Norwegian term is translated at every single use.** Example: `the beredskapsleder (emergency team leader)` every time. Norwegian terms are opaque to an English-language reader and must carry their English gloss everywhere they appear.
- **Specialist technical terms are glossed at first use in each section**, then may stand alone within that section. When a specialist term returns in a later section after a gap, re-gloss. A term is "specialist" if a reader with no prior exposure to the field would not recognise it.
- **Common-English role and domain terms do NOT repeat their gloss.** Examples: medic, radio operator, platform manager, helicopter, lifeboat, muster, escape route. Define at first use only if the meaning is not obvious from context; after that the term stands alone for the rest of the article.
- **Mechanisms are explained, not just named.** Describe how the thing works, not just what it is called.
- **Why a thing exists and what problem it solves comes before how it is used.**
- **Examples are NCS-concrete** when possible: specific installations, specific operators, specific equipment models and standards.
- **Analogies are allowed when they genuinely help the reader learn.** Never forced.
- **Paragraphs that would stack three or more undefined technical terms in a row must be broken up or rewritten.**

Prose runs longer than a typical encyclopedia would produce because acronyms and Norwegian terms carry expansions at every use. That cost is accepted for those two categories. Reading friction from role-name repetition is avoided; common-English terms do not repeat their gloss. Validator rules W-CON-03 (acronyms) and W-CON-06 (Norwegian terms) enforce the mechanical portion. The review agent catches specialist-term and common-English-term semantic issues and articles that are dense-and-incomprehensible or simple-but-shallow.

### Mandatory

1. Acronym expansion at every single use in every article. See the Pedagogical accessibility section above. Every acronym, every occurrence. Examples: `GSK (Grunnleggende Sikkerhets- og Beredskapskurs)`, `HUET (Helicopter Underwater Escape Training)`, `SAR (Search and Rescue)`, `ERRV (Emergency Response and Rescue Vessel)`, `FRC (Fast Rescue Craft)`, `HLO (Helicopter Landing Officer)`, `HDA (Helideck Assistant)`, `OIM (Offshore Installation Manager)`, `ESD (Emergency Shutdown)`, `PSD (Process Shutdown)`, `APS (Abandon Platform Shutdown)`, `TR (Temporary Refuge)`, `FFL (Free-Fall Lifeboat)`, `MES (Marine Evacuation System)`, `SCBA (Self-Contained Breathing Apparatus)`, `EEBD (Emergency Escape Breathing Device)`, `EBS (Emergency Breathing System)`, `PPE (Personal Protective Equipment)`, `RNNP (Risikonivå i norsk petroleumsvirksomhet)`.
2. Norwegian term pairing at every single use. See the Pedagogical accessibility section above. Every use, not only first. Examples: `the beredskap (emergency preparedness)`, `the innsatslag (response team)`, `the beredskapsleder (emergency team leader)`, `the plattformsjef (platform manager, OIM)`, `the brannlag (fire team)`, `the redningslag (rescue team)`, `the forstehjelpslag (first aid team)`, `the baretelag (stretcher team)`, `the mob-lag (MOB team)`, `the monstring (mustering)`, `the omradeberedskap (area preparedness)`, `the rommingsveier (escape routes)`, `the varslingsplikt (notification duty)`, `the storulykke (major accident)`.
3. No em dashes. Ever. Use commas, periods, or restructure.
4. Cite every substantive claim from the whitelist. Inline numeric references matched to the Sources list.
5. Safety-critical content takes priority over stylistic concerns. Err toward clarity and unambiguity.

### Forbidden

1. Do not read other trees at write time.
2. Do not duplicate drilling well-control content.
3. Do not duplicate crane rigging content.
4. Do not reproduce NORSOK or Offshore Norge text verbatim. Paraphrase and cite.
5. Do not mark `status: published` without validator pass and a human review.
6. Do not invent equipment model numbers, contract dates, or regulatory citations. If uncertain, flag and leave empty.

---

## 8. Cross-domain link construction

`cross_domain` is the field in frontmatter for references to other trees. Construction rules:

- Format: `"<domain>/<folder-path>/<leaf-slug>"`, for example `"drilling/well-control/bop-annular-preventer"`.
- Agent must not attempt to resolve the target file at write time. The validator checks resolution.
- If the target does not exist, the entry is still valid. Sibling trees may not have built the target yet.
- One cross_domain entry per unique relationship. Do not duplicate across leaves in the same folder unless semantically distinct.

Valid cross-domain domains from this tree: `drilling`, `crane-and-logistics`, `subsea`.

---

## 9. Special content rules for emergency response

- **CAT B EBS (Category B Emergency Breathing System, rebreather).** Mandatory for all NCS helicopter passenger transport from 1 April 2026. State this explicitly in every relevant article: HUET, helicopter ditching, passenger equipment, GSK syllabus.
- **GSK structure.** 4 days standard, 3 days with e-learning pre-course module. GSK-repetisjon 2 days every 48 months. Full re-sit after 8 years. Reference Offshore Norge 002 rev 24.
- **OPITO BOSIET equivalence.** Accepted under Mutual Agreement if CAT B rebreather EBS module and escape-chute element are included. Accepted centres from the Offshore Norge list.
- **HSS-4 is current (2023, SINTEF).** HSS-3b (2017) is superseded. HSS-3b may be referenced for historical trend analysis only.
- **State SAR system.** 330 Skvadron RNoAF operates Leonardo AW101 612 SAR Queen. Bases: Sola, Ørland, Bodø, Banak (Lakselv), Rygge, Florø (operational 2024). Tromsø is civilian CHC S-92, interim to planned 2030 handover.
- **Operator-funded SAR helicopter contracts (current 2024-2026):**
  - Bristow Norway: Equinor Nordsjø (S-92, contract 2022-2030), Equinor Barents / Hammerfest (S-92 with SAR-configured S-92, contract firmed February 2026), ConocoPhillips Ekofisk (S-92 AWSAR at Ekofisk 2/4 L).
  - CHC Helikopter Service: Aker BP strategic partnership (S-92 + AW189, January 2025) at Sola and Valhall. Also Harbour Energy.
  - Lufttransport RW AS: Equinor Troll-Oseberg SAR contract with two AW139 (operational early 2026) plus five AW189 crew-change.
- **Helicopter types on NCS 2026.** Sikorsky S-92 dominant. Leonardo AW189 phasing in (CHC, Lufttransport). Leonardo AW139 for Troll-Oseberg SAR. Bell 525 on order for Equinor (first four in 2026). H175 NOT in NCS service. H225 / AS332L2 absent from NCS passenger service since the Turøy accident (29 April 2016), despite regulatory ban lift in 2017.
- **Turøy accident (29 April 2016).** Airbus H225 main rotor detached in flight. All 13 on board died. Led to fleet-wide H225 grounding and significant changes to maintenance procedures. Must be cited in articles on helicopter types on NCS and historical accidents.
- **ERRV operators on NCS (current).** Simon Møkster Shipping (Stril Poseidon, Herkules, Merkur, Mariner), Havila Shipping (Havila Troll), Esvagt (Esvagt Corona plus Hermit Fighter / Hermit Prosper hybrid conversions, Esvagt Dana W2W/ERRV). Viking Supply Ships and Remøy Shipping are NOT significant current pure-ERRV contract holders on NCS.
- **Helideck regulation stack.** BSL D 5-1 (FOR 2019-05-14-604) under Luftfartstilsynet, read with NORSOK C-004 and CAP 437. Helideck Certification Agency performs inspections. DIFFS standard for foam firefighting.
- **Regulatory rename confirmations.** Havtil replaced Ptil on 1 January 2024. Sokkeldirektoratet (Sodir) replaced NPD on 1 January 2024. Norsk olje og gass rebranded to Offshore Norge in 2022 (NHO-affiliated).

---

## 10. Validator behaviour (summary)

Validator runs on every commit to the tree. It checks:

- Frontmatter schema v1.0 compliance. Required fields present, enum values in allowed set.
- Slug matches filename and `id` suffix.
- `folder` field matches the actual folder path.
- `domain` is `"emergency-response"`.
- `authoritative_sources` entries match the whitelist in section 5.
- `cross_domain` entries point to allowed sibling domains.
- No em dashes in body text.
- Acronym expansion present at every occurrence for the canonical acronym list (per W-CON-03). Norwegian term inline translation at every occurrence (per W-CON-06).
- `ncs_specific: true` unless the leaf is explicitly a cross-reference-only stub.
- `status: published` requires non-empty `authoritative_sources`, non-empty body, `word_count` populated.

Validator failures block publish. Drafts are allowed to fail.

---

## 11. Escalation

If an agent encounters ambiguity it cannot resolve without reading another tree, or a claim that may conflict with another tree, the agent writes the article as a draft, adds a `tags: [needs-cross-tree-review]` entry, and stops. Human review resolves.

If an agent detects a regulatory change that invalidates a whitelist entry (for example a new Offshore Norge guideline revision), the agent does not edit the whitelist. The agent writes a note to `_VERIFICATION_FINDINGS.md` under the "Items to re-verify" list and flags the affected leaves with `tags: [regulatory-change-pending]`.

---

## 12. Version and sync

- This file is the authoritative rulebook for the emergency-response tree at `schema_version: 1.0`.
- Sibling trees (drilling, crane-and-logistics, subsea) carry their own CLAUDE.md at the same schema version.
- Changes to this file require a schema bump and a migration plan across all leaves.
- Last updated: 2026-04-19.
