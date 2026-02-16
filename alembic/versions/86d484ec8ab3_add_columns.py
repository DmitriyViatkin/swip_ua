"""Add columns

Revision ID: 86d484ec8ab3
Revises: 00597d29e042
Create Date: 2025-11-26 11:44:52.446882
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86d484ec8ab3'
down_revision: Union[str, Sequence[str], None] = '00597d29e042'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # add column to redirections
    op.add_column(
        'redirections',
        sa.Column('redirection', sa.Boolean(), nullable=True)
    )

    # add self-referencing agent_id to users
    op.add_column(
        'users',
        sa.Column('agent_id', sa.Integer(), nullable=True)
    )

    op.create_foreign_key(
        'fk_users_agent_id_users',
        source_table='users',
        referent_table='users',
        local_cols=['agent_id'],
        remote_cols=['id'],
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        'fk_users_agent_id_users',
        'users',
        type_='foreignkey'
    )

    op.drop_column('users', 'agent_id')
    op.drop_column('redirections', 'redirection')
