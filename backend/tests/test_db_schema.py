import os
import subprocess
import sys
import unittest
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

from app.core.config import get_settings


class DatabaseSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(get_settings().DATABASE_URL)

    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()

    def setUp(self):
        self.connection = self.engine.connect()
        self.transaction = self.connection.begin()
        self.role_id = self.connection.execute(text("INSERT INTO roles (role_name) VALUES ('schema-test-role') RETURNING role_id")).scalar_one()
        self.user_id = self.connection.execute(text("INSERT INTO users (username, password_hash, full_name, role_id, is_active, created_at) VALUES ('schema-test-user', 'hash', 'Schema Test', :role_id, true, now()) RETURNING user_id"), {"role_id": self.role_id}).scalar_one()
        self.farmer_id = self.connection.execute(text("INSERT INTO farmers (fin_code, full_name, national_id, created_at) VALUES ('SCHEMA-FIN-1', 'Schema Farmer', 'SCHEMA-NID-1', now()) RETURNING farmer_id")).scalar_one()
        self.farm_id = self.connection.execute(text("INSERT INTO farms (farmer_id, polygon_geom, area_hectares, eudr_risk_flag, created_at) VALUES (:farmer_id, ST_GeomFromText('POLYGON((0 0,0 1,1 1,1 0,0 0))', 4326), 1.0, false, now()) RETURNING farm_id"), {"farmer_id": self.farmer_id}).scalar_one()

    def tearDown(self):
        self.transaction.rollback()
        self.connection.close()

    def assert_integrity_error(self, statement, parameters):
        with self.assertRaises(IntegrityError):
            with self.connection.begin_nested():
                self.connection.execute(text(statement), parameters)

    def test_polygon_geometry_is_postgis_polygon_srid_4326(self):
        geometry = self.connection.execute(text("SELECT type, srid FROM geometry_columns WHERE f_table_schema = 'public' AND f_table_name = 'farms' AND f_geometry_column = 'polygon_geom'" )).one()
        self.assertEqual(geometry, ('POLYGON', 4326))

    def test_unique_farmer_fin_code_is_enforced_by_database(self):
        self.assert_integrity_error("INSERT INTO farmers (fin_code, full_name, national_id, created_at) VALUES (:fin, 'Duplicate', 'SCHEMA-NID-2', now())", {"fin": "SCHEMA-FIN-1"})

    def test_unique_farmer_national_id_is_enforced_by_database(self):
        self.assert_integrity_error("INSERT INTO farmers (fin_code, full_name, national_id, created_at) VALUES ('SCHEMA-FIN-2', 'Duplicate', :national_id, now())", {"national_id": "SCHEMA-NID-1"})

    def test_unique_lot_gin_code_is_enforced_by_database(self):
        statement = "INSERT INTO coffee_lots (gin_code, farm_id, created_by, status, created_at) VALUES (:gin, :farm_id, :user_id, 'created', now())"
        self.connection.execute(text(statement), {"gin": "SCHEMA-GIN-1", "farm_id": self.farm_id, "user_id": self.user_id})
        self.assert_integrity_error(statement, {"gin": "SCHEMA-GIN-1", "farm_id": self.farm_id, "user_id": self.user_id})

    def test_foreign_key_violation_is_enforced_by_database(self):
        self.assert_integrity_error("INSERT INTO farms (farmer_id, polygon_geom, area_hectares, eudr_risk_flag, created_at) VALUES (999999999, ST_GeomFromText('POLYGON((0 0,0 1,1 1,1 0,0 0))', 4326), 1.0, false, now())", {})

    def test_migration_is_idempotent_after_initial_application(self):
        backend_directory = Path(__file__).resolve().parents[1]
        result = subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], cwd=backend_directory, env=os.environ.copy(), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
