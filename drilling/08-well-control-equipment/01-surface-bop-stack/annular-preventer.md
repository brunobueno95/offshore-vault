---
schema_version: "1.0"
id: "drilling-annular-preventer"
title: "Annular Preventer"
title_no: "Ringromspreventer"
slug: "annular-preventer"
type: equipment
status: draft
domain: "drilling"
folder: "08-well-control-equipment/01-surface-bop-stack"
parents: []
siblings: []
topics: []
life_cycle_phases: ["drilling", "completion", "intervention"]
depth: operational
perspective: ["IWCF Level 2", "IWCF Level 3", "NORSOK D-010 well barrier element", "API STD 53 BOP system", "driller onboarding", "toolpusher reference"]
authoritative_sources:
  - id: "api-spec-16a"
    title: "API Specification 16A, Specification for Drill-through Equipment"
    publisher: "American Petroleum Institute"
    year: 2017
    access: "paywalled"
    cited_sections: ["Section 3 (design)", "Section 4 (annular preventers)"]
    verified_date: "2026-04-20"
    verified_by: "agent:drilling-content-v1"
  - id: "api-std-53"
    title: "API Standard 53, Blowout Prevention Equipment Systems for Drilling Wells"
    publisher: "American Petroleum Institute"
    year: 2018
    access: "paywalled"
    cited_sections: ["Section 6 (equipment)", "Section 7 (testing)"]
    verified_date: "2026-04-20"
    verified_by: "agent:drilling-content-v1"
  - id: "norsok-d-010-rev5"
    title: "NORSOK D-010 Rev 5, Well Integrity in Drilling and Well Operations"
    publisher: "Standards Norway"
    year: 2021
    access: "paywalled"
    cited_sections: ["Clause 6 (well barriers)", "Clause 7 (testing and verification)"]
    verified_date: "2026-04-20"
    verified_by: "agent:drilling-content-v1"
  - id: "iwcf-level-2"
    title: "IWCF Drilling Well Control Level 2 Syllabus"
    publisher: "International Well Control Forum"
    year: 2023
    access: "restricted"
    cited_sections: ["Well control equipment module"]
    verified_date: "2026-04-20"
    verified_by: "agent:drilling-content-v1"
  - id: "offshore-norge-135"
    title: "Offshore Norge Guideline 135, Classification and Reporting of Well Control Incidents"
    publisher: "Offshore Norge"
    year: 2020
    access: "open"
    cited_sections: ["Incident classification", "Post-event review"]
    verified_date: "2026-04-20"
    verified_by: "agent:drilling-content-v1"
reference_textbooks: []
related_incidents: []
related:
  - "08-well-control-equipment/01-surface-bop-stack/pipe-rams.md"
  - "08-well-control-equipment/01-surface-bop-stack/blind-rams.md"
  - "08-well-control-equipment/01-surface-bop-stack/blind-shear-rams.md"
  - "08-well-control-equipment/01-surface-bop-stack/variable-bore-rams-vbr.md"
  - "08-well-control-equipment/01-surface-bop-stack/stack-configurations.md"
cross_domain:
  - "subsea/15-rov-systems-operations-missions/rov-missions-bop-interface/bop-stack-gvi-external.md"
relevant_to_roles: ["driller", "assistant-driller", "toolpusher", "senior-toolpusher", "drilling-supervisor", "drilling-engineer"]
ncs_specific: true
norwegian_terms:
  - { "no": "ringromspreventer", en: "annular preventer" }
  - { "no": "utblåsningssikring", en: "blowout preventer (BOP)" }
  - { "no": "pakningselement", en: "packing element" }
  - { "no": "boresjef", en: "toolpusher" }
  - { "no": "borebas", en: "toolpusher (alternative title)" }
  - { "no": "boreleder", en: "drilling supervisor" }
  - { "no": "trykktest", en: "pressure test" }
  - { "no": "funksjonstest", en: "function test" }
  - { "no": "brønnbarriere", en: "well barrier" }
authors: ["agent:drilling-content-v1", "agent:drilling-review-v1"]
created: "2026-04-19"
updated: "2026-04-20"
review_due: "2027-10-19"
tags: ["bop", "well-control-equipment", "annular-preventer", "surface-bop", "packing-element", "ncs"]
citation_density: 0.80
word_count: 2994
---

## Overview

