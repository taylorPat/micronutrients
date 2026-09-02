"""create table food

Revision ID: 526f7bf7bf4e
Revises: de7173e74256
Create Date: 2026-08-29 23:54:46.625383

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '526f7bf7bf4e'
down_revision: Union[str, Sequence[str], None] = 'de7173e74256'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "food",
        sa.Column("id", sa.UUID, nullable=False),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("food_category_name", sa.String(50), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk__food"),
        sa.ForeignKeyConstraint(["food_category_name"], ["food_category.name"], name="fk__food__name__food_category")    
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("food")
