"""empty message

Revision ID: 0b90dc1a4c97
Revises: 9d4664e1c189
Create Date: 2021-06-07 17:24:24.262979

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b90dc1a4c97'
down_revision = '9d4664e1c189'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('points', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fallback_value', sa.Float(), nullable=False, server_default='16'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('points', schema=None) as batch_op:
        batch_op.drop_column('fallback_value')

    # ### end Alembic commands ###
