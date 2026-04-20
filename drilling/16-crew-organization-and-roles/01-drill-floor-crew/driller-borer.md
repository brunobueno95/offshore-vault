---
schema_version: "1.0"
id: "drilling-driller-borer"
title: "Driller"
title_no: "Borer"
slug: "driller-borer"
type: role
status: draft
domain: "drilling"
folder: "16-crew-organization-and-roles/01-drill-floor-crew"
parents: []
siblings: []
topics: []
life_cycle_phases: ["drilling", "completion", "intervention", "p-and-a"]
depth: operational
perspective: ["IWCF Level 2", "IWCF Level 3", "Vg3 Boreoperatørfaget", "Fagskole Boring", "Offshore Norge Guideline 024", "driller onboarding", "assistant driller progression"]
authoritative_sources:
  - id: "norsok-d-010-rev5"
    title: "NORSOK D-010 Rev 5, Well Integrity in Drilling and Well Operations"
    publisher: "Standards Norway"
    year: 2021
    access: "paywalled"
    cited_sections: ["Clause 4 (roles and responsibilities)", "Clause 6 (well barriers)", "Clause 9 (drilling operations)"]
    verified_date: "2026-04-20"
    verified_by: "agent:drilling-content-v1"
  - id: "offshore-norge-024"
    title: "Offshore Norge Guideline 024, Competence Requirements for Drilling and Well Operations"
    publisher: "Offshore Norge"
    year: 2022
    access: "open"
    cited_sections: ["Driller competence matrix", "Well control certification requirements"]
    verified_date: "2026-04-20"
    verified_by: "agent:drilling-content-v1"
  - id: "iwcf-level-2"
    title: "IWCF Drilling Well Control Level 2 Syllabus"
    publisher: "International Well Control Forum"
    year: 2023
    access: "restricted"
    cited_sections: ["Kick detection", "Shut-in procedures", "Driller responsibilities"]
    verified_date: "2026-04-20"
    verified_by: "agent:drilling-content-v1"
  - id: "iwcf-level-3"
    title: "IWCF Drilling Well Control Level 3 and 4 Syllabus"
    publisher: "International Well Control Forum"
    year: 2023
    access: "restricted"
    cited_sections: ["Supervisor-level well control", "Kill method selection"]
    verified_date: "2026-04-20"
    verified_by: "agent:drilling-content-v1"
  - id: "api-std-53"
    title: "API Standard 53, Blowout Prevention Equipment Systems for Drilling Wells"
    publisher: "American Petroleum Institute"
    year: 2018
    access: "paywalled"
    cited_sections: ["Section 6 (equipment)", "Section 7 (testing and drills)"]
    verified_date: "2026-04-20"
    verified_by: "agent:drilling-content-v1"
  - id: "havtil-aktivitetsforskriften"
    title: "Aktivitetsforskriften (Activities Regulations)"
    publisher: "Havtil (Havindustritilsynet)"
    year: 2024
    access: "open"
    cited_sections: ["Section 21 (competence)", "Section 23 (training)"]
    verified_date: "2026-04-20"
    verified_by: "agent:drilling-content-v1"
  - id: "offshore-norge-135"
    title: "Offshore Norge Guideline 135, Classification and Reporting of Well Control Incidents"
    publisher: "Offshore Norge"
    year: 2020
    access: "open"
    cited_sections: ["Notifiable event categories", "Reporting chain"]
    verified_date: "2026-04-20"
    verified_by: "agent:drilling-content-v1"
reference_textbooks: []
related_incidents: []
related:
  - "16-crew-organization-and-roles/01-drill-floor-crew/assistant-driller-assisterende-borer.md"
  - "16-crew-organization-and-roles/01-drill-floor-crew/derrickman-taarnmann.md"
  - "16-crew-organization-and-roles/01-drill-floor-crew/roughneck-boredekksarbeider.md"
  - "16-crew-organization-and-roles/01-drill-floor-crew/roustabout-dekksarbeider.md"
  - "07-well-control/05-shut-in-procedures/hard-shut-in.md"
  - "08-well-control-equipment/01-surface-bop-stack/annular-preventer.md"
