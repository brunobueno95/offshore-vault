# _TOPICS.md — Subsea tree

Allowed `topics` values for frontmatter in this tree. Topics are orthogonal to folder location. An article lives in one folder but can be tagged with multiple topics. Content-fill agents must choose topics only from the lists below; validator rejects unknown topics.

Topic slugs are kebab-case. Group headings below are organisational only; do not put the heading itself in `topics`.

Schema version: `1.0`.

---

## Foundations and NCS context

- `geology-ncs`
- `water-depths`
- `seabed-soil`
- `regulatory-overview`
- `industry-bodies`

## Subsea production systems (SPS)

- `wellheads`
- `xmas-trees`
- `tree-valves`
- `tree-caps`
- `wellhead-connectors`
- `tubing-hangers`
- `manifolds`
- `templates`
- `protection-structures`
- `ssiv-hipps`
- `plem-plet-ilt-ils`

## Control systems

- `control-architectures`
- `topsides-control`
- `scm`
- `subsea-instrumentation`
- `all-electric-aes`
- `iwocs`
- `control-fluid`

## Umbilicals, flying leads, terminations

- `umbilical-types`
- `umbilical-construction`
- `umbilical-terminations`
- `flying-leads`
- `umbilical-installation`

## Flowlines and pipelines

- `flowline-architectures`
- `rigid-pipeline`
- `flexible-pipeline`
- `thermal-insulation`
- `pipeline-attributes`
- `pigging`

## Risers

- `riser-types`
- `riser-configurations`
- `riser-interfaces`
- `riser-integrity`

## Tie-in and connection systems

- `jumper-types`
- `tie-in-methods`
- `connection-systems`
- `metrology`
- `installation-aids`

## Subsea processing

- `subsea-separation`
- `subsea-boosting`
- `subsea-compression`
- `subsea-power-distribution`
- `qualification-reliability`

## Flow assurance and chemical systems

- `hydrate-management`
- `wax-management`
- `scale-management`
- `asphaltene-sand`
- `corrosion-management`
- `meg-loop`
- `chemical-injection`

## Field architectures and developments

- `host-archetypes`
- `tieback-patterns`
- `ncs-fields`
- `export-pipelines`
- `operator-landscape`

## Installation methods and vessels

- `pipelay-methods`
- `pipelay-vessels`
- `construction-support-vessels`
- `installation-spreads`
- `subsea-lifts`
- `foundations-seabed-prep`
- `trenching-burial`
- `surveys`

## IRM (Inspection Repair Maintenance)

- `irm-strategy`
- `inspection-techniques`
- `pipeline-integrity`
- `structure-inspection`
- `repair-options`
- `leak-detection`
- `bolted-joint-work`

## Subsea intervention

- `intervention-categories`
- `rig-based-intervention`
- `rlwi`
- `rlwi-contractors`
- `through-tree-techniques`
- `tree-hanger-ops`
- `intervention-planning`

## Subsea P&A

- `pa-phases`
- `barrier-philosophy`
- `subsea-pa-execution`
- `wellhead-severance`
- `regulatory-pa`

## ROV — vehicles and systems

- `imca-rov-classes`
- `rov-manufacturers`
- `lars`
- `tms`
- `tether-umbilical`
- `propulsion-motion`
- `sensors-perception`
- `manipulators`
- `tooling-interfaces`
- `rov-tooling-suite`
- `navigation-positioning`
- `piloting-modes`
- `control-cabin`
- `crew-structure`
- `operational-envelopes`

## ROV — missions

- `rov-missions-inspection`
- `rov-missions-construction`
- `rov-missions-intervention`
- `rov-missions-bop-interface`
- `rov-missions-well-intervention-support`
- `rov-missions-survey`
- `rov-missions-salvage`
- `rov-support-diving`

## ROV — governance and contracting

- `regulatory-rov`
- `ncs-rov-contractors`
- `rov-career-ladder`

## Diving (manned underwater)

- `dive-modes`
- `saturation-diving`
- `air-mixed-gas`
- `dive-spread`
- `dsvs-ncs`
- `regulations-diving`
- `imca-diving`
- `diver-tasks-owned`
- `tasks-owned-by-rov`
- `diving-to-rov-historical`
- `dive-to-rov-skill-transfer`

## Decommissioning and seabed environment

- `regulatory-frameworks`
- `decommissioning-strategies`
- `subsea-removal`
- `environmental-considerations`
- `safety-environment-ncs`

## Standards and regulations

- `ncs-havtil`
- `sokkeldirektoratet`
- `norsok-u-series`
- `norsok-cross-discipline`
- `offshore-norge-guidelines`
- `api-17-series-iso-13628`
- `dnv-standards`
- `iso-iec-general`
- `imca-guidance`
- `client-specifications`

## Life cycle and project phases

- `concept-feasibility`
- `detailed-engineering-epci`
- `fabrication-fat`
- `load-out-transportation`
- `offshore-installation`
- `hook-up-commissioning`
- `production-operations`
- `life-extension`
- `cessation-decommissioning`

## Workforce and career pathways

- `roustabout-to-subsea`
- `rov-technical-pathway`
- `diver-to-rov-transition`
- `rov-simulator-training`
- `surveyor-data-pathway`
- `subsea-engineer-longer-term`
- `remote-operations-frontier`
- `ncs-contractor-employers`

---

## Cross-cutting dimensions

These are meta-tags that span multiple chapters. Apply liberally where relevant.

- `polyhierarchy` — article is referenced from multiple folders but has one canonical home (see `CLAUDE.md` section 9 for canonical homes).
- `dive-background-transfer` — article specifically maps diver knowledge or skill to subsea/ROV work.
- `iwcf-interface` — article touches the IWCF well-control curriculum boundary, typically in intervention or P&A contexts.
- `iso-13628-api-17-parallel` — article discusses both the ISO and API edition of a parallel standard and notes any revision-cycle divergence.

---

## How agents use this list

1. Read the file.
2. Choose the narrowest-matching topic or topics. An article can carry two or three topics; rarely more.
3. If the article's subject does not fit any topic, escalate per `CLAUDE.md` section 11 rather than inventing a new topic. New topics are added to this file by a human reviewer.
4. Cross-cutting dimensions are orthogonal to the chapter topics. Apply them in addition to chapter topics, not in place of them.
