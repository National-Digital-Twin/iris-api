# SPDX-License-Identifier: Apache-2.0
# © Crown Copyright 2025. This work has been developed by the National Digital Twin Programme
# and is legally attributed to the Department for Business and Trade (UK) as the governing entity.

from unittest.mock import ANY, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.query import (
    get_building,
    get_buildings_in_bounding_box_query,
    get_filterable_buildings_in_bounding_box_query,
    get_floor_for_building,
    get_roof_for_building,
    get_walls_and_windows_for_building,
)
from api.routes import router
from unit_tests.query_response_mocks import (
    bounded_buildings_response,
    bounded_buildings_response_two_forms,
    bounded_detailed_buildings_response,
    empty_query_response,
    mock_known_building,
)


@pytest.fixture(autouse=True)
def set_identity_api_url(monkeypatch):
    # Set the environment variable for all tests.
    monkeypatch.setenv("IDENTITY_API_URL", "https://test.com")


@pytest.fixture
def client():
    """Create a test client with the router mounted on a FastAPI app."""
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


class TestGetBuildingsInBoundingBox:
    def test_successful_get_buildings(self, client, monkeypatch):
        """Test successful retrieval of buildings in a bounding box"""
        mock_query = MagicMock(return_value=bounded_buildings_response())
        monkeypatch.setattr("api.routes.run_sparql_query", mock_query)

        response = client.get(
            "/buildings?min_long=-1.1835&max_long=-1.1507&min_lat=50.6445&max_lat=50.7261"
        )

        assert response.status_code == 200
        buildings = response.json()

        assert len(buildings) == 2
        building = buildings[0]

        assert building["uprn"] == "100060763456"
        assert building["first_line_of_address"] == "1 Apple Avenue"
        assert building["energy_rating"] == "C"
        assert building["structure_unit_type"] == "Bungalow"
        assert building["toid"] == "osgb1000013062259"
        assert building["longitude"] == -1.1834759844410794
        assert building["latitude"] == 50.72234886358317

        self.verify_query_run_with_correct_args(mock_query)

    def test_successful_get_buildings_two_forms(self, client, monkeypatch):
        """Test successful retrieval of buildings in a bounding box"""
        mock_query = MagicMock(return_value=bounded_buildings_response_two_forms())
        monkeypatch.setattr("api.routes.run_sparql_query", mock_query)

        response = client.get(
            "/buildings?min_long=-1.1835&max_long=-1.1507&min_lat=50.6445&max_lat=50.7261"
        )

        assert response.status_code == 200
        buildings = response.json()

        assert len(buildings) == 2
        apple_bungalow = buildings[0]
        cherry_flat = buildings[1]
        self.verify_building_data(
            apple_bungalow,
            "100060763456",
            "1 Apple Avenue",
            "C",
            "Bungalow",
            "osgb1000013062259",
            -1.1834759844410794,
            50.72234886358317,
        )
        self.verify_building_data(
            cherry_flat,
            "100060768638",
            "3a Cherry Street",
            "D",
            "Maisonette",
            "osgb1000013076936",
            -1.178467890878929,
            50.725098060722736,
        )

        self.verify_query_run_with_correct_args(mock_query)

    def test_empty_results(self, client, monkeypatch):
        """Test when no buildings are found"""
        mock_query = MagicMock(return_value=empty_query_response())
        monkeypatch.setattr("api.routes.run_sparql_query", mock_query)

        response = client.get(
            "/buildings?min_long=-1.1835&max_long=-1.1507&min_lat=50.6445&max_lat=50.7261"
        )

        assert response.status_code == 200
        buildings = response.json()
        assert len(buildings) == 0

        self.verify_query_run_with_correct_args(mock_query)

    def verify_building_data(
        self,
        result,
        exp_uprn,
        exp_address,
        exp_epc,
        exp_type,
        exp_toid,
        exp_long,
        exp_lat,
    ):
        assert result["uprn"] == exp_uprn
        assert result["first_line_of_address"] == exp_address
        assert result["energy_rating"] == exp_epc
        assert result["structure_unit_type"] == exp_type
        assert result["toid"] == exp_toid
        assert result["longitude"] == exp_long
        assert result["latitude"] == exp_lat

    def verify_query_run_with_correct_args(self, mock_query):
        polygon = "POLYGON((-1.1835 50.6445, -1.1507 50.6445, -1.1507 50.7261, -1.1835 50.7261, -1.1835 50.6445))"
        mock_query.assert_any_call(get_buildings_in_bounding_box_query(polygon), ANY)
        call_args = mock_query.call_args[0]
        assert polygon in call_args[0]


