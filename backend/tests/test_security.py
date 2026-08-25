import unittest

from app.core.security import hash_password, verify_password


class SecurityTests(unittest.TestCase):
    def test_hash_and_verify_password(self):
        plain_text = "S3cureP@ssw0rd"
        hashed = hash_password(plain_text)

        self.assertNotEqual(hashed, plain_text)
        self.assertTrue(verify_password(plain_text, hashed))
        self.assertFalse(verify_password("wrong-password", hashed))
