from __future__ import annotations

from abc import ABC, abstractmethod

from domain.models import InventoryItem, InventoryMovement


class InventoryRepository(ABC):
    @abstractmethod
    def initialize(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def create_item(self, item: InventoryItem) -> InventoryItem:
        raise NotImplementedError

    @abstractmethod
    def get_item_by_barcode(self, barcode: str) -> InventoryItem | None:
        raise NotImplementedError

    @abstractmethod
    def list_items(self, search: str | None = None) -> list[InventoryItem]:
        raise NotImplementedError

    @abstractmethod
    def adjust_quantity(
        self,
        barcode: str,
        delta: float,
        movement_type: str,
        *,
        note: str = "",
        source: str = "",
    ) -> InventoryItem:
        raise NotImplementedError

    @abstractmethod
    def list_movements(
        self,
        item_id: int | None = None,
        *,
        limit: int = 100,
    ) -> list[InventoryMovement]:
        raise NotImplementedError
