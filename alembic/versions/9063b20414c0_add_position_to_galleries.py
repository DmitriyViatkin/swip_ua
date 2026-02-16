"""add position to galleries

Revision ID: 9063b20414c0
Revises: eb9b95684cca
Create Date: 2025-12-25 18:57:52.250287
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9063b20414c0'
down_revision: Union[str, Sequence[str], None] = 'eb9b95684cca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Добавляем колонку position с временным дефолтом
    op.add_column(
        'galleries',
        sa.Column('position', sa.Integer(), nullable=False, server_default="0")
    )

    # Убираем дефолт после заполнения существующих данных
    op.alter_column('galleries', 'position', server_default=None)

    op.alter_column('galleries', 'image',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('galleries', 'is_main',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('galleries', 'house_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_index(op.f('ix_galleries_id'), table_name='galleries')
    op.create_index('ix_gallery_house_position', 'galleries', ['house_id', 'position'], unique=False)
    op.drop_constraint(op.f('galleries_house_id_fkey'), 'galleries', type_='foreignkey')
    op.create_foreign_key(None, 'galleries', 'houses', ['house_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'galleries', type_='foreignkey')
    op.create_foreign_key(op.f('galleries_house_id_fkey'), 'galleries', 'houses', ['house_id'], ['id'])
    op.drop_index('ix_gallery_house_position', table_name='galleries')
    op.create_index(op.f('ix_galleries_id'), 'galleries', ['id'], unique=False)
    op.alter_column('galleries', 'house_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('galleries', 'is_main',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('galleries', 'image',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.drop_column('galleries', 'position')
