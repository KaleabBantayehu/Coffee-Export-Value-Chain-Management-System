import unittest
from unittest.mock import patch

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.identifiers import FIN_FORMAT_PATTERN, generate_farmer_fin, validate_farmer_fin


class FarmerFinTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(get_settings().DATABASE_URL)

    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()

    def setUp(self):
        self.connection = self.engine.connect()
        self.transaction = self.connection.begin()
        self.session = Session(bind=self.connection)

    def tearDown(self):
        self.session.close()
        self.transaction.rollback()
        self.connection.close()

    def test_generate_farmer_fin_returns_canonical_shape(self):
        with patch("app.core.identifiers.secrets.randbelow", side_effect=[12, 345678]):
            fin = generate_farmer_fin(self.session)

        self.assertEqual(fin, "ETH-FAR-0012-345678")
        self.assertRegex(fin, r"^ETH-FAR-\d{4}-\d{6}$")
        self.assertTrue(validate_farmer_fin(fin))
        self.assertEqual(FIN_FORMAT_PATTERN, "ETH-FAR-XXXX-XXXXXX")

    def test_generate_farmer_fin_returns_distinct_values(self):
        with patch("app.core.identifiers.secrets.randbelow", side_effect=[12, 345678, 98, 765432]):
            first = generate_farmer_fin(self.session)
            second = generate_farmer_fin(self.session)

        self.assertNotEqual(first, second)
        self.assertTrue(validate_farmer_fin(first))
        self.assertTrue(validate_farmer_fin(second))

    def test_generate_farmer_fin_retries_after_database_collision(self):
        colliding_fin = "ETH-FAR-0001-000001"
        self.session.execute(
            text(
                "INSERT INTO farmers (fin_code, full_name, national_id, created_at) VALUES (:fin, 'Collision Farmer', 'NATIONAL-001', now())"
            ),
            {"fin": colliding_fin},
        )
        self.session.flush()

        with patch("app.core.identifiers.secrets.randbelow", side_effect=[1, 1, 1234, 567890]):
            fin = generate_farmer_fin(self.session)

        self.assertEqual(fin, "ETH-FAR-1234-567890")
        self.assertTrue(validate_farmer_fin(fin))

    def test_validate_farmer_fin_rejects_invalid_values(self):
        invalid_values = [
            "ETH-FAR-123-123456",
            "ETH-FAR-1234-12345",
            "ETH-AGR-1234-123456",
            "ETH-FAR-ABCD-123456",
            "ETH-FAR-1234-ABCDEF",
        ]

        for invalid_value in invalid_values:
            with self.subTest(value=invalid_value):
                self.assertFalse(validate_farmer_fin(invalid_value))

        self.assertTrue(validate_farmer_fin("ETH-FAR-1234-123456"))


if __name__ == "__main__":
    unittest.main()
