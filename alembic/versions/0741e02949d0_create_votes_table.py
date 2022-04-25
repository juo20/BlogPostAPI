"""Create votes table

Revision ID: 0741e02949d0
Revises: 99bc7120ea61
Create Date: 2022-04-25 13:42:59.749641

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0741e02949d0'
down_revision = '99bc7120ea61'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'votes',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column('post_id', sa.Integer(), sa.ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    )


def downgrade():
    op.drop_table('votes')
