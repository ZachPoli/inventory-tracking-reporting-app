# Zenith Inventory — Project State

## Current branch

`product/streamlined-modular-core`

Draft PR: #2 — `Productize inventory app around a streamlined modular core`

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
- Moved ProNest-specific constants, mappings, material transformations, source-row selection, and dataframe creation out of the generic export service and into `integrations/pronest.py`.
- Replaced Environmental Pneumatics-specific ProNest defaults with configurable/neutral adapter defaults.
- Reduced `services/export_service.py` to generic spreadsheet export plus a temporary backward-compatible ProNest bridge for the legacy UI.
- Added a regression test for configurable ProNest transformation.

## Current architecture status

ProNest is now implemented as an integration adapter rather than general inventory export logic.

The old Tkinter UI still calls the compatibility function in `services/export_service.py`. That wrapper resolves the ProNest integration through the registry, so existing UI behavior can remain intact while we streamline the application incrementally.

The current production bottleneck is now **storage/deployment coupling**: inventory services still assume PostgreSQL and a separately configured database server.

## Exact next implementation task

### Milestone 0B — Repository/data seam

Create a storage interface that inventory/application services can call without knowing whether the underlying database is PostgreSQL or SQLite.

Do **not** begin by rewriting every query. Build the smallest vertical slice needed for the primary product workflow:

1. initialize/open data store
2. create item
3. fetch item by barcode
4. list/search items
5. adjust quantity
6. record the adjustment as an inventory movement

Then implement that slice using SQLite while keeping the legacy PostgreSQL path available until equivalence is proven.

### Required model direction for the slice

Generic core fields:

- id
- sku/barcode
- name/description
- category/material
- quantity
- unit
- location/bin/shelf
- minimum stock
- supplier (optional)
- notes (optional)
- last updated

Optional manufacturing extension fields:

- thickness/gauge
- dimensions
- grade/material details

Movement record fields:

- id
- item id
- timestamp
- movement type (`receive`, `consume`, `adjust`)
- quantity delta
- resulting quantity
- note/source (optional)

## Task after the SQLite vertical slice

### Milestone 0C — Primary UI simplification

Replace the current all-in-one add/edit workflow with the product's primary loop:

`scan/search -> item -> receive / consume / adjust -> movement recorded -> ready for next scan`

Secondary actions such as import/export, labels, backup, reporting, and integrations should remain available without dominating the primary screen.

## Near-term acceptance target

A clean Windows user should eventually be able to:

`download/install -> launch -> add/import item -> scan/search -> receive/consume -> close/reopen -> backup`

without installing Python or PostgreSQL.

## Integration rule

External factory software is expected to vary.

- ProNest is adapter #1.
- A laser/CNC system, ERP, accounting package, supplier system, or customer-specific CSV mapping should become another adapter when a real workflow justifies it.
- Integrations may translate/import/export data, validate system-specific fields, and expose configuration.
- Integrations should not own core inventory quantity rules or force their fields throughout the core UI/data model.

## Guardrails

- no full ERP/MRP scope
- no cloud/multi-user work before local trial evidence
- no customer-specific machine/ERP logic in the core
- no new integration unless a real workflow justifies it
- no deletion of legacy behavior until equivalent core behavior is verified
- no adding features while installation and primary inventory flow remain painful
