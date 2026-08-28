"""Business logic for admin-only user management (EPIC-1-AUTH-005).

Kept framework-agnostic: the service raises domain exceptions and the route
layer (``app/api/v1/users.py``) maps them to structured HTTP responses. This
preserves the layered separation required by ``.agents/rules/03-coding-rules.md``
(API / business-logic / data-access kept distinct) and keeps the logic unit
testable without a live HTTP server.
"""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.models import AuditLog, Role, User


class UserServiceError(Exception):
    """Base class for user-management domain errors."""


class DuplicateUsernameError(UserServiceError):
    """Raised when a requested username already exists."""


class InvalidRoleError(UserServiceError):
    """Raised when a requested role is not one of the seeded roles."""


class UserNotFoundError(UserServiceError):
    """Raised when a targeted user id does not exist."""


# Audit action name for a role change, recorded in AuditLog.action. Kept
# consistent with Design Document §10's "create/update" action vocabulary; the
# Farmer/Farm/Lot audit logging in later epics reuses this same pattern.
ROLE_CHANGE_ACTION = "update_role"


def _get_role_by_name(session: Session, role_name: str) -> Role:
    """Resolve a seeded role by name, or raise :class:`InvalidRoleError`.

    Reads the seeded ``roles`` table rather than hard-coding role-name strings,
    so "one of the four seeded roles" is enforced by the data, consistent with
    the RBAC approach established in AUTH-004.
    """
    role = session.query(Role).filter(Role.role_name == role_name).one_or_none()
    if role is None:
        raise InvalidRoleError(role_name)
    return role


def list_users(session: Session, *, page: int, page_size: int) -> tuple[list[User], int]:
    """Return one page of users (ordered by id) and the total user count."""
    total = session.query(User).count()
    offset = (page - 1) * page_size
    users = session.query(User).order_by(User.user_id).offset(offset).limit(page_size).all()
    return users, total


def create_user(
    session: Session,
    *,
    username: str,
    password: str,
    full_name: str,
    role_name: str,
) -> User:
    """Create a new user with a hashed password.

    Validates the role exists and the username is unique. The plaintext
    password is hashed via AUTH-001's utility before storage and is never
    persisted or returned.
    """
    role = _get_role_by_name(session, role_name)

    existing = session.query(User).filter(User.username == username).one_or_none()
    if existing is not None:
        raise DuplicateUsernameError(username)

    user = User(
        username=username,
        password_hash=hash_password(password),
        full_name=full_name,
        role=role,
        is_active=True,
    )
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        # Fail closed on a concurrent insert that beat the pre-check: surface a
        # structured domain error rather than a raw database exception.
        session.rollback()
        raise DuplicateUsernameError(username) from None

    session.refresh(user)
    return user


def change_user_role(
    session: Session,
    *,
    target_user_id: int,
    new_role_name: str,
    acting_admin_id: int,
) -> User:
    """Change a user's role and write an ``AuditLog`` entry.

    The audit row records the acting admin, the target user, and the old/new
    role names, per Design Document §8 ("Writes an AuditLog entry") and the
    scaled-down old/new-value audit pattern in Design Document §10.
    """
    user = session.query(User).filter(User.user_id == target_user_id).one_or_none()
    if user is None:
        raise UserNotFoundError(target_user_id)

    new_role = _get_role_by_name(session, new_role_name)
    old_role_name = user.role.role_name

    user.role = new_role
    session.add(
        AuditLog(
            user_id=acting_admin_id,
            action=ROLE_CHANGE_ACTION,
            entity_type="User",
            entity_id=user.user_id,
            old_value=old_role_name,
            new_value=new_role.role_name,
        )
    )
    session.commit()
    session.refresh(user)
    return user
