# _PATH_CONVENTIONS.md — master naming and path rules

**Version:** 1.0  
**Scope:** every folder, every file, every path reference in `offshore-vault/`

These rules make paths predictable across trees. An agent working in one tree can construct a correct cross-tree link to another tree without reading that other tree, because both trees follow the same rules.

---

## Character rules

### Always

- **Kebab-case.** Lowercase, ASCII, words joined by single hyphens.
- **ASCII only.** No Norwegian characters (æøå) in paths. Norwegian terms are represented by their closest ASCII spelling: `løfteleder` → `lofteleder`, `bronnramme` → `bronnramme`, `kranfører` → `kranforer`.
- **File extension `.md`** for articles and index files. No other extensions.
- **Numeric prefixes with hyphen.** `01-earth-structure/`, never `01_earth_structure/` or `01.earth-structure/`.

### Never

- **No spaces.** Ever.
- **No underscores** in paths. Underscores only permitted inside YAML frontmatter values as part of compound Norwegian terms.
- **No parentheses** in paths. Preserve them in the folder's `_INDEX.md` title field instead.
- **No special punctuation.** No `()`, `[]`, `{}`, `&`, `§`, `%`, `#`, `'`, `"`, `!`, `?`, `,`, `;`, `:`, `/`, `\`.
- **No leading digits in slugs that are not numeric prefixes.** `6dof` becomes `six-dof`. `500m-safety-zone` becomes `five-hundred-meter-safety-zone`.
- **No embedded URLs or markdown links** in filenames. Source citations go in `authoritative_sources`, not in the filename.

---

## Folder naming

### Singular vs plural

- **Singular for categories:** `equipment/`, `procedure/`, `role/`, `standard/` when the folder names a class.
- **Plural for instance collections:** `equipments/`, `procedures/`, `standards/` only when the folder explicitly groups instances (rare).

Current convention across existing trees: plural is used because the folders group instances. Follow the existing tree convention when extending.

### Numeric prefix rule

Top-level chapter folders and direct chapter sub-folders use a zero-padded two-digit prefix followed by a hyphen:

```
01-geology-and-reservoir/
  01-earth-structure/
  02-rock-types/
    sedimentary/                  <- no prefix, nested classification
  03-petroleum-system/
