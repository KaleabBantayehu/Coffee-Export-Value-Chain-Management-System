from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, Table, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from geoalchemy2 import Geometry


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
    audit_logs: Mapped[list["AuditLog"]] = relationship("AuditLog", back_populates="user")


class Cooperative(Base):
    __tablename__ = "cooperatives"

    cooperative_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    region: Mapped[str] = mapped_column(String(128), nullable=False)


class Farmer(Base):
    __tablename__ = "farmers"

    farmer_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fin_code: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(256), nullable=False)
    national_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    gender: Mapped[str | None] = mapped_column(String(32), nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String(64), nullable=True)
    cooperative_id: Mapped[int | None] = mapped_column(ForeignKey("cooperatives.cooperative_id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    farms: Mapped[list["Farm"]] = relationship("Farm", back_populates="farmer")


class Farm(Base):
    __tablename__ = "farms"

    farm_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    farmer_id: Mapped[int] = mapped_column(ForeignKey("farmers.farmer_id"), nullable=False)
    polygon_geom: Mapped[object] = mapped_column(Geometry("POLYGON", srid=4326, spatial_index=False), nullable=False)
    area_hectares: Mapped[float | None] = mapped_column(Numeric(12, 4), nullable=True)
    eudr_risk_flag: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    farmer: Mapped[Farmer] = relationship("Farmer", back_populates="farms")


class CoffeeLot(Base):
    __tablename__ = "coffee_lots"

    lot_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gin_code: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    farm_id: Mapped[int] = mapped_column(ForeignKey("farms.farm_id"), nullable=False)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    status: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class TraceabilityEvent(Base):
    __tablename__ = "traceability_events"

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey("coffee_lots.lot_id"), nullable=False)
    event_type: Mapped[str] = mapped_column(String(128), nullable=False)
    event_timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    recorded_by: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class QRRecord(Base):
    __tablename__ = "qr_records"

    qr_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey("coffee_lots.lot_id"), nullable=False)
    payload_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    hmac_signature: Mapped[str] = mapped_column(String(256), nullable=False)
    verification_url: Mapped[str] = mapped_column(String(512), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    audit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    action: Mapped[str] = mapped_column(String(128), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(128), nullable=False)
    entity_id: Mapped[int] = mapped_column(Integer, nullable=False)
    old_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    new_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped[User] = relationship("User", back_populates="audit_logs")
