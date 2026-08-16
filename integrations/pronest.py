from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Sequence

import pandas as pd

from db.connection import get_cursor
from db.queries import fetch_all
from services.inventory_service import parse_dimensions

from .base import IntegrationMetadata, InventoryExportIntegration


GAUGE_TO_INCHES = {
    "6": 0.1935, "7": 0.1875, "8": 0.1644, "9": 0.1500,
    "10": 0.1350, "11": 0.1200, "12": 0.1050, "13": 0.0897,
    "14": 0.0750, "15": 0.0673, "16": 0.0600, "17": 0.0538,
    "18": 0.0480, "19": 0.0418, "20": 0.0360, "22": 0.0300,
    "24": 0.0240, "26": 0.0180, "28": 0.0150, "30": 0.0120,
}

PRONEST_HEADERS = [
    "Description", "Plate Type", "Units", "Length", "Width", "MaterialID",
    "Material", "Thickness", "Stock Qty", "Unit Price", "Date Created",
    "Rotation", "Heat Num", "Stock Num", "Misc1", "Misc2", "Misc3",
    "Location", "Reorder limit", "Reorder quantity", "Supplier",
    "Created by", "Plate Path", "Grade",
]


@dataclass(frozen=True)
class ProNestConfig:
    """Customer/site-specific defaults kept outside the inventory core."""

    supplier: str = ""
    created_by: str = "Zenith Inventory"
    default_length_in: float = 48.0
    default_width_in: float = 48.0


def thickness_to_decimal(thickness_str: str) -> float:
    if not thickness_str:
        return 0.0

    value = thickness_str.strip()
    upper = value.upper()

    if any(marker in upper for marker in ("G", "GA", "GAUGE")):
        digits = "".join(char for char in value if char.isdigit())
        return GAUGE_TO_INCHES.get(digits, 0.0)

    if value in GAUGE_TO_INCHES:
        return GAUGE_TO_INCHES[value]

    if "/" in value:
        fraction_map = {
            "1/8": 0.1250,
            "1/4": 0.2500,
            "3/8": 0.3750,
            "1/2": 0.5000,
            "5/8": 0.6250,
            "3/4": 0.7500,
            "7/8": 0.8750,
            "1": 1.0,
        }
        if value in fraction_map:
            return fraction_map[value]
        try:
            numerator, denominator = value.split("/", 1)
            return float(numerator) / float(denominator)
        except (ValueError, ZeroDivisionError):
            return 0.0

    try:
        return float(value)
    except ValueError:
        return 0.0


def classify_material_code(metal_type: str | None, thickness_original: str | None) -> str:
    metal_type_lower = (metal_type or "").lower()
    code = thickness_original or ""

    if "black" in metal_type_lower:
        return code + "B"
    if "plate" in metal_type_lower:
        return code + "PL"
    if "galv" in metal_type_lower:
        return code + "G"
    if "aluminum" in metal_type_lower or metal_type_lower == "al":
        return code + "AL"

    abbreviation = "".join(
        word[0].upper() for word in (metal_type or "").split() if word
    )
    return code + abbreviation


def pronest_material_abbrev(metal_type: str | None) -> str:
    material = (metal_type or "").lower()
    if "aluminum" in material or material == "al":
        return "AL"
    if "stainless" in material or "ss" in material:
        return "SS"
    return "MS"


def description_prefix(metal_type: str | None) -> str:
    material = (metal_type or "").lower()
    if "plate" in material:
        return "~"
    if "black" in material:
        return "+"
    if "galv" in material:
        return "-"
    if "aluminum" in material or material == "al":
        return "="
    if "stainless" in material or "ss" in material:
        return "<"
    return ""


def _normalize_visible_items(
    visible_items: Sequence[dict[str, Any] | Sequence[Any]] | None,
) -> list[tuple[Any, Any, Any, Any]] | None:
    if not visible_items:
        return None

    normalized: list[tuple[Any, Any, Any, Any]] = []
    for item in visible_items:
        if isinstance(item, dict):
            normalized.append(
                (
                    item.get("shelf"),
                    item.get("thickness"),
                    item.get("metal_type"),
                    item.get("dimensions"),
                )
            )
        else:
            shelf, thickness, metal_type, dimensions = item[:4]
            normalized.append((shelf, thickness, metal_type, dimensions))
    return normalized


def _fetch_source_rows(
    visible_items: Sequence[dict[str, Any] | Sequence[Any]] | None = None,
):
    normalized = _normalize_visible_items(visible_items)
    if normalized:
        rows = []
        with get_cursor() as cursor:
            for shelf, thickness, metal_type, dimensions in normalized:
                cursor.execute(
                    """
                    SELECT metal_type, thickness, dimensions, quantity, length, width,
                           location, date, shelf, usable_scrap
                    FROM inventory
                    WHERE shelf=%s AND thickness=%s AND metal_type=%s AND dimensions=%s
                    """,
                    (shelf, thickness, metal_type, dimensions),
                )
                row = cursor.fetchone()
                if row:
                    rows.append(row)
        return rows

    return fetch_all(
        """
        SELECT metal_type, thickness, dimensions, quantity, length, width,
               location, date, shelf, usable_scrap
        FROM inventory
        """
    )


def build_pronest_dataframe(source_rows, config: ProNestConfig | None = None):
    config = config or ProNestConfig()
    output_rows = []

    for index, row in enumerate(source_rows):
        (
            metal_type,
            thickness,
            dimensions,
            quantity,
            length,
            width,
            location,
            date_value,
            shelf,
            usable_scrap,
        ) = row

        if (not length or not width) and dimensions:
            parsed = parse_dimensions(str(dimensions))
            if parsed:
                length, width = parsed

        length = float(length or config.default_length_in)
        width = float(width or config.default_width_in)
        length_feet = int(length / 12)
        width_feet = int(width / 12)

        thickness_text = thickness.strip() if thickness else ""
        decimal_thickness = thickness_to_decimal(thickness_text)
        material_code = classify_material_code(metal_type, thickness_text)
        description = (
            f"{description_prefix(metal_type)}{material_code} "
            f"({width_feet}' x {length_feet}')"
        )
        stock_number = f"{material_code}{width_feet}{length_feet}"
        material_id = f"MAT{index + 1:03d}"
        date_created = date_value or datetime.now().strftime("%Y-%m-%d")
        quantity_int = int(quantity) if quantity else 0
        reorder_limit = max(1, quantity_int // 2) if quantity_int else 1
        reorder_quantity = max(1, quantity_int // 4) if quantity_int else 1

        output_rows.append(
            [
                description,
                "Rectangular",
                "Inches",
                length,
                width,
                material_id,
                pronest_material_abbrev(metal_type),
                decimal_thickness,
                quantity_int,
                0.0,
                date_created,
                0,
                "",
                stock_number,
                usable_scrap,
                shelf,
                "",
                location,
                reorder_limit,
                reorder_quantity,
                config.supplier,
                config.created_by,
                "",
                "",
            ]
        )

    return pd.DataFrame(output_rows, columns=PRONEST_HEADERS)


class ProNestIntegration(InventoryExportIntegration):
    metadata = IntegrationMetadata(
        key="pronest",
        name="ProNest",
        description="Export material inventory for ProNest workflows.",
    )

    def __init__(self, config: ProNestConfig | None = None):
        self.config = config or ProNestConfig()

    def build_export(
        self,
        visible_items: Sequence[dict[str, Any] | Sequence[Any]] | None = None,
    ):
        source_rows = _fetch_source_rows(visible_items)
        if not source_rows:
            return None
        return build_pronest_dataframe(source_rows, self.config)
