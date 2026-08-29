"""create enum nutrient unit

Revision ID: 18588a8ff2bc
Revises: bc1ed3f0bd4c
Create Date: 2026-08-29 12:27:37.698344

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "18588a8ff2bc"
down_revision: Union[str, Sequence[str], None] = "bc1ed3f0bd4c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE TYPE nutrient_unit AS ENUM ('mg', 'ug', 'g')")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TYPE nutrient_unit")
