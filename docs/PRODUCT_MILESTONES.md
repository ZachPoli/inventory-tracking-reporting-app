# Zenith Inventory — Product Milestones

This roadmap turns the Environmental Pneumatics inventory project into a product that a small industrial business can install, understand, trial, buy, and extend without Zenith rebuilding the entire application for every customer.

## Operating rule

Work **one milestone at a time**. Do not add a feature because it sounds useful. A milestone closes only when its exit gate is satisfied.

The product loop is:

`build -> run ourselves -> make installation easy -> pilot -> sell -> learn -> turn repeated needs into reusable modules`

## Product position

**Simple barcode-first inventory for small industrial teams that have outgrown spreadsheets but do not want a full ERP rollout.**

Core inventory stays generic. Customer/factory-specific behavior becomes an integration.

---

# Milestone 0 — Secure and separate the product core

**Status: substantially complete on `product/streamlined-modular-core`.**

Objectives:
- remove active committed secrets
- establish generic inventory and movement models
- add a storage/repository boundary
- add embedded SQLite storage
- isolate ProNest behind an integration boundary
- preserve the legacy EP application as a reference instead of continuing to expand it
- add automated regression tests

Exit gate:
- [x] core repository can create/search/adjust inventory without PostgreSQL
- [x] quantity changes create movement history
- [x] ProNest transformation lives behind an integration module
- [ ] CI automatically runs core tests on pushes and pull requests

---

# Milestone 1 — Run Zenith Inventory on Zach's PC

**Purpose:** the founder must be able to use the new product path before asking anyone else to try it.

Build:
- new product entry point separate from `Inventory_Management_Fixed.py`
- automatic SQLite database creation in the user's application-data folder
- thin barcode-first UI
- barcode/SKU search box with keyboard/scanner focus
- item result panel
- `Receive`, `Consume`, and `Adjust` actions
- automatic movement/history record
- fast `Add Item` path for unknown barcodes
- inventory list/search view
- simple local bootstrap/run instructions

Primary fields:
- barcode/SKU
- name
- category/material
- quantity
- unit
- location/bin/shelf
- minimum stock

Optional/hidden manufacturing details for now:
- thickness/gauge
- dimensions
- grade
- supplier
- notes

**Decision on legacy manufacturing fields:** do not delete them yet. They remain optional and hidden from the primary workflow. Before public beta, revisit whether they belong in a manufacturing profile/extension rather than the generic core model.

Exit gate:
- [ ] clean clone works on Zach's Windows PC
- [ ] app launches without PostgreSQL
- [ ] create an item
- [ ] close/reopen and item persists
- [ ] search/scan item
- [ ] receive inventory
- [ ] consume inventory
- [ ] movement history is correct
- [ ] user can complete the loop without touching a terminal after initial developer setup

**Do not start Milestone 2 until Zach personally passes this flow.**

---

# Milestone 2 — Make the core useful for a real stockroom

**Purpose:** cover the small set of capabilities nearly every first customer needs.

Build in this order:
1. CSV/XLSX import with validation and preview
2. generic CSV/XLSX export
3. backup/restore for the local data store
4. low-stock view using minimum-stock thresholds
5. inventory activity/history view
6. barcode/label generation and printing
7. basic dashboard: item count, low-stock count, recent movements, locations/categories
8. Integrations screen showing installed/available adapters; ProNest is adapter #1

Streamlining rule:
- do not port a legacy feature merely because it exists
- no database wipe/admin controls on the normal user surface
- no ProNest controls on the main inventory screen
- no full ERP/MRP, purchasing, accounting, or production scheduling

Exit gate:
- [ ] representative inventory can be imported from a spreadsheet
- [ ] user can run one normal workday's inventory actions
- [ ] user can back up and restore data
- [ ] low-stock state is obvious
- [ ] labels can be produced for representative items
- [ ] integration features do not clutter the primary workflow

---

# Milestone 3 — Make installation boring

**Purpose:** remove Zach from the installation process.

Automate:
- Windows build in CI/release workflow
- version number included in build
- packaged executable/installer
- first-run database setup
- fictional demo-data option
- release artifact generated from a tagged release
- automated core tests before a release artifact is produced

Product assets:
- neutral Zenith Inventory branding
- app icon
- one-page quick-start
- basic backup/recovery explanation
- changelog/versioning

