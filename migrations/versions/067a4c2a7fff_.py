"""empty message

Revision ID: 067a4c2a7fff
Revises: b0ced5e0efc6
Create Date: 2020-05-06 14:30:26.443537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '067a4c2a7fff'
down_revision = 'b0ced5e0efc6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student', sa.Column('code', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('student', 'code')
    # ### end Alembic commands ###
