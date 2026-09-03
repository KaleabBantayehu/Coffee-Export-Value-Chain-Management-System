import unittest
from unittest.mock import MagicMock, patch

from app.core.identifiers import (
    GIN_FORMAT_PATTERN,
    format_coffee_lot_gin,
    generate_coffee_lot_gin,
    validate_coffee_lot_gin,
)


class CoffeeLotGinTests(unittest.TestCase):
    def test_format_and_validation_use_approved_canonical_shape(self):
        gin = format_coffee_lot_gin(2026, 1)

        self.assertEqual(gin, "ETH-LOT-2026-000001")
        self.assertEqual(GIN_FORMAT_PATTERN, "ETH-LOT-YYYY-NNNNNN")
        self.assertTrue(validate_coffee_lot_gin(gin))

    def test_generation_returns_distinct_candidates(self):
        with patch("app.core.identifiers.secrets.randbelow", side_effect=[1, 2]):
            first = generate_coffee_lot_gin()
            second = generate_coffee_lot_gin()

        self.assertNotEqual(first, second)
        self.assertTrue(validate_coffee_lot_gin(first))
        self.assertTrue(validate_coffee_lot_gin(second))

    def test_generation_retries_after_existing_gin_collision(self):
        session = MagicMock()
        session.query.return_value.filter.return_value.first.side_effect = [object(), None]

        with patch("app.core.identifiers.secrets.randbelow", side_effect=[1, 2]):
            gin = generate_coffee_lot_gin(session)

        self.assertTrue(validate_coffee_lot_gin(gin))
        self.assertTrue(gin.endswith("-000002"))
        self.assertEqual(session.query.return_value.filter.return_value.first.call_count, 2)

    def test_validation_rejects_invalid_values(self):
        invalid_values = [
            "ETH-LOT-2026-G1-000001",
            "ETH-LOT-202-000001",
            "ETH-LOT-2026-00001",
            "ETH-FAR-2026-000001",
            None,
        ]

        for value in invalid_values:
            with self.subTest(value=value):
                self.assertFalse(validate_coffee_lot_gin(value))


if __name__ == "__main__":
    unittest.main()
