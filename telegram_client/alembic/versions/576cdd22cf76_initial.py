"""Initial

Revision ID: 576cdd22cf76
Revises: 
Create Date: 2024-04-12 01:22:00.693862

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '576cdd22cf76'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('telegramuser',
    sa.Column('username', sa.String(length=25), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.Column('tg_user_id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=256), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('telegramuser')
    # ### end Alembic commands ###