An annular preventer is a type of BOP (Blowout Preventer) that uses a single ring-shaped rubber packing element to seal the wellbore around almost any object that happens to be in the hole. It can close on drill pipe, on drill collars, on a tool joint, on the kelly, on a wireline, and even on open hole with nothing in the bore. <!-- REVIEW-FLAG: specialist term "tool joint" used without first-use gloss --> <!-- REVIEW-FLAG: specialist term "kelly" used without first-use gloss --> That versatility is what separates the annular preventer from ram preventers, which are the other main type of BOP (Blowout Preventer) and which use opposing steel rams dressed for one specific pipe diameter at a time. On a surface BOP (Blowout Preventer) stack, which is the type of BOP (Blowout Preventer) assembly mounted above the rig floor on a fixed platform, a jack-up, or a land rig, the annular preventer is the element that sits at the very top and is the first element closed when the crew needs to shut in the well (api-std-53, Section 6).

The annular preventer exists because a working well has many different things hanging in the hole at different moments. A crew may be running casing, then tripping drill pipe, then stripping (moving pipe in or out of the well while the BOP (Blowout Preventer) is closed and pressure is contained) through tool joints while a kick (an unwanted influx of formation fluid into the wellbore under pressure) is circulated out. Ram preventers seal only on the exact pipe size they are dressed for. The annular preventer uses a rubber packing element that can squeeze down around any shape, and that flexibility makes it the first tool the driller reaches for when flow is detected and the well must be closed in fast. This article explains how the annular preventer seals, how it is used during normal drilling and during a kick, how it is tested, and how the NCS (Norwegian Continental Shelf) regulatory regime under Havtil (Havindustritilsynet, the Norwegian Ocean Industry Authority) governs its condition (norsok-d-010-rev5, Clause 6).

## Details

### Why the annular preventer exists

Before the annular preventer was developed in the 1940s by Hydril, a BOP (Blowout Preventer) stack was just a set of ram preventers, each sized for one pipe diameter. Every time the crew changed from drill pipe to drill collars or ran tubing of a different size, the stack could not reliably seal around the new string until the matching ram was installed or redressed. The Hydril annular preventer solved that problem by replacing rigid steel rams with a single reinforced rubber packing element that can deform around whatever is in the bore (api-spec-16a, Section 4).

The problem the annular preventer solves is versatile sealing under pressure. The mechanism is a hydraulic squeeze applied through a shaped housing. The result is a seal that accepts a range of object diameters, tolerates some wear, survives pipe movement without losing the seal (an operation called stripping, which is moving pipe in or out of the well while pressure is contained), and closes quickly (api-spec-16a, Section 4).

### How an annular preventer seals

An annular preventer has a small number of parts that all serve the squeeze mechanism:

- A steel housing with a tapered or spherical internal profile above the bore.
- An annular piston (a ring-shaped steel piston that rides inside the housing below the packing element and moves vertically when hydraulic fluid is applied under it).
- A packing element (a donut-shaped block of rubber reinforced with steel inserts, which is the part that actually contacts the pipe or the bore).
- A hydraulic closing port and an opening port on the BOP (Blowout Preventer) body, both plumbed to the BOP (Blowout Preventer) control system and the rig accumulator bank.

When closing pressure is applied, hydraulic fluid enters the closing port and pushes the piston upward. The piston pushes the bottom of the packing element upward into the tapered or spherical upper housing. That taper forces the packing element radially inward toward the centre of the bore. The rubber flows inward around whatever is in the bore, while the steel inserts embedded in the rubber limit how far the rubber can extrude and keep the overall element geometry stable under pressure. Whatever is in the bore, drill pipe, tool joint, kelly, or nothing at all, the rubber wraps around it and seals against it (api-spec-16a, Section 4).

When opening pressure is applied, fluid enters the opening port and pushes the piston back down. The packing element's own elasticity then returns it approximately to the open position. A worn element may not fully return to the original open profile; the element is designed as a wear item and is replaced through a top cap without removing the preventer from the stack (api-spec-16a, Section 4).

### Major design variants

Three design families cover most annular preventers on the NCS (Norwegian Continental Shelf):

