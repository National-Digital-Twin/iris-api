# SPDX-License-Identifier: Apache-2.0
# © Crown Copyright 2025. This work has been developed by the National Digital Twin Programme
# and is legally attributed to the Department for Business and Trade (UK) as the governing entity.

"""001_create_building_geo_mapping_table

Revision ID: 0cba3d41c22e
Revises: 447db7945a72
Create Date: 2025-06-02 17:36:27.192043

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0cba3d41c22e"
down_revision: Union[str, None] = "447db7945a72"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE iris.building_geo_mapping (
            uprn TEXT,
            first_line_of_address TEXT,
            toid TEXT,
            point GEOMETRY(Point, 4326),
            epc_rating CHAR(1),
            structure_unit_type TEXT
        );
    """
    )

    op.execute(
        """
        CREATE INDEX point_ix
        ON iris.building_geo_mapping
        USING GIST (point);
    """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        DROP INDEX point_ix ON iris.building_geo_mapping;
    """
    )

    op.execute(
        """
        DROP TABLE iris.building_geo_mapping;
               """
    )
