"""create table vitamin

Revision ID: b5bef7f06d8a
Revises: a8439740f0b7
Create Date: 2026-08-29 23:41:36.255883

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'b5bef7f06d8a'
down_revision: Union[str, Sequence[str], None] = 'a8439740f0b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    vitamin_group =  postgresql.ENUM("A", "B", "C", "D", "E", "K", name="vitamin_group", create_type=False)
    op.create_table(
        "vitamin",
        sa.Column("micronutrient_id", sa.UUID, nullable=False),
        sa.Column("vitamin_group", vitamin_group, nullable=False),

        sa.PrimaryKeyConstraint("micronutrient_id", name="pk__vitamin"),
        sa.ForeignKeyConstraint(["micronutrient_id"], ["micronutrient.id"], name="fk__vitamin__micronutrient_id_micronutrient")    
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("vitamin")
