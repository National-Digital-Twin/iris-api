import requests

with open("ies4.ttl") as file:
    data = file.read()
    headers = {"Content-Type": "text/turtle;charset=utf-8"}
    r = requests.post(
        "http://localhost:3030/ontology/data?default", data=data, headers=headers
    )
print("IES loaded")

with open("iesExtensions.ttl") as file:
    data = file.read()
    headers = {"Content-Type": "text/turtle;charset=utf-8"}
    r = requests.post(
        "http://localhost:3030/ontology/data?default", data=data, headers=headers
    )
print("IES Extensions loaded")

with open("ndt_retrofit_buildings_extensions.ttl") as file:
    data = file.read()
    headers = {"Content-Type": "text/turtle;charset=utf-8"}
    r = requests.post(
        "http://localhost:3030/ontology/data?default", data=data, headers=headers
    )
print("NDT ontology Extensions loaded")
