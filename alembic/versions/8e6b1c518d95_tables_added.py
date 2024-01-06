"""Tables added

Revision ID: 8e6b1c518d95
Revises: f53a40baa390
Create Date: 2024-01-06 20:58:36.014996

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e6b1c518d95'
down_revision: Union[str, None] = 'f53a40baa390'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('auther', sa.Column('created_At', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.add_column('publisher', sa.Column('created_At', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('publisher', 'created_At')
    op.drop_column('auther', 'created_At')
    # ### end Alembic commands ###
