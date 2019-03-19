"""empty message

Revision ID: 95d57b76c8c0
Revises: e1e8404ef481
Create Date: 2019-03-19 11:49:15.466861

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '95d57b76c8c0'
down_revision = 'e1e8404ef481'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('emerging_fact')
    op.drop_table('fact_old')
    op.drop_table('emerging_plan_document')
    op.drop_table('plan_document_old')
    op.add_column('fact', sa.Column('from_', sa.String(), nullable=True))
    op.add_column('fact', sa.Column('to', sa.String(), nullable=True))
    op.drop_column('local_plan', 'states')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('local_plan', sa.Column('states', postgresql.ARRAY(sa.VARCHAR()), server_default=sa.text("'{}'::character varying[]"), autoincrement=False, nullable=True))
    op.drop_column('fact', 'to')
    op.drop_column('fact', 'from_')
    op.create_table('emerging_fact',
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('fact', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('fact_type', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('notes', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('emerging_plan_document_id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('created_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('image_url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['emerging_plan_document_id'], ['emerging_plan_document.id'], name='emerging_fact_emerging_plan_document_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='emerging_fact_pkey')
    )
    op.create_table('plan_document_old',
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('plan_document_type', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('local_plan_id', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['local_plan_id'], ['local_plan.local_plan'], name='plan_document_local_plan_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='plan_document_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('fact_old',
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('notes', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('plan_document_id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('fact', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('fact_type', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('created_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('image_url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['plan_document_id'], ['plan_document_old.id'], name='fact_plan_document_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='fact_pkey')
    )
    op.create_table('emerging_plan_document',
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('planning_authority_id', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['planning_authority_id'], ['planning_authority.id'], name='emerging_plan_document_planning_authority_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='emerging_plan_document_pkey')
    )
    # ### end Alembic commands ###