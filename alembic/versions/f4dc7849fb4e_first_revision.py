"""first revision

Revision ID: f4dc7849fb4e
Revises: 
Create Date: 2022-04-24 23:11:42.310734

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision = 'f4dc7849fb4e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('published', sa.Boolean(), nullable=False, server_default="True"),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")),
    )


def downgrade():
    op.drop_table('posts')
