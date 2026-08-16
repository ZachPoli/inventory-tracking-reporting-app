from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InventoryItem:
    barcode: str
    name: str
    id: int | None = None
    category: str = ""
    quantity: float = 0.0
    unit: str = "ea"
    location: str = ""
    minimum_stock: float = 0.0
    supplier: str = ""
    notes: str = ""
    thickness: str = ""
    dimensions: str = ""
    grade: str = ""
    updated_at: str | None = None


@dataclass(frozen=True)
class InventoryMovement:
    item_id: int
    movement_type: str
    quantity_delta: float
    resulting_quantity: float
    id: int | None = None
    note: str = ""
    source: str = ""
    occurred_at: str | None = None
