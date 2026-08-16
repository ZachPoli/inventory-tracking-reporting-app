# Streamline Audit

This audit records the highest-value cleanup targets before the original application grows into the commercial product.

## Keep — valuable proven behavior

- inventory CRUD
- barcode lookup and label generation
- quantity adjustment
- filtering/search/sort
- CSV/XLSX interchange
- backup/restore concept
- manufacturing dimensions/thickness support as optional fields
- ProNest behavior as an optional integration

## Extract / decouple

### ProNest

Current state: ProNest transformation logic lives in the general export service and includes Environmental Pneumatics-specific defaults.

Target: move all ProNest rules to `integrations/pronest.py`; the core only supplies normalized inventory records.

### Database

Current state: the app depends directly on PostgreSQL connection/query helpers.

Target: application services should depend on a repository/data-access boundary. The first commercial implementation should use an embedded local database so installation does not require PostgreSQL administration.

### UI vs services

Current state: the main Tkinter file contains UI construction, direct SQL/query construction, validation, export orchestration, backup actions, barcode behavior, filtering, destructive maintenance controls, and legacy migration utilities.

Target: thin UI -> application services -> repository/integrations.

### Backup service

Current state: backup code contains Tkinter dialogs/message boxes in the service layer.

Target: services return results/errors; UI owns dialogs and file selection.

## Remove or quarantine

- legacy barcode migration/rebuild utilities that are not part of the normal user workflow
- duplicated imports and developer comments left in runtime code
- company-specific branding in the product UI
- company-specific supplier/creator defaults in shared exports
- maintenance actions that are dangerous or confusing for normal users
- implementation-specific controls such as manual dimension extraction when the product can normalize data automatically

## Known structural problems

1. `Inventory_Management_Fixed.py` is a large monolithic UI/controller file.
2. Core query/filter behavior is partially assembled directly in the UI.
3. External integration behavior is mixed into general export code.
4. The application requires an externally configured PostgreSQL server.
5. There is no product installer/release path in the repository.
6. There is no clear schema migration/first-run initialization path for a new customer.
7. There is no inventory movement ledger; the system mostly represents current quantity.
8. There is no automated test suite protecting critical workflows before refactoring.

## Refactor order

Do not rewrite the entire program at once.

1. security cleanup
2. smoke-test baseline
3. integration seam (started)
4. isolate ProNest behind adapter
5. data/repository seam
6. embedded database + first-run schema
7. movement/history model
8. simplify primary UI workflow
9. remove legacy code after replacement behavior is verified
10. package clean Windows build

## Definition of streamlined

The product is streamlined when a new user primarily sees and understands:

- Find/scan item
- Add item
- Receive stock
- Consume stock
- Adjust stock
- Inventory list/search
- Low stock
- Activity history
- Import/export
- Labels
- Backup
- Integrations

Everything else must justify why it belongs in the product core.
