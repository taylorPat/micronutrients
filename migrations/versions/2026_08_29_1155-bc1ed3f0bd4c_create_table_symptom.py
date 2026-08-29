"""create table symptom

Revision ID: bc1ed3f0bd4c
Revises: 44c0c7435087
Create Date: 2026-08-29 11:55:16.249641

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "bc1ed3f0bd4c"
down_revision: Union[str, Sequence[str], None] = "44c0c7435087"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "symptom",
        sa.Column("id", sa.UUID, primary_key=True, nullable=False),
        sa.Column("name", sa.VARCHAR(50), nullable=False),
        sa.Column(
            "category",
            postgresql.ENUM(
                "inner", "outer", name="symptom_category", create_type=False
            ),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("symptom")
