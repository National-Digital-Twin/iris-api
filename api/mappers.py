from models import SingleBuilding

def strip_uri(uri: str) -> str:
    """
    Utility method to strip the relevant resource from the URI.
    
    Args:
        uri (str): The URI from which to extract the resource.
        
    Returns:
        str: The resource.
    """
    if "UPRN_" in uri:
        split = uri.split("UPRN_")
    elif "iso8601.iso.org/" in uri:
        split = uri.split("iso8601.iso.org/")
    else:
        split = uri.split("#")
    if len(split) > 1:
        return split[-1]
    else:
        return ""
    
def get_value_from_result(result: dict, field: str) -> str:
    return strip_uri(result[field]["value"])

def map_building_results(building: SingleBuilding, results: dict) -> None:
    """
    Maps generic building data to a `SingleBuilding` instance.
    
    Args:
        building (SingleBuilding): A representation of a building.
        results (dict): General SPARQL data retrieved regarding the building e.g. the type of the structure unit.
    
    Returns:
        None
    """
    if results and results["results"] and results["results"]["bindings"]:
        for result in results["results"]["bindings"]:
            building.lodgement_date = get_value_from_result(result, "lodgementDate")
            building.built_form = get_value_from_result(result, "builtForm")
            building.structure_unit_type = get_value_from_result(result, "structureUnitType")

def map_roof_results(building: SingleBuilding, results: dict) -> None:
    """
    Maps roof-related data to a `SingleBuilding` instance.
    
    Args:
        building (SingleBuilding): A representation of a building.
        results (dict): Roof-related SPARQL data retrieved regarding the building e.g. the construction of the roof.
    
    Returns:
        None
    """
    if results and results["results"] and results["results"]["bindings"]:
        for result in results["results"]["bindings"]:
            building.roof_construction = get_value_from_result(result, "roofConstruction")
            building.roof_insulation_location = get_value_from_result(result, "roofInsulation")
            building.roof_insulation_thickness = get_value_from_result(result, "roofInsulationThickness")

def map_floor_results(building: SingleBuilding, results: dict) -> None:
    """
    Maps floor-related data to a `SingleBuilding` instance.
    
    Args:
        building (SingleBuilding): A representation of a building.
        results (dict): Floor-related SPARQL data retrieved regarding the building e.g. the construction of the floor.
    
    Returns:
        None
    """
    if results and results["results"] and results["results"]["bindings"]:
        for result in results["results"]["bindings"]:
            building.floor_construction = get_value_from_result(result, "floorConstruction")
            building.floor_insulation = get_value_from_result(result, "floorInsulation")

def map_wall_window_results(building: SingleBuilding, results: dict) -> None:
    """
    Maps wall and window-related data to a `SingleBuilding` instance.
    
    Args:
        building (SingleBuilding): A representation of a building.
        results (dict): Wall and window-related SPARQL data retrieved regarding the building e.g. the glazing of the windows.
    
    Returns:
        None
    """
    if results and results["results"] and results["results"]["bindings"]:
        for result in results["results"]["bindings"]:
            building.wall_construction = get_value_from_result(result, "wallConstruction")
            building.wall_insulation = get_value_from_result(result, "wallInsulation")
            building.window_glazing = get_value_from_result(result, "windowGlazing")

def map_single_building_response(uprn: str, building_results: dict, roof_results: dict, floor_results: dict, wall_window_results: dict) -> SingleBuilding:
    """
    Maps a `SingleBuilding` response from SPARQL requests made for generic, roof, floor, wall and window data.
    
    Args:
        urpn (str): The UPRN of the building.
        building_results (dict): General SPARQL data retrieved regarding the building e.g. the type of the structure unit.
        roof_results (dict): Roof-related SPARQL data retrieved regarding the building e.g. the construction of the roof.
        floor_results (dict): Floor-related SPARQL data retrieved regarding the building e.g. the construction of the floor.
        wall_window_results (dict): Wall and window-related SPARQL data retrieved regarding the building e.g. the glazing of the windows.
        
    Returns:
        SingleBuilding: A representation of a building.
    """
    building = SingleBuilding()
    building.uprn = uprn
    map_building_results(building, building_results)
    map_roof_results(building, roof_results)
    map_floor_results(building, floor_results)
    map_wall_window_results(building, wall_window_results)
    return building