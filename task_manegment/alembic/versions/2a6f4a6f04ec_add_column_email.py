"""add column email

Revision ID: 2a6f4a6f04ec
Revises: 
Create Date: 2025-04-05 14:13:46.472406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a6f4a6f04ec'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("Users",sa.Column('Email',sa.String(40)))


def downgrade() -> None:
    op.drop_column("Users",'Email')