- The spherical or tapered-bowl type (Hydril GK, GL, and GX product lines) uses a piston that pushes the packing element upward into a spherical or conical upper housing. This is the most common configuration on surface BOP (Blowout Preventer) stacks worldwide and on the NCS (Norwegian Continental Shelf) (api-spec-16a, Section 4).
- The wedge type (Cameron Type D and DL product lines) uses a piston that works against the packing element through a wedge-shaped internal geometry. Functionally similar to the spherical type; the mechanical detail of how squeeze is generated differs.
- The Shaffer spherical type is a variant of the spherical family with a slightly different packer shape but the same operating principle.

The working principle is the same across all three families: hydraulic squeeze through a shaped housing. The differences are in manufacturer lineage, element geometry, and wear behaviour, not in how the annular preventer actually closes a well.

### The packing element as a consumable

The packing element is a wear item. Every closure, every strip through a tool joint, and every pressure cycle takes life off the element. Field life depends on how the preventer is used. An annular preventer that stripped two strings through its element during a kick (an unwanted influx of formation fluid into the wellbore under pressure) event has significantly less element life left than one that has only been function-tested monthly with no string movement (iwcf-level-2, Well control equipment module).

Elastomer chemistry is selected to match well conditions. Common options:

- Natural rubber compound, for water-based mud service at moderate temperature.
- Nitrile, for oil-based mud service.
- Hydrogenated nitrile or specialty fluoroelastomer compounds, for high-temperature service or for wells containing H2S (hydrogen sulphide, a toxic and corrosive gas that attacks standard elastomers).

Element selection is part of the well design that the boreleder (drilling supervisor) reviews before drilling starts. NCS (Norwegian Continental Shelf) wells into sour zones, meaning zones containing H2S (hydrogen sulphide), must have sour-service packing elements, and the sour-service requirement is tracked through the well programme and confirmed by the borebas (toolpusher) at rig-up (norsok-d-010-rev5, Clause 6).

### Pressure ratings and operating envelope

Annular preventers are manufactured in standard pressure classes defined by API (American Petroleum Institute) Spec 16A: 2,000 psi (pounds per square inch), 3,000 psi (pounds per square inch), 5,000 psi (pounds per square inch), 10,000 psi (pounds per square inch), and 15,000 psi (pounds per square inch) rated working pressure. The rated working pressure is the maximum wellbore pressure the preventer is qualified to hold when properly closed on the pipe size for which it is rated (api-spec-16a, Section 3).

Two de-rating rules apply in practice:

- On open hole, with nothing in the bore, the annular preventer's sealing capability is reduced. Manufacturer data typically allows the full rated working pressure when closed on pipe and only a fraction of that when closed on open hole. The specific open-hole rating is published by the OEM (Original Equipment Manufacturer) for each element and must be taken from the datasheet, not assumed.
- When closing around an object much smaller or larger than the design optimum, for example a thin wireline or a slick kelly, the effective working pressure drops. The closing pressure regulator on the BOP (Blowout Preventer) control panel must be set accordingly (api-std-53, Section 6).

The hydraulic closing pressure delivered to the closing port is typically around 1,500 psi (pounds per square inch), regulated down from the rig accumulator supply of 3,000 psi (pounds per square inch). This closing pressure is lower than the closing pressure used on ram preventers because the annular preventer does not rely on metal-to-metal interference to seal. It relies on rubber squeeze and on pressure assist, meaning that once an initial seal is made, the wellbore pressure itself helps push the packing element more firmly against the object in the bore (api-std-53, Section 6).

### Stripping

Stripping is the operation of moving pipe into or out of the well while a BOP (Blowout Preventer) element is closed and holds wellbore pressure. Stripping is how the driller and the boreleder (drilling supervisor) bring pipe to bottom during a kick circulation when the well cannot simply be opened up.

The annular preventer is the preferred element for stripping because the rubber can ride over tool joints without damage that would end the seal. During stripping, the closing pressure is regulated down to the minimum that still holds well pressure, so that when a tool joint enters the element, the rubber deforms around the joint rather than tearing off. Ram preventers can also be used for stripping in a ram-to-annular sequence on a more complex stack, but stripping with the annular preventer alone is the simplest configuration (iwcf-level-2, Well control equipment module).

Stripping wears the packing element considerably faster than static closure. Operators track element wear using closure count and strip count logs, and they set an element replacement threshold below which the preventer must be redressed before further stripping is allowed (api-std-53, Section 6).

### Testing and verification

