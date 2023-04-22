"""add post table

Revision ID: 80eed3d3b729
Revises: 477ffa69061c
Create Date: 2023-04-22 16:45:45.142658

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80eed3d3b729'
down_revision = '477ffa69061c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts_sql',
                    sa.Column('id', sa.Integer(),nullable=False,index=True),
                    sa.Column('title', sa.String(),nullable=False),
                    sa.Column('content', sa.String(),nullable=False),
                    sa.Column('published', sa.String(),nullable=False,server_default='TRUE'),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    
    )
    pass


def downgrade() -> None:
    op.drop_table('posts_sql')
    pass
