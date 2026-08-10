"""add chunk processing metadata

Revision ID: 245f94201030
Revises: 6da298f5afba
Create Date: 2026-08-03 00:16:19.172598

"""
from typing import Sequence, Union

from sqlalchemy.dialects import postgresql
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '245f94201030'
down_revision: Union[str, Sequence[str], None] = '6da298f5afba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    chunk_status = postgresql.ENUM(
        "PENDING",
        "RUNNING",
        "COMPLETED",
        "FAILED",
        name="chunk_status",
    )

    chunk_status.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "document_chunks",
        sa.Column(
            "chunker_name",
            sa.String(length=50),
            nullable=True,
            server_default="RecursiveCharacterTextSplitter",
        ),
    )

    op.add_column(
        "document_chunks",
        sa.Column(
            "chunker_version",
            sa.String(length=50),
            nullable=True,
            server_default="1.0",
        ),
    )

    op.add_column(
        "documents",
        sa.Column(
            "chunk_status",
            chunk_status,
            nullable=False,
            server_default="PENDING",
        ),
    )

    op.alter_column(
        "documents",
        "chunk_status",
        server_default=None,
    )

    op.alter_column(
        "document_chunks",
        "chunker_name",
        server_default=None,
    )

    op.alter_column(
        "document_chunks",
        "chunker_version",
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column("documents", "chunk_status")

    op.drop_column("document_chunks", "chunker_version")
    op.drop_column("document_chunks", "chunker_name")

    chunk_status = postgresql.ENUM(
        "PENDING",
        "RUNNING",
        "COMPLETED",
        "FAILED",
        name="chunk_status",
    )

    chunk_status.drop(op.get_bind(), checkfirst=True)