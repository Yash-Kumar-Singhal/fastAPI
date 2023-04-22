"""add foreign key to  post table

Revision ID: 683ddbf5d22f
Revises: 80eed3d3b729
Create Date: 2023-04-22 16:51:31.557728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '683ddbf5d22f'
down_revision = '80eed3d3b729'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts_sql',
                  sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_user_id_fkey', source_table='posts_sql',
                          referent_table='user', local_cols=['user_id'], remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_user_id_fkey',table_name='posts_sql')
    op.drop_column('posts_sql', 'user_id')
    pass
