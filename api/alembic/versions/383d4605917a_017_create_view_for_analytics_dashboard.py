# SPDX-License-Identifier: Apache-2.0
# © Crown Copyright 2025. This work has been developed by the National Digital Twin Programme
# and is legally attributed to the Department for Business and Trade (UK) as the governing entity.

"""create view for analytics dashboard

Revision ID: 383d4605917a
Revises: 37989279ce33
Create Date: 2025-10-02 14:26:58.535815

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "383d4605917a"
down_revision: Union[str, None] = "37989279ce33"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE MATERIALIZED VIEW IF NOT EXISTS iris.analytics
        AS (
            SELECT b.uprn, b.point, b.is_residential, ea.lodgement_date, ea.epc_rating, su.type, su.built_form,
                su.fuel_type, su.window_glazing, su.wall_construction, su.wall_insulation, su.roof_construction,
                su.roof_insulation, su.roof_insulation_thickness, su.floor_construction, su.floor_insulation,
                su.has_roof_solar_panels, su.roof_material, su.roof_aspect_area_facing_north_m2,
                su.roof_aspect_area_facing_east_m2, su.roof_aspect_area_facing_south_m2,
                su.roof_aspect_area_facing_west_m2, su.roof_aspect_area_facing_north_east_m2,
                su.roof_aspect_area_facing_south_east_m2, su.roof_aspect_area_facing_south_west_m2,
                su.roof_aspect_area_facing_north_west_m2, su.roof_aspect_area_indeterminable_m2, su.roof_shape,
                COALESCE(er.name, sawr.name) AS region_name
            FROM iris.building b
            LEFT JOIN iris.epc_assessment ea ON ea.uprn = b.uprn
            JOIN iris.structure_unit su ON su.epc_assessment_id = ea.id OR su.uprn = ea.uprn
            JOIN iris.district_borough_unitary dbu ON ST_INTERSECTS(dbu.geometry, b.point)
            LEFT JOIN iris.english_region er ON er.fid = dbu.english_region_fid
            LEFT JOIN iris.scotland_and_wales_region sawr ON sawr.fid = dbu.scotland_and_wales_region_fid
        )
        WITH NO DATA;
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        DROP MATERIALIZED VIEW iris.analytics;
        """
    )
