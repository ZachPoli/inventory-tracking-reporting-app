from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sqlite3

from domain.models import InventoryItem, InventoryMovement
from .base import InventoryRepository


_ALLOWED_MOVEMENT_TYPES = {"receive", "consume", "adjust"}


class SQLiteInventoryRepository(InventoryRepository):
    def __init__(self, database_path: str | Path):
        self.database_path = Path(database_path)

    def _connect(self) -> sqlite3.Connection:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    @staticmethod
    def _now_iso() -> str:
        return datetime.now(timezone.utc).isoformat(timespec="seconds")

    def initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    barcode TEXT NOT NULL UNIQUE,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL DEFAULT '',
                    quantity REAL NOT NULL DEFAULT 0,
                    unit TEXT NOT NULL DEFAULT 'ea',
                    location TEXT NOT NULL DEFAULT '',
                    minimum_stock REAL NOT NULL DEFAULT 0,
                    supplier TEXT NOT NULL DEFAULT '',
                    notes TEXT NOT NULL DEFAULT '',
                    thickness TEXT NOT NULL DEFAULT '',
                    dimensions TEXT NOT NULL DEFAULT '',
                    grade TEXT NOT NULL DEFAULT '',
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS movements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER NOT NULL,
                    occurred_at TEXT NOT NULL,
                    movement_type TEXT NOT NULL,
                    quantity_delta REAL NOT NULL,
                    resulting_quantity REAL NOT NULL,
                    note TEXT NOT NULL DEFAULT '',
                    source TEXT NOT NULL DEFAULT '',
                    FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_items_name ON items(name);
                CREATE INDEX IF NOT EXISTS idx_items_category ON items(category);
                CREATE INDEX IF NOT EXISTS idx_items_location ON items(location);
                CREATE INDEX IF NOT EXISTS idx_movements_item_time
                    ON movements(item_id, occurred_at DESC);
                """
            )

    def create_item(self, item: InventoryItem) -> InventoryItem:
        if not item.barcode.strip():
            raise ValueError("Barcode/SKU is required.")
        if not item.name.strip():
            raise ValueError("Item name is required.")
        if item.quantity < 0:
            raise ValueError("Initial quantity cannot be negative.")

        updated_at = self._now_iso()
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO items (
                    barcode, name, category, quantity, unit, location,
                    minimum_stock, supplier, notes, thickness, dimensions,
                    grade, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item.barcode.strip(),
                    item.name.strip(),
                    item.category.strip(),
                    float(item.quantity),
                    item.unit.strip() or "ea",
                    item.location.strip(),
                    float(item.minimum_stock),
                    item.supplier.strip(),
                    item.notes.strip(),
                    item.thickness.strip(),
                    item.dimensions.strip(),
                    item.grade.strip(),
                    updated_at,
                ),
            )
            item_id = cursor.lastrowid

        return self._require_item_by_id(item_id)

    def get_item_by_barcode(self, barcode: str) -> InventoryItem | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM items WHERE barcode = ?",
                (barcode.strip(),),
            ).fetchone()
        return self._item_from_row(row) if row else None

    def list_items(self, search: str | None = None) -> list[InventoryItem]:
        sql = "SELECT * FROM items"
        params: tuple[str, ...] = ()
        if search and search.strip():
            pattern = f"%{search.strip()}%"
            sql += (
                " WHERE barcode LIKE ? OR name LIKE ? OR category LIKE ?"
                " OR location LIKE ?"
            )
            params = (pattern, pattern, pattern, pattern)
        sql += " ORDER BY name, barcode"

        with self._connect() as connection:
            rows = connection.execute(sql, params).fetchall()
        return [self._item_from_row(row) for row in rows]

    def adjust_quantity(
        self,
        barcode: str,
        delta: float,
        movement_type: str,
        *,
        note: str = "",
        source: str = "",
    ) -> InventoryItem:
        if movement_type not in _ALLOWED_MOVEMENT_TYPES:
            raise ValueError(
                f"Movement type must be one of: {', '.join(sorted(_ALLOWED_MOVEMENT_TYPES))}."
            )

        with self._connect() as connection:
            row = connection.execute(
                "SELECT id, quantity FROM items WHERE barcode = ?",
                (barcode.strip(),),
            ).fetchone()
            if not row:
                raise KeyError(f"No inventory item found for barcode/SKU: {barcode}")

            current_quantity = float(row["quantity"])
            new_quantity = current_quantity + float(delta)
            if new_quantity < 0:
                raise ValueError(
                    f"Quantity cannot go below zero (current={current_quantity}, delta={delta})."
                )

            occurred_at = self._now_iso()
            connection.execute(
                "UPDATE items SET quantity = ?, updated_at = ? WHERE id = ?",
                (new_quantity, occurred_at, row["id"]),
            )
            connection.execute(
                """
                INSERT INTO movements (
                    item_id, occurred_at, movement_type, quantity_delta,
                    resulting_quantity, note, source
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row["id"],
                    occurred_at,
                    movement_type,
                    float(delta),
                    new_quantity,
                    note.strip(),
                    source.strip(),
                ),
            )

        return self._require_item_by_id(row["id"])

    def list_movements(
        self,
        item_id: int | None = None,
        *,
        limit: int = 100,
    ) -> list[InventoryMovement]:
        if limit < 1:
            return []

        sql = "SELECT * FROM movements"
        params: list[object] = []
        if item_id is not None:
            sql += " WHERE item_id = ?"
            params.append(item_id)
        sql += " ORDER BY occurred_at DESC, id DESC LIMIT ?"
        params.append(limit)

        with self._connect() as connection:
            rows = connection.execute(sql, params).fetchall()
        return [self._movement_from_row(row) for row in rows]

    def _require_item_by_id(self, item_id: int | None) -> InventoryItem:
        if item_id is None:
            raise RuntimeError("Inventory item was not assigned an id.")
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM items WHERE id = ?",
                (item_id,),
            ).fetchone()
        if row is None:
            raise RuntimeError(f"Inventory item {item_id} disappeared after write.")
        return self._item_from_row(row)

    @staticmethod
    def _item_from_row(row: sqlite3.Row) -> InventoryItem:
        return InventoryItem(
            id=row["id"],
            barcode=row["barcode"],
            name=row["name"],
            category=row["category"],
            quantity=float(row["quantity"]),
            unit=row["unit"],
            location=row["location"],
            minimum_stock=float(row["minimum_stock"]),
            supplier=row["supplier"],
            notes=row["notes"],
            thickness=row["thickness"],
            dimensions=row["dimensions"],
            grade=row["grade"],
            updated_at=row["updated_at"],
        )

    @staticmethod
    def _movement_from_row(row: sqlite3.Row) -> InventoryMovement:
        return InventoryMovement(
            id=row["id"],
            item_id=row["item_id"],
            occurred_at=row["occurred_at"],
            movement_type=row["movement_type"],
            quantity_delta=float(row["quantity_delta"]),
            resulting_quantity=float(row["resulting_quantity"]),
            note=row["note"],
            source=row["source"],
        )
