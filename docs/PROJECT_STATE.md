# Zenith Inventory — Project State

## Current branch

`product/streamlined-modular-core`

## Product direction

**Simple barcode-first inventory for small industrial teams that have outgrown spreadsheets but do not want a full ERP rollout.**

The Environmental Pneumatics application is the proven starting point, not the final product architecture.

## Completed in this productization pass

- Removed active committed PostgreSQL credentials from current `master` configuration and moved legacy PostgreSQL settings to environment variables.
- Created the productization branch from the secured baseline.
- Defined the streamlined product/core architecture.
- Documented the legacy/bloat audit and refactor order.
- Added an integration contract.
- Added an integration registry.
- Wrapped the existing ProNest export behind the first integration adapter without changing the existing implementation yet.

## Current architecture status

The new integration seam exists, but the old UI still imports ProNest directly from `services/export_service.py` and the actual ProNest transformation logic still lives there.

This is intentional incremental refactoring: establish the seam first, then migrate behavior behind it while preserving the working legacy path.

## Exact next implementation task

### Milestone 0A — Make ProNest truly modular

1. Move ProNest-only constants and transformation helpers from `services/export_service.py` to `integrations/pronest.py`.
2. Keep generic CSV/XLSX inventory export in `services/export_service.py`.
3. Replace EP-specific export defaults with adapter configuration or neutral defaults.
4. Change the UI export action to resolve the ProNest adapter through `integrations.get_export_integration("pronest")` rather than importing ProNest logic directly.
5. Verify output compatibility against the current ProNest export behavior before deleting the legacy path.

## Task after ProNest extraction

### Milestone 0B — Repository/data seam

Create a storage interface that inventory services can call without knowing whether the underlying database is PostgreSQL or SQLite.

Do **not** begin by rewriting every query. Start with the smallest vertical slice needed for:

- initialize/open data store
- create item
- fetch item by barcode
- list items
- adjust quantity

Then implement that slice using SQLite and validate the basic barcode workflow.

## Near-term acceptance target

A clean Windows user should eventually be able to:

`download/install -> launch -> add/import item -> scan/search -> receive/consume -> close/reopen -> backup`

without installing Python or PostgreSQL.

## Guardrails

- no full ERP/MRP scope
- no cloud/multi-user work before local trial evidence
- no customer-specific machine/ERP logic in the core
- no new integration unless a real workflow justifies it
- no deletion of legacy behavior until equivalent core behavior is verified
- no adding features while installation and primary inventory flow remain painful