BOP (Blowout Preventer) testing on the NCS (Norwegian Continental Shelf) is governed by NORSOK D-010 Rev 5 (the Norwegian well integrity standard) and by API (American Petroleum Institute) STD 53. Together they define two distinct test types and their intervals:

- Function test, where the preventer is opened and closed hydraulically and the timing of each operation is recorded. Function tests are performed at least weekly on a surface BOP (Blowout Preventer) stack (api-std-53, Section 7; norsok-d-010-rev5, Clause 7).
- Pressure test, where the closed preventer is held against a test pressure. Typical practice applies a low pressure first (around 200 to 300 psi (pounds per square inch)) and then a high pressure matching the rated working pressure or the maximum anticipated surface pressure, whichever is lower. Pressure tests are performed at rig-up, after any element change, after any repair, and at defined operating intervals, typically every 14 days on an NCS (Norwegian Continental Shelf) surface BOP (Blowout Preventer) stack (norsok-d-010-rev5, Clause 7; api-std-53, Section 7).

For an annular preventer specifically, the pressure test is performed on a test joint of the expected pipe size, so that the element seals on pipe under test conditions similar to operational conditions. Testing the annular preventer against a test plug in open hole is avoided because of the open-hole de-rating and the risk of damaging the packing element against the plug.

The test record is retained by the drilling contractor and countersigned by the borebas (toolpusher) and the boreleder (drilling supervisor). Failed tests require repair or element replacement before drilling continues, because the annular preventer is a well barrier element (a tested component that is credited as one of the independent barriers in the NCS (Norwegian Continental Shelf) two-barrier philosophy) during drilling (norsok-d-010-rev5, Clause 6).

### Position in a surface BOP stack

On a surface BOP (Blowout Preventer) stack, the annular preventer sits at the top, above the ram preventers. Two operational reasons explain the placement:

- It closes first. When the crew sees flow and the driller calls "shut in", the annular preventer is the fastest-closing element because its closing pressure is lowest and the element does not need to align with a specific pipe size. Closing the annular preventer first isolates the well while the driller chooses which rams to close below it (api-std-53, Section 6).
- It is the easiest element to redress. The packing element can be replaced through the top cap without breaking the stack or disturbing the ram preventers below. Putting the annular preventer on top minimises the downtime of an element change.

Some stacks include two annular preventers in series to provide redundancy, especially on high-pressure wells or on wells where long stripping operations are expected. That two-annular configuration is more common on subsea BOP (Blowout Preventer) stacks, where one annular preventer is placed in the LMRP (Lower Marine Riser Package, the upper removable half of a subsea BOP (Blowout Preventer) stack) and a second in the main stack. On surface BOP (Blowout Preventer) stacks, a single annular preventer is more common and redundancy is provided by the ram preventers below (api-std-53, Section 6).

## NCS-specific context

The NCS (Norwegian Continental Shelf) regulatory regime for BOP (Blowout Preventer) equipment is layered. At the top sits Havtil (Havindustritilsynet, the Norwegian Ocean Industry Authority), whose regulations, principally the Innretningsforskriften (the Facilities Regulations) and the Aktivitetsforskriften (the Activities Regulations), require that well control equipment be designed, tested, and maintained to recognised standards. At the operational level, NORSOK D-010 Rev 5 (the Norwegian well integrity standard) is the dominant reference in every well programme on the NCS (Norwegian Continental Shelf). API (American Petroleum Institute) Spec 16A and API (American Petroleum Institute) STD 53 are cited through NORSOK D-010 Rev 5 (the Norwegian well integrity standard) as the equipment-level specifications for drill-through equipment and BOP (Blowout Preventer) system requirements (norsok-d-010-rev5, Clause 6).

On fixed-platform drilling rigs on the NCS (Norwegian Continental Shelf), such as those on Ekofisk, Valhall, Statfjord, Gullfaks, and Troll B and C, the annular preventer is part of a surface BOP (Blowout Preventer) stack that is nippled up above the wellhead after each surface casing string is set and cemented. Platform drilling crews on the NCS (Norwegian Continental Shelf) typically run a Hydril-type annular preventer as the top element above a set of pipe rams, variable-bore rams, and blind-shear rams. Function tests are run on a schedule set by the operator's drilling operations manual, cross-referenced against NORSOK D-010 Rev 5 (the Norwegian well integrity standard) minimum intervals, and pressure tests are recorded in the rig's BOP (Blowout Preventer) test log (norsok-d-010-rev5, Clause 7).

