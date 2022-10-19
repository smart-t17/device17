# type: ignore
""" remove devices and leave only points

Revision ID: 33d0b93fd652
Revises: 1268589f2c36
Create Date: 2020-04-23 22:56:39.189821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "33d0b93fd652"
down_revision = "1268589f2c36"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("UPDATE history set point_id = device_id")
    op.create_unique_constraint(
        op.f("uq_history_point_id"), "history", ["point_id", "ts"]
    )
    op.drop_index("ix_history_device_id", table_name="history")
    op.drop_constraint("uq_history_device_id", "history", type_="unique")
    op.drop_column("history", "device_id")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "history",
        sa.Column(
            "device_id", sa.VARCHAR(length=255), autoincrement=False, nullable=False
        ),
    )
    op.create_unique_constraint("uq_history_device_id", "history", ["device_id", "ts"])
    op.create_index("ix_history_device_id", "history", ["device_id"], unique=False)
    op.drop_constraint(op.f("uq_history_point_id"), "history", type_="unique")
    # ### end Alembic commands ###
