"""added user and  url model

Revision ID: 82eb8ca530e2
Revises: 
Create Date: 2024-03-11 04:22:24.389846

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82eb8ca530e2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_first_name'), 'users', ['first_name'], unique=False)
    op.create_index(op.f('ix_users_last_name'), 'users', ['last_name'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('urls',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('qrcode', sa.String(), nullable=True),
    sa.Column('short_url', sa.String(), nullable=True),
    sa.Column('custom_alias', sa.String(), nullable=True),
    sa.Column('original_url', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('clicks', sa.Integer(), nullable=True),
    sa.Column('click_location', sa.String(), nullable=True),
    sa.Column('date_time_created', sa.DateTime(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_urls_custom_alias'), 'urls', ['custom_alias'], unique=True)
    op.create_index(op.f('ix_urls_original_url'), 'urls', ['original_url'], unique=False)
    op.create_index(op.f('ix_urls_short_url'), 'urls', ['short_url'], unique=True)
    op.create_index(op.f('ix_urls_title'), 'urls', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_urls_title'), table_name='urls')
    op.drop_index(op.f('ix_urls_short_url'), table_name='urls')
    op.drop_index(op.f('ix_urls_original_url'), table_name='urls')
    op.drop_index(op.f('ix_urls_custom_alias'), table_name='urls')
    op.drop_table('urls')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_last_name'), table_name='users')
    op.drop_index(op.f('ix_users_first_name'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