Exit gate:
- [ ] install on a clean Windows machine/VM without Python or PostgreSQL
- [ ] launch -> add/import inventory in under five minutes
- [ ] uninstall/reinstall does not silently destroy user data
- [ ] release process is documented and mostly automated

---

# Milestone 4 — Dogfood and trial hardening

**Purpose:** find obvious problems before exposing the product to a business.

Use the program ourselves with fictional and representative industrial inventory.

Test:
- 100+ items
- barcode keyboard-wedge scanner behavior
- repeated receive/consume actions
- bad spreadsheet imports
- duplicate barcodes
- missing fields
- backup -> restore
- application restart
- low-stock logic
- label output
- ProNest adapter with representative data

Create:
- demo inventory dataset
- 2–3 minute product demo
- feedback/bug-report route
- short known-limitations list

Exit gate:
- [ ] no known data-loss bug
- [ ] no blocker in the primary scan/search -> quantity workflow
- [ ] clean install tested by someone other than the development environment
- [ ] demo can be shown without explaining source code

---

# Milestone 5 — External pilot

**Purpose:** prove that someone outside Zenith can install and use it.

Target only 3–5 qualified pilot users/businesses initially.

Ideal first pilot:
- small manufacturer, fabricator, machine shop, warehouse, distributor, or industrial stockroom
- still uses spreadsheets/manual tracking for at least part of inventory
- decision-maker or operations user is reachable
- no expectation that Zenith replaces the company's entire ERP

Pilot process:
1. give them the installer and quick-start
2. do **not** immediately take over their computer
3. observe where installation/onboarding fails
4. have them import or enter representative inventory
5. have them complete receive/consume/lookup tasks
6. ask what existing software/file/machine the inventory needs to exchange data with
7. record requested changes
8. classify each request as core, integration, customer-specific, or out-of-scope

Pilot success gate:
- [ ] at least 3 outside users/businesses attempt installation
- [ ] at least 2 complete a real inventory workflow
- [ ] at least 1 wants to continue using it or requests a concrete integration/customization
- [ ] repeated requests are distinguishable from one-off preferences

No major architecture expansion until this evidence exists.

---

# Milestone 6 — First paid release

**Purpose:** prove commercial value, not maximize revenue yet.

Initial offers to test:
- desktop/local Zenith Inventory license
- paid onboarding / spreadsheet migration
- paid integration or custom file mapping
- bounded workflow customization
- optional support/maintenance

Keep the first quote easy to understand. One customer should know exactly what is standard product versus paid implementation work.

Commercial success gate:
- [ ] first paid Zenith Inventory transaction
- [ ] first $500+ customer relationship across license/setup/integration
- [ ] installation/onboarding time is measured
- [ ] support burden is measured
- [ ] customer gives permission for a testimonial/case study if satisfied

---

# Milestone 7 — Reusable integration business

**Purpose:** turn customer variation into leverage rather than product bloat.

Integration policy:
- ProNest remains adapter #1
- a laser/CNC, ERP, accounting package, supplier system, API, or customer CSV mapping becomes another adapter only when a real workflow justifies it
- core inventory rules do not live inside adapters
- repeated customer-specific mappings should become configurable/reusable modules

For every requested integration record:
- external system
- direction: import/export/two-way
- file/API/protocol
- fields required
- frequency
- business value
- customer-specific assumptions
- reusable percentage
- implementation/support price

Exit gate:
- [ ] at least one paid integration exists
- [ ] adapter contract works for something beyond ProNest
- [ ] new integrations can be added without editing primary inventory screens/core quantity rules

---

# Milestone 8 — Scale decision

Only after paid usage decide whether evidence supports:
- multi-user/network edition
- authentication/roles
- cloud synchronization
- hosted SaaS
- mobile scanner companion
- purchase orders
- supplier/order workflows
- manufacturing/BOM consumption
- deeper ERP integrations

These are **not promises**. They are options triggered by paying users.

Decision gate:
- what do customers repeatedly pay for?
- what creates support burden?
- does a recurring hosted model solve a demonstrated problem?
- which integrations are reusable?
- should Zenith Inventory remain a focused desktop product or become a larger platform?

---

# Daily execution rule

When beginning a work session:

1. Open `docs/PROJECT_STATE.md`.
2. Work only the exact next task.
3. Run automated tests.
4. Commit a bounded change.
5. Update `PROJECT_STATE.md` when the next task changes.

A productive day does **not** require writing a lot of code. It requires moving the current exit gate closer to complete.
