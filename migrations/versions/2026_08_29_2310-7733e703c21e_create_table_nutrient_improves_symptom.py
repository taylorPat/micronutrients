"""create table nutrient improves system

Revision ID: 7733e703c21e
Revises: baf7c8b37036
Create Date: 2026-08-29 23:10:46.840551

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7733e703c21e'
down_revision: Union[str, Sequence[str], None] = 'baf7c8b37036'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
    "nutrient_improves_symptom",
    sa.Column("micronutrient_id", sa.UUID, nullable=False),
    sa.Column("symptom_id", sa.UUID, nullable=False),        
    sa.PrimaryKeyConstraint("micronutrient_id", "symptom_id", name="pk__symptom__micronutrient"),
    sa.ForeignKeyConstraint(["micronutrient_id"], ["micronutrient.id"], name="fk__nutrient_symptom__micronutrient_id__micronutrient"),
    sa.ForeignKeyConstraint(["symptom_id"], ["symptom.id"], name="fk__nutrient_symptom__symptom_id__symptom")
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(constraint_name="fk__nutrient_symptom__micronutrient_id__micronutrient", table_name="nutrient_improves_symptom")
    op.drop_constraint(constraint_name="fk__nutrient_symptom__symptom_id__symptom", table_name="nutrient_improves_symptom")
    op.drop_constraint(constraint_name="pk__symptom__micronutrient", table_name="nutrient_improves_symptom")
    op.drop_table("nutrient_improves_symptom")
