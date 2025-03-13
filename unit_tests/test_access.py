import os
import pytest
from api.access import AccessClient

@pytest.fixture
def connection_string():
    return "dummy_connection_string"

@pytest.fixture
def headers():
    return {
        "Authorization": "Bearer dummy_token",
        "X-Auth-Request-Access-Token": "dummy_jwt_token"
    }

def test_dev_mode_returns_dummy_data(connection_string, headers):
    client = AccessClient(connection_string, dev_mode=True)
    result = client.get_user_details(headers)
    expected = {"username": "Test User1", "user_id": "1234-5678-99ab-cdef"}
    assert result == expected

def test_api_successful_response(mocker, connection_string, headers):
    # Create a fake successful response.
    fake_response = mocker.MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {
        "content": {
            "displayName": "Test User",
            "username": "069292e4-3081-704c-68cd-b5e621f48b62"
        }
    }
    # Patch requests.get in the access module.
    get_mock = mocker.patch("access.requests.get", return_value=fake_response)

    client = AccessClient(connection_string, dev_mode=False)
    result = client.get_user_details(headers)
    expected = {
        "username": "Test User",
        "user_id": "069292e4-3081-704c-68cd-b5e621f48b62"
    }
    assert result == expected

    # Ensure the API was called with the correct URL and headers.
    expected_url = "https://test.com/api/v1/user-details"
    get_mock.assert_called_with(expected_url, headers=headers)

def test_api_error_response(mocker, connection_string, headers):
    # Create a fake error response from the API.
    fake_response = mocker.MagicMock()
    fake_response.status_code = 400
    fake_response.text = "Bad Request"
    fake_response.json.return_value = {"error": "Bad Request"}
    mocker.patch("access.requests.get", return_value=fake_response)

    client = AccessClient(connection_string, dev_mode=False)
    result = client.get_user_details(headers)
    assert result == {"error": "Bad Request"}

def test_missing_environment_variable(monkeypatch, connection_string, headers):
    # Remove the environment variable to simulate a missing configuration.
    monkeypatch.delenv("IDENTITY_API_BASE_URL", raising=False)
    with pytest.raises(Exception, match="IDENTITY_API_BASE_URL environment variable is not set"):
        AccessClient(connection_string, dev_mode=False)
