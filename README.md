# iris-api

# Project Overview

IRIS is a digital tool designed to support data-driven decision-making for retrofitting domestic properties by identifying homes that could benefit from energy efficiency improvements. It enables stakeholders to assess housing stock based on energy performance data to help target funding schemes and policy interventions more effectively

# Repository Description

This repository functions as the backend of IRIS and contains API routes that serve and process data to/from the frontend.

## Running the server

If you want to run this locally, you'll need to:

* install Apache Jena Fuseki - https://jena.apache.org/download/index.cgi
* run Apache Jena Fuseki
* create two datasets in Fuseki - ontology and knowledge
* load the ontology ttl files in this repo into the ontology dataset (again, use the Fuseki UI) - this will provide the API with access to the ontologies
* add your test data (e.g. buildings.ttl) to the knowledge dataset
* pip install all the modules listed in requirements.txt
* run a `make run-api` command (Python 3.9 or later)

## Basic Usage

To get all the buildings within a given GeoHash, call `/buildings` and pass in a geohash parameter (at least 5 digits) and it will return all buildings within that geohash. The returned payload will also include any flags against the property. A typical return payload would be:

    [
        {
            "uri": "data:building_100060748037",
            "securityLabel": null,
            "types": [
                "ndt_ont:House",
                "ndt_ont:SemiDetached"
            ],
            "uprn": "100060748037",
            "currentEnergyRating": "D",
            "parentBuildingTOID": null,
            "buildingTOID": "osgb1000013026999",
            "parentBuilding": null,
            "flags": {
                "data:4e1d2127-b1ff-4446-8e1a-e50fe5dd3d61": {
                    "flagType": "data:InterestedInInvestigating",
                    "flaggingPerson": "http://nationaldigitaltwin.gov.uk/data#TestUser",
                    "date": "http://iso.org/iso8601#2023-12-10T14:27:56.176601"
                },
                "data:c7163507-b195-48ad-8010-0d995efd1662": {
                    "flagType": "data:InterestedInVisiting",
                    "flaggingPerson": "http://nationaldigitaltwin.gov.uk/data#TestUser",
                    "date": "http://iso.org/iso8601#2023-12-10T14:28:17.751216",
                    "invalidated": "http://iso.org/iso8601#2023-12-10T16:33:23.247985",
                    "invalidatedBy": "http://nationaldigitaltwin.gov.uk/data#TestUser"
                }
            }
        }
    ]

Note that the API has shortened some of the URIs to keep the payload size down. You should use fully formed URIs when passing data in.

To flag a building for investigation, call `/flag-to-investigate` and pass in the full URI of the building, the flag URI will be returned

To flag a building for visiting, call `/flag-to-visit` and pass in the full URI of the building, the flag URI will be returned

To invalidate a flag, call `/invalidate-flag`, passing in the URI of the flag to be invalidated. This adds an AssessToBeFalse node to the graph, referring to the flag node. You can override the assessment type by setting `assessmentTypeOverride` to be another subclass of ies:Assess

These can be tested in Insomnia, and a JSON insomnia config is provided in this repo.

## Additional Calls

The /buildings/states/classes endpoint. That will return a list of class objects - e.g.

    [
        {
            "uri": "http://nationaldigitaltwin.gov.uk/ontology#BuildingState",
            "shortName": "ndt:BuildingState",
            "superClasses": [
                "http://ies.data.gov.uk/ontology/ies4#LocationState"
            ],
            "description": []
        },
        {
            "uri": "http://gov.uk/government/organisations/department-for-levelling-up-housing-and-communities/ontology/epc#BuildingWithEnergyRatingOfA",
            "shortName": "http://gov.uk/government/organisations/department-for-levelling-up-housing-and-communities/ontology/epc#BuildingWithEnergyRatingOfA",
            "superClasses": [
                "http://nationaldigitaltwin.gov.uk/ontology#BuildingState"
            ],
            "description": []
        },
        {
            "uri": "http://gov.uk/government/organisations/department-for-levelling-up-housing-and-communities/ontology/epc#BuildingWithEnergyRatingOfB",
            "shortName": "http://gov.uk/government/organisations/department-for-levelling-up-housing-and-communities/ontology/epc#BuildingWithEnergyRatingOfB",
            "superClasses": [
                "http://nationaldigitaltwin.gov.uk/ontology#BuildingState"
            ],
            "description": []
        }
    ]

The API will (eventually) detect the user logged in and use the user ID to create a person. For testing purposes, in the short term, this will just be a single test user (synthetic data)


You then need to create a new state instance, and apply it to the building. That means posting an iesState object to the /buildings/states endpoint. An example would be:

    {
        "uri":"http://myItem.com/my_building_state_1",
        "stateOf":"http://myItem.com/my_building",
        "stateType":"http://gov.uk/government/organisations/department-for-levelling-up-housing-and-communities/ontology/epc#BuildingWithEnergyRatingOfD",
        "startDateTime":"2023-11-17T09:00:00",
        "endDateTime":"2023-11-17T17:00:00"
    }

The start and end datetimes specify the temporal extent of the state (if known...if not, you can leave them blank). The stateOf property refers to the URI of the building. The stateType should be one of the classes returned by the /buildings/states/classes endpoint

You can also optionally provide a uri property for the state. If no uri is provided, one will be minted, and returned in the http response body.

All that remains after that is to put some assessment information into the system, by posting to the /assessments/assess-to-be-true endpoint:

    {
        "assessedItem":"http://myItem.com/my_building_state_1",
        "assessor":"http://ndtp.co.uk/data/d6cfb50d-c72c-40a8-a5e9-5b5a717aa730",
        "inPeriod":"2023-11-19"
    }

The assessedItem and assessor are the URIs we've already produced for the state and the person. The inPeriod property is the date of the assessment in ISO8601 format. If you don't provide the inPeriod property, the API will just use today's date.

An Insomnia (https://insomnia.rest/) test suite is also provided as a JSON config file - `ndt-write-insomnia.json`

## Unit Tests

Unit tests can be run by running the following command in the root directory: `python -m pytest`

## Security

The Integration Architecture uses a label-based approach to access control, based on the UK Government Enterprise Data Headers standard (policy based access control). This is currently limited in this version of the API to nationality, organisation and classification. In all the IES POST operations, you can set a securityLabel property that will override the default label.

You can also get and set the default security label.


---
### Contributors

The development of these works has been made possible with thanks to our [contributors](https://github.com/National-Digital-Twin/ndtp-styling-assets/graphs/contributors).
