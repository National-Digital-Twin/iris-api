# SPDX-License-Identifier: Apache-2.0
# © Crown Copyright 2025. This work has been developed by the National Digital Twin Programme
# and is legally attributed to the Department for Business and Trade (UK) as the governing entity.

"""add region name to district_borough_unitary

Revision ID: 37989279ce33
Revises: cc816c325e2a
Create Date: 2025-10-02 12:04:32.313209

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "37989279ce33"
down_revision: Union[str, None] = "cc816c325e2a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add region_name column to district borough unitary table and assign it a value based on location"""
    op.execute(
        """
        ALTER TABLE iris.district_borough_unitary
        ADD COLUMN region_name TEXT;
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        ALTER TABLE iris.district_borough_unitary
        DROP region_name;
        """
    )
