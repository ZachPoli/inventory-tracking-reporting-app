from __future__ import annotations

from typing import Any, Sequence

from services.export_service import export_inventory_pronest_dataframe

from .base import IntegrationMetadata, InventoryExportIntegration


class ProNestIntegration(InventoryExportIntegration):
    """
    Compatibility adapter for the existing ProNest export.

    This is intentionally a thin wrapper first. The next refactor will move
    ProNest-specific transformation rules out of services/export_service.py
    and into this module without changing the user-visible export behavior.
    """

    metadata = IntegrationMetadata(
        key="pronest",
        name="ProNest",
        description="Export inventory/material data for ProNest workflows.",
    )

    def build_export(self, visible_items: Sequence[dict[str, Any]] | None = None):
        return export_inventory_pronest_dataframe(visible_items)
