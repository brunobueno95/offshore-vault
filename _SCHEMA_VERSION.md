# _SCHEMA_VERSION.md

**Current version:** 1.0  
**Locked:** 2026-04-19  
**Next planned review:** when first 100 articles have been filled by agents

## Version history

### 1.0 (2026-04-19)

Initial locked schema. Defined in `_SCHEMA.md`.

Scope:
- Full leaf frontmatter contract (30 fields)
- Structured `authoritative_sources` and `reference_textbooks` objects
- Folder `_INDEX.md` simpler schema
- Publication requirements enforced mechanically

## Versioning policy

- **Patch** (1.0 → 1.0.1): clarifications, typo fixes, non-breaking documentation updates. No article changes required.
- **Minor** (1.0 → 1.1): new optional fields, new enum values. Existing articles remain valid. Agents may start using new features immediately.
- **Major** (1.0 → 2.0): required field removal, type change, enum removal, or semantic reinterpretation. All articles must be migrated. A migration script is required before a major bump is landed.

## How to bump

1. Draft the change in a branch.
2. Update `_SCHEMA.md` with new contract.
3. Update `_CONTROLLED_VOCABULARY.md` if enums changed.
4. Bump `_SCHEMA_VERSION.md` (this file).
5. For minor bumps: `_sync.sh` propagates to all per-tree `CLAUDE.md` files.
6. For major bumps: write migration script under `tools/migrate-vN-to-vN+1.py`, run against the full vault, verify, then commit.
7. Update `.github/workflows/validate.yml` to assert the new version.

## Deprecation policy

Fields marked deprecated in a minor version are removed only in the next major version. Minimum two-version lifetime for removal: minor that deprecates, major that removes.
