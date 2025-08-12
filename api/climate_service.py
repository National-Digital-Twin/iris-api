from sqlalchemy import text
from db import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def fetch_geojson_for_wind_driven_rain(
    db: AsyncSession = Depends(get_db),):
    result = await db.execute(text("SELECT geojson FROM iris.wind_driven_rain_projections_geojson;"))
    row = result.fetchone()
    return row[0]
    