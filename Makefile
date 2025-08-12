docker-image:
	docker build --no-cache -t iris/write-api:latest .

docker-run:
	docker run --rm --name iris-write-api -e PORT=3010 -e DEV=True -e JENA_PROTOCOL=http -e JENA_URL=127.0.0.1 -e JENA_PORT:3030 -p 3010:3010 iris/write-api:latest

run-api:
	python api/main.py

test:
	python -m pytest

load-met-office-data:
	GPKG_SOURCE=https://services.arcgis.com/Lq3V5RFuTBC9I7kv/arcgis/rest/services/Annual_Index_of_Wind_Driven_Rain_Projections_5km/FeatureServer/replicafilescache/Annual_Index_of_Wind_Driven_Rain_Projections_5km_-6134910210859057092.gpkg python developer-resources/load_gpkg_to_postgis.py

migrate:
	alembic upgrade head