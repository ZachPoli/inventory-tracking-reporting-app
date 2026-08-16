# AGENTS.md — Zenith Inventory

These instructions govern AI-assisted work in this repository.

## Start every coding session here

Before editing code:

1. Read `docs/PROJECT_STATE.md` completely.
2. Read `docs/PRODUCT_MILESTONES.md` for the active milestone and exit gate.
3. Read the active GitHub milestone issue referenced by `PROJECT_STATE.md`.
4. Inspect the code directly related to the next unchecked task.
5. Do not begin work from old chat assumptions when the repository state differs.

## Current product goal

Build **simple barcode-first inventory for small industrial teams that have outgrown spreadsheets but do not want a full ERP rollout**.

The legacy Environmental Pneumatics application is a reference implementation, not the architecture to continue expanding.

## Work one milestone at a time

`docs/PROJECT_STATE.md` identifies the only active milestone.

- Do not pull future-milestone features forward because they seem useful.
- Do not redesign completed systems without a demonstrated defect or active milestone requirement.
- Prefer the smallest change that advances the active exit gate.
- When the active milestone passes, update project state before beginning the next milestone.

## Architecture rules

### Core responsibilities

The product core may own:
- item/SKU/barcode identity
- quantity on hand
- unit
- location/bin/shelf
- receive/consume/adjust behavior
- movement history
- search/list/filter
- minimum-stock behavior
- generic import/export
- backup/recovery

### Integrations

Factory/customer-specific systems must normally live behind the integration boundary.

Examples:
- ProNest
- laser/CNC software
- ERP systems
- accounting systems
- supplier systems
- APIs
- customer-specific file mappings

An integration may translate/import/export data and validate its own configuration. It must not become the owner of generic inventory quantity rules.

### Manufacturing fields

Thickness/gauge/dimensions/grade currently remain optional for legacy compatibility and manufacturing use cases.

- Do not put them on the primary M1 UI.
- Do not spend M1 removing them from storage.
- Revisit their long-term location before external beta based on actual product needs.

## Legacy code rule

Do not continue adding product responsibilities to `Inventory_Management_Fixed.py`.

Use the legacy application only to understand or deliberately port proven behavior.

Do not delete legacy behavior until the replacement path is verified.

## Storage rule

The new product path uses `InventoryRepository` abstractions and embedded SQLite.

Do not reintroduce PostgreSQL as an end-user requirement for the local product.

Future network/cloud storage is blocked until customer evidence justifies it.

## Testing

For every behavior change:

- add/update focused automated tests when practical
- run `python -m unittest discover -s tests -v`
- do not claim verification that was not actually run
- keep ProNest/integration regression tests separate from generic core tests
- treat data loss, quantity corruption, failed persistence, and backup failures as release blockers

CI lives under `.github/workflows/` and should remain green before a milestone is considered complete.

## Security

- never commit passwords, API keys, tokens, customer credentials, or private operational data
- use environment/local configuration where secrets are genuinely required
- demo/test data must be fictional or sanitized

## Dependencies

Keep dependencies minimal.

Before adding a dependency, determine whether the standard library or an existing dependency is sufficient. Document why a substantial new runtime dependency is needed.

## UI rule

The primary UI optimizes this loop:

`scan/search -> item -> receive/consume/adjust -> movement recorded -> next scan`

Secondary features must not dominate the main screen.

## Definition of a good AI-assisted change

A good change:
- advances the active milestone
- is small enough to review
- preserves verified behavior
- includes appropriate tests
- does not introduce speculative architecture
- leaves the repository in a clearer state

## End every implementation session

Report:

1. what changed
2. tests actually run and result
3. files changed
4. active milestone checklist items completed
5. remaining risks/known issues
6. exact next implementation task

Update `docs/PROJECT_STATE.md` if the exact next task changed.

Do not merge the product branch into `master` without explicit user approval.
