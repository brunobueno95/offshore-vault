# CLAUDE.md — offshore-vault root

This file is the orchestration contract at the library root. It is read by a top-level orchestrator agent or by humans reviewing the vault. It is NOT read by tree-scoped agents, which read only their own tree's `CLAUDE.md`.

## What this vault is

A structured knowledge database for AI agents to read, write, validate, and maintain. Apps consume it. Agents populate it. Other agents validate and clean it. The vault is the single source of truth for NCS (Norwegian Continental Shelf) offshore knowledge.

The skeleton is the product first. Content comes from agents later. Schema and rules are locked before content is written.

## Scope domains

Four trees, each self-contained, each owning a distinct knowledge domain:

- `drilling/` — geology, well planning, drilling operations, well control, completion, intervention, formation evaluation, well integrity and P&A, drilling-side HSE
- `crane-and-logistics/` — G5 pedestal, G4 traverskran, G20 hydraulic, personnel transfer, CCUs, DROPS, cargo handling, rigging gear, lifting standards, offshore forklift
- `subsea/` — SPS, controls, umbilicals, flowlines, risers, tie-in, subsea processing, IRM, intervention, subsea P&A, ROV systems, diving, decommissioning
- `emergency-response/` — regulatory framework, GSK training, helicopter ops, SAR, muster and evacuation, fire, gas detection, process safety, ATEX, permits, confined space, fall protection, medevac, command organisation, drills, cold water, RNNP

## Scope boundaries (non-negotiable)

Duplication is the enemy. One canonical home per topic.

- BOP taxonomy and ram theory live in `drilling/`. ROV-facing BOP interface tasks (external inspection, hot stab, pod retrieval, emergency shear ram activation) live in `subsea/chapter-15-rov-systems-operations-missions/`. Both reference each other via `cross_domain`.
- Well barriers and kick response live in `drilling/`. Post-ignition emergency response (fire, evacuation, SAR) lives in `emergency-response/`. The boundary is the moment of ignition or evacuation trigger.
- Crane rigging mechanics and lift planning live in `crane-and-logistics/`. Subsea module lift analysis (splash zone dynamics, DAF, guide wire systems) is referenced from there into `subsea/chapter-11-installation-methods-and-vessels/` for subsea-specific context.
- Cement chemistry and primary cementing live in `drilling/`. Well integrity barrier theory for cement also lives in `drilling/` (chapter 14), not duplicated into subsea P&A.
- Operator names (Equinor, Aker BP, Var Energi, etc.) have full articles only in `drilling/chapter-16-crew-organization-and-roles/` and `crane-and-logistics/chapter-26-ncs-industry-ecosystem-and-career/` as context. Other trees reference via `cross_domain`.

## How cross-tree links work

Agents write `cross_domain: ["target-tree/chapter/.../file.md"]` without verifying targets exist. The post-run validator walks all `cross_domain` and `related` entries, confirms they resolve, and writes broken links to `_UNRESOLVED_LINKS.md` at this root. Broken links are normal during construction; the validator triages.

## Parallel agent operation

Each tree can be worked by an independent agent simultaneously. No runtime coordination between trees. Coordination happens through:
1. The schema (every article conforms, so structure is predictable)
2. The path conventions (so cross-tree paths are guessable)
3. The post-run validator (so broken links are caught systematically)

Never instruct a tree agent to read another tree at write time. If it needs context from another tree, that context must be embedded in its own tree via a summary article or noted as a `cross_domain` reference to a to-be-validated path.

## Files at this root

- `_SCHEMA.md` — master frontmatter contract (v1.0)
- `_CONTROLLED_VOCABULARY.md` — master enums for root-level constrained fields
- `_PATH_CONVENTIONS.md` — naming rules that make cross-tree paths predictable
- `_AGENT_RULES.md` — how agents write, cite, and what they never do
- `_VALIDATION.md` — rules the validator enforces
- `_SCHEMA_VERSION.md` — current schema version, bump on breaking change
- `_UNRESOLVED_LINKS.md` — validator output (auto-generated)
- `_MANIFEST.txt` — list of every path in the vault, regenerated on each build
- `.github/workflows/validate.yml` — CI validator (to be implemented in Phase 4)

## Read order for an orchestrator agent

1. This file (`CLAUDE.md`)
2. `_SCHEMA.md`
3. `_CONTROLLED_VOCABULARY.md`
4. `_PATH_CONVENTIONS.md`
5. `_AGENT_RULES.md`
6. `_VALIDATION.md`

## Read order for a tree-scoped agent

1. The tree's own `CLAUDE.md` and nothing else at the root. The tree's CLAUDE.md contains all necessary rules, self-contained.

## Do not do

- Do not edit articles in more than one tree per agent session.
- Do not invent frontmatter fields. Use only those defined in `_SCHEMA.md`.
- Do not duplicate content across trees. Use `cross_domain` instead.
- Do not paraphrase authoritative sources. Cite them in `authoritative_sources` and write your own analysis.
- Do not write articles shorter than the `depth` minimum defined in `_AGENT_RULES.md`.
- Do not mark an article `status: published` unless it passes all validator checks.

## Schema version

Current: 1.0 (see `_SCHEMA_VERSION.md`). Breaking changes require a version bump and a sync across all per-tree `CLAUDE.md` files.
