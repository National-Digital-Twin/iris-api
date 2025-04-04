from api.query import get_building, get_roof_for_building, get_floor_for_building, get_walls_and_windows_for_building, get_buildings_in_bounding_box_query

def building_query_response(uprn):
    return {
        "results": {
            "bindings": [
                { 
                    "uprn": { "type": "uri" , "value": f"http://ndtp.co.uk/data#UPRN_{uprn}" } ,
                    "lodgementDate": { "type": "uri" , "value": "http://iso8601.iso.org/2024-03-30" } ,
                    "builtForm": { "type": "uri" , "value": "http://ies.data.gov.uk/ontology/ies-building1#SemiDetached" } ,
                    "structureUnitType": { "type": "uri" , "value": "http://ies.data.gov.uk/ontology/ies-building1#House" }
                }
            ]
        }
    }

def roof_query_response(uprn):
    return {
        "results": {
            "bindings": [
            {
                "uprn": { "type": "uri" , "value": f"http://ndtp.co.uk/data#UPRN_{uprn}" } ,
                "roofConstruction": { "type": "uri" , "value": "http://ies.data.gov.uk/ontology/ies-building1#RoofRooms" } ,
                "roofInsulation": { "type": "uri" , "value": "http://ies.data.gov.uk/ontology/ies-building1#InsulatedAssumed" },
                "roofInsulationThickness": { "type": "uri" , "value": "http://ies.data.gov.uk/ontology/ies-building1#250mm_Insulation" }
            }
            ]
        }
    }
    
def floor_query_response(uprn):
    return {
        "results": {
            "bindings": [
            { 
                "uprn": { "type": "uri" , "value": f"http://ndtp.co.uk/data#UPRN_{uprn}" } ,
                "floorConstruction": { "type": "uri" , "value": "http://ies.data.gov.uk/ontology/ies-building1#Suspended" } ,
                "floorInsulation": { "type": "uri" , "value": "http://ies.data.gov.uk/ontology/ies-building1#NoInsulationInFloor" }
            }
            ]
        }
    }
    
def wall_window_query_response(uprn):
    return {
        "results": {
            "bindings": [
            { 
                "uprn": { "type": "uri" , "value": f"http://ndtp.co.uk/data#UPRN_{uprn}" } ,
                "wallConstruction": { "type": "uri" , "value": "http://ies.data.gov.uk/ontology/ies-building1#CavityWall" } ,
                "wallInsulation": { "type": "uri" , "value": "http://ies.data.gov.uk/ontology/ies-building1#InsulatedWall" } ,
                "windowGlazing": { "type": "uri" , "value": "http://ies.data.gov.uk/ontology/ies-building1#DoubleGlazingBefore2002" }
            }
            ]
        }
    }

def empty_query_response():
    return {
        "results": {
            "bindings": []
        }
    }
    
def bounded_buildings_response():
    return {
        "results": {
            "bindings": [
                {
                    "uprn": { "type": "uri" , "value": "http://ndtp.co.uk/data#UPRN_100060763456" } ,
                    "toid": { "type": "literal" , "value": "osgb1000013062259" } ,
                    "point": { "type": "literal" , "datatype": "http://www.opengis.net/ont/geosparql#wktLiteral" , "value": "POINT(-1.1834759844410794 50.72234886358317)" } ,
                    "epcRating": { "type": "uri" , "value": "http://ies.data.gov.uk/ontology/ies-building1#UK_DOM_EPC_C" } ,
                    "structureUnitType": { "type": "uri" , "value": "http://ies.data.gov.uk/ontology/ies-building1#Bungalow" }
                } ,
                { 
                    "uprn": { "type": "uri" , "value": "http://ndtp.co.uk/data#UPRN_100060768637" } ,
                    "toid": { "type": "literal" , "value": "osgb1000013076936" } ,
                    "point": { "type": "literal" , "datatype": "http://www.opengis.net/ont/geosparql#wktLiteral" , "value": "POINT(-1.178467890878929 50.725098060722736)" } ,
                    "epcRating": { "type": "uri" , "value": "http://ies.data.gov.uk/ontology/ies-building1#UK_DOM_EPC_C" } ,
                    "structureUnitType": { "type": "uri" , "value": "http://ies.data.gov.uk/ontology/ies-building1#House" }
                }
            ]
        }
    }
        
    

def mock_known_building(query, headers):
    uprn = 10023456789
    if query == get_building(uprn):
        return building_query_response(uprn)
    if query == get_roof_for_building(uprn):
        return roof_query_response(uprn)
    if query == get_floor_for_building(uprn):
        return floor_query_response(uprn)
    if query == get_walls_and_windows_for_building(uprn):
        return wall_window_query_response(uprn)
    else:
        return "default response"
    