"""empty message

Revision ID: 843d74267808
Revises: d39988708544
Create Date: 2019-03-05 11:03:48.123489

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '843d74267808'
down_revision = 'd39988708544'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('emerging_fact',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('fact', sa.String(), nullable=True),
    sa.Column('fact_type', sa.String(), nullable=True),
    sa.Column('notes', sa.String(), nullable=True),
    sa.Column('emerging_plan_document_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['emerging_plan_document_id'], ['emerging_plan_document.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('fact', 'number')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fact', sa.Column('number', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_table('emerging_fact')
    # ### end Alembic commands ###