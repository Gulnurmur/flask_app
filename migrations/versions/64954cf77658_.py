"""empty message

Revision ID: 64954cf77658
Revises: 527108e3aefe
Create Date: 2020-08-07 16:19:39.027837

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '64954cf77658'
down_revision = '527108e3aefe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'post', ['id'])
    op.add_column('user', sa.Column('password', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'user', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'password')
    op.drop_constraint(None, 'post', type_='unique')
    # ### end Alembic commands ###
