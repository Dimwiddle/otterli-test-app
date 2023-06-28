import pytest
from api.client import Client
from api_settings import get_endpoint
import json


FAKE_TOKEN = "123488820xasdbf123"

@pytest.mark.auth
def test_invalid_token():
    client = Client(token=FAKE_TOKEN)
    response = client.send_query(get_endpoint(), return_raw=True)
    assert response.status_code == 403
    
@pytest.mark.auth
def test_valid_token():
    """Verifies that a valid user token allows access to the API"""
    client = Client()
    response = client.send_query(get_endpoint(), return_raw=True)
    assert response.status_code == 200

@pytest.mark.auth
def test_kill_switch():
    """Verifies that the API only accepts specific versions"""
    client = Client(version='1.1.0')
    endpoint = f"{get_endpoint()}categories/?icons=True"
    response = client.send_query(endpoint, return_raw=True)
    assert response.status_code == 406
    assert "This API accepts versions" in response.text
