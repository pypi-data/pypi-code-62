"""add_scenes

Revision ID: 119f5f1434f7
Revises: 
Create Date: 2018-07-28 12:12:32.114158

"""

# revision identifiers, used by Alembic.
revision = "119f5f1434f7"
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "scene",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uuid", sa.String(length=64), nullable=True),
        sa.Column("matcher", sa.Text(), nullable=False),
        sa.Column("power", sa.Boolean(), nullable=True),
        sa.Column("color", sa.Text(), nullable=True),
        sa.Column("zones", sa.Text(), nullable=True),
        sa.Column("chain", sa.Text(), nullable=True),
        sa.Column("duration", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_scene_uuid"), "scene", ["uuid"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_scene_uuid"), table_name="scene")
    op.drop_table("scene")
    # ### end Alembic commands ###
