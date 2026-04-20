---
schema_version: "1.0"
id: "drilling-hard-shut-in"
title: "Hard Shut In"
title_no: "Hard innstengning"
slug: "hard-shut-in"
type: procedure
status: draft
domain: "drilling"
folder: "07-well-control/05-shut-in-procedures"
parents: []
siblings: []
topics: []
life_cycle_phases: ["drilling", "completion", "intervention"]
depth: operational
perspective: ["IWCF Level 2", "IWCF Level 3", "NORSOK D-010 well control", "API RP 59 well control operations", "driller onboarding", "toolpusher reference"]
authoritative_sources:
  - id: "api-std-53"
    title: "API Standard 53, Blowout Prevention Equipment Systems for Drilling Wells"
    publisher: "American Petroleum Institute"
    year: 2018
    access: "paywalled"
    cited_sections: ["Section 6 (equipment)", "Section 7 (testing)"]
    verified_date: "2026-04-20"
    verified_by: "agent:drilling-content-v1"
  - id: "api-rp-59"
    title: "API Recommended Practice 59, Well Control Operations"
    publisher: "American Petroleum Institute"
    year: 2019
    access: "paywalled"
    cited_sections: ["Shut-in procedures", "Kick response"]
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
    cited_sections: ["Shut-in procedures module", "Kick size and kill planning module"]
    verified_date: "2026-04-20"
    verified_by: "agent:drilling-content-v1"
  - id: "offshore-norge-135"
    title: "Offshore Norge Guideline 135, Classification and Reporting of Well Control Incidents"
    publisher: "Offshore Norge"
    year: 2020
    access: "open"
    cited_sections: ["Incident classification", "Notification", "Post-event review"]
    verified_date: "2026-04-20"
    verified_by: "agent:drilling-content-v1"
  - id: "iadc-drilling-manual"
    title: "IADC Drilling Manual, 12th Edition"
    publisher: "International Association of Drilling Contractors"
    year: 2015
    access: "paywalled"
    cited_sections: ["Well control chapter"]
    verified_date: "2026-04-20"
    verified_by: "agent:drilling-content-v1"
reference_textbooks: []
related_incidents: []
related:
  - "07-well-control/05-shut-in-procedures/soft-shut-in.md"
  - "07-well-control/05-shut-in-procedures/shut-in-while-drilling.md"
  - "07-well-control/05-shut-in-procedures/shut-in-while-tripping.md"
  - "07-well-control/05-shut-in-procedures/shut-in-while-out-of-hole.md"
  - "07-well-control/05-shut-in-procedures/shut-in-during-casing-running.md"
  - "07-well-control/05-shut-in-procedures/recording-sidpp-sicp-pit-gain.md"
  - "08-well-control-equipment/01-surface-bop-stack/annular-preventer.md"
cross_domain:
  - "subsea/15-rov-systems-operations-missions/rov-missions-bop-interface/bop-stack-gvi-external.md"
relevant_to_roles: ["driller", "assistant-driller", "toolpusher", "senior-toolpusher", "drilling-supervisor", "drilling-engineer"]
ncs_specific: true
norwegian_terms:
  - { "no": "hard innstengning", en: "hard shut-in" }
  - { "no": "myk innstengning", en: "soft shut-in" }
  - { "no": "innstengning", en: "shut-in" }
  - { "no": "utblåsningssikring", en: "blowout preventer (BOP)" }
  - { "no": "boresjef", en: "toolpusher" }
  - { "no": "borebas", en: "toolpusher (alternative title)" }
  - { "no": "boreleder", en: "drilling supervisor" }
  - { "no": "brønnbarriere", en: "well barrier" }
  - { "no": "strupe", en: "choke" }
  - { "no": "strupeventil", en: "choke valve" }
  - { "no": "innretningsforskriften", en: "Facilities Regulations" }
  - { "no": "aktivitetsforskriften", en: "Activities Regulations" }
