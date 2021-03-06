"""empty message

Revision ID: 8ab300e5003d
Revises: dc9ee7b1894b
Create Date: 2020-05-04 14:08:44.592072

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ab300e5003d'
down_revision = 'dc9ee7b1894b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cms_operation',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('desc', sa.String(length=200), nullable=True),
    sa.Column('operation_time', sa.DateTime(), nullable=True),
    sa.Column('adm_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['adm_id'], ['cms_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cms_operation')
    # ### end Alembic commands ###
