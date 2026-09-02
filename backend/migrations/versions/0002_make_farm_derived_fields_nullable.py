"""Make Farm derived fields nullable pending FARM-004 computation."""

from alembic import op
import sqlalchemy as sa


revision = "0002_farm_derived_nullable"
down_revision = "0001_initial_core_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("farms", "area_hectares", existing_type=sa.Numeric(12, 4), nullable=True)
    op.alter_column("farms", "eudr_risk_flag", existing_type=sa.Boolean(), nullable=True)


def downgrade() -> None:
    op.alter_column("farms", "eudr_risk_flag", existing_type=sa.Boolean(), nullable=False)
    op.alter_column("farms", "area_hectares", existing_type=sa.Numeric(12, 4), nullable=False)
