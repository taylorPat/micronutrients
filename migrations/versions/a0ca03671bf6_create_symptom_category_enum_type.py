"""create symptom_category enum type

Revision ID: a0ca03671bf6
Revises: 
Create Date: 2026-08-23 21:54:52.993133

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a0ca03671bf6'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE TYPE symptom_category AS ENUM ('outer', 'inner')")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TYPE symptom_category")
