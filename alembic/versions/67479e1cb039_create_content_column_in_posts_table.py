"""create content column in  posts table

Revision ID: 67479e1cb039
Revises: 9b73745e8a36
Create Date: 2023-11-23 12:09:50.922569

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67479e1cb039'
down_revision: Union[str, None] = '9b73745e8a36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column('content_new',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column("posts","content")
    pass