authors: ["agent:drilling-content-v1"]
created: "2026-04-19"
updated: "2026-04-20"
review_due: "2027-10-19"
tags: ["well-control", "shut-in", "hard-shut-in", "kick-response", "bop", "ncs"]
citation_density: 0.48
word_count: 3141
---

## Overview

Hard shut-in is the well control procedure in which the drilling crew closes a flowing well as quickly as possible by closing the BOP (Blowout Preventer) while every flow path out of the wellbore is already closed. "Hard" refers to the abrupt stop: the kick (an unwanted influx of formation fluid into the wellbore under pressure) is not allowed to flow anywhere between the moment the BOP (Blowout Preventer) seals and the moment the shut-in pressures are read. The opposite method, soft shut-in, lets the kick flow briefly out through the choke manifold (the surface-mounted set of adjustable chokes and valves that meters pressure out of the well during a kill) before that choke is closed. On the NCS (Norwegian Continental Shelf), hard shut-in is the default method on many surface BOP (Blowout Preventer) fixed-platform installations and is taught as the baseline procedure by the IWCF (International Well Control Forum) Level 2 syllabus (iwcf-level-2, Shut-in procedures module).

Hard shut-in exists to minimise kick size. Every second that a kick (an unwanted influx of formation fluid into the wellbore under pressure) is allowed to flow adds more formation fluid to the annulus, displaces more drilling mud, and raises the shut-in pressures the crew reads later. A smaller kick is easier to circulate out safely and less likely to push the surface pressure above the MAASP (Maximum Allowable Annular Surface Pressure, the pressure at which the formation at the casing shoe is expected to fracture). Faster closure means less influx. The cost of that speed is water hammer (a pressure transient created when moving fluid is stopped abruptly). Abruptly sealing the wellbore on a stream that is flowing hundreds of gallons per minute generates a brief pressure spike that propagates up and down the mud column. On a well where the casing shoe (the bottom of the last cemented casing string, and the weakest point in the wellbore below which any pressure excess will fracture the formation) is already close to its fracture limit, that spike can induce an underground blowout (a flow between formations that does not reach surface), which is harder to diagnose and harder to kill than a conventional surface kick (api-rp-59, Shut-in procedures).

This article explains the hard shut-in sequence on an NCS (Norwegian Continental Shelf) surface BOP (Blowout Preventer) stack, contrasts it with the soft method, describes the water hammer physics that makes the choice non-trivial, and sets out the NCS (Norwegian Continental Shelf) regulatory and operator framework that governs which method is used.

## Details

### Why hard shut-in minimises influx

A kick (an unwanted influx of formation fluid into the wellbore under pressure) is, by definition, formation fluid entering the wellbore under positive pressure differential. The rate of influx depends on the formation's permeability and on how far the wellbore pressure has fallen below the pore pressure. The total volume admitted before the well is closed depends on the rate and on the time allowed. Time is the variable the crew controls. Minimising that time is what hard shut-in is designed to do.

The driving logic is simple. A ten-barrel kick (an unwanted influx of formation fluid into the wellbore under pressure) on a 12¼-inch hole section is a routine event and is circulated out using a standard kill method, typically either the Driller's Method or the Wait-and-Weight Method. A fifty-barrel kick on the same section is at or beyond the capacity of the circulating system and risks exceeding the MAASP (Maximum Allowable Annular Surface Pressure) during the kill. Every barrel that is not admitted during shut-in is one fewer barrel that must be circulated back out against tight pressure margins (iwcf-level-2, Kick size and kill planning module).

Hard shut-in compresses the timeline between flow detection and closure to the minimum that the equipment allows. There is no intermediate step of routing flow to the choke and then closing that choke. The sequence is: stop the pumps, check for flow, close the BOP (Blowout Preventer). The BOP (Blowout Preventer) closing time on a properly maintained rig accumulator system is specified by API (American Petroleum Institute) STD 53 as 30 seconds or less for an annular preventer on a surface BOP (Blowout Preventer) stack and 30 seconds or less for ram preventers on the same stack (api-std-53, Section 6).

