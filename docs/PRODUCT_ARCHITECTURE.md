# Zenith Inventory — Product Architecture

## Product Goal

Build a **small, dependable, barcode-first inventory application for industrial teams** that can be installed and used without developer setup.

The original Environmental Pneumatics application proved the workflow and contains valuable manufacturing features. Productization should preserve that value while removing company-specific assumptions, deployment friction, and accumulated UI/service coupling.

## Architectural North Star

```text
+--------------------------------------------------+
|                   Desktop UI                     |
|  Inventory | Barcode | Activity | Low Stock     |
+------------------------+-------------------------+
                         |
                         v
+--------------------------------------------------+
|                Application Services              |
| Inventory | Movements | Barcode | Import/Export |
| Backup/Restore | Search | Reporting              |
+------------------------+-------------------------+
                         |
              +----------+----------+
              |                     |
              v                     v
+-------------------------+   +----------------------+
|      Data Repository    |   | Integration Boundary |
| SQLite first            |   | ProNest              |
| future network/cloud    |   | ERP / CSV mappings   |
+-------------------------+   | Laser/CNC systems    |
                              | Supplier/API adapters |
                              +----------------------+
```

## Core Rule

**The core application owns inventory behavior. Integrations translate between Zenith Inventory and external systems.**

A customer's factory software should not force changes throughout the inventory data model, UI, and business logic.

If a requirement exists because a specific external system needs a particular file format, field mapping, protocol, or workflow, it should normally live in an adapter.

## Core Responsibilities

The first sellable core should own only broadly useful inventory behavior:

- item/SKU/barcode identity
- item description/name
- category/material
- quantity on hand
- unit of measure
- location/bin/shelf
- minimum stock/reorder threshold
- supplier (optional)
- notes (optional)
- optional industrial attributes such as thickness/gauge and dimensions
- receive inventory
- consume inventory
- adjust inventory
- inventory movement/history log
- barcode lookup
- search/filter/sort
- low-stock view
- CSV/XLSX import/export
- label generation/printing
- backup/restore
- basic dashboard/reporting

## Integration Responsibilities

Integrations can:

- transform core inventory records into an external system's format
- import/match data from an external system
- expose integration-specific configuration
- validate required external fields
- provide a human-readable name and description

Integrations should **not**:

- directly own core inventory quantity rules
- silently mutate core data outside application services
- require unrelated core UI changes
- hard-code one customer's company name into shared product behavior

## Initial Integration: ProNest

The existing ProNest export is valuable but currently lives in the general export service and contains EP-specific assumptions.

Migration path:

1. Add a stable integration interface without changing current behavior.
2. Register a ProNest adapter around the existing implementation.
3. Move ProNest transformation logic out of `services/export_service.py` into the adapter.
4. Replace EP-specific defaults with adapter configuration.
5. Make the UI discover integrations through the registry rather than importing ProNest directly.
6. Keep ordinary CSV/XLSX export in the core.

This makes ProNest the **first example integration**, not part of the inventory domain itself.

## Data Layer Direction

### First commercial release

Use an embedded local database so a single-user Windows customer does not need to install or administer PostgreSQL.

SQLite is the first implementation target because it supports a local application database with no separate database server.

### Future

Do not build network/cloud complexity until users prove the need. The repository/service boundary should eventually allow alternate backends such as:

- shared PostgreSQL
- hosted database/API
- multi-location service

without rewriting the inventory workflow.

## UI Direction

The current Tkinter application contains too many responsibilities in one file. Productization should move toward thin UI code that calls application services.

The main user workflow should be obvious:

1. Scan/search an item.
2. View current quantity/location.
3. Receive, consume, or adjust.
4. See the movement recorded.
5. Continue scanning.

Secondary actions such as backup, import, reporting, labels, and integrations should not crowd the primary workflow.

## Streamlining Rules

Before preserving or adding a feature, classify it as one of:

### Core
Nearly every target industrial inventory user needs it.

### Optional module/integration
Useful for a specific industry, machine, ERP, file format, or customer.

### Legacy/remove
Exists because of an old implementation detail, abandoned workflow, duplicated function, migration utility, or developer-only need.

No feature stays merely because it already exists.

## Compatibility Strategy

Do not rewrite everything at once.

Use incremental seams:

- keep the existing app runnable while extracting modules
- add adapters around existing functionality before moving it
- add smoke tests before removing legacy behavior
- preserve the original manufacturing use case as a test/template
- move to the embedded data layer behind a repository boundary

## First Product Milestone

A stranger on Windows should be able to:

1. download/install Zenith Inventory
2. launch it without Python/PostgreSQL
3. start with an empty database or optional demo data
4. import a spreadsheet or add an item
5. scan/search a barcode
6. receive/consume inventory
7. close and reopen without losing data
8. create a backup

in under five minutes of setup.

## Commercial Architecture Principle

Modularity is not only an engineering preference; it is part of the business model.

The stable core can be licensed broadly. Customer-specific or system-specific adapters can be:

- sold as reusable integration modules
- configured during paid onboarding
- built as bounded paid customization
- promoted into standard integrations when demand repeats

That creates a path from one-off customer needs to reusable Zenith-owned IP.
