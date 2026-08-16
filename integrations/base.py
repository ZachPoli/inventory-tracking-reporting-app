from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Sequence


@dataclass(frozen=True)
class IntegrationMetadata:
    """Human-readable information the UI can display for an integration."""

    key: str
    name: str
    description: str


class InventoryExportIntegration(ABC):
    """
    Boundary between Zenith Inventory and an external system.

    Core inventory code should not know an external system's file layout,
    naming rules, or customer-specific defaults. Those belong here.
    """

    metadata: IntegrationMetadata

    @abstractmethod
    def build_export(self, visible_items: Sequence[dict[str, Any]] | None = None):
        """Return export-ready data for the external system."""
        raise NotImplementedError
