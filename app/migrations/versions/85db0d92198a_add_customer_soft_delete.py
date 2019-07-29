"""Add Customer soft delete

Revision ID: 85db0d92198a
Revises: 5037b3bfae4b
Create Date: 2019-07-28 06:32:51.851231

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85db0d92198a'
down_revision = '5037b3bfae4b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('is_deleted', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix_customer_is_deleted'), 'customer', ['is_deleted'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_customer_is_deleted'), table_name='customer')
    op.drop_column('customer', 'is_deleted')
    # ### end Alembic commands ###
