"""Create user table

Revision ID: 99bc7120ea61
Revises: f4dc7849fb4e
Create Date: 2022-04-25 13:39:18.284979

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99bc7120ea61'
down_revision = 'f4dc7849fb4e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                  server_default=sa.sql.expression.text("now()"))
    )


def downgrade():
    op.drop_table('users')
