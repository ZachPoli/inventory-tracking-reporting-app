# Zenith Inventory — Project State

## Current branch

`product/streamlined-modular-core`

Draft PR: #2 — `Productize inventory app around a streamlined modular core`

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

The SQLite vertical slice was validated independently before being committed.

## Current architecture status

There are now two paths in the repository:

### Legacy/reference path

The original Environmental Pneumatics Tkinter/PostgreSQL application remains intact as a working reference for proven features such as barcode tooling, manufacturing fields, import/export, backup/restore, and the original shop-floor workflow.

### New product path

The new domain/storage/integration modules are intentionally independent of the old UI and PostgreSQL implementation. They are the foundation for the streamlined Zenith Inventory product.

This avoids spending months trying to clean every historical concern out of one large legacy UI file before we can test the new product experience.

## Exact next implementation task

### Milestone 0C — Build the new thin barcode-first UI

Create a new product entry point on top of `SQLiteInventoryRepository` rather than adding more responsibilities to `Inventory_Management_Fixed.py`.

First screen/workflow:

1. application opens local SQLite data store automatically
2. scan/type barcode or SKU
3. item is shown immediately if found
4. user can `Receive`, `Consume`, or `Adjust`
5. movement is recorded automatically
6. cursor returns to scan/search for the next item
7. user can open a simple inventory list/search view
8. user can add a new item when a scanned barcode is unknown

### First UI fields

Keep the initial form intentionally small:

- barcode/SKU
- item name
- category/material
- quantity
- unit
- location/bin/shelf
- minimum stock

Manufacturing detail can live behind an optional/details section:

- thickness/gauge
- dimensions
- grade/material details
- supplier
- notes

### Not on the primary screen

- ProNest-specific controls
- barcode migration/rebuild utilities
- database wipe/developer maintenance tools
- raw database controls
- every possible report
- future ERP/machine integrations

Those belong in secondary screens, optional modules, or developer tooling.

## Task after the thin UI

### Milestone 0D — Bring proven capabilities across deliberately

Once the new barcode loop is pleasant to use, migrate only the valuable existing features:

1. CSV/XLSX import with preview/validation
2. barcode/label printing
3. backup/restore for the SQLite database
4. low-stock view
5. activity/history view
6. generic spreadsheet export
7. Integrations screen with ProNest as adapter #1

Do not port legacy code merely because it exists.

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
- no deletion of legacy behavior until equivalent product behavior is verified
- no feature porting while installation and primary inventory flow remain painful
