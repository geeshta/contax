"""Modify contact model to have just one name field

Revision ID: 284b734c33bc
Revises: d362b4da417e
Create Date: 2023-09-21 14:24:34.900151

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "284b734c33bc"
down_revision: Union[str, None] = "d362b4da417e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("contact") as batch_op:
        batch_op.alter_column("first_name", new_column_name="name")
        batch_op.alter_column("phone_number", nullable=True)
        batch_op.alter_column("email", nullable=True)
        batch_op.drop_column("last_name")

    # ### end Alembic commands ###


def downgrade() -> None:
    with op.batch_alter_table("contact") as batch_op:
        batch_op.alter_column("name", new_column_name="first_name")
        batch_op.add_column(sa.Column("last_name", sa.VARCHAR(), nullable=False))
        batch_op.alter_column("email", nullable=False)
        batch_op.alter_column("phone_number", nullable=False)

    # ### end Alembic commands ###
