"""add fk to posts table

Revision ID: 5982c3776d5f
Revises: 0741e02949d0
Create Date: 2022-04-25 13:57:38.800214

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5982c3776d5f'
down_revision = '0741e02949d0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    )


def downgrade():
    op.drop_column('posts', 'owner_id')