The boreleder (drilling supervisor), as the operator's onsite representative, holds operator-side responsibility for confirming that the annular preventer has a valid test within its interval before any operation that may build wellbore pressure. The borebas (toolpusher), also called the boresjef (toolpusher) on some installations, holds rig-side responsibility for executing the test and the associated function checks. Both sign off on the BOP (Blowout Preventer) test report, which becomes part of the daily drilling report reviewed onshore by the operator's drilling engineer (norsok-d-010-rev5, Clause 7).

Element inspection is a practical NCS (Norwegian Continental Shelf) concern on wells with long drilling intervals or long kill operations. After a kick (an unwanted influx of formation fluid into the wellbore under pressure) event that required stripping (moving pipe in or out of the well while the BOP (Blowout Preventer) is closed and pressure is contained) through the annular preventer, the packing element is typically pulled and visually inspected at the next operational window, even when the most recent pressure test is still passing. Offshore Norge Guideline 135 (the NCS (Norwegian Continental Shelf) guideline on well control incident classification and reporting) triggers a post-event review after any notifiable well control incident, and BOP (Blowout Preventer) equipment condition, including annular element condition, is part of that review (offshore-norge-135, Post-event review).

The annular preventer is one element in the secondary well barrier (the second of two independent barriers required by NORSOK D-010 Rev 5 (the Norwegian well integrity standard) during drilling) on an NCS (Norwegian Continental Shelf) well. The primary barrier is typically the hydrostatic pressure of the mud column, and the secondary barrier is the BOP (Blowout Preventer) stack together with the wellhead, the casing, and the cement. Without a functional annular preventer, the secondary barrier is incomplete, and NORSOK D-010 Rev 5 (the Norwegian well integrity standard) does not permit drilling to continue (norsok-d-010-rev5, Clause 6).

## Norwegian terminology

| Norwegian | English | Notes |
|---|---|---|
| ringromspreventer | annular preventer | Literal Norwegian rendering. |
| utblåsningssikring | blowout preventer (BOP) | Generic Norwegian term covering any BOP (Blowout Preventer) element. |
| pakningselement | packing element | The rubber plus steel insert block inside the annular preventer. |
| boresjef | toolpusher | Senior rig-based drilling supervisor on an NCS (Norwegian Continental Shelf) installation. |
| borebas | toolpusher | Alternative title for the same rig-side role. |
| boreleder | drilling supervisor | Operator's senior onsite representative. |
| trykktest | pressure test | Periodic BOP (Blowout Preventer) pressure test per NORSOK D-010 Rev 5 (the Norwegian well integrity standard). |
| funksjonstest | function test | Operational check that the preventer opens and closes within specification. |
| brønnbarriere | well barrier | Tested component credited in the two-barrier philosophy. |

## Sources

1. API Specification 16A, Fourth Edition (2017). American Petroleum Institute. Sections 3 and 4. Paywalled. Verified 2026-04-20 by agent:drilling-content-v1.
2. API Standard 53, Fifth Edition (2018). American Petroleum Institute. Sections 6 and 7. Paywalled. Verified 2026-04-20 by agent:drilling-content-v1.
3. NORSOK D-010 Rev 5 (2021). Standards Norway. Clauses 6 and 7. Paywalled. Verified 2026-04-20 by agent:drilling-content-v1.
4. IWCF Drilling Well Control Level 2 Syllabus (2023). International Well Control Forum. Well control equipment module. Restricted. Verified 2026-04-20 by agent:drilling-content-v1.
5. Offshore Norge Guideline 135 (2020). Offshore Norge. Classification and post-event review sections. Open. Verified 2026-04-20 by agent:drilling-content-v1.

## Related concepts

- Pipe rams (sibling article; the ram preventer type that complements the annular preventer for specific pipe sizes).
- Blind rams and blind-shear rams (sibling articles; the ram preventer types used for open-hole closure and emergency pipe shearing).
- Variable-bore rams (sibling article; a ram preventer type that spans a range of pipe sizes, partially overlapping the annular preventer's role).
- Stack configurations (sibling article; how annular preventers and rams are ordered in surface stacks on the NCS (Norwegian Continental Shelf)).
