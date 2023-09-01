"""empty message

Revision ID: 564306a16cdf
Revises:
Create Date: 2023-09-01 15:28:55.719658

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '564306a16cdf'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        'users', sa.Column('username', sa.String(length=150), nullable=False),
        sa.Column('password', sa.String(length=200), nullable=False),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_request', sa.DateTime(timezone=True), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('username'))
    op.create_table(
        'posts', sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('created_at',
                  sa.DateTime(timezone=True),
                  server_default=sa.text('now()'),
                  nullable=False), sa.Column('id',
                                             sa.Integer(),
                                             nullable=False),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
        ), sa.PrimaryKeyConstraint('id'))
    op.create_index(op.f('ix_posts_user_id'),
                    'posts', ['user_id'],
                    unique=False)
    op.create_table(
        'post_likes', sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('created_at',
                  sa.DateTime(timezone=True),
                  server_default=sa.text('now()'),
                  nullable=False), sa.Column('id',
                                             sa.Integer(),
                                             nullable=False),
        sa.ForeignKeyConstraint(
            ['post_id'],
            ['posts.id'],
        ), sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
        ), sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'post_id'))
    op.create_index(op.f('ix_post_likes_post_id'),
                    'post_likes', ['post_id'],
                    unique=False)
    op.create_index(op.f('ix_post_likes_user_id'),
                    'post_likes', ['user_id'],
                    unique=False)


def downgrade() -> None:

    op.drop_index(op.f('ix_post_likes_user_id'), table_name='post_likes')
    op.drop_index(op.f('ix_post_likes_post_id'), table_name='post_likes')
    op.drop_table('post_likes')
    op.drop_index(op.f('ix_posts_user_id'), table_name='posts')
    op.drop_table('posts')
    op.drop_table('users')
