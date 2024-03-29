"""removed approve datetime from test record model and added it to the order models

Revision ID: e670d6e99921
Revises: d306f038a381
Create Date: 2023-10-27 00:39:48.566688

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e670d6e99921'
down_revision = 'd306f038a381'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lab_qual_result_records', schema=None) as batch_op:
        batch_op.drop_constraint('lab_qual_result_records_approver_id_fkey', type_='foreignkey')
        batch_op.drop_column('approver_id')

    with op.batch_alter_table('lab_qual_test_orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column('approver_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'user', ['approver_id'], ['id'])

    with op.batch_alter_table('lab_quan_result_records', schema=None) as batch_op:
        batch_op.drop_constraint('lab_quan_result_records_approver_id_fkey', type_='foreignkey')
        batch_op.drop_column('approver_id')
        batch_op.drop_column('approved_at')

    with op.batch_alter_table('lab_quan_test_orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column('approver_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'user', ['approver_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lab_quan_test_orders', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('approver_id')
        batch_op.drop_column('approved_at')

    with op.batch_alter_table('lab_quan_result_records', schema=None) as batch_op:
        batch_op.add_column(sa.Column('approved_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('approver_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('lab_quan_result_records_approver_id_fkey', 'user', ['approver_id'], ['id'])

    with op.batch_alter_table('lab_qual_test_orders', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('approver_id')
        batch_op.drop_column('approved_at')

    with op.batch_alter_table('lab_qual_result_records', schema=None) as batch_op:
        batch_op.add_column(sa.Column('approver_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('lab_qual_result_records_approver_id_fkey', 'user', ['approver_id'], ['id'])

    # ### end Alembic commands ###
