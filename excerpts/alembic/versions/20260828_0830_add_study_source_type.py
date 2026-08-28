"""add study source type

Revision ID: 15f595230a62
Revises: 985de57c8200
Create Date: 2026-08-28 08:30:47.053962

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "15f595230a62"
down_revision: Union[str, Sequence[str], None] = "985de57c8200"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE source_type ADD VALUE 'study'")


def downgrade() -> None:
    # Reassign rows that use `study`.
    op.execute("UPDATE sources SET type = 'essay' WHERE type = 'study'")

    # Swap `source_type` TYPE for a version without `study`.
    op.execute("ALTER TYPE source_type RENAME TO source_type_old")

    # Recreate `source_type` enum without `study`.
    sa.Enum("article", "book", "essay", "podcast", "video", name="source_type").create(bind=op.get_bind())

    # Assign "new" type to `sources.type` and drop _old type.
    op.execute("ALTER TABLE sources ALTER COLUMN type TYPE source_type USING type::text::source_type")
    sa.Enum(name="source_type_old").drop(bind=op.get_bind())