### The basic hard shut-in procedure while drilling

When a flow check confirms unwanted flow during drilling on an NCS (Norwegian Continental Shelf) surface BOP (Blowout Preventer) stack, the hard shut-in sequence is:

1. **Space out.** The driller picks up the drill string so that a plain pipe body, not a tool joint (the thickened threaded end of a drill pipe section that connects to the next joint), is across the expected sealing element of the BOP (Blowout Preventer). A tool joint inside an annular preventer (a BOP (Blowout Preventer) element that uses a rubber packing element to seal around any object in the bore) is acceptable because the rubber deforms around any shape, but a tool joint inside a pipe ram (a BOP (Blowout Preventer) element with opposing steel rams dressed for one specific pipe outer diameter) is not acceptable because the ram bore is sized for pipe body and will not seal on the larger tool joint.
2. **Stop the rotary.** The driller disengages the rotary drive and locks the string.
3. **Stop the mud pumps.** The pumps are ramped to zero flow. This is the last moment at which standpipe pressure indicates anything about downhole state; once the pumps are off, only the BOP (Blowout Preventer) shut-in pressures remain as diagnostic.
4. **Confirm the choke path is closed.** In a hard shut-in the HCR (Hydraulically-Controlled Remote) valve on the choke line (the high-pressure line that routes flow from the BOP (Blowout Preventer) stack to the choke manifold) is already closed. Downstream, the choke manifold valves and the choke itself are also closed. The driller verifies both before moving on. No flow path out of the wellbore is open.
5. **Close the BOP (Blowout Preventer).** Standard practice is to close the annular preventer first, because it closes fastest and seals on any object in the bore, and then set the upper pipe ram below it as a secondary well barrier element. Closing times are governed by API (American Petroleum Institute) STD 53 (api-std-53, Section 6).
6. **Record SIDPP (Shut-In Drill Pipe Pressure), SICP (Shut-In Casing Pressure), and pit gain** (the increase in the volume of drilling mud in the rig's surface pits, which is the primary direct indicator of kick size). Pressures are allowed to stabilise. On a gas kick, they may drift upward for several minutes as the gas migrates; on a water or oil kick, they stabilise faster. Standard practice is to record at one-minute intervals over at least five to ten minutes.
7. **Notify.** The driller informs the boresjef (toolpusher) and the boreleder (drilling supervisor). Both in turn initiate the operator and regulatory notification chain required under Offshore Norge Guideline 135 (the NCS (Norwegian Continental Shelf) guideline on well control incident classification and reporting) (offshore-norge-135, Notification).

The step that the hard method skips, relative to the soft method, is the deliberate opening of the HCR (Hydraulically-Controlled Remote) valve and choke path before the BOP (Blowout Preventer) closes. In a soft shut-in, that path is opened first, the BOP (Blowout Preventer) is closed, the influx above the BOP (Blowout Preventer) flows out through the choke manifold, and only then is the choke closed to build surface pressure. In a hard shut-in, the flow path stays closed throughout, and the BOP (Blowout Preventer) closure alone stops the flow.

### The water hammer transient

Abruptly stopping a flowing fluid converts its kinetic energy into a pressure spike. The amplitude of the spike is described by the Joukowsky relation (the classical fluid-mechanics result for pressure rise from sudden flow stoppage in a pipe):

```
dP = rho * c * dv
```

where dP is the pressure rise, rho is the fluid density, c is the speed of sound in the fluid in the pipe, and dv is the change in flow velocity.

For a typical NCS (Norwegian Continental Shelf) water-based drilling mud with density near 1,200 kg/m3 and an effective speed of sound of 1,200 to 1,500 m/s, stopping a flow velocity of 2 m/s gives a pressure rise on the order of 3 to 4 MPa (megapascals), which is roughly 450 to 600 psi (pounds per square inch). An oil-based mud gives a similar order because density is higher and sound speed is lower. The spike is short, on the order of the time it takes a pressure wave to travel to the nearest reflecting boundary (the casing shoe or surface) and return, but it adds directly to the static shut-in surface pressure that then builds up.

On a well where the predicted shut-in surface pressure is already close to the MAASP (Maximum Allowable Annular Surface Pressure), the water hammer transient can push the instantaneous casing-shoe pressure above the formation's fracture pressure and start an underground blowout. This is the specific risk that the soft shut-in alternative mitigates. A soft shut-in lets the flow continue briefly into the choke manifold after the BOP (Blowout Preventer) closes, which damps the transient before it reaches the shoe. The trade-off is more influx admitted during the routing, which raises the eventual static shut-in pressures (api-rp-59, Shut-in procedures; iadc-drilling-manual, Well control chapter).

### When hard shut-in is preferred

Hard shut-in is the preferred method when the casing shoe has ample pressure margin above the expected shut-in surface pressure and where response time is the dominant risk driver. Conditions on the NCS (Norwegian Continental Shelf) that typically favour hard shut-in:

- **Shallow hole sections**, where the fracture pressure at the shoe is far above any credible kick surface pressure. Surface casing and intermediate casing sections on NCS (Norwegian Continental Shelf) wells on Ekofisk, Valhall, Statfjord, Gullfaks, and Troll often fall in this category.
- **Surface BOP (Blowout Preventer) installations** where the choke line volume is small and water hammer damps quickly. The short plumbing between the BOP (Blowout Preventer) stack and the choke manifold on a fixed platform or jack-up limits the transient.
- **Fast-developing kicks**, for example connection gas that is observed to grow between connections, where the incremental seconds gained by hard shut-in translate directly into less influx volume.
- **Operator well programmes** that specify hard shut-in as the default for the section, subject to the crew being drilled on it and the BOP (Blowout Preventer) having a valid pressure test within its interval per NORSOK D-010 Rev 5 (the Norwegian well integrity standard) (norsok-d-010-rev5, Clause 7).

### When soft shut-in is preferred instead

Soft shut-in is typically preferred on NCS (Norwegian Continental Shelf) wells under the opposite conditions:

- **Deep sections** where the shoe is marginal to the expected shut-in surface pressure and where a water hammer spike would exceed the MAASP (Maximum Allowable Annular Surface Pressure).
- **Subsea BOP (Blowout Preventer) stacks**, where the long choke line from the seabed BOP (Blowout Preventer) up to the surface manifold amplifies water hammer and where the damping benefit of the soft method is large. Many NCS (Norwegian Continental Shelf) operators running subsea BOP (Blowout Preventer) stacks on floating drilling units default to soft shut-in for that reason.
- **Wells with weak formations above the shoe** flagged in the well programme, where the drilling engineer has determined that transient pressure control is more important than influx control.

The choice is made in the operator's well programme for each section and reviewed at the pre-drill meeting by the boreleder (drilling supervisor), the boresjef (toolpusher), and the drilling engineer. Once the section is drilling, the crew executes the method that the programme specifies, without improvising (iwcf-level-2, Shut-in procedures module).

### Hard shut-in in other operational contexts

The same "no flow path open" logic applies in every shut-in scenario, not only during drilling. Sibling articles cover the variants:

- Shut in while drilling: pipe on bottom, pumps running, rotary engaged.
- Shut in while tripping: pipe partially out of the hole, mud returns being monitored against the trip sheet.
- Shut in while running casing: large outer diameter string, displacement is substantial, float valves in play.
- Shut in while out of hole: no string across the BOP (Blowout Preventer), blind rams or blind-shear rams close on open hole.

In every variant, the hard method means that the BOP (Blowout Preventer) is closed with no open route out, and the soft method means that the choke path is opened first. The choice of which sealing element in the BOP (Blowout Preventer) stack is closed varies with what is in the hole.

### Pre-job requirements

Before an NCS (Norwegian Continental Shelf) drilling section starts, the crew and the rig must have:

- A weekly shut-in drill on the method chosen for the section, executed with timings recorded (iwcf-level-2, Shut-in procedures module).
- A BOP (Blowout Preventer) pressure test within its interval, typically within 14 days on a surface BOP (Blowout Preventer) stack on the NCS (Norwegian Continental Shelf) (norsok-d-010-rev5, Clause 7; api-std-53, Section 7).
- A BOP (Blowout Preventer) function test within its interval, typically weekly.
- A pre-tour toolbox talk covering the shut-in procedure for the section.
- An up-to-date kill sheet (a pre-calculated worksheet that gives the initial and final circulating pressures for the kill based on current mud weight, formation pressure, pump strokes, and volumes) with current MAASP (Maximum Allowable Annular Surface Pressure) and the most recent formation integrity or leak-off test value.

Without these pre-job items in place, NORSOK D-010 Rev 5 (the Norwegian well integrity standard) does not accept the BOP (Blowout Preventer) as a credited well barrier element (a tested component counted toward the two independent barriers required during drilling), and drilling cannot continue (norsok-d-010-rev5, Clause 6).

## NCS-specific context

On the NCS (Norwegian Continental Shelf) the framework for shut-in procedures is a layered stack of regulation, standards, syllabi, and operator practice. Havtil (Havindustritilsynet, the Norwegian Ocean Industry Authority, formerly Petroleumstilsynet) sets the top-level requirement through the Innretningsforskriften (the Facilities Regulations) and the Aktivitetsforskriften (the Activities Regulations): well control equipment must be designed, tested, and maintained to recognised standards, and a tested well control procedure must exist. Neither regulation names hard or soft shut-in explicitly. NORSOK D-010 Rev 5 (the Norwegian well integrity standard) operationalises these requirements, referencing API (American Petroleum Institute) STD 53 and API (American Petroleum Institute) RP 59 for equipment and well control operations and setting the two-barrier philosophy that frames all NCS (Norwegian Continental Shelf) kick response (norsok-d-010-rev5, Clause 6).

Operator practice on surface BOP (Blowout Preventer) fixed-platform installations on the NCS (Norwegian Continental Shelf) commonly defaults to hard shut-in. The rationale is that fixed-platform surface stacks have short choke lines, manageable water hammer, and benefit most from the rapid influx containment that hard shut-in provides. On Ekofisk, Valhall, Gullfaks, Statfjord, and Troll platform drilling operations, hard shut-in is the procedure the crew has drilled and the procedure that the well programme specifies for most sections.

On floating drilling units working subsea BOP (Blowout Preventer) stacks on the NCS (Norwegian Continental Shelf), soft shut-in is more commonly the default. The long choke line running from the seabed BOP (Blowout Preventer) up through the LMRP (Lower Marine Riser Package, the upper removable half of a subsea BOP (Blowout Preventer) stack) and the riser to the surface manifold amplifies the water hammer transient. The influx-control benefit of hard shut-in does not outweigh the transient-pressure penalty at the shoe, so operators on subsea operations frequently select soft shut-in as the baseline.

Role responsibility is consistent across installation types. The boresjef (toolpusher), on some rigs also called the borebas (toolpusher), holds rig-side responsibility for ensuring the crew is drilled on the chosen shut-in method and that BOP (Blowout Preventer) equipment is function-tested and pressure-tested within its interval. The boreleder (drilling supervisor), as the operator's senior onsite representative, holds operator-side responsibility for confirming the method choice against the well programme and for countersigning the BOP (Blowout Preventer) test records. The driller and the assistant driller execute the drill and execute the real procedure when a kick is taken (norsok-d-010-rev5, Clause 6; iwcf-level-2, Shut-in procedures module).

After a real hard shut-in on a kick, Offshore Norge Guideline 135 (the NCS (Norwegian Continental Shelf) guideline on well control incident classification and reporting) applies. The event is classified by influx volume, by formation fluid type, and by duration. The recorded SIDPP (Shut-In Drill Pipe Pressure), SICP (Shut-In Casing Pressure), and pit gain become part of the incident case file reviewed by the operator and by Havtil (Havindustritilsynet, the Norwegian Ocean Industry Authority). BOP (Blowout Preventer) equipment condition, including the annular preventer element inspection after a stripping job, is part of the post-event review (offshore-norge-135, Classification; offshore-norge-135, Post-event review).

## Norwegian terminology

| Norwegian | English | Notes |
|---|---|---|
| hard innstengning | hard shut-in | Direct rendering of the procedure name used in NCS (Norwegian Continental Shelf) operator manuals. |
| myk innstengning | soft shut-in | The alternative procedure with the choke path opened first. |
| innstengning | shut-in | General term for closing in the well. |
| utblåsningssikring | blowout preventer (BOP) | Generic Norwegian term for any BOP (Blowout Preventer) element. |
| boresjef | toolpusher | Senior rig-based drilling supervisor on an NCS (Norwegian Continental Shelf) installation. |
| borebas | toolpusher | Alternative title for the same rig-side role, used on some installations. |
| boreleder | drilling supervisor | Operator's senior onsite representative, sign-off authority on the well programme. |
| brønnbarriere | well barrier | Tested component credited in the NORSOK D-010 Rev 5 (the Norwegian well integrity standard) two-barrier philosophy. |
| strupe | choke | The adjustable orifice on the choke manifold. |
| strupeventil | choke valve | Valve in the choke line and manifold. |
| innretningsforskriften | Facilities Regulations | Havtil (Havindustritilsynet, the Norwegian Ocean Industry Authority) regulation governing facility design. |
| aktivitetsforskriften | Activities Regulations | Havtil (Havindustritilsynet, the Norwegian Ocean Industry Authority) regulation governing operations. |

## Sources

1. API Standard 53, Fifth Edition (2018). American Petroleum Institute. Sections 6 and 7. Paywalled. Verified 2026-04-20 by agent:drilling-content-v1.
2. API Recommended Practice 59 (2019). American Petroleum Institute. Shut-in procedures and kick response sections. Paywalled. Verified 2026-04-20 by agent:drilling-content-v1.
3. NORSOK D-010 Rev 5 (2021). Standards Norway. Clauses 6 and 7. Paywalled. Verified 2026-04-20 by agent:drilling-content-v1.
4. IWCF Drilling Well Control Level 2 Syllabus (2023). International Well Control Forum. Shut-in procedures and kick size and kill planning modules. Restricted. Verified 2026-04-20 by agent:drilling-content-v1.
5. Offshore Norge Guideline 135 (2020). Offshore Norge. Classification, notification, and post-event review sections. Open. Verified 2026-04-20 by agent:drilling-content-v1.
6. IADC Drilling Manual, 12th Edition (2015). International Association of Drilling Contractors. Well control chapter. Paywalled. Verified 2026-04-20 by agent:drilling-content-v1.

## Related concepts

- Soft shut-in (sibling article; the alternative method with the choke path opened before the BOP (Blowout Preventer) closes).
- Shut in while drilling, while tripping, while running casing, and while out of hole (sibling articles; variant procedures keyed to what is in the hole).
- Recording SIDPP (Shut-In Drill Pipe Pressure), SICP (Shut-In Casing Pressure), and pit gain (sibling article; the diagnostic step that follows every shut-in).
- Annular preventer (tree-internal article; the BOP (Blowout Preventer) element most commonly closed first in a hard shut-in on a surface BOP (Blowout Preventer) stack).
