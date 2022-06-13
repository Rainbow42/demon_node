"""empty message

Revision ID: 6e5d5222432c
Revises: 7711fb984b48
Create Date: 2022-06-12 22:06:47.724122

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6e5d5222432c'
down_revision = '7711fb984b48'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transporter_repositories',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('transporter_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('repositories_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['repositories_id'], ['repositories.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['transporter_id'], ['transporter.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_unique_constraint(None, 'merge_request', ['id'])
    op.create_unique_constraint(None, 'pipline_merge_requests', ['id'])
    op.alter_column('repositories_token', 'id',
               existing_type=postgresql.UUID(),
               existing_nullable=False,
               autoincrement=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('repositories_token', 'id',
               existing_type=sa.Integer(),
               type_=postgresql.UUID(),
               existing_nullable=False,
               autoincrement=True)
    op.drop_constraint(None, 'pipline_merge_requests', type_='unique')
    op.alter_column('pipline_merge_requests', 'status',
               existing_type=sa.Enum('FAILED', 'DONE', 'PROGRESS', 'FUTURE', name='statusstagetransporter'),
               type_=sa.VARCHAR(),
               nullable=False,
               existing_server_default=sa.text("'FUTURE'::character varying"))
    op.drop_constraint(None, 'merge_request', type_='unique')
    op.drop_table('transporter_repositories')
    # ### end Alembic commands ###
