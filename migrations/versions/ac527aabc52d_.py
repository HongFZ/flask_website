"""empty message

Revision ID: ac527aabc52d
Revises: 8ab300e5003d
Create Date: 2020-05-06 10:58:35.031469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac527aabc52d'
down_revision = '8ab300e5003d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('cleaned_text', sa.Text(), nullable=True))
    op.add_column('comment', sa.Column('keyword', sa.Text(), nullable=True))
    op.add_column('comment', sa.Column('sentiment', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comment', 'sentiment')
    op.drop_column('comment', 'keyword')
    op.drop_column('comment', 'cleaned_text')
    # ### end Alembic commands ###
