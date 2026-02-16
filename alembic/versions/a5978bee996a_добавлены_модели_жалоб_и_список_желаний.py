"""добавлены модели жалоб и список желаний

Revision ID: a5978bee996a
Revises: 74a510968c3b
Create Date: 2026-01-29 14:12:56.550824

"""
"""добавлены модели жалоб и список желаний

Revision ID: a5978bee996a
Revises: 74a510968c3b
Create Date: 2026-01-29 14:12:56.550824
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision: str = 'a5978bee996a'
down_revision: Union[str, Sequence[str], None] = '74a510968c3b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Безопасное удаление таблицы
    op.execute("DROP TABLE IF EXISTS messages CASCADE")


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table(
        'messages',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('sender_id', sa.INTEGER(), nullable=False),
        sa.Column('recipient_id', sa.INTEGER(), nullable=False),
        sa.Column('text', sa.VARCHAR(), nullable=False),
        sa.Column(
            'is_read',
            sa.BOOLEAN(),
            server_default=sa.text('false'),
            nullable=False
        ),
        sa.Column(
            'created_at',
            postgresql.TIMESTAMP(),
            server_default=sa.text('now()'),
            nullable=False
        ),
        sa.ForeignKeyConstraint(
            ['recipient_id'],
            ['users.id'],
            name='messages_recipient_id_fkey'
        ),
        sa.ForeignKeyConstraint(
            ['sender_id'],
            ['users.id'],
            name='messages_sender_id_fkey'
        ),
        sa.PrimaryKeyConstraint('id', name='messages_pkey')
    )