```

Prefixes exist for stable ordering. Nested sub-folders below the section level may drop prefixes when the ordering is semantic (e.g. a classification tree) rather than sequential.

### Descriptor preservation

Parentheticals and long descriptors are stripped from paths but preserved in the folder's `_INDEX.md` `title` field. Example:

- Source tree name: `01_G5_Offshorekran_Fundamentals_(Offshore_Pedestal_Crane)/`
- Path: `01-g5-offshorekran-fundamentals/`
- `_INDEX.md` title: `"G5 Offshorekran Fundamentals (Offshore Pedestal Crane)"`

This keeps paths short and predictable while preserving the full human-readable name.

---

## File naming

### Leaf articles

Each leaf article is a `.md` file named with its slug:

- `hydrostatic-pressure.md`
- `blowout-preventer.md`
- `piper-alpha-1988.md`
- `norsok-d-010.md`

### Naming patterns by article type

- **Equipment:** canonical English name, not manufacturer in filename. Manufacturer lives in folder path and frontmatter. Wrong: `nov-kongsberg-offshore-crane.md`. Right: `offshore-pedestal-crane.md`.
- **Specific product lines:** product identifier only, descriptor in `_INDEX.md` title. Wrong: `schilling-uhd-iii-ultra-heavy-duty.md`. Right: `schilling-uhd-iii.md`.
- **Standards:** identifier plus descriptor. `norsok-d-010.md`, `api-17d-subsea-equipment.md`, `iso-4309-wire-rope-discard.md`.
- **Incidents:** location plus year. `piper-alpha-1988.md`, `macondo-2010.md`, `turoy-2016.md`, `bravo-blowout-ekofisk-1977.md`.
- **Roles:** NCS working term, Norwegian where that is the working term. `roustabout.md`, `toolpusher.md`, `kranforer.md`, `lofteleder.md`.
- **Procedures:** procedure name. `hard-shut-in.md`, `driller-method-two-circulation.md`.
- **Concepts:** concept name. `hydrostatic-pressure.md`, `equivalent-circulating-density-ecd.md`.

### Acronym handling

When an article's name is an acronym or contains one, include both the acronym and the full-name slug component for discoverability:

- `rop-rate-of-penetration.md` — not just `rop.md`.
- `ecd-equivalent-circulating-density.md` — not just `ecd.md`.
- `loto-lockout-tagout.md` — not just `loto.md`.

Exception: when the acronym is the unambiguous canonical name of the thing (standards, for instance), the acronym alone is fine: `norsok-d-010.md`, not `norsok-drilling-010.md`.

---

## Standard folder shapes per tree

When creating new folders within a tree, prefer these shapes where applicable. This is a soft convention to aid cross-tree predictability.

| Folder | Purpose |
|---|---|
| `concepts/` | Theory, physics, principles |
| `equipment/` | Tools, machines, hardware |
| `procedures/` | Step-by-step operations |
| `standards/` | Regulations, specs, codes |
| `roles/` | Job functions |
| `incidents/` | Case studies |
| `life-cycle-phases/` | Life-cycle-specific articles |
| `norwegian-terminology/` | NCS term glossary |
| `tools-and-software/` | Rare: software, calculators |

Existing chapter-numbered top-level folders take precedence over these category folders; the shapes above apply at deeper nesting.

---

## Cross-tree link construction

An agent in one tree writes a `cross_domain` link to another tree without reading that tree. The path is constructed as:

```
<target-tree>/<chapter-folder>/<section-folder>/<slug>.md
```

Rules:

1. **Start with the target tree name.** One of: `drilling/`, `crane-and-logistics/`, `subsea/`, `emergency-response/`.
2. **Choose the most likely chapter.** Use the tree's chapter map (see each tree's `_INDEX.md` for quick reference).
3. **Use the canonical slug for the concept.** Follow the acronym, equipment, standard, incident, or role conventions above.
4. **If uncertain about a sub-folder, omit it.** A path like `drilling/07-well-control/kill-methods/drillers-method-two-circulation.md` is preferred. If you are not sure whether "kill-methods" is numbered `07` within well-control, write the simpler `drilling/07-well-control/drillers-method-two-circulation.md`. The validator will either resolve it, suggest the correct path, or flag for creation.

### Validator behaviour on cross-tree links

The post-run validator:
1. Walks every `cross_domain` entry in every article.
2. Attempts to resolve the path literally.
3. If literal resolution fails, attempts fuzzy matching on the slug within the target tree.
4. Writes results to `_UNRESOLVED_LINKS.md` at the vault root with:
   - Resolved links (informational only)
   - Broken links with closest match if found (agent or human triages)
   - Ambiguous links (multiple matches, human chooses)

Agents never block on unresolved links. The vault tolerates them during construction.

---

## Tree root names (locked)

Trees live under `offshore-vault/`:

- `drilling/`
- `crane-and-logistics/`
- `subsea/`
- `emergency-response/`

These names are the canonical `domain` values and the first segment of all cross-tree paths.

---

## Reserved filenames at every folder level

- `_INDEX.md` — mandatory folder index, one per folder.

At tree roots only:

- `CLAUDE.md` — tree-scoped agent rules (self-contained)
- `_TOPICS.md` — tree-specific topic vocabulary
- `_VERIFICATION_FINDINGS.md` — research notes from tree scoping
- `_VIEWS/` — cross-cutting thematic indexes

At vault root only:

- `CLAUDE.md`, `_SCHEMA.md`, `_CONTROLLED_VOCABULARY.md`, `_PATH_CONVENTIONS.md`, `_AGENT_RULES.md`, `_VALIDATION.md`, `_SCHEMA_VERSION.md`, `_UNRESOLVED_LINKS.md`, `_MANIFEST.txt`.

No other leading-underscore files at any level. The underscore prefix signals "infrastructure, not content".

---

## Normalization cheat sheet (for agents ingesting source trees)

| Input pattern | Normalized |
|---|---|
| `snake_case_name` | `snake-case-name` |
| `PascalCaseName` | `pascal-case-name` (split on case boundaries, then lowercase) |
| `NN_prefix_name` | `nn-prefix-name` (prefix preserved) |
| `name_(parenthetical)` | `name` (parenthetical moved to `_INDEX.md` title) |
| `name_[cite](https://...)` | `name` (citation moved to `authoritative_sources`) |
| `name_with_§_or_%` | `name-with-section-or-percent` (symbols replaced with words) |
| `6DOF_concept` | `six-dof-concept` (digits-first replaced with spelled form) |
| `500m_zone` | `five-hundred-meter-zone` |
| `name with spaces` | `name-with-spaces` |
| `kranfører` | `kranforer` (ASCII only) |
| `Brønnteknikk` | `bronnteknikk` |
