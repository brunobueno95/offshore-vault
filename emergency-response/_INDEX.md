---
schema_version: "1.0"
title: "Emergency Response"
slug: "emergency-response"
folder_scope: "Foundation safety layer for all NCS offshore operations. Organised by hazard class and response capability, not by career track. Drilling, crane-and-logistics, and subsea trees inherit from this layer via cross_domain references."
contains_leaves: false
contains_subfolders: true
parent_folder: ""
---

<!-- TREE ROOT INDEX. -->

# Emergency response tree

This is the root of the emergency-response tree inside `offshore-vault/`.

## Scope

Foundation safety layer every offshore worker touches regardless of role. Twenty-two chapters covering regulatory framework, standards, GSK training, helicopter operations and emergencies, SAR and area preparedness, alarm and muster, evacuation, personal survival, MOB and sea rescue, fire, gas detection, process safety, ATEX, permits, confined space, work at height, first aid and medevac, emergency command, drills, polar operations, and major accident hazards.

## Structure

- `CLAUDE.md`, tree-scoped agent rules and source whitelist.
- `_TOPICS.md`, allowed topic values.
- `_VERIFICATION_FINDINGS.md`, confirmed research findings and items to re-verify.
- `_INDEX.md`, this file.
- `_VIEWS/`, placeholder for generated cross-cut views.
- `01-ncs-regulatory-framework-and-authorities/` through `22-major-accident-hazards-rnnp-and-investigation/`, the 22 chapter folders.

## Build metadata

- Schema version: 1.0
- Build date: 2026-04-19
- Chapters: 22
- Subfolders total: 147
- Leaves total: 662
- Every folder carries an `_INDEX.md`.
- Every leaf carries frontmatter at schema v1.0 with stub content placeholder.

## Cross-tree relationships

The emergency-response tree does not read other trees at write time. Cross-domain links to `drilling/`, `crane-and-logistics/`, and `subsea/` are constructed by reference only. See `CLAUDE.md` section 8 for construction rules.
