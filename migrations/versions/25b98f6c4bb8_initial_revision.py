"""Initial revision

Revision ID: 25b98f6c4bb8
Revises: 
Create Date: 2021-03-08 02:48:59.123408

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25b98f6c4bb8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'shifts',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('start_time', sa.Text(), nullable=False),
        sa.Column('end_time', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'workers',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('first_name', sa.Text(), nullable=False),
        sa.Column('last_name', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'workers_shifts',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('day', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('worker_id', sa.BigInteger(), nullable=False),
        sa.Column('shift_id', sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(['shift_id'], ['shifts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['worker_id'], ['workers.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('workers_shifts')
    op.drop_table('workers')
    op.drop_table('shifts')
    # ### end Alembic commands ###