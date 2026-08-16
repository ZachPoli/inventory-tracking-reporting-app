# -*- coding: utf-8 -*-
from __future__ import annotations

import pandas as pd

from db.queries import fetch_all


def fetch_inventory_rows_for_csv():
    """Return normalized inventory rows for generic CSV/XLSX export."""
    return fetch_all(
        """
        SELECT barcode, shelf, thickness, metal_type,
               dimensions, location, quantity, usable_scrap, date
        FROM inventory
        """
    )


def build_csv_dataframe(rows):
    """Build the core spreadsheet export without external-system rules."""
    columns = (
        "barcode",
        "shelf",
        "thickness",
        "metal_type",
        "dimensions",
        "location",
        "quantity",
        "usable_scrap",
        "date",
    )
    return pd.DataFrame([list(row) for row in rows], columns=columns)


def export_inventory_pronest_dataframe(visible_items=None):
    """
    Backward-compatible bridge for the legacy UI.

    ProNest is no longer implemented in the core export service. New code
    should resolve the integration from `integrations` directly. This wrapper
    remains temporarily so the existing Tkinter application continues to run
    while the UI is streamlined incrementally.
    """
    from integrations import get_export_integration

    integration = get_export_integration("pronest")
    return integration.build_export(visible_items)


__all__ = [
    "fetch_inventory_rows_for_csv",
    "build_csv_dataframe",
    "export_inventory_pronest_dataframe",
]
