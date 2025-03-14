docker-image:
	docker build --no-cache -t iris/write-api:latest .

docker-run:
	docker run --rm --name iris-write-api -e PORT=3010 -e DEV=True -e JENA_PROTOCOL=http -e JENA_URL=127.0.0.1 -e JENA_PORT:3030 -p 3010:3010 iris/write-api:latest

run-api:
	uvicorn api.main:app --reload --port 5021

test:
	python -m pytest