"""create table micronutrient

Revision ID: baf7c8b37036
Revises: 18588a8ff2bc
Create Date: 2026-08-29 12:30:30.485090

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "baf7c8b37036"
down_revision: Union[str, Sequence[str], None] = "18588a8ff2bc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    nutrient_unit = postgresql.ENUM(
        "mg", "ug", "g", name="nutrient_unit", create_type=False
    )
    op.create_table(
        "micronutrient",
        sa.Column("id", sa.UUID, primary_key=True, nullable=False),
        sa.Column("name", sa.VARCHAR(50), nullable=False, unique=True),
        sa.Column("recommended_daily_amount", sa.DECIMAL(precision=10, scale=3)),
        sa.Column("unit", nutrient_unit, nullable=False),
        sa.CheckConstraint("""
            (recommended_daily_amount IS NULL AND unit IS NULL)
            OR
            (
                recommended_daily_amount IS NOT NULL
                AND recommended_daily_amount > 0
                AND unit IS NOT NULL
            )
        """),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("micronutrient")
