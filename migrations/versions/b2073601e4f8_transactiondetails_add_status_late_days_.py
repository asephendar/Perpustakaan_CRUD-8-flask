"""TransactionDetails add status_late & days_late

Revision ID: b2073601e4f8
Revises: 35dfabdef078
Create Date: 2024-03-28 09:42:24.804631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2073601e4f8'
down_revision = '35dfabdef078'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction_details', schema=None) as batch_op:
        batch_op.add_column(sa.Column('days_late', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('status_late', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction_details', schema=None) as batch_op:
        batch_op.drop_column('status_late')
        batch_op.drop_column('days_late')

    # ### end Alembic commands ###