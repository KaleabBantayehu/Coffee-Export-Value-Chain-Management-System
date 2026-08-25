from sqlalchemy.exc import IntegrityError

from app.core.config import get_settings
from app.core.security import hash_password
from app.db.models import Permission, Role, User
from app.db.session import get_session


ROLE_NAMES = [
    "Admin",
    "ECTA Officer",
    "Field/Registry Agent",
    "Verifier",
]

PERMISSIONS = [
    {"permission_code": "users:manage", "description": "Create, update and view user accounts."},
    {"permission_code": "roles:view", "description": "View role and permission data."},
]

ROLE_PERMISSIONS = {
    "Admin": ["users:manage", "roles:view"],
    "ECTA Officer": ["roles:view"],
    "Field/Registry Agent": [],
    "Verifier": [],
}


def seed_auth_data():
    settings = get_settings()
    with get_session() as session:
        permissions = {}
        for perm_data in PERMISSIONS:
            permission = session.query(Permission).filter_by(permission_code=perm_data["permission_code"]).one_or_none()
            if not permission:
                permission = Permission(**perm_data)
                session.add(permission)
            permissions[perm_data["permission_code"]] = permission

        roles = {}
        for role_name in ROLE_NAMES:
            role = session.query(Role).filter_by(role_name=role_name).one_or_none()
            if not role:
                role = Role(role_name=role_name, description=f"{role_name} role.")
                session.add(role)
            roles[role_name] = role

        session.flush()

        for role_name, permission_codes in ROLE_PERMISSIONS.items():
            role = roles[role_name]
            for permission_code in permission_codes:
                permission = permissions[permission_code]
                if permission not in role.permissions:
                    role.permissions.append(permission)

        if not settings.BOOTSTRAP_ADMIN_PASSWORD:
            raise ValueError("BOOTSTRAP_ADMIN_PASSWORD must be set in the environment to create the bootstrap Admin user.")

        admin_role = roles[settings.BOOTSTRAP_ADMIN_ROLE_NAME]
        admin_user = session.query(User).filter_by(username=settings.BOOTSTRAP_ADMIN_USERNAME).one_or_none()
        if not admin_user:
            admin_user = User(
                username=settings.BOOTSTRAP_ADMIN_USERNAME,
                password_hash=hash_password(settings.BOOTSTRAP_ADMIN_PASSWORD),
                full_name=settings.BOOTSTRAP_ADMIN_FULL_NAME,
                role=admin_role,
                is_active=True,
            )
            session.add(admin_user)
        else:
            admin_user.role = admin_role
            if not admin_user.password_hash.startswith("$2b$"):
                admin_user.password_hash = hash_password(settings.BOOTSTRAP_ADMIN_PASSWORD)

        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise


if __name__ == "__main__":
    seed_auth_data()
