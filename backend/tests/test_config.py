import os
import unittest

from app.core.config import get_settings


class ConfigTests(unittest.TestCase):
    def test_settings_load_from_env(self):
        os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
        os.environ.setdefault("JWT_SECRET_KEY", "testsecretkey123")
        settings = get_settings()

        self.assertTrue(settings.DATABASE_URL)
        self.assertEqual(settings.BOOTSTRAP_ADMIN_USERNAME, "admin")
        self.assertEqual(settings.BOOTSTRAP_ADMIN_FULL_NAME, "Administrator")
        self.assertEqual(settings.BOOTSTRAP_ADMIN_ROLE_NAME, "Admin")
        self.assertEqual(settings.JWT_SECRET_KEY, "testsecretkey123")
