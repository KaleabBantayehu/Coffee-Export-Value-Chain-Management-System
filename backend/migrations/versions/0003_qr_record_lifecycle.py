"""Add active QR lifecycle state."""

from alembic import op
import sqlalchemy as sa

revision = "0003_qr_record_lifecycle"
down_revision = "0002_farm_derived_nullable"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("qr_records", sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()))
    op.create_index("uq_qr_records_active_lot", "qr_records", ["lot_id"], unique=True, postgresql_where=sa.text("is_active"))


def downgrade() -> None:
    op.drop_index("uq_qr_records_active_lot", table_name="qr_records")
    op.drop_column("qr_records", "is_active")
