"""Tables added

Revision ID: 2c5cab4f9084
Revises: 
Create Date: 2024-01-06 20:38:24.090603

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c5cab4f9084'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('author_id', sa.Integer(), nullable=True))
    op.add_column('books', sa.Column('publisher_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'books', 'auther', ['author_id'], ['id'])
    op.create_foreign_key(None, 'books', 'publisher', ['publisher_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'books', type_='foreignkey')
    op.drop_constraint(None, 'books', type_='foreignkey')
    op.drop_column('books', 'publisher_id')
    op.drop_column('books', 'author_id')
    # ### end Alembic commands ###
