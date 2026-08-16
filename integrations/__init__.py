from __future__ import annotations

from .base import InventoryExportIntegration
from .pronest import ProNestIntegration


_EXPORT_INTEGRATIONS: dict[str, InventoryExportIntegration] = {
    "pronest": ProNestIntegration(),
}


def get_export_integration(key: str) -> InventoryExportIntegration:
    try:
        return _EXPORT_INTEGRATIONS[key]
    except KeyError as exc:
        raise KeyError(f"Unknown inventory export integration: {key}") from exc


def list_export_integrations() -> tuple[InventoryExportIntegration, ...]:
    return tuple(_EXPORT_INTEGRATIONS.values())


__all__ = [
    "InventoryExportIntegration",
    "get_export_integration",
    "list_export_integrations",
]
