# _AGENT_RULES.md — how agents write articles

**Version:** 1.0  
**Scope:** every agent that writes content into any tree of `offshore-vault/`

This file defines how an agent fills a leaf article's content body after the skeleton is built. The stub frontmatter is already present in every leaf; the agent's job is to populate it and write the article body.

---

## The contract

An agent working in a tree:

1. Reads only its tree's `CLAUDE.md` plus the specific article stub it is filling.
2. May read sibling articles in the same folder for context.
3. May read `_INDEX.md` files up the folder path for scope orientation.
4. Does NOT read other trees.
5. Writes article content per the structure defined below.
6. Updates frontmatter fields per the schema.
7. Leaves the article at `status: draft` or `status: review` but never `published` (only the validator may promote to published).

---

## Article body structure

Every article body follows this structure. Section headers use `##` for the main sections. Skip a section if genuinely not applicable, but most articles will use all of them.

### Required sections

**`## Overview`**  
One to three paragraphs. Defines the concept, equipment, procedure, or topic in plain terms. Answers "what is this" and "why does it matter on the NCS". No lists. Assumes the reader has the prerequisite knowledge implied by the article's `depth` tier.

**`## Details`**  
The main content. Depth-specific:

- `foundational`: principles, physics, classifications, definitions. Tables and diagrams welcome.
- `operational`: how it works in practice, operational envelopes, decision rules, day-to-day use.
- `advanced`: quantitative treatment, edge cases, failure modes, standards interpretation.

Use subheadings (`###`) freely within this section.

**`## NCS-specific context`**  
How this topic manifests on the Norwegian Continental Shelf specifically. Regulatory references (Havtil, NORSOK, Offshore Norge), NCS operators and fields where relevant, NCS incident history, Norwegian working terms. This section is what distinguishes the vault from generic oilfield reference material.

**`## Norwegian terminology`**  
Table of Norwegian terms relevant to the article. Format:

```markdown
| Norwegian | English | Notes |
|---|---|---|
| kranfører | crane operator | G5 competence holder on NCS |
| løfteleder | lift supervisor | Appointed for critical lifts per NORSOK R-003 |
```

Include at least one row when `ncs_specific: true`. Skip the section entirely when the article is genuinely not Norway-specific.

**`## Sources`**  
Not a free-form section. The `authoritative_sources` frontmatter is the canonical citation. The `## Sources` section in the body renders those sources in human-readable form, one per line:

```markdown
## Sources

1. NORSOK D-010 Rev 5 (2021). Standards Norway. Clause 6.2. Paywalled. Verified 2026-04-18.
2. IWCF Level 2 syllabus (2023). IWCF. Section 3.4. Restricted. Verified 2026-04-18.
```

### Optional sections

**`## Related concepts`** — short pointer list to `related` articles when explicit in-text cross-references help the reader.

**`## Historical incidents`** — when the article is usefully illustrated by case studies. Link to incident articles via `related_incidents`.

**`## Equipment and tools`** — when a concept or procedure article naturally references specific equipment covered elsewhere in the tree.

---

## Pedagogical accessibility with technical depth

This is the foundation rule. Every article is written for a reader who needs to become technically competent but is a beginner in the field. The article must be deeply technical AND easy to understand. Both together. Dense jargon that assumes prior domain knowledge fails the rule. Shallow summary that avoids the technical substance also fails the rule. Never assume prior knowledge. Always be pedagogical.

The foundation of this rule is repetition. Human memory decays. A reader who sees a term defined once, on page one, will not remember the definition on page three. The article keeps the definitions in front of the reader at all times, so the reader learns through repeated exposure rather than through effort. This is binding, not a style preference. Agents may sacrifice prose elegance, brevity, and flow to honour it. They must not sacrifice depth.

### Concrete rules

1. **Every acronym is expanded at every single use**, not only at first use. Example: write `BOP (Blowout Preventer)` every time the acronym appears, in every paragraph, in every section. If an article uses BOP thirty times, the expansion appears thirty times. No exceptions. If the acronym appears in three consecutive sentences, it is expanded three times.

2. **Every specialist term is redefined in plain language at every single use.** A single-clause gloss in parentheses is sufficient. Example: `the driller (the worker who operates the drilling controls)` every time the term appears. If the term appears in fifteen places, the gloss appears in fifteen places. Specialist terms are domain-specific words that a reader with no prior exposure to the field would not recognise on their own.

3. **Every Norwegian term is translated at every single use.** Example: `the kranfører (crane operator)` every time, not only first appearance. The `norwegian_terms` frontmatter field lists the pairs for the validator. The body carries the translation inline at every use.

