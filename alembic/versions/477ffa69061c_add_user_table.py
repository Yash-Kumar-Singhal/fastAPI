"""add user table

Revision ID: 477ffa69061c
Revises: 
Create Date: 2023-04-22 16:31:02.068458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '477ffa69061c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('user',
                    sa.Column('id', sa.Integer(),nullable=False,index=True),
                    sa.Column('email', sa.String(),nullable=False),
                    sa.Column('password', sa.String(),nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
    )
    pass


def downgrade() -> None:
    op.drop_table('user')
    pass
