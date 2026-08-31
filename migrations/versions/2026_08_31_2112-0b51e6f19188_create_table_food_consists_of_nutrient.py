"""create table food consists of nutrient

Revision ID: 0b51e6f19188
Revises: 4122ad632ac7
Create Date: 2026-08-31 21:12:27.043484

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '0b51e6f19188'
down_revision: Union[str, Sequence[str], None] = '4122ad632ac7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    food_unit = postgresql.ENUM('g', 'kg', 'ml', 'l', 'piece', 'portion', name="food_unit", create_type=False)
    nutrient_unit = postgresql.ENUM(
        "mg", "ug", "g", name="nutrient_unit", create_type=False
    )
    op.create_table(
        "food_consists_of_nutrient",
        sa.Column("food_id", sa.UUID, nullable=False),
        sa.Column("micronutrient_id", sa.UUID, nullable=False),
        sa.Column("nutrient_amount", sa.DECIMAL(10,3), nullable=False),
        sa.Column("nutrient_unit", nutrient_unit, nullable=False),
        sa.Column("food_amount", sa.DECIMAL(10,3), nullable=False),
        sa.Column("food_unit", food_unit, nullable=False),
        sa.PrimaryKeyConstraint("food_id", "micronutrient_id", name="pk__food_nutrient"),
        sa.ForeignKeyConstraint(["food_id"], ["food.id"], name="fk__food_nutrient_food_id__food"),
        sa.ForeignKeyConstraint(["micronutrient_id"], ["micronutrient.id"], name="fk__food_nutrient__micronutrient_id__micronutrient"),
        sa.CheckConstraint("nutrient_amount > 0 AND food_amount > 0")
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("food_consists_of_nutrient")
