"""Create the CEVCMS V1.0 core schema."""

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry


revision = "0001_initial_core_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("roles", sa.Column("role_id", sa.Integer(), primary_key=True), sa.Column("role_name", sa.String(128), nullable=False, unique=True), sa.Column("description", sa.String(256)))
    op.create_table("permissions", sa.Column("permission_id", sa.Integer(), primary_key=True), sa.Column("permission_code", sa.String(128), nullable=False, unique=True), sa.Column("description", sa.String(256)))
    op.create_table("role_permission", sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.role_id"), primary_key=True), sa.Column("permission_id", sa.Integer(), sa.ForeignKey("permissions.permission_id"), primary_key=True))
    op.create_table("users", sa.Column("user_id", sa.Integer(), primary_key=True), sa.Column("username", sa.String(128), nullable=False, unique=True), sa.Column("password_hash", sa.String(256), nullable=False), sa.Column("full_name", sa.String(256), nullable=False), sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.role_id"), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_table("cooperatives", sa.Column("cooperative_id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(256), nullable=False, unique=True), sa.Column("region", sa.String(128), nullable=False))
    op.create_table("farmers", sa.Column("farmer_id", sa.Integer(), primary_key=True), sa.Column("fin_code", sa.String(128), nullable=False, unique=True), sa.Column("full_name", sa.String(256), nullable=False), sa.Column("national_id", sa.String(128), nullable=False, unique=True), sa.Column("gender", sa.String(32)), sa.Column("phone_number", sa.String(64)), sa.Column("cooperative_id", sa.Integer(), sa.ForeignKey("cooperatives.cooperative_id")), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_table("farms", sa.Column("farm_id", sa.Integer(), primary_key=True), sa.Column("farmer_id", sa.Integer(), sa.ForeignKey("farmers.farmer_id"), nullable=False), sa.Column("polygon_geom", Geometry("POLYGON", srid=4326, spatial_index=False), nullable=False), sa.Column("area_hectares", sa.Numeric(12, 4), nullable=False), sa.Column("eudr_risk_flag", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_table("coffee_lots", sa.Column("lot_id", sa.Integer(), primary_key=True), sa.Column("gin_code", sa.String(128), nullable=False, unique=True), sa.Column("farm_id", sa.Integer(), sa.ForeignKey("farms.farm_id"), nullable=False), sa.Column("created_by", sa.Integer(), sa.ForeignKey("users.user_id"), nullable=False), sa.Column("status", sa.String(64), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_table("traceability_events", sa.Column("event_id", sa.Integer(), primary_key=True), sa.Column("lot_id", sa.Integer(), sa.ForeignKey("coffee_lots.lot_id"), nullable=False), sa.Column("event_type", sa.String(128), nullable=False), sa.Column("event_timestamp", sa.DateTime(), nullable=False), sa.Column("recorded_by", sa.Integer(), sa.ForeignKey("users.user_id"), nullable=False), sa.Column("notes", sa.Text()))
    op.create_table("qr_records", sa.Column("qr_id", sa.Integer(), primary_key=True), sa.Column("lot_id", sa.Integer(), sa.ForeignKey("coffee_lots.lot_id"), nullable=False), sa.Column("payload_hash", sa.String(256), nullable=False), sa.Column("hmac_signature", sa.String(256), nullable=False), sa.Column("verification_url", sa.String(512), nullable=False), sa.Column("generated_at", sa.DateTime(), nullable=False))
    op.create_table("audit_logs", sa.Column("audit_id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.user_id"), nullable=False), sa.Column("action", sa.String(128), nullable=False), sa.Column("entity_type", sa.String(128), nullable=False), sa.Column("entity_id", sa.Integer(), nullable=False), sa.Column("old_value", sa.Text()), sa.Column("new_value", sa.Text()), sa.Column("timestamp", sa.DateTime(), nullable=False))


def downgrade() -> None:
    for table_name in ("audit_logs", "qr_records", "traceability_events", "coffee_lots", "farms", "farmers", "cooperatives", "users", "role_permission", "permissions", "roles"):
        op.drop_table(table_name)
