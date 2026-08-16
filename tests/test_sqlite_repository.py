import tempfile
import unittest
from pathlib import Path

from domain.models import InventoryItem
from storage.sqlite_repository import SQLiteInventoryRepository


class SQLiteInventoryRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "inventory.db"
        self.repository = SQLiteInventoryRepository(self.db_path)
        self.repository.initialize()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_lookup_search_and_quantity_movement(self):
        created = self.repository.create_item(
            InventoryItem(
                barcode="AL-14-4896",
                name="14ga Aluminum Sheet",
                category="Raw Material",
                quantity=5,
                location="Rack A",
                thickness="14",
                dimensions="48 x 96",
            )
        )
        self.assertIsNotNone(created.id)
        self.assertEqual(created.quantity, 5.0)

        found = self.repository.get_item_by_barcode("AL-14-4896")
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "14ga Aluminum Sheet")

        search_results = self.repository.list_items("Rack A")
        self.assertEqual(
            [item.barcode for item in search_results],
            ["AL-14-4896"],
        )

        updated = self.repository.adjust_quantity(
            "AL-14-4896",
            -2,
            "consume",
            note="Laser job",
            source="test",
        )
        self.assertEqual(updated.quantity, 3.0)

        movements = self.repository.list_movements(created.id)
        self.assertEqual(len(movements), 1)
        self.assertEqual(movements[0].movement_type, "consume")
        self.assertEqual(movements[0].quantity_delta, -2.0)
        self.assertEqual(movements[0].resulting_quantity, 3.0)

    def test_quantity_cannot_go_negative(self):
        self.repository.create_item(
            InventoryItem(barcode="PART-1", name="Part", quantity=1)
        )
        with self.assertRaises(ValueError):
            self.repository.adjust_quantity("PART-1", -2, "consume")


if __name__ == "__main__":
    unittest.main()