class TestGetFilterableBuildingsInBoundingBox:
    def test_successful_get_buildings(self, client, monkeypatch):
        """Test successful retrieval of filterable buildings in a bounding box"""
        mock_query = MagicMock(return_value=bounded_detailed_buildings_response())
        monkeypatch.setattr("api.routes.run_sparql_query", mock_query)

        response = client.get(
            "/detailed-buildings?min_long=-1.1835&max_long=-1.1507&min_lat=50.6445&max_lat=50.7261"
        )

        assert response.status_code == 200
        buildings = response.json()

        assert len(buildings) == 2
        building = buildings[0]

        assert building["uprn"] == "10003319738"
        assert building["postcode"] == "PO36 9JA"
        assert building["window_glazing"] == "DoubleGlazingBefore2002"
        assert building["wall_construction"] == "CavityWall"
        assert building["wall_insulation"] == "InsulatedWall"
        assert building["floor_construction"] == "Suspended"
        assert building["floor_insulation"] == "NoInsulationInFloor"
        assert building["roof_construction"] == ""
        assert building["roof_insulation_location"] == ""
        assert building["roof_insulation_thickness"] == ""

        self.verify_query_run_with_correct_args(mock_query)

    def test_empty_results(self, client, monkeypatch):
        """Test when no buildings are found"""
        mock_query = MagicMock(return_value=empty_query_response())
        monkeypatch.setattr("api.routes.run_sparql_query", mock_query)

        response = client.get(
            "/detailed-buildings?min_long=-1.1835&max_long=-1.1507&min_lat=50.6445&max_lat=50.7261"
        )

        assert response.status_code == 200
        buildings = response.json()
        assert len(buildings) == 0

        self.verify_query_run_with_correct_args(mock_query)

    def verify_query_run_with_correct_args(self, mock_query):
        polygon = "POLYGON((-1.1835 50.6445, -1.1507 50.6445, -1.1507 50.7261, -1.1835 50.7261, -1.1835 50.6445))"
        mock_query.assert_any_call(
            get_filterable_buildings_in_bounding_box_query(polygon), ANY
        )
        call_args = mock_query.call_args[0]
        assert polygon in call_args[0]


class TestGetBuildingByUprn:
    def test_successful_get_building(self, client, monkeypatch):
        """Test successful retrieval of a building by UPRN"""
        # Mock the run_sparql_query function
        uprn = 10023456789
        mock_query = MagicMock()
        mock_query.side_effect = mock_known_building
        monkeypatch.setattr("api.routes.run_sparql_query", mock_query)

        response = client.get(f"/buildings/{uprn}")

        assert response.status_code == 200
        data = response.json()

        # Check the data
        assert data["uprn"] == f"{uprn}"
        assert data["lodgement_date"] == "2024-03-30"
        assert data["built_form"] == "SemiDetached"
        assert data["structure_unit_type"] == "House"
        assert data["roof_construction"] == "RoofRooms"
        assert data["roof_insulation_location"] == "InsulatedAssumed"
        assert data["roof_insulation_thickness"] == "250mm_Insulation"
        assert data["floor_construction"] == "Suspended"
        assert data["floor_insulation"] == "NoInsulationInFloor"
        assert data["wall_construction"] == "CavityWall"
        assert data["wall_insulation"] == "InsulatedWall"
        assert data["window_glazing"] == "DoubleGlazingBefore2002"

        # Verify run_sparql_query was called with the correct params
        assert mock_query.call_count == 4
        mock_query.assert_any_call(get_building(uprn), ANY)
        mock_query.assert_any_call(get_roof_for_building(uprn), ANY)
        mock_query.assert_any_call(get_floor_for_building(uprn), ANY)
        mock_query.assert_any_call(get_walls_and_windows_for_building(uprn), ANY)
        call_args = mock_query.call_args[0]
        assert str(uprn) in call_args[0]

    def test_building_not_found(self, client, monkeypatch):
        """Test when building is not found"""
        # Mock the run_sparql_query function to return empty results
        mock_query = MagicMock(return_value=empty_query_response())
        monkeypatch.setattr("api.routes.run_sparql_query", mock_query)
        uprn = 99999999999

        response = client.get(f"/buildings/{uprn}")

        assert response.status_code == 404
        assert response.json() == {"detail": f"Building with UPRN {uprn} not found"}


if __name__ == "__main__":
    pytest.main(["-v", __file__])