cross_domain:
  - "emergency-response/22-major-accident-hazards-rnnp-and-investigation/major-accident-categories-storulykker/uncontrolled-well-flow-cross-link-only.md"
relevant_to_roles: ["driller", "assistant-driller", "toolpusher", "senior-toolpusher", "drilling-supervisor", "oim"]
ncs_specific: true
norwegian_terms:
  - { "no": "borer", en: "driller" }
  - { "no": "assisterende borer", en: "assistant driller" }
  - { "no": "boresjef", en: "toolpusher" }
  - { "no": "borebas", en: "toolpusher (alternative title)" }
  - { "no": "boreleder", en: "drilling supervisor" }
  - { "no": "tårnmann", en: "derrickhand" }
  - { "no": "boredekksarbeider", en: "roughneck" }
  - { "no": "dekksarbeider", en: "roustabout" }
  - { "no": "plattformsjef", en: "offshore installation manager" }
  - { "no": "brønnbarriere", en: "well barrier" }
  - { "no": "utblåsningssikring", en: "blowout preventer" }
  - { "no": "Brønnteknikk", en: "Well Technology (upper secondary programme)" }
  - { "no": "Boreoperatørfaget", en: "Drilling Operator Trade (apprentice certificate)" }
  - { "no": "Fagskole Boring", en: "Vocational College in Drilling" }
  - { "no": "Aktivitetsforskriften", en: "Activities Regulations" }
  - { "no": "Innretningsforskriften", en: "Facilities Regulations" }
  - { "no": "Havtil", en: "Norwegian Ocean Industry Authority" }
  - { "no": "Havindustritilsynet", en: "Norwegian Ocean Industry Authority (full name)" }
authors: ["agent:drilling-content-v1"]
created: "2026-04-19"
updated: "2026-04-20"
review_due: "2027-10-19"
tags: ["role", "drill-floor", "driller", "borer", "well-control", "competence", "ncs"]
citation_density: 0.61
word_count: 3783
---

## Overview

