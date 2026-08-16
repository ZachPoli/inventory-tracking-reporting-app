# Zenith Inventory — Project State

## Current branch

`product/streamlined-modular-core`

Draft PR: #2 — `Productize inventory app around a streamlined modular core`

Master roadmap: `docs/PRODUCT_MILESTONES.md`

## Active milestone

**M1 — Run Zenith Inventory on Zach's Windows PC** — GitHub Issue #3.

This is the only active product milestone. Issues #4–#10 are blocked roadmap stages and should not pull work away from M1 unless a security/data-integrity problem requires attention.

## Product direction

**Simple barcode-first inventory for small industrial teams that have outgrown spreadsheets but do not want a full ERP rollout.**

The Environmental Pneumatics application is the proven starting point, not the final product architecture.

## Completed in this productization pass

### Security / baseline

- Removed active committed PostgreSQL credentials from current `master` configuration and moved legacy PostgreSQL settings to environment variables.
- Created the productization branch from the secured baseline.
- Defined the streamlined product/core architecture.
- Documented the legacy/bloat audit and refactor order.

### Modular integrations

- Added an integration contract and registry.
- Moved ProNest-specific constants, mappings, material transformations, source-row selection, and dataframe creation out of the generic export service and into `integrations/pronest.py`.
- Replaced Environmental Pneumatics-specific ProNest defaults with configurable/neutral adapter defaults.
- Reduced `services/export_service.py` to generic spreadsheet export plus a temporary backward-compatible ProNest bridge for the legacy UI.
- Added a regression test for configurable ProNest transformation.

### Streamlined data core

- Added generic `InventoryItem` and `InventoryMovement` domain models.
- Added an `InventoryRepository` boundary so product code does not have to know which database is underneath it.
- Added a zero-config embedded `SQLiteInventoryRepository`.
- Added automatic first-run table/index creation.
- Added generic item creation, barcode lookup, item search/listing, and quantity adjustment.
- Added inventory movement/history recording for `receive`, `consume`, and `adjust` actions.
- Added protection against negative resulting quantity.
- Added platform-appropriate default application-data/database paths.
- Added repository tests covering create -> lookup/search -> consume -> movement history and negative-quantity protection.

### Automation

- Added `.github/workflows/product-core-ci.yml` to run product regression tests on Windows and Ubuntu for pushes/PRs.
- First workflow execution still needs to be observed/confirmed in GitHub Actions; do not mark CI complete until a real run passes.

## Current architecture status

There are now two paths in the repository.

### Legacy/reference path

The original Environmental Pneumatics Tkinter/PostgreSQL application remains intact as a reference for proven barcode tooling, manufacturing fields, import/export, backup/restore, and the original shop-floor workflow.

### New product path

The new domain/storage/integration modules are independent of the old UI and PostgreSQL implementation. They are the foundation for the streamlined Zenith Inventory product.

Do not spend months cleaning every historical concern out of the large legacy UI. Port only behavior that earns a place in the product roadmap.

## Exact next implementation task

### Issue #3 / M1 — Build the thin barcode-first product UI

Create a new product entry point on top of `SQLiteInventoryRepository` rather than adding responsibilities to `Inventory_Management_Fixed.py`.

First workflow:

1. application opens local SQLite data store automatically
2. scan/type barcode or SKU
3. item is shown immediately if found
4. user can `Receive`, `Consume`, or `Adjust`
5. movement is recorded automatically
6. cursor returns to scan/search for the next item
7. user can open a simple inventory list/search view
8. user can add a new item when a scanned barcode is unknown

Primary UI fields:
- barcode/SKU
- item name
- category/material
- quantity
- unit
- location/bin/shelf
- minimum stock

Optional/hidden for now:
- thickness/gauge
- dimensions
- grade/material details
- supplier
- notes

### Manufacturing-field decision

Do **not** spend M1 removing thickness/gauge/dimensions from storage. They are optional and hidden from the main workflow. Revisit before external beta whether they belong in a manufacturing profile/extension instead of the generic item model.

### Not on the primary screen

- ProNest-specific controls
- barcode migration/rebuild utilities
- database wipe/developer maintenance tools
- raw database controls
- every possible report
- future ERP/machine integrations

## M1 exit gate

Zach must personally pass this flow on his Windows PC:

`clean clone -> launch new product -> add item -> find item -> receive -> consume -> close -> reopen -> data persists`

No PostgreSQL. No legacy EP application. No terminal interaction after the initial developer setup.

Do not start M2 until this passes.

## Integration rule

External factory software is expected to vary.

- ProNest is adapter #1.
- Laser/CNC systems, ERPs, accounting packages, supplier systems, APIs, and customer-specific CSV mappings become adapters when real workflows justify them.
- Integrations may translate/import/export data, validate system-specific fields, and expose configuration.
- Integrations must not own core inventory quantity rules or force system-specific fields throughout the main UI.

## Daily execution rule

1. Read this file.
2. Open the active milestone issue.
3. Work only the next unchecked task needed for the exit gate.
4. Run automated tests.
5. Commit a bounded change.
6. Update this file only when the exact next task changes.

A good work session is one that moves the active exit gate closer to passing. It does not require a large amount of code.

## Guardrails

- no full ERP/MRP scope
- no cloud/multi-user work before paid/trial evidence
- no customer-specific machine/ERP logic in the core
- no new integration unless a real workflow justifies it
- no deletion of legacy behavior until equivalent product behavior is verified
- no feature porting while installation and the primary inventory flow remain painful