4. **Mechanisms are explained, not just named.** "A BOP closes on the pipe" is weak. The right explanation describes how the rams move, how the rubber seats, what is sealed off, and why it matters.

5. **Why a thing exists and what problem it solves comes before how it is used.**

6. **Examples are NCS-concrete when possible.** Specific fields (Troll, Johan Sverdrup, Ekofisk), specific operators (Equinor, Aker BP, Vår Energi), specific equipment models and standards.

7. **Analogies are allowed when they genuinely help the reader learn.** Never forced.

8. **Paragraphs that would stack three or more undefined technical terms in a row must be broken up or rewritten.**

### Cost of this rule

Prose runs longer under these rules. That cost is accepted. Depth floors (800 words foundational, 1500 operational, 3000 advanced) absorb the overhead. Articles routinely exceed the floor. That is expected.

### Enforcement

Validator rules W-CON-03 (acronyms) and W-CON-06 (Norwegian terms) enforce the mechanical portion on every occurrence. Specialist-term repetition is enforced by the review agent, which flags articles using specialist terms bare.

The review agent additionally flags articles that are dense-and-incomprehensible or simple-but-shallow. Human review promotes to `review` or `published` only after both bars (depth AND accessibility) are met.

---

## Writing style

### Voice

- 
- Direct and factual, teaching tone, make complex things easy to understand. No marketing language. No hype.
- Present tense for descriptions of how things work or are done.
- Past tense only for historical incidents and deprecated practice.
- Active voice preferred. Passive where the actor is genuinely unclear or irrelevant ("the BOP was activated" is fine; "the driller activated the BOP" is better when the actor matters).

### Terminology

- **Acronym expansion at every single use.** See the Pedagogical accessibility section for the full rule. Every acronym, every occurrence, every article. Examples: `BOP (Blowout Preventer)`, `ROP (Rate of Penetration)`, `NCS (Norwegian Continental Shelf)`. If the acronym appears thirty times in the article, the expansion appears thirty times. No exception for recent repetition in the same paragraph.
- **Norwegian term pairing at every single use.** See the Pedagogical accessibility section. Every Norwegian working term is paired with the English gloss at every occurrence, not only first use. Example: `the løfteleder (lift supervisor)`.
- **Specialist term gloss at every single use.** See the Pedagogical accessibility section. A brief plain-language gloss in parentheses at every occurrence of a specialist domain term. Example: `the driller (the worker who operates the drilling controls)`.
- **Units.** SI where the NCS convention is SI. Imperial where the NCS convention is imperial (oilfield tradition retains some imperial units: wellbore diameters in inches, pump pressure sometimes in psi). Always state the unit. Never mix without noting conversion.

### Formatting rules

- **No em dashes.** Use commas, periods, or restructure. This matches the vault owner's explicit preference and makes agent output consistent.
- **Use tables for comparative data.** Rows beat long comma-separated prose.
- **Use numbered lists for sequential procedures.** Bullets for non-sequential enumeration.
- **Code blocks** for equations, example calculations, or structured data.
- **Bold for safety-critical items** inside otherwise-running prose. Do not overuse.

### What to avoid

- Filler phrases ("it is important to note", "it should be emphasized that", "in the context of"). Just say the thing.
- Redundant hedging ("generally", "often", "typically") unless genuinely uncertain.
- Generic intros ("This article discusses..."). Start with the actual content.

---

## Citation rules

### Every substantive claim needs a source

A substantive claim is a statement of fact the reader would want to verify. Examples:

- "The NCS uses a two-barrier philosophy codified in NORSOK D-010." → source: NORSOK D-010.
- "G5 competence implicitly covers G4 and G20." → source: Samarbeidsrådet Petroleum training matrix P-4.1.
- "The Turøy accident on 29 April 2016 killed 13 people." → source: AIBN report or equivalent.

Not every sentence. Not definitions or principles that are universally known. A rough target density is expressed in `_CONTROLLED_VOCABULARY.md` under the `depth` table.

### How to cite in-text

Parenthetical reference to the source ID from `authoritative_sources`:

```markdown
The NCS requires two independent well barriers during well construction (NORSOK D-010, Clause 6.2).
```

The validator cross-checks that every `(<source-id>, ...)` in-text reference resolves to an entry in `authoritative_sources`.

### Never

- **Never fabricate a source.** If you cannot cite, omit the claim or flag it as `status: draft` with a `TODO` comment.
- **Never paraphrase a paywalled source** closely enough that the paraphrase substitutes for reading the source. Write your own analysis citing the source.
- **Never embed URLs in prose.** URLs go in the frontmatter `authoritative_sources[].url` field.
- **Never reproduce standards text verbatim.** NORSOK, API, ISO, and DNV standards are copyrighted. Summarize and cite.