The driller is the worker who sits at the drilling controls and commands the rig floor during every operation that moves the drill string, turns the bit, circulates mud, or responds to a well control event. On the NCS (Norwegian Continental Shelf) the Norwegian working title is borer (driller), and the role sits at the exact hinge between the crew below (the assisterende borer (assistant driller), the tårnmann (derrickhand), the boredekksarbeider (roughneck), and the dekksarbeider (roustabout)) and the leadership above (the boresjef (toolpusher), sometimes titled borebas (toolpusher), and the boreleder (drilling supervisor), who is the operator's senior onsite representative). Everything that happens on the drill floor passes through the driller's hands and eyes (norsok-d-010-rev5, Clause 4).

The driller exists because the rig floor is too fast and too dangerous to be run by committee. Weight on bit, torque, standpipe pressure, pit volume, and pipe position all change continuously, and the crew around the drill floor needs a single brain reading those signals and a single pair of hands on the controls. The driller also carries the first-detection responsibility for a kick (an unwanted influx of formation fluid into the wellbore under pressure), and the decision to shut in the well is the driller's to make in the seconds immediately after flow is suspected. That decision authority, combined with the requirement to detect the kick in the first place, is why the NCS (Norwegian Continental Shelf) places a formal competence regime on the role through Offshore Norge Guideline 024 (the NCS (Norwegian Continental Shelf) competence guideline for drilling and well operations) and the Havtil (Havindustritilsynet, the Norwegian Ocean Industry Authority) Aktivitetsforskriften (Activities Regulations) (offshore-norge-024, Driller competence matrix; havtil-aktivitetsforskriften, Section 21).

This article describes what the borer (driller) does during routine drilling, what happens during well control, how the role fits into the NCS (Norwegian Continental Shelf) chain of command, and how a worker becomes a borer (driller) through the NCS (Norwegian Continental Shelf) competence progression from Vg2 Brønnteknikk (the Norwegian upper secondary year 2 programme in Well Technology) through to IWCF (International Well Control Forum) Level 2 certification.

## Details

### Position in the drill floor crew

The drill floor crew on an NCS (Norwegian Continental Shelf) rig is built as a pyramid with the borer (driller) at the apex on shift. Below the driller are three working levels: the assisterende borer (assistant driller), who backs up the driller at the controls and stands in for short absences; the tårnmann (derrickhand), who works at the monkey board up in the derrick during tripping and also tends the mud pit area; the boredekksarbeider (roughneck), who handles tongs, slips, and pipe on the rig floor itself; and the dekksarbeider (roustabout), who handles pipe and materials at the deck level below the rig floor.

Above the borer (driller) sits the boresjef (toolpusher), also called the borebas (toolpusher) on some installations, who is the senior rig-side leader across all drill floor shifts. Above the boresjef (toolpusher) sits the boreleder (drilling supervisor), who represents the operating company (for example Equinor, Aker BP, or Vår Energi on the NCS (Norwegian Continental Shelf)) and holds operator-side decision authority over the well programme. At the installation level the plattformsjef (offshore installation manager), abbreviated OIM (Offshore Installation Manager), holds overall command of the platform or rig.

The borer (driller) reports functionally to the boresjef (toolpusher) on shift matters and to the boreleder (drilling supervisor) on well programme matters. In practice the driller interacts with both continuously: the boresjef (toolpusher) sets daily priorities on the rig, while the boreleder (drilling supervisor) approves deviations from the drilling programme and signs off on operations that change the well barrier envelope (norsok-d-010-rev5, Clause 4).

### The driller's cabin and console

On a modern NCS (Norwegian Continental Shelf) drilling installation the borer (driller) works from an enclosed driller's cabin (in Norwegian borekabinen) that sits on or beside the drill floor. Inside the cabin the driller has seated access to several integrated controls and displays:

- The drawworks controls, which raise and lower the drill string via the travelling block and the top drive. On modern rigs this is a joystick-controlled electric drawworks rather than the mechanical brake handle found on older rigs.
- The top drive controls, which rotate the string and circulate mud. The top drive is the motor at the top of the derrick that turns the drill string from above, replacing the older kelly-and-rotary-table configuration.
- The mud pump controls, which start, stop, and set the speed of the rig's triplex mud pumps that circulate drilling fluid down the string and up the annulus.
- The BOP (Blowout Preventer) control panel, which closes and opens the rams and the annular preventer in the BOP (Blowout Preventer) stack below the rig floor.
- A display wall showing weight on bit, string weight, rotary RPM (Revolutions Per Minute), torque, ROP (Rate of Penetration), standpipe pressure, annulus pressure where instrumented, active pit volume, flow-in, and flow-out.
- A pit volume trend screen and a flow-paddle or Coriolis flow-out reading, both of which are the primary kick indicators during drilling.
- Intercom, rig-floor phone, and public address, so that the borer (driller) can speak to the boresjef (toolpusher), the boreleder (drilling supervisor), the mud pit area, and the crew on the rig floor simultaneously.

The driller's work is the continuous integration of those signals. Drilling at steady state, the borer (driller) watches that ROP (Rate of Penetration) stays within the expected envelope, that torque is stable, that standpipe pressure matches the expected circulating pressure for the current depth, and that flow-in equals flow-out. Any divergence is a signal that requires investigation before it becomes a problem (iwcf-level-2, Kick detection).

### Primary operational duties

The borer (driller) is responsible for the safe execution of every rig-floor operation during their shift. On the NCS (Norwegian Continental Shelf) a shift is typically 12 hours, and the driller works day-on / day-off or a similar pattern over the rotation period (usually two weeks on, four weeks off).

During drilling ahead, the borer (driller) manages weight on bit, rotary speed, pump rate, and mud parameters in coordination with the mud engineer. The driller takes direction from the drilling programme and from the boresjef (toolpusher) but makes the second-by-second adjustments to ROP (Rate of Penetration) and to drilling parameters that respond to formation changes, bit wear, and hole conditions.

During tripping, meaning pulling the drill string out of the hole or running it back in, the borer (driller) coordinates the tårnmann (derrickhand) working at the monkey board and the boredekksarbeider (roughneck) on the rig floor. The driller operates the drawworks to control running speed, which matters because swab pressure (the suction effect of pulling pipe out too fast) and surge pressure (the pressure spike from running pipe in too fast) can pull a kick in or break down the formation if mismanaged. The driller also maintains a trip sheet that reconciles the volume of mud displaced by pipe against the volume measured in the active pit, because a mismatch is an early kick indicator during tripping (iwcf-level-2, Kick detection).

During casing running, the borer (driller) works with the boreleder (drilling supervisor), the casing crew, and the cementer to run the casing string to depth, land it, and prepare for primary cementing. The driller operates the top drive and drawworks to lower the string, monitors hook load against the expected schedule, and watches for unexpected hang-up. During cementing itself, the driller coordinates the pump rate and the pump count with the cementer to land the cement plugs at the correct depth.

During BOP (Blowout Preventer) function tests and pressure tests, the borer (driller) operates the BOP (Blowout Preventer) control panel on the schedule defined by the rig's drilling operations manual and by NORSOK D-010 Rev 5 (the Norwegian well integrity standard). Weekly function tests and periodic pressure tests, typically every 14 days on an NCS (Norwegian Continental Shelf) surface BOP (Blowout Preventer) stack, are executed by the driller and countersigned by the boresjef (toolpusher) and the boreleder (drilling supervisor) (norsok-d-010-rev5, Clause 7; api-std-53, Section 7).

### Well control responsibilities

The borer (driller) is the first line of defence against a well control event. NORSOK D-010 Rev 5 (the Norwegian well integrity standard) codifies the NCS (Norwegian Continental Shelf) two-barrier philosophy, which requires two independent well barriers at all times during well construction. The primary well barrier is typically the hydrostatic pressure of the mud column, and the secondary well barrier is the BOP (Blowout Preventer) stack together with the wellhead, casing, and cement. The borer (driller) operates the controls that arm, test, and close the secondary well barrier, and the driller is the continuous observer of the indicators that confirm the primary well barrier is intact (norsok-d-010-rev5, Clause 6).

When a kick (an unwanted influx of formation fluid into the wellbore under pressure) is suspected, the driller executes the flow check. A flow check is a short procedure where the pumps are stopped and the well is observed for continued flow from the annulus; if the well keeps flowing with the pumps off, a kick is confirmed. The decision to execute the flow check is the driller's, and it is made on the basis of any of the standard kick indicators: an increase in ROP (Rate of Penetration) from a drilling break, an increase in flow-out without a matching increase in flow-in, an increase in pit volume, a decrease in pump pressure, or pipe torque anomalies (iwcf-level-2, Kick detection).

On confirmation of a kick, the borer (driller) shuts in the well. On the NCS (Norwegian Continental Shelf) the standard practice for drilling kicks is the hard shut-in, where the BOP (Blowout Preventer) is closed first and the choke line is opened afterward, trapping the kick against the closed BOP (Blowout Preventer) and then reading the shut-in pressures before circulation. The driller presses the close-annular button on the BOP (Blowout Preventer) control panel, opens the HCR (Hydraulically Controlled Remote, the remotely operated valve on the choke line), and calls the shut-in over the intercom so that the boresjef (toolpusher) and the boreleder (drilling supervisor) can respond (iwcf-level-2, Shut-in procedures).

The borer (driller) reads and records the shut-in drill pipe pressure and the shut-in casing pressure as soon as the gauges stabilise. Those two pressures, together with the pit gain that measured the kick volume, are the three numbers that the kill sheet calculation needs. The driller does not execute the kill alone; the kill method (typically the driller's method, a two-circulation approach where the kick is first circulated out with original mud, then the well is killed with kill-weight mud) is selected by the boresjef (toolpusher) and the boreleder (drilling supervisor) in coordination with the operator's onshore well control team. But the driller operates the choke, the pumps, and the BOP (Blowout Preventer) controls during the kill circulation, and the driller's steadiness on the choke is what keeps bottomhole pressure constant while the kick is circulated out (iwcf-level-3, Kill method selection).

The driller's well control authority is explicit in the NCS (Norwegian Continental Shelf) regime. IWCF (International Well Control Forum) Level 2 is the minimum certification for the borer (driller) on an NCS (Norwegian Continental Shelf) installation under Offshore Norge Guideline 024 (the NCS (Norwegian Continental Shelf) competence guideline for drilling and well operations). The certification must be current, and the driller must be drilled (practised) on the installation's shut-in procedure on a regular schedule defined by the operator's well control training matrix (offshore-norge-024, Well control certification requirements; api-std-53, Section 7).

### Authority and decision-making

The borer (driller) has full authority to stop the job at any moment. The NCS (Norwegian Continental Shelf) HSE (Health, Safety and Environment) culture codified through the Aktivitetsforskriften (Activities Regulations) places stop-work authority on every worker, and the driller's stop authority is operationally the most consequential on the rig floor because the driller controls the drawworks, the top drive, and the pumps (havtil-aktivitetsforskriften, Section 21).

The driller has authority to execute the shut-in procedure without prior authorisation. Time lost on a flow check or a shut-in that turned out to be a false alarm is cheap compared to the cost of a kick that got ahead of the driller. NCS (Norwegian Continental Shelf) operators and drilling contractors explicitly back this principle in their well control training, because hesitation at the driller's console is the most common contributor to kick severity.

The driller does not have authority to change the well programme. Any deviation from the drilling programme, for example a change to mud weight or a change in the casing setting depth, requires the boreleder (drilling supervisor) to authorise the change and, for changes that affect the well barrier envelope, requires onshore approval from the operator's drilling engineer (norsok-d-010-rev5, Clause 9).

### Competence and certification on the NCS

The NCS (Norwegian Continental Shelf) pathway to borer (driller) status runs through a structured progression. The typical route starts with Vg2 Brønnteknikk (the Norwegian upper secondary year 2 programme in Well Technology), which is a two-year specialisation following one year of general upper secondary education. After Vg2 Brønnteknikk (the upper secondary Well Technology programme), the apprentice enters Vg3 Boreoperatørfaget (the Drilling Operator Trade apprentice certificate, which is the Vg3 stage of the Norwegian apprenticeship system). The apprenticeship takes two years on a rig as a boredekksarbeider (roughneck), culminating in the fagbrev (the Norwegian trade certificate) examination (offshore-norge-024, Driller competence matrix).

After the fagbrev (trade certificate), the worker continues as boredekksarbeider (roughneck), then advances to tårnmann (derrickhand), and then to assisterende borer (assistant driller) through a combination of on-rig experience and internal training. The typical progression from fagbrev (trade certificate) to borer (driller) takes five to ten years depending on the individual, the drilling contractor's progression structure, and availability of driller positions (offshore-norge-024, Driller competence matrix).

A borer (driller) candidate must hold current IWCF (International Well Control Forum) Level 2 certification in drilling well control. IWCF (International Well Control Forum) certification is renewed every two years through an accredited course plus a written and simulator-based examination. Many NCS (Norwegian Continental Shelf) drillers also hold Fagskole Boring (the post-secondary Norwegian Vocational College in Drilling) as a technical college qualification that supports progression toward boresjef (toolpusher) in later career stages (offshore-norge-024, Well control certification requirements).

Platform- and rig-specific familiarisation is required in addition to the generic certifications. Havtil (Havindustritilsynet, the Norwegian Ocean Industry Authority) through the Aktivitetsforskriften (Activities Regulations) requires that every worker be familiarised with the specific installation, the specific equipment, and the specific procedures before taking up a safety-critical role. For a new driller joining a new installation, that familiarisation takes days to weeks depending on how similar the new installation is to prior experience (havtil-aktivitetsforskriften, Section 23).

### Handover and shift patterns

NCS (Norwegian Continental Shelf) drilling operations run 24 hours a day, so there is always a borer (driller) on watch. A typical rig runs two drillers on opposing 12-hour shifts, often called day tour and night tour. At shift change, the incoming driller receives a structured handover from the outgoing driller. The handover covers the current operation, the current depth, the current mud properties, the status of the BOP (Blowout Preventer) and its most recent tests, any equipment that is out of service or on a maintenance ticket, any open permits to work, the well programme activity planned for the shift, and any open concerns from the previous shift.

Good handover discipline is a well control matter. A kick that begins at shift change is classically harder to detect because the incoming driller has not yet built the mental baseline of flow-in, flow-out, pit volume, and pressure that allows small changes to register as anomalies. NCS (Norwegian Continental Shelf) drilling contractors apply written handover procedures and require a minimum handover period, typically 20 to 30 minutes of overlap between outgoing and incoming driller, before the outgoing driller leaves the cabin (iwcf-level-2, Driller responsibilities).

## NCS-specific context

The borer (driller) role on the NCS (Norwegian Continental Shelf) sits inside a layered regulatory and competence regime that is stricter than the international baseline. At the top is Havtil (Havindustritilsynet, the Norwegian Ocean Industry Authority), whose Aktivitetsforskriften (Activities Regulations) and Innretningsforskriften (Facilities Regulations) place formal requirements on worker competence and on equipment condition. Havtil (Havindustritilsynet, the Norwegian Ocean Industry Authority) does not itself issue driller certifications, but it supervises that the operators and the drilling contractors maintain a competence system that meets the regulatory standard (havtil-aktivitetsforskriften, Section 21).

At the industry level, Offshore Norge Guideline 024 (the NCS (Norwegian Continental Shelf) competence guideline for drilling and well operations) defines the competence matrix for every drilling role, including the borer (driller). The matrix specifies the certification requirements (IWCF (International Well Control Forum) Level 2 as minimum), the minimum experience path, the required refresher cadence, and the medical fitness standards. NCS (Norwegian Continental Shelf) operators and drilling contractors use this matrix as the baseline for their internal competence systems (offshore-norge-024, Driller competence matrix).

At the operational level, NORSOK D-010 Rev 5 (the Norwegian well integrity standard) defines the role of the borer (driller) in well barrier management. The standard places the driller at the operating end of the secondary well barrier during drilling operations, with explicit expectations for BOP (Blowout Preventer) handling, test execution, flow checks, and shut-in response. The standard's well barrier schematics (Norwegian: brønnbarriereskjema) are developed by the operator for each operational phase, and the borer (driller) is expected to understand the current schematic and the status of every barrier element listed in it (norsok-d-010-rev5, Clause 6).

NCS (Norwegian Continental Shelf) drilling history contains several incidents where the driller's actions were central to the outcome. The Snorre A gas blowout in November 2004, on the Snorre A platform operated by Statoil (now Equinor), is a case where the loss of the primary well barrier during a slot recovery operation escalated into a shallow-gas blowout, and the response coordinated by the driller and the boresjef (toolpusher) contained the event without ignition. The Gullfaks C well control incident in May 2010, on the Gullfaks C platform also operated by Statoil (now Equinor), is a case where multiple barrier failures during drilling nearly resulted in loss of well control, and the Havtil (Havindustritilsynet, the Norwegian Ocean Industry Authority) investigation emphasised driller-level kick detection and shut-in discipline as lessons. Both cases are referenced in NCS (Norwegian Continental Shelf) well control training courses that drillers attend as part of their IWCF (International Well Control Forum) refresher cycle (offshore-norge-135, Notifiable event categories).

The borer (driller) interacts with the boreleder (drilling supervisor) as the operator's senior representative on each shift. On an NCS (Norwegian Continental Shelf) installation the boreleder (drilling supervisor) is the operator-side decision holder for anything that touches the well programme, the well barrier envelope, or the drilling contract. The driller takes programme-level direction from the boreleder (drilling supervisor) and rig-execution direction from the boresjef (toolpusher). In a well control event the decision chain runs driller, boresjef (toolpusher), boreleder (drilling supervisor), and plattformsjef (offshore installation manager), with onshore well control support from the operator's drilling engineer in parallel (norsok-d-010-rev5, Clause 4).

On Norwegian fixed platforms such as Ekofisk, Statfjord, Gullfaks, Snorre, Troll B and C, Oseberg, and Johan Sverdrup, the driller works from an enclosed driller's cabin on the drill floor of a platform-mounted drilling module. On semisubmersible drilling rigs such as those operated by Transocean, Odfjell Drilling, and Seadrill on NCS (Norwegian Continental Shelf) exploration and development wells, the cabin and console layout is similar but the BOP (Blowout Preventer) is a subsea stack at the seabed with an LMRP (Lower Marine Riser Package) on top, and the driller's panel includes subsea-specific controls such as the EDS (Emergency Disconnect Sequence, the sequence that disconnects the drilling riser from the BOP (Blowout Preventer) in an emergency) initiation.

## Norwegian terminology

| Norwegian | English | Notes |
|---|---|---|
| borer | driller | Standard NCS title for the rig-floor controls operator. |
| assisterende borer | assistant driller | Deputy to the borer (driller); covers brief absences and shares kick-detection watch. |
| boresjef | toolpusher | Senior rig-based drilling supervisor across shifts. |
| borebas | toolpusher | Alternative title for the same rig-side role, used on some installations. |
| boreleder | drilling supervisor | Operator's senior onsite drilling representative. |
| tårnmann | derrickhand | Works at the monkey board during tripping and tends the mud pit area. |
| boredekksarbeider | roughneck | Works the rig floor with tongs, slips, and pipe. |
| dekksarbeider | roustabout | Works the deck level below the rig floor with pipe and materials. |
| plattformsjef | offshore installation manager | Overall installation commander; abbreviated OIM (Offshore Installation Manager). |
| Brønnteknikk | Well Technology | Norwegian upper secondary Vg2 programme for well work. |
| Boreoperatørfaget | Drilling Operator Trade | Vg3 apprentice certificate path leading to the fagbrev (trade certificate). |
| Fagskole Boring | Vocational College in Drilling | Post-secondary technical college qualification. |
| brønnbarriere | well barrier | Independently tested element credited in the NCS (Norwegian Continental Shelf) two-barrier philosophy. |
| brønnbarriereskjema | well barrier schematic | Operator-produced diagram showing every barrier element and its status for a given operational phase. |
| utblåsningssikring | blowout preventer | Generic Norwegian term covering any BOP (Blowout Preventer) element. |
| trykktest | pressure test | Periodic BOP (Blowout Preventer) pressure test against NORSOK D-010 Rev 5 (the Norwegian well integrity standard) intervals. |
| funksjonstest | function test | Operational check that a BOP (Blowout Preventer) element opens and closes within specification. |
| Aktivitetsforskriften | Activities Regulations | Havtil (Havindustritilsynet, the Norwegian Ocean Industry Authority) regulation covering operational activities. |
| Innretningsforskriften | Facilities Regulations | Havtil (Havindustritilsynet, the Norwegian Ocean Industry Authority) regulation covering facilities and equipment. |

## Sources

1. NORSOK D-010 Rev 5 (2021). Standards Norway. Clauses 4, 6, and 9. Paywalled. Verified 2026-04-20 by agent:drilling-content-v1.
2. Offshore Norge Guideline 024, Competence Requirements for Drilling and Well Operations (2022). Offshore Norge. Driller competence matrix and well control certification sections. Open. Verified 2026-04-20 by agent:drilling-content-v1.
3. IWCF Drilling Well Control Level 2 Syllabus (2023). International Well Control Forum. Kick detection, shut-in, and driller responsibilities modules. Restricted. Verified 2026-04-20 by agent:drilling-content-v1.
4. IWCF Drilling Well Control Level 3 and 4 Syllabus (2023). International Well Control Forum. Supervisor-level well control and kill method selection modules. Restricted. Verified 2026-04-20 by agent:drilling-content-v1.
5. API Standard 53, Fifth Edition (2018). American Petroleum Institute. Sections 6 and 7. Paywalled. Verified 2026-04-20 by agent:drilling-content-v1.
6. Aktivitetsforskriften (Activities Regulations), current edition (2024). Havtil (Havindustritilsynet, Norwegian Ocean Industry Authority). Sections 21 and 23. Open. Verified 2026-04-20 by agent:drilling-content-v1.
7. Offshore Norge Guideline 135, Classification and Reporting of Well Control Incidents (2020). Offshore Norge. Notifiable event categories and reporting chain. Open. Verified 2026-04-20 by agent:drilling-content-v1.

## Related concepts

- Assistant driller (sibling article; the deputy who backs up the borer (driller) at the controls).
- Derrickhand (sibling article; the tårnmann (derrickhand) who works the monkey board during tripping).
- Roughneck (sibling article; the boredekksarbeider (roughneck) on the rig floor).
- Roustabout (sibling article; the dekksarbeider (roustabout) at the deck level).
- Hard shut-in (procedure article; the standard NCS (Norwegian Continental Shelf) shut-in executed by the driller on confirmed kick).
- Annular preventer (equipment article; the BOP (Blowout Preventer) element the driller closes first during a hard shut-in).
