"""create items table

Revision ID: 0001_create_items
Revises:
Create Date: 2026-10-15

"""
import sqlalchemy as sa

from alembic import op

revision = "0001_create_items"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "items",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column(
            "creado",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.bulk_insert(
        sa.table("items", sa.column("nombre", sa.String)),
        [{"nombre": "primer item desde migracion Alembic"}],
    )


def downgrade() -> None:
    op.drop_table("items")
