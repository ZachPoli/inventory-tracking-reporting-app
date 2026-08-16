import unittest

from integrations.pronest import ProNestConfig, build_pronest_dataframe


class ProNestTransformTests(unittest.TestCase):
    def test_builds_configurable_pronest_row_without_company_hardcoding(self):
        source_rows = [
            (
                "Aluminum",
                "14",
                "48 x 96",
                8,
                96,
                48,
                "Rack A",
                "2026-08-16",
                "Shelf 1",
                "Full Sheet",
            )
        ]
        config = ProNestConfig(
            supplier="Example Fabrication",
            created_by="Zenith Inventory Test",
        )

        frame = build_pronest_dataframe(source_rows, config)

        self.assertEqual(len(frame), 1)
        self.assertEqual(frame.loc[0, "Supplier"], "Example Fabrication")
        self.assertEqual(frame.loc[0, "Created by"], "Zenith Inventory Test")
        self.assertEqual(frame.loc[0, "Material"], "AL")
        self.assertEqual(frame.loc[0, "Stock Qty"], 8)
        self.assertEqual(frame.loc[0, "Length"], 96.0)
        self.assertEqual(frame.loc[0, "Width"], 48.0)


if __name__ == "__main__":
    unittest.main()