---

## Authority whitelists

Each tree's `CLAUDE.md` contains the authoritative source whitelist for that tree. An agent checks that every source it cites is on the whitelist. If the source is not on the whitelist, the agent:

1. Writes the article anyway with the source cited.
2. Flags the source in a `TODO` comment at the bottom of the article.
3. Leaves the article at `status: draft` for human review.

New sources enter the whitelist only via human approval.

---

## Frontmatter population rules

When filling a leaf stub, the agent sets:

- `title` — final human-readable title if the derived one is awkward. Leave as-is if the derived one is fine.
- `title_no` — Norwegian equivalent if applicable, else null.
- `type` — REQUIRED, per `_CONTROLLED_VOCABULARY.md`.
- `depth` — REQUIRED, chosen based on article scope. Drives word count expectations.
- `topics` — draw from the tree's `_TOPICS.md`. If a topic needs to be added, write the article and add the new topic to a `_PROPOSALS.md` at the tree root.
- `life_cycle_phases` — enum list, may be empty.
- `perspective` — free-form list of syllabi or audiences served.
- `authoritative_sources` — at least one. Required before publication.
- `reference_textbooks` — optional.
- `related` — pointers to sibling articles in same tree. Populate as you write; the sibling-sync pass catches anything missed.
- `cross_domain` — pointers to articles in other trees. Write the best-guess path per `_PATH_CONVENTIONS.md`. Validator resolves.
- `relevant_to_roles` — which roles on the NCS care about this article.
- `ncs_specific` — boolean.
- `norwegian_terms` — list of `{no, en}` pairs mentioned in the article.
- `authors` — append your agent ID.
- `updated` — today's date.
- `review_due` — date 12 / 18 / 24 months out based on depth.
- `tags` — free-form.

Do not manually set:
- `slug` (already set at generation; do not rename files)
- `id` (already set)
- `folder` (already set)
- `domain` (already set)
- `citation_density` and `word_count` (validator computes)
- `created` (set at generation, never change)

---

## Hard don'ts

The following are categorical rule violations and cause validator rejection regardless of content quality.

1. **Do not invent frontmatter fields.** Use only those in `_SCHEMA.md`.
2. **Do not duplicate content from another tree.** If the canonical home is elsewhere, write a short pointer article and `cross_domain` link to it, or skip the article entirely.
3. **Do not write articles shorter than the `depth` minimum.** If you cannot meet the word count, the article is either wrongly depth-tiered or not ready to write.
4. **Do not mark `status: published`.** Only the validator promotes.
5. **Do not exceed schema enum values.** If you need a new value, propose it; do not write articles using unapproved values.
6. **Do not read or edit other trees.** Your agent session is scoped to one tree.
7. **Do not include em dashes.** Use commas, periods, or restructure.
8. **Do not fabricate sources.** Cite real sources or flag the article as incomplete.
9. **Do not reproduce copyrighted standards text.** Summarize and cite.
10. **Do not skip the NCS-specific context section** when `ncs_specific: true`. If there is genuinely no NCS angle, the article probably does not belong in this vault.
11. **Never use an acronym bare.** Expand it every single time, not only first use. This is the mechanical implementation of the Pedagogical accessibility rule. Validator rule W-CON-03 flags every bare occurrence.
12. **Never use a Norwegian term without inline English translation at every use.** Not only first use. Validator rule W-CON-06 flags every bare occurrence.
13. **Never use a specialist domain term without a plain-language gloss at every use.** Not only first use. Assume the reader does not remember the earlier definition. The review agent flags bare specialist terms.
14. **Never shortcut the pedagogy rule for the sake of prose elegance.** The rule is binding. Clunky prose is accepted. Longer article length is accepted.

---

## TODO comments

When an agent cannot complete something, it leaves an HTML comment at the end of the article body, above the `## Sources` section:

```markdown
<!-- TODO:
- Verify NORSOK D-010 Clause 6.2 wording; agent did not have standard accessible at drafting time.
- Expand Norwegian terminology table with løfteleder role description.
- Add cross_domain link to subsea tree once target article exists.
-->
```

These are machine-parseable. The validator emits a `_TODO_QUEUE.md` listing all TODOs across the vault.

---

## Agent identity

Every agent declares itself in the `authors` list with the format `"agent:<identifier>-v<version>"`. Examples:

- `agent:drilling-filler-v1`
- `agent:crane-validator-v2`
- `agent:cross-link-repair-v1`

This identifies what wrote or touched each article. Multiple agents may touch the same article; each appends to the list.
