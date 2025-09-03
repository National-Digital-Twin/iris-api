docker-build:
	docker build --no-cache --secret id=pat_token,env=GITHUB_ACCESS_TOKEN -t iris/write-api:latest .

docker-run:
	docker run -d --rm --name iris-write-api --network developer-resources_iris -e PORT=3010 -e DEV=True -e JENA_PROTOCOL=http -e JENA_URL=127.0.0.1 -e JENA_PORT:3030 -e DB_HOST=postgis -p 3010:3010 iris/write-api:latest

run-api:
	python api/main.py
	python -m pytest

load-met-office-data:
	MATERIALIZED_VIEW=iris.wind_driven_rain_projections_geojson TARGET_TABLE=wind_driven_rain_projections GPKG_SOURCE=https://services.arcgis.com/Lq3V5RFuTBC9I7kv/arcgis/rest/services/Annual_Index_of_Wind_Driven_Rain_Projections_5km/FeatureServer/replicafilescache/Annual_Index_of_Wind_Driven_Rain_Projections_5km_-6134910210859057092.gpkg python developer-resources/load_gpkg_to_postgis.py
	MATERIALIZED_VIEW=iris.icing_days_geojson TARGET_TABLE=annual_count_of_icing_days_1991_2020 GPKG_SOURCE=https://services.arcgis.com/Lq3V5RFuTBC9I7kv/arcgis/rest/services/Annual_Count_of_Icing_Days_1991_2020/FeatureServer/replicafilescache/Annual_Count_of_Icing_Days_1991_2020_5977951113111576455.gpkg python developer-resources/load_gpkg_to_postgis.py
	MATERIALIZED_VIEW=iris.hot_summer_days_geojson TARGET_TABLE=annual_count_of_hot_summer_days_projections_12km GPKG_SOURCE=https://services.arcgis.com/Lq3V5RFuTBC9I7kv/arcgis/rest/services/Annual_Count_of_Hot_Days___Projections__12km_grid_/FeatureServer/replicafilescache/Annual_Count_of_Hot_Days___Projections__12km_grid__5151054028377652076.gpkg python developer-resources/load_gpkg_to_postgis.py
	JOIN_VIEW=iris.uk_ward DATA_VIEW=iris.uk_ward_epc_data MATERIALIZED_VIEW=iris.uk_ward_epc TARGET_TABLE=district_borough_unitary_ward GPKG_SOURCE=https://api.os.uk/downloads/v1/products/BoundaryLine/downloads?area=GB&format=GeoPackage&redirect GPKG_TABLE=district_borough_unitary_ward python developer-resources/load_gpkg_to_postgis.py
	JOIN_VIEW=iris.uk_ward DATA_VIEW=iris.uk_ward_epc_data MATERIALIZED_VIEW=iris.uk_ward_epc TARGET_TABLE=unitary_electoral_division GPKG_SOURCE=https://api.os.uk/downloads/v1/products/BoundaryLine/downloads?area=GB&format=GeoPackage&redirect GPKG_TABLE=unitary_electoral_division python developer-resources/load_gpkg_to_postgis.py

migrate:
	alembic upgrade head
	
