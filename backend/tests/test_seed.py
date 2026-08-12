import gc
import os
import tempfile
import unittest

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.core.security import verify_password
from app.core.config import get_settings
from app.db.models import Base, Permission, Role, User
from app.db.seed import ROLE_NAMES, PERMISSIONS, seed_auth_data
from app.db.session import reset_engine, SessionLocal


class SeedTests(unittest.TestCase):
    def setUp(self):
        self.tmp_db = tempfile.NamedTemporaryFile(suffix='.sqlite', delete=False)
        self.tmp_db.close()
        self.db_url = f'sqlite:///{self.tmp_db.name}'
        os.environ['DATABASE_URL'] = self.db_url
        os.environ['BOOTSTRAP_ADMIN_PASSWORD'] = 'TempP@ss1234'
        self.engine = create_engine(self.db_url, future=True)
        self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False, future=True)
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        self.engine.dispose()
        reset_engine()
        gc.collect()
        os.unlink(self.tmp_db.name)

    def test_seed_authorization_data(self):
        reset_engine()

        with self.SessionLocal() as session:
            session.execute(text('PRAGMA foreign_keys=ON'))
            session.commit()

        seed_auth_data()

        with self.SessionLocal() as session:
            roles = session.query(Role).all()
            self.assertEqual({role.role_name for role in roles}, set(ROLE_NAMES))
            permissions = session.query(Permission).all()
            self.assertEqual({perm.permission_code for perm in permissions}, {p['permission_code'] for p in PERMISSIONS})
            admin_user = session.query(User).filter_by(username='admin').one()
            self.assertEqual(admin_user.role.role_name, 'Admin')
            self.assertTrue(verify_password('TempP@ss1234', admin_user.password_hash))

    def test_seed_idempotency(self):
        seed_auth_data()
        seed_auth_data()

        from app.db.session import init_engine

        init_engine()

        from app.db.session import SessionLocal

        with SessionLocal() as session:
            self.assertEqual(session.query(Role).filter(Role.role_name == 'Admin').count(), 1)
            self.assertEqual(session.query(Permission).filter(Permission.permission_code == 'users:manage').count(), 1)
            self.assertEqual(session.query(User).filter(User.username == 'admin').count(), 1)
