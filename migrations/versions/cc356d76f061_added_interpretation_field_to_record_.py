"""added interpretation field to record mode

Revision ID: cc356d76f061
Revises: e875ba6cb2ce
Create Date: 2020-03-29 14:05:49.005041

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc356d76f061'
down_revision = 'e875ba6cb2ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lab_result_choice_item', sa.Column('interpretation', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lab_result_choice_item', 'interpretation')
    # ### end Alembic commands ###
