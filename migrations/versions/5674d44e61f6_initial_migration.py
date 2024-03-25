"""Initial migration.

Revision ID: 5674d44e61f6
Revises: 
Create Date: 2024-03-25 21:59:50.459362

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5674d44e61f6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authors',
    sa.Column('id_author', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('nationality', sa.String(length=255), nullable=False),
    sa.Column('year_birth', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id_author')
    )
    op.create_table('categories',
    sa.Column('id_category', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id_category')
    )
    op.create_table('users',
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('user_type', sa.String(length=255), nullable=False),
    sa.CheckConstraint("user_type IN ('admin', 'member')", name='user_type_check'),
    sa.PrimaryKeyConstraint('id_user')
    )
    op.create_table('books',
    sa.Column('id_book', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('total_pages', sa.Integer(), nullable=False),
    sa.Column('id_category', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_category'], ['categories.id_category'], ),
    sa.PrimaryKeyConstraint('id_book')
    )
    op.create_table('transactions',
    sa.Column('id_transaction', sa.Integer(), nullable=False),
    sa.Column('id_admin', sa.Integer(), nullable=False),
    sa.Column('id_member', sa.Integer(), nullable=False),
    sa.Column('borrowing_date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['id_admin'], ['users.id_user'], ),
    sa.ForeignKeyConstraint(['id_member'], ['users.id_user'], ),
    sa.PrimaryKeyConstraint('id_transaction')
    )
    op.create_table('book_authors',
    sa.Column('id_book_author', sa.Integer(), nullable=False),
    sa.Column('id_book', sa.Integer(), nullable=False),
    sa.Column('id_author', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_author'], ['authors.id_author'], ),
    sa.ForeignKeyConstraint(['id_book'], ['books.id_book'], ),
    sa.PrimaryKeyConstraint('id_book_author')
    )
    op.create_table('transaction_details',
    sa.Column('id_transaction_detail', sa.Integer(), nullable=False),
    sa.Column('id_transaction', sa.Integer(), nullable=False),
    sa.Column('id_book', sa.Integer(), nullable=False),
    sa.Column('return_date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['id_book'], ['books.id_book'], ),
    sa.ForeignKeyConstraint(['id_transaction'], ['transactions.id_transaction'], ),
    sa.PrimaryKeyConstraint('id_transaction_detail')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction_details')
    op.drop_table('book_authors')
    op.drop_table('transactions')
    op.drop_table('books')
    op.drop_table('users')
    op.drop_table('categories')
    op.drop_table('authors')
    # ### end Alembic commands ###
