"""create posts table

Revision ID: 2fe128dfd7c4
Revises: 79c43f2f8fde
Create Date: 2025-12-12 16:21:57.033200

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2fe128dfd7c4'
down_revision: Union[str, Sequence[str], None] = '79c43f2f8fde'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("posts",sa.Column("id",sa.INTEGER,primary_key=True, nullable=False),
                    sa.Column("title",sa.VARCHAR(50), nullable=False),
                    sa.Column("content",sa.VARCHAR(100), nullable=False),
                    sa.Column("published",sa.BOOLEAN, nullable=False,server_default="TRUE"),
                    sa.Column("created_at",sa.TIMESTAMP(timezone=True), nullable=False,server_default=sa.text("NOW()")),
                    sa.Column("owner_id", sa.INTEGER, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

                     )    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("posts")
    pass
