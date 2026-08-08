# Environmental Pneumatics Inventory Tracking & Reporting App

A Python/PostgreSQL inventory application I independently designed, built, and **used in a real manufacturing workflow** while working as a CNC laser operator at Environmental Pneumatics in Oakland, Tennessee.

## Why I Built It

Sheet-metal availability directly affected laser-production work. I wanted a faster, more structured way to track what material was on hand rather than relying only on manual observation and informal records.

I built this system to track sheet metal by attributes such as material type, gauge/thickness, dimensions, storage location, and quantity.

The longer-term idea was broader shop integration. My employment ended before that full rollout was completed, so I do not describe this as a shop-wide production deployment. However, **I did personally use the database and application in my laser-operating work to track the material available to me.**

## What It Does

- Create, read, update, and delete inventory records
- Store and query structured inventory data in PostgreSQL
- Track sheet metal by type, gauge/thickness, dimensions, location, and quantity
- Validate inventory inputs
- Generate and print barcode labels
- Filter and sort stored material
- Export CSV/XLSX data for reporting
- Export data for ProNest-related workflows
- Back up and restore inventory data
- Maintain indexed fields for frequently queried inventory attributes

## Technology

- **Python** — application and workflow logic
- **PostgreSQL / SQL** — structured inventory storage and querying
- **Tkinter** — desktop user interface
- **ReportLab / Pillow** — barcode and printable-output workflows
- **CSV / XLSX** — data exchange and reporting
- **ProNest-related exports** — support for the CNC laser workflow

## Why It Matters

This project connects my manufacturing background directly to software development.

I wasn't building an abstract portfolio exercise. I was operating CNC laser equipment, seeing an inventory problem in my own work, and building software to make that workflow more structured and useful.

It demonstrates:

- translating an operational problem into software requirements
- relational data modeling
- SQL query design
- inventory data validation
- CRUD application development
- reporting/export workflows
- barcode tooling
- backup/recovery thinking
- iterative development informed by real use

## Representative Data Model

The inventory system tracks fields such as:

- barcode
- shelf/storage location
- thickness/gauge
- metal type
- dimensions
- quantity
- sheet length and width
- date
- usable scrap status

Frequently searched attributes are indexed to support practical lookup workflows.

## Project Structure

```text
EP_Inventory_Management/
├── db/
│   ├── config.py
│   ├── connection.py
│   └── queries.py
├── services/
│   ├── inventory_service.py
│   ├── export_service.py
│   ├── backup_service.py
│   └── barcode_service.py
├── utils/
│   └── formatting.py
├── inventory_import.py
├── Inventory_Management_Fixed.py
└── requirements.txt
```

## Running Locally

Requirements:

- Python 3.11+
- PostgreSQL 13+
- dependencies in `requirements.txt`

Create a local PostgreSQL database, configure the local connection, apply the inventory schema, install the Python dependencies, and run:

```powershell
python Inventory_Management_Fixed.py
```

Do not commit local database credentials.

## Potential Next Steps

- add inventory trend and reorder analytics
- add production-consumption history
- add dashboard reporting
- formalize roles/authentication
- further automate ProNest/material workflows

---

Built by **Zachary Maness** as an independently developed manufacturing/inventory tool used during his work at Environmental Pneumatics.
