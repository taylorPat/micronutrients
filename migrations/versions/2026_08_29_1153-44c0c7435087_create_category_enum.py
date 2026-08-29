"""create category enum

Revision ID: 44c0c7435087
Revises:
Create Date: 2026-08-29 11:53:14.401372

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "44c0c7435087"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE TYPE symptom_category AS ENUM ('outer', 'inner')")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TYPE symptom_category")
