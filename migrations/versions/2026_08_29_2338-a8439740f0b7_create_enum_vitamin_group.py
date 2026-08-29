"""create type vitamin group

Revision ID: a8439740f0b7
Revises: 7733e703c21e
Create Date: 2026-08-29 23:38:05.227440

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8439740f0b7'
down_revision: Union[str, Sequence[str], None] = '7733e703c21e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE TYPE vitamin_group AS ENUM ('A', 'B', 'C', 'D', 'E', 'K')")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TYPE vitamin_group")
