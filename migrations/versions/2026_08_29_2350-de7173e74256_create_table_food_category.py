"""create table food category

Revision ID: de7173e74256
Revises: b5bef7f06d8a
Create Date: 2026-08-29 23:50:12.008244

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de7173e74256'
down_revision: Union[str, Sequence[str], None] = 'b5bef7f06d8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "food_category",
        sa.Column("name", sa.String(50),nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("name", name="pk__food_category")    
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("food_category")
