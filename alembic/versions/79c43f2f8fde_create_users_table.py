"""create users table

Revision ID: 79c43f2f8fde
Revises: 
Create Date: 2025-12-12 16:17:58.153214

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79c43f2f8fde'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("users",sa.Column("id",sa.INTEGER,primary_key=True, nullable=False),
                    sa.Column("email",sa.VARCHAR(50), nullable=False),
                    sa.Column("password",sa.VARCHAR(100), nullable=False),
                    sa.Column("created_at",sa.TIMESTAMP(timezone=True), nullable=False,server_default=sa.text("NOW()")),
                    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
    pass
