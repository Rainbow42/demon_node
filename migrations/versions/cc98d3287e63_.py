"""empty message

Revision ID: cc98d3287e63
Revises: d899771edb71
Create Date: 2022-06-14 00:26:48.172985

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cc98d3287e63'
down_revision = 'd899771edb71'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'container', ['id'])
    op.create_unique_constraint(None, 'container_pipline_merge_requests', ['id'])
    op.add_column('pipline_merge_requests', sa.Column('mr_id', sa.Integer(), nullable=True))
    op.alter_column('pipline_merge_requests', 'stage_transporter_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.create_foreign_key(None, 'pipline_merge_requests', 'merge_request', ['mr_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'pipline_merge_requests', type_='foreignkey')
    op.alter_column('pipline_merge_requests', 'status',
               existing_type=sa.Enum('FAILED', 'DONE', 'PROGRESS', 'FUTURE', name='statusstagetransporter'),
               type_=sa.VARCHAR(),
               nullable=False,
               existing_server_default=sa.text("'FUTURE'::character varying"))
    op.alter_column('pipline_merge_requests', 'stage_transporter_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.drop_column('pipline_merge_requests', 'mr_id')
    op.drop_constraint(None, 'container_pipline_merge_requests', type_='unique')
    op.drop_constraint(None, 'container', type_='unique')
    # ### end Alembic commands ###