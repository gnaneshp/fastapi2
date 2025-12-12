"""create votes table

Revision ID: a44e665c38f5
Revises: 2fe128dfd7c4
Create Date: 2025-12-12 16:23:06.801020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a44e665c38f5'
down_revision: Union[str, Sequence[str], None] = '2fe128dfd7c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("votes",sa.Column("post_id",sa.INTEGER,sa.ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
                    ,sa.Column("user_id",sa.INTEGER,sa.ForeignKey("users.id",ondelete="CASCADE"),primary_key=True))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("votes")
    pass
