"""create posts table

Revision ID: 9b73745e8a36
Revises: 
Create Date: 2023-11-23 11:48:38.864221

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b73745e8a36'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table
    ('posts',                                                      # Name of Table
    sa.Column('id',sa.Integer(),nullable=False,primary_key=True),  # create one new column
    sa.Column('title',sa.String(),nullable=False)                  # create second column
    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
