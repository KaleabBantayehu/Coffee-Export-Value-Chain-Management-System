from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


role_permission_table = Table(
    "role_permission",
    Base.metadata,
    Column("role_id", ForeignKey("roles.role_id"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.permission_id"), primary_key=True),
)


class Role(Base):
    __tablename__ = "roles"

    role_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role_name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(256), nullable=True)

    permissions: Mapped[list["Permission"]] = relationship(
        "Permission",
        secondary=role_permission_table,
        back_populates="roles",
    )
    users: Mapped[list["User"]] = relationship("User", back_populates="role")


class Permission(Base):
    __tablename__ = "permissions"

    permission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    permission_code: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(256), nullable=True)

    roles: Mapped[list[Role]] = relationship(
        "Role",
        secondary=role_permission_table,
        back_populates="permissions",
    )


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    full_name: Mapped[str] = mapped_column(String(256), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.role_id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    role: Mapped[Role] = relationship("Role", back_populates="users")
