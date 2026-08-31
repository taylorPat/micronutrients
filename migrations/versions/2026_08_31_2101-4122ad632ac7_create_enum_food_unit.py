"""create enum food unit

Revision ID: 4122ad632ac7
Revises: 526f7bf7bf4e
Create Date: 2026-08-31 21:01:42.320006

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4122ad632ac7'
down_revision: Union[str, Sequence[str], None] = '526f7bf7bf4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE TYPE food_unit AS ENUM ('g', 'kg', 'ml', 'l', 'piece', 'portion')")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TYPE food_unit")
